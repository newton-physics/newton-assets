# asOverDog Simulation Assets

## Overview

This package contains simulation and control assets for
[asOverDog](https://github.com/asOverDog/asoverdog_newton), a quadruped
platform with overconstrained closed-chain legs. Three interchangeable leg
mechanisms are provided:

- **Bennett**: spatial four-bar legs based on a Bennett linkage.
- **Planar**: planar four-bar legs.
- **Spherical**: spherical four-bar legs.

Each robot has the same 12-motor control interface and uses the same learned
actuator model. The robot-specific locomotion policies accept planar velocity
and yaw-rate commands.

## Contents

- `usd`: Self-contained USD models for the Bennett, Planar, and Spherical
  robots, including visual and collision geometry.
- `policies`: Robot-specific ONNX locomotion policies.
- `actuators`: Weights for the shared learned actuator model.

The policies take one `obs` tensor with shape `(1, 1525)` and produce one
`actions` tensor with shape `(1, 12)`. The observation contains 25 frames of
61 features. The policy networks use ONNX `Gemm` and `Elu` operators.

The actuator weights define a `12 -> 64 -> 64 -> 1` multilayer perceptron with
Softsign activations. It is evaluated independently for each motor from six
samples of joint position error and velocity history. The NumPy archive uses
the layer names `0`, `2`, and `4`, with `weight` and `bias` arrays matching
the corresponding linear layers.

## Sources

The USD models, locomotion policies, and actuator model originate from the
[asOverDog Newton project](https://github.com/asOverDog/asoverdog_newton).
The NumPy actuator weights are a format conversion of the project's
TorchScript actuator model; the learned parameters are unchanged.

## License

The assets are distributed under the [Apache License 2.0](LICENSE).

## Changelog

- 2026-08-31: Add the three self-contained USD robots, their ONNX locomotion
  policies, and the shared learned actuator weights.
