# OneRobotics A1 Robot Simulation Assets

## Overview

本目录包含用于 Newton 的 OneRobotics A1 双臂站架资产。当前版本不包含夹爪、
传感器、控制器或训练策略。

## Contents

- **meshes/a1_bimanual_stand**：双臂站架 USD 所引用的 STL 网格；
- **usd**：使用 Newton 官方 `urdf-usd-converter` 生成的结构化 OpenUSD；
- **LICENSE**：OneRobotics A1 资产的 CC BY 4.0 完整许可文本；
- **ASSET_LICENSE_STATUS.md**：受许可文件清单、署名和范围说明。

## Models

| 模型 | Newton USD |
|---|---|
| 双臂站架 | `usd/a1_bimanual_stand/onerobotics_a1_bimanual_stand.usda` |

USD 采用 Atomic Component 结构，入口 USDA 通过 `Payload/Contents.usda` 组合
Geometry、Materials 和 Physics 层。转换结果为自包含资产，不依赖包外 URDF 或 STL
文件。

## Loading in Newton

```python
import newton

builder = newton.ModelBuilder()
builder.add_usd("usd/a1_bimanual_stand/onerobotics_a1_bimanual_stand.usda")
model = builder.finalize()
```

## Sources
- Original repository: https://github.com/katazen/onerobot_h1
- Source revision: `ecf530911284ba0e559f7a24dc222fd8e60d31ed`
- Packaged mesh files: `meshes/a1_bimanual_stand/`

本发布包的规范化源文件全部位于当前 `onerobotics_a1` 目录内：

- 双臂站架源模型：`meshes/a1_bimanual_stand/`。


## Validation

| 模型 | Links | Joints | Mesh references | USD prims | USD layers |
|---|---:|---:|---:|---:|---:|
| 双臂站架 | 17 | 16 | 34 | 93 | 7 |

USD Stage 可打开，默认 Prim 为 `/onerobotics_a1_bimanual_stand`，所有组成层均位于
该 USD 目录内。

## License

OneRobotics A1 robot assets © 2026 OneRobotics，采用 Creative Commons
Attribution 4.0 International（CC BY 4.0）。完整条款见 [`LICENSE`](LICENSE)，
详细覆盖范围及署名要求见 [`ASSET_LICENSE_STATUS.md`](ASSET_LICENSE_STATUS.md)。

修改后的再分发必须保留版权与许可信息、注明 OneRobotics 为创作者，并说明所做
修改。许可不授予 OneRobotics 商标权，也不得暗示官方背书。

## Changelog

- 2026-10-12：增加 Newton 资产包；加入双臂站架 STL 和结构化 USD。
