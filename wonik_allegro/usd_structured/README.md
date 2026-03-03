# About Structured USD Robots

This asset was created with the [mujoco-usd-converter](https://github.com/newton-physics/mujoco-usd-converter), having converted the source MJCF from the MuJoCo Menagerie as of [this commit](https://github.com/google-deepmind/mujoco_menagerie/blob/a03e87bf13502b0b48ebbf2808928fd96ebf9cf3/wonik_allegro/left_hand.xml). The conversion results are unchanged here.

[This layer](./allegro_left.usda) is the main entrypoint for the asset, called the Asset Interface. Consuming users/code/applications should load this file to access the fully composed USD Robot. The interface is a lightweight plain text layer & the bulk of the robot is behind a Payload, enabling delayed-load access to the asset.

The pertinent simulation data is contained in the [Physics Layer](./Payload/Physics.usda) within the Payload. This is a plain text layer, for legibility & ease of editing. It includes all `UsdPhysics`, `NewtonPhysics`, and `MjcPhysics` schemas & attributes, so tuning simulation values can be entirely accomplished by editing this layer alone.

Larger structural changes (e.g. adding new bodies or colliders) would require editing several layers & is best done with a USD aware application rather than by manual edits.

The body hierarchy in this asset is nested, with child bodies specified relative to their parent body, just like the original MJCF. This is a newer feature in OpenUSD & requires at least USD v25.11 for full support, though it is possible to parse nested bodies in older runtimes as well.
