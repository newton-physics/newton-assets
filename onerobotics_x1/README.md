# OneRobotics X1 Mobile Manipulator Assets

## Overview

This package contains the OneRobotics X1 mobile manipulator for Newton. The
model combines an omnidirectional wheeled base, a lift mechanism, a two-axis
upper-body mechanism, and two 7-DoF A1 arms.

**The current asset does not include grippers.** `Link_r7` and `Link_l7` are
the terminal links of the two arms. The model must not be presented as capable
of physical grasping until validated gripper geometry and joints are added.

## Contents

- `urdf/x1.urdf`: portable X1 robot description;
- `meshes/`: visual and collision STL meshes;
- `usd/onerobotics_x1.usda`: self-contained structured OpenUSD entry point;
- `LICENSE`: CC BY 4.0 license text;
- `ASSET_LICENSE_STATUS.md`: attribution, covered files, and modifications.

## Model summary

| Component | Count |
|---|---:|
| Links | 30 |
| Joints | 29 |
| Arm DoFs | 14 |
| Lift DoFs | 1 |
| Upper-body DoFs | 2 |
| Grippers | 0 |

## Loading in Newton

```python
import newton

builder = newton.ModelBuilder()
builder.add_usd("usd/onerobotics_x1.usda")
model = builder.finalize()
```

## Source and modifications

- Source model: OneRobotics `X1_URDF_V1_3`;
- Source revision: `e022a7a3ed1d0e408e9837147c3de4f0029867f0`;
- Mesh references were changed from ROS `package://` URIs to portable relative
  paths;
- the robot name was normalized to `onerobotics_x1`;
- zero effort and velocity values were replaced with positive simulation
  limits so Newton does not interpret actuated joints as immobile;
- a structured USD asset was generated with Newton's
  `urdf-usd-converter`.

The arm limits follow the standalone A1 assets. The upper-body and lift values
are conservative simulation limits and are not published hardware ratings.

## License

OneRobotics X1 robot assets © 2026 OneRobotics, licensed under Creative
Commons Attribution 4.0 International. See [`LICENSE`](LICENSE) and
[`ASSET_LICENSE_STATUS.md`](ASSET_LICENSE_STATUS.md).

## Changelog

- 2026-10-14: Initial Newton asset package with mobile base, lift, upper body,
  and dual A1 arms. Grippers are not included.
