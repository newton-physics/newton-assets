# About Structured USD Robots

This asset was created with the
[mujoco-usd-converter](https://github.com/newton-physics/mujoco-usd-converter)
0.5.0 from the asRoBallet MJCF source at
[this commit](https://github.com/asRoBallet/asRoBallet_mujoco/blob/0747bf245081f892fc12b723a0fe78581f121c61/robots/mjcf/asRoBallet.xml).
The conversion results are unchanged here.

[This layer](./asRoBallet.usda) is the main entrypoint for the asset, called the
Asset Interface. Consuming users, code, and applications should load this file
to access the fully composed USD robot. The interface is a lightweight plain
text layer, while the bulk of the robot is behind a payload for delayed loading.

The pertinent simulation data is contained in the
[Physics Layer](./Payload/Physics.usda) within the payload. This plain text layer
includes the `UsdPhysics`, `NewtonPhysics`, and `MjcPhysics` schemas and
attributes, so simulation values can be tuned without editing the geometry
layers.

Larger structural changes, such as adding bodies or colliders, require editing
several layers and are best made with a USD-aware application rather than by
manually editing the generated files.

The body hierarchy is nested, with child bodies specified relative to their
parent bodies, as in the source MJCF. Support for nested rigid bodies varies by
application; consumers should verify payload loading and simulation in their
target runtime.

## Warnings

MJCF sensors are not currently exported by the converter. The robot geometry,
materials, bodies, collisions, sites, joints, and actuators are included.
