# Seeed Studio reBot DevArm (RobStride) Simulation Assets

## Overview

This package contains robot assets for the **reBot DevArm**, a 6-DOF manipulator with a 2-finger parallel gripper (8 DoF total) developed by [Seeed Studio](https://www.seeedstudio.com/) around [RobStride](https://robstride.com/) quasi-direct-drive actuators. It is derived from the URDF in [Seeed-Projects/reBot-Isaacsim](https://github.com/Seeed-Projects/reBot-Isaacsim).

The subfolders contain:

- **urdf**: Robot description format files
- **usd_structured**: Structured USD layer files, converted from the MuJoCo Menagerie MJCF

## Sources

### URDF

The URDF is the vendor description from [Seeed-Projects/reBot-Isaacsim](https://github.com/Seeed-Projects/reBot-Isaacsim), carrying the full link inertia tensors. Its actuator limits were verified against the physical arm: the effort limit of every joint matches the torque limit read live from the motor firmware over CAN (motors 1-3 are RobStride RS-06 at 36 Nm, motors 4-7 are RS-00 at 14 Nm), and the gripper's limits are the motor's own envelope reflected through the transmission.

Convert it with [urdf-usd-converter](https://github.com/newton-physics/urdf-usd-converter):

```
urdf_usd_converter urdf/seeed_rebot_devarm.urdf <out_dir>
```

URDF cannot express actuator gains or the gripper coupling, so a USD converted from it carries kinematics, inertials and joint limits only; a consuming runtime must author its own drives. The structured USD below carries that information.

### USD (Structured)

The structured USD model was created with the [mujoco-usd-converter](https://github.com/newton-physics/mujoco-usd-converter), converted from the MuJoCo Menagerie MJCF source. For details, see the [usd_structured README](usd_structured/README.md).

## Gripper

The two fingers are not independent degrees of freedom: a single motor drives two opposed racks through one pinion, so their travel is rigidly coupled 1:1. Both the MJCF-derived USD and the source MJCF express this as a joint equality constraint. Consuming runtimes must honor it — without the coupling the jaws drift apart under arm motion instead of holding their commanded opening.

## License

This model is released under an [MIT License](LICENSE), matching what Seeed Studio publishes for the [source repository](https://github.com/Seeed-Projects/reBot-Isaacsim); the license text is carried verbatim.
