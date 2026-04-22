# SO-101 Simulation Assets

## Overview

This folder contains robot assets for the [SO-101](https://huggingface.co/docs/lerobot/so101)
low-cost 6-DoF manipulator (leader/follower pair) developed by
[The Robot Studio](https://www.therobotstudio.com/) and used by the
[LeRobot](https://github.com/huggingface/lerobot) project.

The follower arm uses six STS3215 (1/345 gearing) smart-servo motors; the leader
arm uses the same motor body with mixed gear ratios
(1/191, 1/345, 1/191, 1/147, 1/147, 1/147) so it can be back-driven by hand.

## Layout

```text
therobotstudio_soarm101/
├── LICENSE
├── README.md
├── meshes/                        # visual + collision meshes (STL) and Onshape .part sidecars
├── urdf/
│   └── so101_new_calib.urdf       # URDF – zero = mid-range of each joint
├── mjcf/
│   ├── scene.xml                  # MuJoCo scene that includes the robot model
│   ├── so101_new_calib.xml        # MJCF – zero = mid-range of each joint
│   └── joints_properties.xml      # upstream provenance only – not <include>d by scene.xml (see note below)
└── usd/                           # Isaac Sim 4-layer structured USD (binary .usd crate)
    ├── so101_new_calib.usd        # top-level composition (payload + sublayers)
    └── configuration/
        ├── so101_new_calib_base.usd     # geometry + materials (≈23 MB)
        ├── so101_new_calib_physics.usd  # PhysX articulation, joints, collisions
        ├── so101_new_calib_robot.usd    # Isaac Sim robot schema layer
        └── so101_new_calib_sensor.usd   # sensor-hook layer (empty stub upstream)
```

This layout follows the same convention as the other manipulators in this
repo (e.g. `unitree_g1/`): meshes under `meshes/`, URDF under `urdf/`, MJCF
under `mjcf/`, structured USD under `usd/`. The URDF uses relative
`../meshes/…` paths (inherited from upstream, which replaced `package://`
with relative paths) and the MJCF uses `<compiler meshdir="../meshes"/>`,
so both load directly against the sibling `meshes/` folder.

## Calibration

Only the **new calibration** (`*_new_calib.*`) is vendored here — joint zero
is defined at the middle of each joint range. This is the calibration
convention used by NVIDIA Isaac Sim 6.0 and is the default in upstream.
The legacy *old* calibration (zero = arm fully extended horizontally) is
intentionally omitted because Isaac Sim does not publish a USD for it.

## Sources

### URDF, MJCF, meshes

The URDF, MJCF and mesh files were retrieved from the
[`TheRobotStudio/SO-ARM100`](https://github.com/TheRobotStudio/SO-ARM100)
repository, under `Simulation/SO101/`, at commit
[`aec17bb`](https://github.com/TheRobotStudio/SO-ARM100/tree/aec17bbc256d1a7342d53aaa4950595d4c30b40d/Simulation/SO101).

Per the upstream README:

- The robot model files were generated from an Onshape CAD model via the
  [`onshape-to-robot`](https://github.com/rhoban/onshape-to-robot) plugin.
- The generated URDFs were modified to use relative mesh paths instead of
  `package://…`, so the files in this directory can be loaded directly by any
  tool that resolves mesh filenames relative to the URDF/MJCF.
- Base collision meshes were removed upstream because they were causing
  problematic collision behavior during simulation and planning.
- STS3215 motor parameters are adapted from the Open Duck Mini project.

### USD

The USD model was collected from the NVIDIA Isaac Sim 6.0 asset bucket
(`omniverse-content-production.s3-us-west-2.amazonaws.com`) under
`Assets/Isaac/6.0/Isaac/Robots/RobotStudio/so101_new_calib/`. It uses the
Isaac Sim 4-layer *structured USD* convention — a top-level composition file
that payload-references a `configuration/*_base.usd` (geometry + materials),
`*_physics.usd` (PhysX articulation & joint state), `*_robot.usd` (robot
schema) and `*_sensor.usd` (sensor mount points).

This is the same robot that appears in the
[Isaac Sim 6.0 Robot Assets catalog](https://docs.isaacsim.omniverse.nvidia.com/6.0.0/assets/usd_assets_robots.html)
as **RobotStudio / so101_new_calib** (Apache 2.0, 6 joints / 6 DOF,
`PhysX JointAPI` + `PhysX ArticulationAPI`). The files are published
byte-identically in the Isaac Sim 5.0, 5.1 and 6.0 buckets; we pin to the
6.0 tree so redistributions track the current GA release.

The USD files under `usd/` are copied byte-for-byte from the Isaac Sim 6.0
bucket (no schema edits); the git blob hashes therefore match the hashes of
the corresponding bucket objects and git itself serves as the provenance
record.

> SO-100 (the predecessor single-calibration arm) is published alongside
> SO-101 at the same NVIDIA location under `RobotStudio/so100/` (also
> Apache 2.0) but is not yet vendored here; happy to add it as a sibling
> folder on request.

## Notes / Known Limitations

- In LeRobot the gripper is treated as a linear joint where `0` = fully closed
  and `100` = fully open; that mapping is **not** yet reflected in these
  URDF/MJCF files (inherited from upstream).
- The `.part` files in `meshes/` are Onshape export metadata that ship with the
  upstream repository; they are kept alongside the STLs for traceability but
  are not required by simulators.
- `mjcf/joints_properties.xml` is kept verbatim from upstream (servo/backlash
  defaults as originally shipped by `TheRobotStudio/SO-ARM100`) as
  **historical provenance only**. It is not `<include>`d by `mjcf/scene.xml`
  or `mjcf/so101_new_calib.xml`, and its `kp`/`kv`/`forcerange` values
  intentionally differ from the inlined defaults in `so101_new_calib.xml`
  (which use the RBE501-RL-arm-project derivation, servo `P=16 → kp≈998.22`).
  Treat `so101_new_calib.xml` — not this file — as the source of truth.
- The URDF's trailing `gripper_frame_link`/`gripper_frame_joint` pair had two
  minor upstream-schema quirks (a stray `<origin>` directly under `<link>`
  and an `<axis xyz="0 0 0"/>` on a `type="fixed"` joint); both were removed
  here because they are no-ops that strict URDF validators reject. The
  kinematics of the dummy gripper frame are unchanged.

## License

All files in this folder are redistributed under the
[Apache License 2.0](LICENSE). There are two upstream copyright holders, each
of whom licenses their own contribution under Apache 2.0:

| Files                                                               | Upstream publisher                                                                              | License                                                                                           |
| ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `urdf/**`, `mjcf/**`, `meshes/**` | [The Robot Studio — SO-ARM100](https://github.com/TheRobotStudio/SO-ARM100) (and Onshape-to-robot contributors) | Apache 2.0 — matches the upstream repo's top-level [`LICENSE`](https://github.com/TheRobotStudio/SO-ARM100/blob/main/LICENSE) |
| `usd/**`                                                            | NVIDIA — Isaac Sim 6.0 asset bucket                                                             | Apache 2.0 — per the [Isaac Sim 6.0 Robot Assets catalog](https://docs.isaacsim.omniverse.nvidia.com/6.0.0/assets/usd_assets_robots.html) entry for `RobotStudio/so101_new_calib` |

### Redistribution checklist (Apache 2.0 §4)

- **§4(a) — License text.** The full Apache 2.0 text is shipped in [`LICENSE`](LICENSE).
- **§4(b) — Change notice.** USD files under `usd/` are byte-for-byte copies
  of the Isaac Sim 6.0 bucket objects. The URDF/MJCF/mesh files are copied
  from the pinned upstream commit
  ([`aec17bb`](https://github.com/TheRobotStudio/SO-ARM100/tree/aec17bbc256d1a7342d53aaa4950595d4c30b40d/Simulation/SO101))
  with only two modifications applied: (1) mesh references rewritten from
  `assets/…` to `../meshes/…` to match this repo's per-robot folder layout,
  and (2) two no-op URDF schema quirks removed from the dummy gripper frame
  (stray `<origin>` under `<link>`, zero-vector `<axis>` on a fixed joint).
  No kinematic, inertial or actuator parameters were changed.
- **§4(c) — Retained notices.** Neither upstream source embeds copyright
  strings in the redistributed files (`strings` on the USD crate files yields
  no copyright/author metadata, and the URDFs carry none either), so there
  are no in-file notices to preserve.
- **§4(d) — NOTICE file.** No `NOTICE` file is published by either upstream —
  not in the `TheRobotStudio/SO-ARM100` repository and not under any
  `Assets/Isaac/6.0/…/RobotStudio/` S3 prefix — so none is included here.

### Isaac Sim application license

The **Isaac Sim application itself** is covered by the separate *NVIDIA Isaac
Sim Additional Software and Materials License* — that governs running the
simulator and is orthogonal to the per-asset license assigned to
`so101_new_calib.usd` in the asset catalog. Nothing in this folder
distributes or depends on the Isaac Sim binaries.
