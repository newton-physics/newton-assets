# Four-Bar Pole

## Description
Four-Bar Pole is a minimal closed-loop test mechanism: a planar parallel four-bar linkage
(`ground_link`, `crank`, `coupler`, `rocker`) with an inverted pendulum `pole` rigidly mounted on
the coupler. The `rocker_to_ground` revolute joint closes the kinematic loop and is excluded from the
articulation tree. The model serves as a compact benchmark for control of closed-loop mechanisms.

The geometry is defined with simple box primitives referenced from `usd/Props/instanceable_meshes.usda`,
so the model has no external mesh dependencies.

## Changelog

### [07/02/2026]
- Initial release.

## Assets

The following assets are provided for this model:

| filename | type | description |
|---|---|---|
| `usd/fourbar_pole.usda` | USD (text) | The fixed-base model of **Four-Bar Pole** as a `UsdPhysics` scene with box primitive geometry referenced from `usd/Props/`. |
| `usd/Props/instanceable_meshes.usda` | USD (text) | Instanceable box primitive geometry (visuals and collisions) referenced by `usd/fourbar_pole.usda`. |

----
Copyright (C) 2026, Disney Enterprises, Inc. All rights reserved.
