# The Robot Studio SO-101 Simulation Assets

## Overview

This package contains robot assets for the [SO-101](https://huggingface.co/docs/lerobot/so101), a 6-DoF low-cost manipulator by [The Robot Studio](https://github.com/TheRobotStudio/SO-ARM100) used by the [LeRobot](https://github.com/huggingface/lerobot) project.

The subfolders contain:

- **usd_structured**: Structured USD layer files, converted from the MuJoCo Menagerie MJCF.

## Sources

### USD (Structured)

The structured USD model was created with the [mujoco-usd-converter](https://github.com/newton-physics/mujoco-usd-converter), converted from the MuJoCo Menagerie [`robotstudio_so101`](https://github.com/google-deepmind/mujoco_menagerie/tree/main/robotstudio_so101) MJCF source. For details, see the [usd_structured README](usd_structured/README.md).

## License

This model is released under an [Apache-2.0 License](LICENSE).
