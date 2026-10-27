---
aliases: [PointLight, SpotLight, SurfaceLight, Highlight, Outline effect]
tags:
  - roblox-dev
  - engine/vfx
type: api
last_updated: 2026-10-27
status: complete
---
# Light Sources & Highlights

> **TL;DR:** `PointLight`, `SpotLight` and `SurfaceLight` add local light (`Brightness`, `Range`, `Color`, `Shadows`, plus `Angle`/`Face` for spot and surface). Short **light flashes** make impacts, muzzle fire and lightning feel real. `Highlight` draws outlines and fills on models: target indicators, x-ray for teammates, interactables. Up to **255** can be visible at once on the client.

## Lights
| Type | Shape | Notes |
| --- | --- | --- |
| `PointLight` | Sphere (`Range`) | Explosions, torches, hit flashes |
| `SpotLight` | Cone (`Angle` ≤ 180, `Face`) | Flashlights, headlights |
| `SurfaceLight` | From a part face (`Face`, `Angle`) | Screens, windows, neon panels |
Shared: `Color`, `Brightness`, `Range`, `Shadows` (costly), `Enabled`.

**Impact flash pattern:** create a PointLight at the hit, tween `Brightness` from ~4 to 0 over 0.12 s, then destroy. Do it client-side ([[Client_Side_VFX_Replication]], [[Hitstop_and_Impact_Feel]]).

## Highlight
Properties: `Adornee` (or parent to the model), `FillColor`, `FillTransparency`, `OutlineColor`, `OutlineTransparency`, `DepthMode` (`AlwaysOnTop` vs `Occluded`), `Enabled`.
Performance (official tips):
- Adding or removing Highlights triggers geometry rebuilds (spikes, draw calls). **Keep instances and toggle `Enabled`/transparency** instead.
- The **first** visible highlight costs the most (up to ~1 ms GPU on mobile). Extras are cheap.
- On mobile, cost grows with screen coverage. Invisible highlights (disabled or fully transparent) cost nothing.
- Avoid nesting highlighted objects inside other highlighted objects (draw-order issues).

## Related
[[Particle_Emitters]] · [[Beams_and_Trails]] · [[Lighting_and_Post_Processing]] · [[Rendering_Pipeline_and_Lighting_Technology]] · [[Lightning_Generation]] · [[Hitstop_and_Impact_Feel]] · [[Rendering_Optimization]] · [[Client_Side_VFX_Replication]] · [[MOC_VFX_and_Weather]]

## Sources
- https://create.roblox.com/docs/effects/light-sources · https://create.roblox.com/docs/effects/highlighting
