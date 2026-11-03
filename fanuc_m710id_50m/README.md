# Fanuc Arm Simulation Assets

## Overview

This folder contains a robot arm asset for a [Fanuc](https://www.fanuc.com/) industrial robot.

The subfolders contain:

- **usd**: `fanuc_arm.usd`, the robot arm in USD format.

## Sources

### USD

The USD file was adapted from the [fanuc_m710id_50m](https://huggingface.co/datasets/nvidia/isaacsim-assets/tree/ea6ff6d95aa7d7e9c578a584711a242c2ad476ee/fanuc_m710id_50m) package in the [NVIDIA Isaac Sim Assets](https://huggingface.co/datasets/nvidia/isaacsim-assets) dataset at ea6ff6d.

### Changes

The following changes were made to the source asset.

**Joint drives and actuators**

A drive is the motor model on a joint. Stiffness pulls the joint to its target angle. An actuator is the motor model that MuJoCo uses.

- The drive force limit was removed. It was 8,000, 10,000, 5,000, 2,000, 1,000 and 900 for J1 to J6.
- The drive target velocity was removed.
- The `PhysicsDriveAPI` and `PhysicsJointStateAPI` tags were removed from the joints. The MuJoCo variant of the source removes them in the same way.
- Each joint got a `mjc:ref` value of 0 and starting position and velocity values of 0.
- A new `Physics` group holds six MuJoCo actuators, one per joint. Each one has a position gain and a velocity damping term. The gains for J1 to J6 are 358,099.7, 520,787.6, 2,665,959.5, 622,515.2, 251,896.2 and 165.9. The damping terms are 14,324, 20,831.5, 106,638.4, 24,900.6, 10,075.8 and 6.6.

**End-of-arm tool**

- The `flange` group on `J6_link` was removed. It held `ee_link` and `fanuc_flange`.
- An `EOAT` group (end-of-arm tool) was added to `J6_link`. It is made of three cuboids. `base` is 0.075 m by 0.200 m by 0.200 m. `arm_y` and `arm_z` are two arms that cross in front of the base. They are 0.322 m and 0.472 m long, 0.040 m wide and 0.032 m thick. Each cuboid is both visible and a collision shape.
- A `GripperPads` group was added to `J6_link`. It holds the visual geometry of the suction cups. It has four cylinders, `pad_0` to `pad_3`. Each is 0.03 m in radius and 0.008 m tall. They are blue and have no collision.

**Structure**

- The source is split into several files and has MuJoCo, Newton, PhysX and Sensor variants. This file is one flat file with no variants. The Newton and PhysX settings of the source are not included.
- The collision meshes of the six links and the base are stored as shared instances. The geometry is the same.

**Not changed**

The visual and collision meshes of the base and links J1 to J6 are identical to the source. So are the link masses and inertias, and the joint axes, limits and positions. The joint drive stiffness, damping, target position and type are also the same as the source.

## Attribution

Fanuc M-710iD/50M asset from the [NVIDIA Isaac Sim Assets](https://huggingface.co/datasets/nvidia/isaacsim-assets) dataset. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

The license text was copied from the [source dataset](https://huggingface.co/datasets/nvidia/isaacsim-assets/blob/ea6ff6d95aa7d7e9c578a584711a242c2ad476ee/fanuc_m710id_50m/.metadata/license.txt).

Fanuc is a trademark of FANUC Corporation. This asset is not endorsed by FANUC Corporation.

## License

This model is released under the [Creative Commons Attribution 4.0 International License](LICENSE).
