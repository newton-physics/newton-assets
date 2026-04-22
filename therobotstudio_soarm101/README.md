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

```
therobotstudio_soarm101/
├── LICENSE
├── README.md
├── joints_properties.xml          # shared MJCF joint limits / actuator defaults
├── scene.xml                      # MuJoCo scene that includes the robot model
├── so101_new_calib.urdf           # URDF – zero = mid-range of each joint
├── so101_new_calib.xml            # MJCF – zero = mid-range of each joint
├── assets/                        # visual + collision meshes (STL) and Onshape .part files
└── usd/                           # Isaac Sim 4-layer structured USD (binary .usd crate)
    ├── .collect.mapping.json      # source-URL + SHA-1 for each redistributed file
    ├── so101_new_calib.usd        # top-level composition (payload + sublayers)
    └── configuration/
        ├── so101_new_calib_base.usd     # geometry + materials (≈23 MB)
        ├── so101_new_calib_physics.usd  # PhysX articulation, joints, collisions
        ├── so101_new_calib_robot.usd    # Isaac Sim robot schema layer
        └── so101_new_calib_sensor.usd   # sensor-hook layer (empty stub upstream)
```

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

The exact source URLs, together with the SHA-1 of each downloaded file, are
recorded in [`usd/.collect.mapping.json`](usd/.collect.mapping.json) so the
content can be re-verified against the upstream bucket. The files were copied
byte-for-byte (no schema edits), so `source_hash` and `target_hash` are equal
— unlike assets produced by Isaac Sim's *Collect Asset* tool, which transcodes
crate → USDA and therefore has differing hashes.

> SO-100 (the predecessor single-calibration arm) is published alongside
> SO-101 at the same NVIDIA location under `RobotStudio/so100/` (also
> Apache 2.0) but is not yet vendored here; happy to add it as a sibling
> folder on request.

## Notes / Known Limitations

- In LeRobot the gripper is treated as a linear joint where `0` = fully closed
  and `100` = fully open; that mapping is **not** yet reflected in these
  URDF/MJCF files (inherited from upstream).
- The `.part` files in `assets/` are Onshape export metadata that ship with the
  upstream repository; they are kept alongside the STLs for traceability but
  are not required by simulators.

## License

All files in this folder are redistributed under the
[Apache License 2.0](LICENSE). There are two upstream copyright holders, each
of whom licenses their own contribution under Apache 2.0:

| Files                                                               | Upstream publisher                                                                              | License                                                                                           |
| ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `so101_new_calib.urdf`, `so101_new_calib.xml`, `joints_properties.xml`, `scene.xml`, `assets/**` | [The Robot Studio — SO-ARM100](https://github.com/TheRobotStudio/SO-ARM100) (and Onshape-to-robot contributors) | Apache 2.0 — matches the upstream repo's top-level [`LICENSE`](https://github.com/TheRobotStudio/SO-ARM100/blob/main/LICENSE) |
| `usd/**`                                                            | NVIDIA — Isaac Sim 6.0 asset bucket                                                             | Apache 2.0 — per the [Isaac Sim 6.0 Robot Assets catalog](https://docs.isaacsim.omniverse.nvidia.com/6.0.0/assets/usd_assets_robots.html) entry for `RobotStudio/so101_new_calib` |

### Redistribution checklist (Apache 2.0 §4)

- **§4(a) — License text.** The full Apache 2.0 text is shipped in [`LICENSE`](LICENSE).
- **§4(b) — Change notice.** USD files are byte-for-byte copies of the Isaac
  Sim 6.0 bucket objects; the SHA-1s in [`usd/.collect.mapping.json`](usd/.collect.mapping.json)
  can be re-verified against the `source_url` for each file. The URDF/MJCF
  files are likewise unmodified from the pinned upstream commit
  ([`aec17bb`](https://github.com/TheRobotStudio/SO-ARM100/tree/aec17bbc256d1a7342d53aaa4950595d4c30b40d/Simulation/SO101)).
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
