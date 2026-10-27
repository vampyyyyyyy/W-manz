---
aliases: [Rendering performance, GPU optimization, Shadows cost, Overdraw, Texture memory]
tags:
  - roblox-dev
  - performance/rendering
type: concept
last_updated: 2026-10-27
status: complete
---
# Rendering Optimization

> **TL;DR:** Rendering cost = **draw calls + triangles + overdraw (transparency, particles, beams) + shadows + post effects + texture memory**. The biggest wins: stream the world, use SLIM for distant geometry, turn off `CastShadow` on small or decor parts, reduce overlapping transparent effects, cap particles, and keep unique textures few and appropriately sized. Always confirm with render stats on a mid- or low-end device.

## Checklist
| Area | Action |
| --- | --- |
| World size | [[StreamingEnabled]] with recommended radii. SLIM for static models ([[SLIM_and_Frustum_Streaming]]) |
| Shadows | `CastShadow = false` for small props, foliage clutter and interior decor. Fewer shadowed local lights ([[Light_Sources_and_Highlights]]) |
| Transparency | Avoid stacked transparent walls, glass and fog cards. Each layer is overdraw |
| Particles | Lower rates and lifetimes. Distance-based disabling. Flipbooks only where they matter ([[Particle_Emitters]]) |
| Beams/trails | Short lifetimes, low segment counts ([[Beams_and_Trails]]) |
| Meshes | Reasonable triangle counts. `RenderFidelity` Automatic. Reuse assets ([[Draw_Calls_and_Instancing]]) |
| Textures | 1024² max for most props, 512² or less for small ones. Shared atlases. Watch `GraphicsTexture` ([[Memory_Categories]]) |
| Post effects | Fewer, cheaper effects. Avoid always-on DepthOfField and Blur in gameplay ([[Lighting_and_Post_Processing]]) |
| UI | Heavy `CanvasGroup` use and many layered frames cost GPU and memory ([[UI_Performance]]) |
| Lighting intent | `LightingStyle` + `PrioritizeLightingQuality` let the engine scale gracefully ([[Rendering_Pipeline_and_Lighting_Technology]]) |

## Verify
Render scopes in [[MicroProfiler]], Shift+F5 stats, and the [[Scene_Analysis_Tool]] triangle view. Test at Graphics Quality 1–3 and on a phone ([[Mobile_and_Low_End_Optimization]]).

## Related
[[Draw_Calls_and_Instancing]] · [[SLIM_and_Frustum_Streaming]] · [[StreamingEnabled]] · [[Particle_Emitters]] · [[Light_Sources_and_Highlights]] · [[Rendering_Pipeline_and_Lighting_Technology]] · [[Memory_Categories]] · [[UI_Performance]] · [[Mobile_and_Low_End_Optimization]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://create.roblox.com/docs/performance-optimization/improve#rendering
