# About Structured USD Robots

This asset was created with the [mujoco-usd-converter](https://github.com/newton-physics/mujoco-usd-converter), having converted the source MJCF from the MuJoCo Menagerie as of [this commit](https://github.com/google-deepmind/mujoco_menagerie/blob/da76818e269b82289eba39808e2fb91d679d6994/seeed_rebot_devarm/seeed_rebot_devarm.xml). The conversion results are unchanged here.

That commit is [mujoco_menagerie#300](https://github.com/google-deepmind/mujoco_menagerie/pull/300) as merged to `main`, so the source is pinned to an immutable SHA rather than to a branch.

[This layer](./seeed_rebot_devarm.usda) is the main entrypoint for the asset, called the Asset Interface. Consuming users/code/applications should load this file to access the fully composed USD Robot. The interface is a lightweight plain text layer & the bulk of the robot is behind a Payload, enabling delayed-load access to the asset.

The pertinent simulation data is contained in the [Physics Layer](./Payload/Physics.usda) within the Payload. This is a plain text layer, for legibility & ease of editing. It includes all `UsdPhysics`, `NewtonPhysics`, and `MjcPhysics` schemas & attributes, so tuning simulation values can be entirely accomplished by editing this layer alone.

Larger structural changes (e.g. adding new bodies or colliders) would require editing several layers & is best done with a USD aware application rather than by manual edits.

The body hierarchy in this asset is nested, with child bodies specified relative to their parent body, just like the original MJCF. This is a newer feature in OpenUSD & requires at least USD v25.11 for full support, though it is possible to parse nested bodies in older runtimes as well.

The source MJCF leaves `solreflimit` at MuJoCo's implicit default, so no `mjc:solreflimit` is authored here and `SolverMuJoCo` applies that default.

## Self-Collision

Self-collision is enabled in the source MJCF and carried into USD. The collision geometry is a convex decomposition (8-12 parts per link, 92 colliders in total) rather than one hull per link, which is what makes robot-robot contacts usable: a single hull per link inflates collision volume to 3.24x the true link volume, against 1.89x for the decomposition.

The MJCF excludes eleven body pairs in `<contact>`, and the converter authors all eleven as `physics:filteredPairs` relationships on the corresponding bodies. Nine are adjacent links that share a motor housing and genuinely interpenetrate in the source meshes. The other two, `gripper_left`/`gripper_right` and `link2`/`link5`, clear each other by only 0.15 mm and 0.77 mm at the `home` keyframe, gaps below what a convex decomposition can represent since its parts necessarily bulge 1-2 mm past the original concave surface.

Consuming runtimes should honour `physics:filteredPairs`; with those pairs filtered the model is contact-free at both keyframes, and self-collision detection remains live everywhere else.

## Gripper Coupling

The two fingers are not independent degrees of freedom on the physical arm: a single motor drives two opposed racks through one pinion, so their travel is rigidly 1:1. The source MJCF expresses this with an `<equality joint>` constraint, which the converter carries into USD as `NewtonMimicAPI` (`newton:mimicJoint`) alongside `MjcEqualityJointAPI` on `joint_left`.

Consuming runtimes must honor that coupling. Without it the two prismatic joints are free to drift apart whenever the arm accelerates, and the jaws no longer hold their commanded opening.

The finger drive gains follow from the same transmission rather than being tuned by hand: the pinion radius is 7.353 mm/rad, so the actuator's rotary stiffness and its 14 Nm torque limit appear at the finger as ~925 kN/m and 1904 N respectively. `mjc:gainPrm` is capped at the stiffest value that remains stable at the solver step, with the bias term set for a damping ratio of 1 against the 0.0752 kg finger.

## Warnings

The following warnings were emitted during conversion, due to unsupported features in the converter:

```
[Warning] [mujoco_usd_converter._impl.convert.warn] keys are not supported
```
