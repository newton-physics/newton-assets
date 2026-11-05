"""Validate the standard H2 conversion, source fidelity, and Newton simulation."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from pxr import Gf, Usd, UsdGeom, UsdPhysics


def validate_package(package: Path, converted_source: Path | None = None) -> None:
    """Check USD composition, sharing, compatibility edits, and package hashes."""
    stage = Usd.Stage.Open(str(package / "H2Loop.usda"))
    assert stage and not stage.GetCompositionErrors(), "USD composition failed"
    assert str(stage.GetDefaultPrim().GetPath()) == "/H2Loop"
    assert not stage.GetPrimAtPath("/H2Loop/Geometry/floor")
    assert not (package / "Source").exists(), "No duplicate source archive is needed"
    assert not (package / "Payload/Mujoco.usda").exists()
    assert not (package / "Payload/Robot.usda").exists()
    manifest = json.loads((package / "BUILD.json").read_text())
    assert set(manifest["files"]) == {
        p.relative_to(package).as_posix()
        for p in package.rglob("*")
        if p.is_file() and p.name != "BUILD.json"
    }
    for name, digest in manifest["files"].items():
        assert hashlib.sha256((package / name).read_bytes()).hexdigest() == digest, name
    assert sum(p.HasAPI(UsdPhysics.RigidBodyAPI) for p in stage.Traverse()) == 44
    assert sum(p.GetTypeName() == "MjcActuator" for p in stage.Traverse()) == 31
    # Confirm the normal nested body layout, rather than a flattened namespace.
    assert stage.GetPrimAtPath(
        "/H2Loop/Geometry/pelvis/left_hip_pitch_link/left_hip_roll_link"
    )
    loops = [
        p
        for p in stage.Traverse()
        if p.IsA(UsdPhysics.Joint)
        and p.GetAttribute("physics:excludeFromArticulation").Get()
    ]
    assert len(loops) == 6
    for loop in loops:
        assert (
            "MjcEqualityConnectAPI"
            in loop.GetMetadata("apiSchemas").GetAddedOrExplicitItems()
        )
    for prim in stage.Traverse():
        assert not any(
            name.startswith("PhysicsDriveAPI:") for name in prim.GetAppliedSchemas()
        ), f"H2 must retain its original MjcActuator actuation: {prim.GetPath()}"
        if prim.HasAPI(UsdPhysics.CollisionAPI) and UsdGeom.Imageable(prim):
            assert UsdGeom.Imageable(prim).ComputePurpose() == UsdGeom.Tokens.guide
        targets = [t for rel in prim.GetRelationships() for t in rel.GetTargets()]
        targets += [t for attr in prim.GetAttributes() for t in attr.GetConnections()]
        for target in targets:
            assert stage.GetObjectAtPath(target), (prim.GetPath(), target)
    library = Usd.Stage.Open(str(package / "Payload/GeometryLibrary.usdc"))
    assert sum(p.IsA(UsdGeom.Mesh) for p in library.TraverseAll()) == 38
    meshes = [p for p in stage.Traverse() if p.IsA(UsdGeom.Mesh)]
    assert len(meshes) == 59
    collision_pairs = 0
    for mesh in meshes:
        if not mesh.HasAPI(UsdPhysics.CollisionAPI):
            continue
        visual = mesh.GetParent().GetChild(mesh.GetName().removesuffix("_1"))
        assert visual and visual != mesh and visual.IsA(UsdGeom.Mesh)
        assert not visual.HasAPI(UsdPhysics.CollisionAPI)
        assert UsdGeom.Imageable(visual).ComputePurpose() == UsdGeom.Tokens.default_
        assert mesh.GetMetadata("references") == visual.GetMetadata("references")
        collision_pairs += 1
    assert collision_pairs == 21
    bounds = (
        UsdGeom.BBoxCache(
            Usd.TimeCode.Default(), [UsdGeom.Tokens.default_, UsdGeom.Tokens.guide]
        )
        .ComputeWorldBound(stage.GetDefaultPrim())
        .ComputeAlignedBox()
    )
    low, high = stage.GetDefaultPrim().GetAttribute("extentsHint").Get()
    assert Gf.IsClose(low, Gf.Vec3f(bounds.GetMin()), 1e-5) and Gf.IsClose(
        high, Gf.Vec3f(bounds.GetMax()), 1e-5
    )
    print(
        "PASS: standard nested layout; 44 bodies, six equality loop closures, 31 actuators; 59 instances / 38 meshes / 21 shared pairs; no floor or archive; hashes and USD composition"
    )

    if converted_source is not None:
        provenance = json.loads((package / "SOURCE.json").read_text())
        for name, digest in provenance["raw_usd_sha256"].items():
            assert (
                hashlib.sha256((converted_source / name).read_bytes()).hexdigest()
                == digest
            ), name
        source = Usd.Stage.Open(str(converted_source / "H2Loop.usda"))
        removed = "/H2Loop/Geometry/floor"
        assert {p.GetPath() for p in stage.Traverse()} == {
            p.GetPath() for p in source.Traverse() if str(p.GetPath()) != removed
        }
        # Every original authored attribute, relationship, and API survives,
        # except floor specs, collision purpose, and refreshed cached bounds.
        for prim in source.Traverse():
            if str(prim.GetPath()) == removed:
                continue
            runtime = stage.GetPrimAtPath(prim.GetPath())
            assert runtime.GetTypeName() == prim.GetTypeName(), prim.GetPath()
            for attr in prim.GetAuthoredAttributes():
                if attr.GetName() == "extentsHint" or (
                    attr.GetName() == "purpose" and prim.HasAPI(UsdPhysics.CollisionAPI)
                ):
                    continue
                assert attr.Get() == runtime.GetAttribute(attr.GetName()).Get(), (
                    attr.GetPath()
                )
            for rel in prim.GetAuthoredRelationships():
                assert (
                    rel.GetTargets()
                    == runtime.GetRelationship(rel.GetName()).GetTargets()
                ), rel.GetPath()
            old_apis = prim.GetMetadata("apiSchemas")
            new_apis = runtime.GetMetadata("apiSchemas")
            old_names = set(old_apis.GetAddedOrExplicitItems()) if old_apis else set()
            new_names = set(new_apis.GetAddedOrExplicitItems()) if new_apis else set()
            assert old_names == new_names, prim.GetPath()
        for name in (
            "Payload/GeometryLibrary.usdc",
            "Payload/MaterialsLibrary.usdc",
            "Payload/Contents.usda",
        ):
            assert (package / name).read_bytes() == (
                converted_source / name
            ).read_bytes(), name
        print(
            "PASS: fresh converter hashes match; original attributes, targets, APIs, hierarchy, and shared libraries preserved"
        )


def validate_mjcf(package: Path, mjcf: Path) -> None:
    """Compare robot mass, inertia, body placement, and anchors to pinned MJCF."""
    import mujoco
    import numpy as np

    provenance = json.loads((package / "SOURCE.json").read_text())
    assert (
        hashlib.sha256(mjcf.read_bytes()).hexdigest()
        == provenance["source_mjcf_sha256"]
    )
    for name, digest in provenance["mesh_files_sha256"].items():
        assert (
            hashlib.sha256((mjcf.parent / name).read_bytes()).hexdigest() == digest
        ), name
    model = mujoco.MjModel.from_xml_path(str(mjcf))
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)
    stage = Usd.Stage.Open(str(package / "H2Loop.usda"))
    bodies = {
        p.GetName(): p for p in stage.Traverse() if p.HasAPI(UsdPhysics.RigidBodyAPI)
    }
    assert model.nbody - 1 == len(bodies) == 44
    cache = UsdGeom.XformCache()

    def rotation(quaternion):
        matrix = np.empty(9)
        mujoco.mju_quat2Mat(matrix, np.asarray(quaternion, dtype=float))
        return matrix.reshape(3, 3)

    for i in range(1, model.nbody):
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, i)
        prim = bodies[name]
        world = cache.GetLocalToWorldTransform(prim)
        np.testing.assert_allclose(
            world.ExtractTranslation(), data.xpos[i], atol=1e-6, rtol=0
        )
        np.testing.assert_allclose(
            # quatf transforms evaluated by OpenUSD differ from MuJoCo by
            # up to 9e-6 for the converter's near-identity waist rotations.
            np.asarray(world)[:3, :3].T,
            rotation(data.xquat[i]),
            atol=1e-5,
            rtol=0,
        )
        mass = UsdPhysics.MassAPI(prim)
        np.testing.assert_allclose(
            mass.GetMassAttr().Get(), model.body_mass[i], rtol=1e-6
        )
        np.testing.assert_allclose(
            mass.GetCenterOfMassAttr().Get(), model.body_ipos[i], atol=1e-6
        )
        principal = mass.GetPrincipalAxesAttr().Get()
        usd_rotation = rotation([principal.GetReal(), *principal.GetImaginary()])
        mjc_rotation = rotation(model.body_iquat[i])
        usd_inertia = (
            usd_rotation @ np.diag(mass.GetDiagonalInertiaAttr().Get()) @ usd_rotation.T
        )
        mjc_inertia = mjc_rotation @ np.diag(model.body_inertia[i]) @ mjc_rotation.T
        np.testing.assert_allclose(usd_inertia, mjc_inertia, atol=1e-7, rtol=1e-5)
    loops = {
        p.GetName(): p
        for p in stage.Traverse()
        if p.IsA(UsdPhysics.Joint)
        and p.GetAttribute("physics:excludeFromArticulation").Get()
    }
    assert model.neq == len(loops) == 6
    for i in range(model.neq):
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_EQUALITY, i)
        joint = UsdPhysics.Joint(loops[name])
        assert model.eq_type[i] == mujoco.mjtEq.mjEQ_CONNECT
        assert joint.GetBody0Rel().GetTargets() == [
            bodies[
                mujoco.mj_id2name(
                    model, mujoco.mjtObj.mjOBJ_BODY, int(model.eq_obj1id[i])
                )
            ].GetPath()
        ]
        assert joint.GetBody1Rel().GetTargets() == [
            bodies[
                mujoco.mj_id2name(
                    model, mujoco.mjtObj.mjOBJ_BODY, int(model.eq_obj2id[i])
                )
            ].GetPath()
        ]
        np.testing.assert_allclose(
            joint.GetLocalPos0Attr().Get(), model.eq_data[i, :3], atol=1e-6, rtol=0
        )
        np.testing.assert_allclose(
            joint.GetLocalPos1Attr().Get(), model.eq_data[i, 3:6], atol=1e-6, rtol=0
        )
    print(
        "PASS: pinned MJCF and meshes match; all 44 masses, inertia tensors, body poses, and six loop endpoints/anchors preserved"
    )


def import_robot(
    entrypoint: Path, *, mjc_only: bool = False, register_mujoco: bool = True
):
    """Import with the G1 example's configuration and selected schema resolver."""
    import newton
    import warp as wp
    from newton.usd import SchemaResolverMjc, SchemaResolverNewton

    builder = newton.ModelBuilder()
    if register_mujoco:
        newton.solvers.SolverMuJoCo.register_custom_attributes(builder)
    builder.default_joint_cfg = newton.ModelBuilder.JointDofConfig(
        limit_ke=1e3, limit_kd=1e1, friction=1e-5
    )
    builder.default_shape_cfg.ke = 1e3
    builder.default_shape_cfg.kd = 2e2
    builder.default_shape_cfg.kf = 1e3
    builder.default_shape_cfg.mu = 0.75
    resolvers = [SchemaResolverMjc()]
    if not mjc_only:
        resolvers.append(SchemaResolverNewton())
    builder.add_usd(
        str(entrypoint),
        xform=wp.transform(wp.vec3(0, 0, 0.2)),
        collapse_fixed_joints=True,
        enable_self_collisions=False,
        hide_collision_shapes=True,
        skip_mesh_approximation=True,
        schema_resolvers=resolvers,
    )
    return builder


def validate_import(package: Path):
    """Verify MuJoCo-resolved dynamics, effort limits, and original motor modes."""
    import newton
    import numpy as np

    imported = import_robot(package / "H2Loop.usda")
    reference = import_robot(package / "H2Loop.usda", mjc_only=True)
    plain = import_robot(package / "H2Loop.usda", register_mujoco=False)
    assert imported.joint_label == reference.joint_label
    assert imported.joint_label == plain.joint_label
    assert imported._custom_frequency_counts["mujoco:actuator"] == 31
    ctrl_source = imported.custom_attributes["mujoco:ctrl_source"]
    assert all(
        (ctrl_source.default if value is None else value)
        == int(newton.solvers.SolverMuJoCo.CtrlSource.CTRL_DIRECT)
        for value in ctrl_source.values
    ), "Original H2 motors must retain direct MuJoCo control"
    for builder in (imported, reference, plain):
        assert all(
            mode == int(newton.JointTargetMode.NONE)
            for mode in builder.joint_target_mode
        ), "USD import must not introduce generic drives on active or passive joints"
    loops = [
        i for i, label in enumerate(plain.joint_label) if label.endswith("_connect")
    ]
    assert plain.body_count == 44 and len(loops) == 6
    assert all(plain.joint_type[i] == newton.JointType.BALL for i in loops)
    assert all(body >= 0 for body in imported.shape_body), (
        "Asset must not import a static floor"
    )
    for name in (
        "joint_armature",
        "joint_damping",
        "joint_friction",
        "joint_effort_limit",
    ):
        np.testing.assert_allclose(
            getattr(imported, name),
            getattr(reference, name),
            rtol=1e-6,
            atol=1e-9,
            err_msg=name,
        )
        np.testing.assert_allclose(
            getattr(imported, name),
            getattr(plain, name),
            rtol=1e-6,
            atol=1e-9,
            err_msg=name,
        )
    stage = Usd.Stage.Open(str(package / "H2Loop.usda"))
    limited_joints = 0
    for index, label in enumerate(imported.joint_label):
        prim = stage.GetPrimAtPath(label)
        if not prim or not prim.GetAttribute("mjc:armature").HasAuthoredValue():
            continue
        start, end = imported.joint_qd_start[index : index + 2]
        np.testing.assert_allclose(
            imported.joint_armature[start:end],
            prim.GetAttribute("mjc:armature").Get(),
            rtol=1e-6,
        )
        np.testing.assert_allclose(
            imported.joint_damping[start:end],
            prim.GetAttribute("mjc:damping").Get(),
            rtol=1e-6,
        )
        np.testing.assert_allclose(
            imported.joint_friction[start:end],
            prim.GetAttribute("mjc:frictionloss").Get(),
            rtol=1e-6,
        )
        lower = prim.GetAttribute("mjc:actuatorfrcrange:min").Get()
        upper = prim.GetAttribute("mjc:actuatorfrcrange:max").Get()
        limited = prim.GetAttribute("mjc:actuatorfrclimited").Get()
        if (
            limited != "false"
            and lower is not None
            and upper is not None
            and lower < upper
        ):
            np.testing.assert_allclose(
                imported.joint_effort_limit[start:end],
                max(abs(lower), abs(upper)),
                rtol=1e-6,
            )
            limited_joints += 1
    assert limited_joints == 35
    print(
        "PASS: explicit MuJoCo resolver preserves dynamics and all 35 effort limits; 31 direct-control motors, no generic drives or passive-joint actuation"
    )
    return imported


def simulate(builder, world_count: int, device: str) -> None:
    """Run a ten-second G1-style posture test, including drives on passive DOFs."""
    import newton
    import numpy as np
    import warp as wp

    for index in range(6, builder.joint_dof_count):
        builder.joint_target_ke[index] = 500.0
        builder.joint_target_kd[index] = 10.0
        builder.joint_target_mode[index] = int(newton.JointTargetMode.POSITION)
    builder.approximate_meshes("bounding_box")
    worlds = newton.ModelBuilder()
    worlds.replicate(builder, world_count)
    worlds.default_shape_cfg.ke = 1e3
    worlds.default_shape_cfg.kd = 2e2
    worlds.add_ground_plane()
    model = worlds.finalize()
    solver = newton.solvers.SolverMuJoCo(
        model,
        use_mujoco_cpu=device == "cpu",
        separate_worlds=world_count > 1,
        use_mujoco_contacts=True,
        solver="newton",
        integrator="implicitfast",
        njmax=300,
        nconmax=150,
        cone="elliptic",
        impratio=100,
        iterations=100,
        ls_iterations=50,
    )
    state, next_state, control = model.state(), model.state(), model.control()
    assert solver.mj_model.neq == 6, "MuJoCo must retain all six loop constraints"
    newton.eval_fk(model, model.joint_q, model.joint_qd, state)
    pelvis = [
        i for i, label in enumerate(model.body_label) if label.endswith("/pelvis")
    ]
    loops = [
        i for i, label in enumerate(model.joint_label) if label.endswith("_connect")
    ]
    assert len(pelvis) == world_count and len(loops) == 6 * world_count
    parent, child = model.joint_parent.numpy(), model.joint_child.numpy()
    parent_anchor, child_anchor = model.joint_X_p.numpy(), model.joint_X_c.numpy()
    min_height, min_upright, max_error = math.inf, 1.0, 0.0
    for _ in range(600):
        for _ in range(6):
            state.clear_forces()
            solver.step(state, next_state, control, None, 1.0 / 360.0)
            state, next_state = next_state, state
        body = state.body_q.numpy()
        assert np.isfinite(body).all(), "Non-finite body state"
        min_height = min(min_height, float(body[pelvis, 2].min()))
        min_upright = min(
            min_upright,
            min(
                float(wp.quat_rotate(wp.quat(body[i, 3:]), wp.vec3(0, 0, 1))[2])
                for i in pelvis
            ),
        )
        for i in loops:
            a = wp.transform_point(
                wp.transform(body[parent[i], :3], body[parent[i], 3:]),
                wp.vec3(parent_anchor[i, :3]),
            )
            b = wp.transform_point(
                wp.transform(body[child[i], :3], body[child[i], 3:]),
                wp.vec3(child_anchor[i, :3]),
            )
            max_error = max(max_error, float(wp.length(a - b)))
    print(
        json.dumps(
            {
                "device": device,
                "world_count": world_count,
                "duration_s": 10,
                "pelvis_final_m": body[pelvis, 2].tolist(),
                "pelvis_min_m": min_height,
                "upright_min": min_upright,
                "loop_anchor_max_m": max_error,
            },
            indent=2,
        )
    )
    assert min_height > 0.9, "H2 fell or lost standing height"
    assert min_upright > 0.95, "H2 lost upright posture"
    assert max_error < 0.005, "Loop anchors separated by more than 5 mm"
    print("PASS: H2 stayed upright and all six loop closures stayed within 5 mm")


def main() -> None:
    """Run structural checks and optional Newton import and simulation checks."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--package",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "usd_structured",
    )
    parser.add_argument(
        "--newton",
        action="store_true",
        help="Also validate MuJoCo-resolved Newton import",
    )
    parser.add_argument(
        "--simulate", action="store_true", help="Also run a ten-second posture test"
    )
    parser.add_argument("--device", default="cpu")
    parser.add_argument(
        "--converted-source",
        type=Path,
        help="Compare with a fresh, unmodified converter output",
    )
    parser.add_argument(
        "--mjcf",
        type=Path,
        help="Verify physical properties against the pinned upstream MJCF and meshes",
    )
    parser.add_argument("--world-count", type=int, default=1)
    args = parser.parse_args()
    if args.world_count < 1:
        parser.error("--world-count must be positive")
    if args.simulate and args.device == "cpu" and args.world_count != 1:
        parser.error(
            "Newton's native MuJoCo CPU backend simulates one world; use --world-count 1 or a CUDA device"
        )
    validate_package(args.package.resolve(), args.converted_source)
    if args.mjcf:
        validate_mjcf(args.package.resolve(), args.mjcf.resolve())
    if args.newton or args.simulate:
        import warp as wp

        with wp.ScopedDevice(args.device):
            builder = validate_import(args.package.resolve())
            if args.simulate:
                simulate(builder, args.world_count, args.device)


if __name__ == "__main__":
    main()
