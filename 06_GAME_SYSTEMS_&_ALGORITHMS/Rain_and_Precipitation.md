---
aliases: [Rain, Rain VFX, Roof detection, Rain occlusion, Rain overlay, Precipitation]
tags:
  - roblox-dev
  - systems/weather
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Rain & Precipitation

> **TL;DR:** Rain = **emitter cells** (transparent, non-colliding parts with downward ParticleEmitters) + **occlusion** (particles don't collide, so you must stop them at roofs) + **impact layers** (splashes, ripples, wet surfaces) + **screen and audio** feedback. Roblox's weather-island sample stops rain at roofs by **shortening each cell's particle `Lifetime`** using a raycast that **leans with the wind**.

## Emitter cell recipe (values from the official sample)
| Property | Value | Why |
| --- | --- | --- |
| Cell part | 30×1×30 studs, at Y = 150, `Transparency 1`, `CanCollide/CanQuery/CanTouch false`, `CastShadow false` | Invisible and free for physics and queries |
| `EmissionDirection` | Bottom | Falls down |
| `Orientation` + `Squash` | `VelocityParallel` + **−3** | Streaks aligned to motion (negative squash with VelocityParallel) |
| `Speed` / `Acceleration` / `Drag` | 50 / (0, −600, 0) / 3 | Drag lets wind push drops sideways. High gravity keeps them fast |
| `WindAffectsDrag` | true | Follows [[Global_Wind]] |
| `Rate` / `Lifetime` | 80 / 1 s | Tuned against device particle limits |
| `Color` / `Transparency` / `LightEmission` / `LightInfluence` | gray / 0.35 / 0.5 / 0.5 | Reads as water in any lighting |
| `Shape` | Disc, ShapeInOut Outward | Even coverage per cell |

## Roof shelter with wind lean (the clever bit)
A drop at terminal fall speed (`g / drag`) slides sideways at wind speed, so its landing point is offset by `wind × (drop × drag / g)`. Cast **one ray per cell along that leaned path**. If it hits a roof (not terrain, not a character), shorten that emitter's lifetime so drops end just above the surface:
```luau
local function leanOver(dropStuds: number): Vector3
	local wind = workspace.GlobalWind
	return Vector3.new(wind.X, 0, wind.Z) * (dropStuds * DRAG / GRAVITY)
end
-- fall time for a given drop with drag: no closed form, so binary-search the closed-form distance(t)
local function fallDistance(t: number): number
	local terminal = GRAVITY / DRAG
	return terminal * t + (SPEED - terminal) * (1 - math.exp(-DRAG * t)) / DRAG
end
```
Roofs rarely move, so re-check cells **round-robin over several seconds** (credit-based budget per frame) instead of every frame ([[Time_Slicing_and_Frame_Budget]], [[Raycasting]]).

## Layers that sell it
1. **Near-camera density:** a client-side emitter box following the camera adds close streaks without a world-sized grid.
2. **Screen-space overlay** (official `RainOverlay`): streak sprites in a full-screen GUI, leaned with wind, eased intensity. It's disabled under shelter, and when **Reduce Motion** is on the streaks hide and only the tint remains.
3. **Splashes:** ground emitters with `EmissionDirection = Top` and a custom splash texture, but only where you've placed them deliberately.
4. **Surfaces:** wet MaterialVariants, puddles, drips ([[Wetness_Puddles_and_Drying]]).
5. **Audio:** rain bed volume = intensity × outdoor factor (a roof ray from the camera), plus a muffled indoor variant ([[Audio_API]]).
6. **Lighting:** desaturate, add haze, darken clouds ([[Lighting_and_Post_Processing]], [[Atmosphere_Clouds_and_Sky]]).

## Performance
Particle limits are per device and much lower on mobile. If distant rain flickers, lower the emitter height, shorten lifetimes, reduce the rate, or shrink coverage ([[Mobile_and_Low_End_Optimization]], [[Particle_Emitters]]).

## Related
[[Weather_System_Architecture]] · [[Particle_Emitters]] · [[Global_Wind]] · [[Wetness_Puddles_and_Drying]] · [[Raycasting]] · [[Time_Slicing_and_Frame_Budget]] · [[Audio_API]] · [[Lighting_and_Post_Processing]] · [[Mobile_and_Low_End_Optimization]] · [[MOC_VFX_and_Weather]]

## Sources
- https://github.com/Roblox/resources/tree/main/experiences/weather-island (RainField.luau, RoofShelter.luau, RainBallistics.luau, RainOverlay)
- https://create.roblox.com/docs/effects/particle-emitters#simulate-rain
