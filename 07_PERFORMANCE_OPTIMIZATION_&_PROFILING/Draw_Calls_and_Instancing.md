---
aliases: [Draw calls, Instancing, GPU instancing, Batching, Mesh instancing]
tags:
  - roblox-dev
  - performance/rendering
type: concept
last_updated: 2026-10-27
status: complete
---
# Draw Calls & Instancing

> **TL;DR:** The renderer can **instance** identical geometry, meaning the same mesh with the same material and textures drawn many times in one batch. **Unique** meshes, textures, materials and transparency settings each break batches into more draw calls. Reuse assets (same MeshId and TextureID, not re-uploads), limit unique materials, and let [[SLIM_and_Frustum_Streaming|SLIM]] composite distant models.

## What breaks batching
| Cause | Fix |
| --- | --- |
| Same-looking mesh **uploaded multiple times** (different asset IDs) | Re-use one asset id. Official perf docs flag asset duplication |
| Many unique `SurfaceAppearance`/`MaterialVariant`/textures | Shared texture atlases and a small material palette ([[Terrain_and_Materials]]) |
| Per-instance color differences on textured meshes | Prefer vertex-color-like variations via `Color` on untextured materials, or accept separate batches deliberately |
| Transparency | Transparent objects sort and render separately, which costs overdraw ([[Rendering_Optimization]]) |
| Highlights added and removed often | Geometry rebuilds and extra draw calls. Toggle instead ([[Light_Sources_and_Highlights]]) |
| Huge part counts of unique `PartOperation`s (unions) | Convert to meshes, reuse |

## Measuring
- **Shift+F5** render stats / MicroProfiler render scopes ([[MicroProfiler]]).
- [[Scene_Analysis_Tool]] ▸ **Triangle composition** and **Instance composition** to find heavy or duplicated content.
- Test on low-end devices: draw calls hurt mobile CPUs most ([[Mobile_and_Low_End_Optimization]]).

## Related
[[Rendering_Optimization]] · [[SLIM_and_Frustum_Streaming]] · [[Scene_Analysis_Tool]] · [[Terrain_and_Materials]] · [[Light_Sources_and_Highlights]] · [[Mobile_and_Low_End_Optimization]] · [[MicroProfiler]] · [[Model_Streaming_Modes]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://create.roblox.com/docs/performance-optimization/improve#asset-memory-usage · https://create.roblox.com/docs/workspace/streaming/slim
