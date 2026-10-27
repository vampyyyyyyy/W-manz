---
aliases: [Terrain, Materials, MaterialVariant, SurfaceAppearance, MaterialService, Voxel terrain]
tags:
  - roblox-dev
  - engine/environment
type: concept
last_updated: 2026-10-27
status: complete
---
# Terrain & Materials

> **TL;DR:** Roblox terrain is a **voxel** grid (4-stud voxels) with per-voxel material and occupancy. You can edit it in Studio or at runtime (`FillBlock`, `FillBall`, `ReadVoxels`/`WriteVoxels`). Surfaces look the way they do because of **materials**: built-in ones, custom **`MaterialVariant`**s (PBR textures via `MaterialService`), and per-mesh **`SurfaceAppearance`**. Weather and footstep systems read `RaycastResult.Material` and `Humanoid.FloorMaterial` to react to surfaces.

## Terrain essentials
| API | Use |
| --- | --- |
| `Terrain:FillBlock(cframe, size, material)`, `FillBall`, `FillCylinder`, `FillWedge` | Procedural shapes ([[Procedural_Generation]]) |
| `Terrain:ReadVoxels(region, resolution)` / `WriteVoxels(...)` | Bulk read and write of materials + occupancy (resolution 4) |
| `Terrain:ReplaceMaterial(region, res, from, to)` | Seasonal swaps: grass → snow ([[Snow_Accumulation]]) |
| `Terrain.WaterWaveSize`, `WaterWaveSpeed`, `WaterColor`, `WaterReflectance`, `WaterTransparency` | Water look. Storms can raise wave size |
| `Terrain.Decoration` (grass) | Animated grass that sways with [[Global_Wind]] |
| `Terrain:SetMaterialColor(material, color)` | Tint materials globally (dry vs lush grass) |

## Material system
- **Built-in materials** (`Enum.Material`) for parts and terrain.
- **`MaterialVariant`** in `MaterialService`: custom color, normal, metalness and roughness maps tied to a base material. Swap variants per part (`part.MaterialVariant = "WetCobblestone"`) or set overrides globally. This is how you do **wet surfaces** convincingly ([[Wetness_Puddles_and_Drying]]).
- **`SurfaceAppearance`** on MeshParts: PBR maps (`ColorMap`, `NormalMap`, `MetalnessMap`, `RoughnessMap`) plus alpha modes. Note: most of its properties aren't script-writable at runtime. Swap instances instead.
- `Reflectance`, `Transparency` and `Color` are scriptable and cheap ways to show change.

## Performance notes
- Terrain is efficient for large natural areas compared with thousands of parts.
- `WriteVoxels` on big regions at runtime is expensive and replicates. Chunk it over frames ([[Time_Slicing_and_Frame_Budget]]).
- Each unique MaterialVariant or SurfaceAppearance is texture memory, so reuse them ([[Rendering_Optimization]]).

## Related
[[Rendering_Pipeline_and_Lighting_Technology]] · [[Wetness_Puddles_and_Drying]] · [[Snow_Accumulation]] · [[Procedural_Generation]] · [[Global_Wind]] · [[Raycasting]] · [[Rendering_Optimization]] · [[Atmosphere_Clouds_and_Sky]] · [[MOC_VFX_and_Weather]]

## Sources
- https://create.roblox.com/docs/parts/terrain · https://create.roblox.com/docs/parts/materials
- https://create.roblox.com/docs/reference/engine/classes/Terrain
