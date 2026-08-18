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

## License

The robot model and mesh assets are released under the [MIT License](LICENSE).
The pre-trained policies are released under the
[Apache License 2.0](rl_policies/LICENSE).

## Changelog

- 2026-08-14: Update the MJCF and structured USD to use high-resolution
  contacts, and update the ELU control policies.
- 2026-08-12: Add the structured USD model.
- 2026-08-03: Add the MJCF model, mesh assets, and ONNX control policies.
