# Robocasa Kitchen Environment Assets

## Changelog

### [30/09/2025]
- Initial release.

## Overview

This package contains a kitchen environment inspired by [Robocasa](https://github.com/robocasa/robocasa).
Most elements in the scene are movable and can be interacted with, making the environment suitable for manipulation tasks.

<p float="left">
  <img src="kitchen_1.jpg" width="400">
</p>

The subfolders contain:
- **mjcf**: Robot description format files that reference files in
- **meshes**: Mesh and texture data for the MJCF description

## Source

### MJCF

The MJCF and mesh files were retrieved from the [mujoco_warp](https://github.com/google-deepmind/mujoco_warp) repository at `5a1b755`.
For convenience, the steps followed to create this asset are reproduced below:

1. Several kitchen environment xml files were generated using [Robocasa](https://github.com/robocasa/robocasa).
2. One file was selected as a reference, while others were used to swap furnitures.
3. The following manual edits were applied to the reference file:
  1. All duplicate textures and materials were merged.
  2. Textures were replaced by uniform colors closely matching the original appearance.
  3. Some furniture items were swapped for equivalent alternatives.
  4. Normals and UV coordinate information were removed from meshes.
  5. Some meshes were slightly modified to reduce their size (see subfolders in `meshes` for more details).
  6. Certain objects were removed to lighten the scene without reducing its overall complexity.
  7. A new (lighter) stool (not present in [Robocasa](https://github.com/robocasa/robocasa)) was added along with simple collision meshes.

## License

The xml file of the model is released under a [MIT License](LICENSE).
Licenses for individual objects composing the scene are provided in their respective subfolders within `meshes/`.
