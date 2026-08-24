# About Structured USD Robots

This asset was created from the packaged
[`asRoBallet.xml`](../mjcf/asRoBallet.xml) with
[mujoco-usd-converter](https://github.com/newton-physics/mujoco-usd-converter)
0.5.0 and its locked dependencies. The packaged MJCF is based on the asRoBallet
source at
[this commit](https://github.com/asRoBallet/asRoBallet_mujoco/blob/0747bf245081f892fc12b723a0fe78581f121c61/robots/mjcf/asRoBallet.xml),
with consistent visual-group classification for all three wheel axle meshes.
The USD package represents both supported topologies; see the
[asset README](../README.md#mjcf-topologies) for their physical differences.

[This layer](./asRoBallet.usda) is the public ball-joint entry point.
[The floating-ball layer](./asRoBallet_floating_ball.usda) is the public entry
point with independent torso and ball state. Both interfaces are lightweight
plain-text layers with the robot data behind payloads for delayed loading.

The two topology layers reference the same
[torso](./Components/Torso.usda) and [ball](./Components/Ball.usda) components.
They differ only in ball placement and whether `torso_ball_joint` connects the
two components. Materials, actuators, and scene settings are shared through the
files under `Payload`.

Both public entries have been validated for layer parsing and payload loading
with OpenUSD 26.03 and for model import with Newton. The ball-joint entry
preserves the complete prim, schema, attribute, and relationship composition of
the converter output.

The body hierarchy is nested, with child bodies specified relative to their
parent bodies, as in the source MJCF. Support for nested rigid bodies varies by
application; consumers should verify payload loading and simulation in their
target runtime.

## Warnings

MJCF sensors are not currently exported by the converter. The robot geometry,
materials, bodies, collisions, sites, joints, and actuators are included.
