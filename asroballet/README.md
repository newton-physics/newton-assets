# asRoBallet Simulation Assets

## Overview

This package contains the MJCF model, mesh geometry, and pre-trained control
policies for [asRoBallet](https://github.com/asRoBallet/asRoBallet_mujoco), an
underactuated humanoid ballbot with a three-wheel omni-drive mechanism.

The subfolders contain:

- **meshes**: Visual and collision STL geometry referenced by the MJCF model.
- **mjcf**: The robot model, an independent floating-ball variant, and their
  simulation scenes with ground contact.
- **rl_policies**: Pre-trained velocity-tracking and station-keeping ONNX
  policies.
- **usd_structured**: Structured USD layers converted from the MJCF model.

## Sources

The robot model and meshes originate from the MIT-licensed
[asRoBallet MuJoCo repository](https://github.com/asRoBallet/asRoBallet_mujoco).
`mjcf/asRoBallet.xml` mirrors the canonical `robots/mjcf/asRoBallet.xml` model
with its mesh directory adjusted to this repository layout. `mjcf/scene.xml`
is the corresponding MuJoCo scene with the ball-to-floor contact definition.
`mjcf/asRoBallet_floating_ball.xml` promotes the ball to an independent free
body, and `mjcf/scene_floating_ball.xml` loads that variant with the same scene
configuration.

The structured USD model was created with the
[mujoco-usd-converter](https://github.com/newton-physics/mujoco-usd-converter).
For conversion details and the main asset entrypoint, see the
[usd_structured README](usd_structured/README.md).

For the model design and system details, see the
[asRoBallet paper](https://arxiv.org/abs/2604.24916).

## MJCF Topologies

Two MJCF topologies are provided:

- **Ball joint**: `mjcf/asRoBallet.xml` connects `ball_link` below `base_link`
  through `torso_ball_joint`. The spherical joint fixes the relative
  translation at the joint anchor while allowing three rotational degrees of
  freedom. `mjcf/scene.xml` loads this model. The structured USD asset also
  represents this topology.
- **Free joint**: `mjcf/asRoBallet_floating_ball.xml` makes `ball_link` an
  independent top-level body with `ball_free_joint`, so the robot base and ball
  have separate translational and rotational state. Contact couples the two
  bodies. `mjcf/scene_floating_ball.xml` loads this model.

The free-joint model and scene are generated from their ball-joint counterparts
to keep shared model data in one canonical source. After editing the canonical
files, regenerate and verify the variants with:

```bash
python asroballet/mjcf/generate_variants.py
python asroballet/mjcf/generate_variants.py --check
```

## License

The robot model and mesh assets are released under the [MIT License](LICENSE).
The pre-trained policies are released under the
[Apache License 2.0](rl_policies/LICENSE).

## Changelog

- 2026-08-19: Generate the free-joint MJCF variant from the canonical model and
  synchronize wheel axle visual-group metadata in the structured USD.
- 2026-08-14: Update the MJCF and structured USD to use high-resolution
  contacts, and update the ELU control policies.
- 2026-08-12: Add the structured USD model.
- 2026-08-03: Add the MJCF model, mesh assets, and ONNX control policies.
