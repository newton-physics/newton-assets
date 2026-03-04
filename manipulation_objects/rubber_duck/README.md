# Rubber Duck

## Overview

A cute rubber duck mesh for use as a deformable manipulation object in Newton.

### Files

- **`mesh.usd`** — Raw geometry (Y-up). Contains both meshes in a shared coordinate space:

  | Prim | Type | Vertices | Faces/Tets |
  |------|------|----------|------------|
  | `/Model` | Surface mesh | 1002 | 2000 faces |
  | `/TetModel` | Tetrahedral mesh | 2734 | 11615 tets |

- **`model.usda`** — Scene-ready asset (Z-up). References `mesh.usd` under a shared Xform with a Y→Z up-axis rotation:

  | Prim path | References |
  |-----------|------------|
  | `/root/Model/SurfaceMesh` | `mesh.usd</Model>` |
  | `/root/Model/TetMesh` | `mesh.usd</TetModel>` |

- **Units**: meters (`metersPerUnit = 1`)

The surface mesh was decimated from the original (7923 vertices) to ~1000 vertices
using quadric decimation. The tetrahedral mesh was generated from the surface using
[fTetWild](https://github.com/wildmeshing/fTetWild) via
[pytetwild](https://github.com/pyvista/pytetwild) (`edge_length_fac=0.05`).

## Source

Created by The Newton Developers.

## License

[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)

See [LICENSE](LICENSE) for the full legal text.
