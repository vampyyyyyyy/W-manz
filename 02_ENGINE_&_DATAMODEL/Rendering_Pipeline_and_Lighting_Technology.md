---
aliases: [LightingStyle, Lighting.Technology, Future lighting, ShadowMap, PrioritizeLightingQuality, Rendering pipeline]
tags:
  - roblox-dev
  - engine/rendering
type: concept
last_updated: 2026-10-27
status: complete
---
# Rendering Pipeline & Lighting Technology

> **TL;DR:** `Lighting.Technology` (Voxel/ShadowMap/Future) is now **deprecated**. Lighting intent is set with **`Lighting.LightingStyle`** (`Realistic` or `Soft`) plus **`Lighting.PrioritizeLightingQuality`** (whether quality or view distance degrades first on weaker devices). The renderer scales quality per device automatically. Your job is controlling **draw calls, transparency, shadows, texture memory and light counts** ([[Rendering_Optimization]]).

## Lighting intent (2025+ model)
| Property | Meaning |
| --- | --- |
| `LightingStyle = Realistic` | The most advanced lighting and shadows Roblox can deliver (`ShadowSoftness` applies) |
| `LightingStyle = Soft` | Stylized, flatter "classic Roblox" look with softer lights and shadows |
| `PrioritizeLightingQuality = true` | When quality drops, keep advanced shadows and shaders up close and give up view distance. `false` keeps view distance and gives up lighting first. *Soft + this enabled uses shadow maps rather than voxel lighting* |
| `GlobalShadows` | Shadows on or off (indoor/outdoor ambient distinction) |

## What the renderer does per frame (high level)
Cull (frustum, distance, streaming) → batch and instance geometry (same mesh + material = instanced) → shadow passes → opaque → transparent (sorted, expensive) → particles, beams, trails → post-processing (Bloom, DoF, SunRays, ColorCorrection, ColorGrading) → UI. Each unique material, texture and mesh combo can become another draw call ([[Draw_Calls_and_Instancing]]).

## Art-direction levers
- **Materials:** built-in materials, `MaterialVariant`s (custom PBR per material), `SurfaceAppearance` on MeshParts (PBR maps) ([[Terrain_and_Materials]]).
- **Global look:** `Lighting` color, ambient and exposure, `Atmosphere` + `Sky` + `Clouds` ([[Atmosphere_Clouds_and_Sky]]), post effects ([[Lighting_and_Post_Processing]]).
- **Local light:** PointLight, SpotLight, SurfaceLight. Shadows from local lights are costly on low-end hardware ([[Light_Sources_and_Highlights]]).

## Gotchas
- Old tutorials say "set Technology to Future". In 2026, use `LightingStyle = Realistic` and leave `PrioritizeLightingQuality` on for small, detailed scenes.
- Lots of **overlapping transparent** surfaces (glass, fog sheets, particle walls) cause overdraw. They're a classic mobile FPS killer ([[Mobile_and_Low_End_Optimization]]).
- `CastShadow = false` on small or decor parts saves shadow-pass cost.

## Related
[[Lighting_and_Post_Processing]] · [[Atmosphere_Clouds_and_Sky]] · [[Light_Sources_and_Highlights]] · [[Terrain_and_Materials]] · [[Draw_Calls_and_Instancing]] · [[Rendering_Optimization]] · [[Mobile_and_Low_End_Optimization]] · [[Day_Night_Cycle]] · [[MOC_VFX_and_Weather]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/environment/lighting
- https://create.roblox.com/docs/reference/engine/classes/Lighting#LightingStyle (Technology tagged Deprecated)
