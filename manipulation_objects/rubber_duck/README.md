# Rubber Duck

## Overview

A cute rubber duck mesh for use as a deformable manipulation object in Newton.

| Prim | Type | Vertices | Faces/Tets |
|------|------|----------|------------|
| `/Model` | Surface mesh | 1002 | 2000 faces |
| `/TetModel` | Tetrahedral mesh | 2734 | 11615 tets |

- **Units**: meters (`metersPerUnit = 1`)
- **Up axis**: Y (mesh.usd), Z (model.usda)

The surface mesh was decimated from the original (7923 vertices) to ~1000 vertices
using quadric decimation. The tetrahedral mesh was generated from the surface using
[fTetWild](https://github.com/wildmeshing/fTetWild) via
[pytetwild](https://github.com/pyvista/pytetwild) (`edge_length_fac=0.05`).

## Source

Created by The Newton Developers.

## License

[Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0)

See [LICENSE](LICENSE) for the full legal text.
