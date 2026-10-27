---
aliases: [Snow, Snowfall, Snow buildup, Accumulation]
tags:
  - roblox-dev
  - systems/weather
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Snow Accumulation

> **TL;DR:** Snow is precipitation with **slow, drifting particles** (low gravity, high drag, wind-affected, flipbook flakes) plus **accumulation**: a per-zone depth that grows with exposure and intensity and melts with temperature and sun. Render depth by blending in snow MaterialVariants, scaling up top-face "snow cap" meshes, or swapping terrain materials. Never simulate per-flake collisions.

## Particles (vs rain)
| Property | Snow | Rain |
| --- | --- | --- |
| Speed | 2–6 | 50+ |
| Acceleration | (0, −2…−6, 0) | (0, −600, 0) |
| Drag | 1–2 (wind dominates) | ~3 |
| Orientation | FacingCamera + `RotSpeed` | VelocityParallel + negative Squash |
| Texture | Flake flipbook (`FlipbookStartRandom`) | Streak |
| Lifetime | Long (6–12 s), so the emitter can sit lower | ~1 s |
The low fall speed means flakes travel far sideways in wind, so lean shelter rays much more than for rain ([[Rain_and_Precipitation]]).

## Accumulation model
```luau
-- depth in studs per zone; exposure from baked roof rays
local function stepSnow(z, snowIntensity: number, tempC: number, sun: number, dt: number)
	local add = snowIntensity * z.exposure * 0.002            -- studs/s at full intensity
	local melt = math.max(0, tempC) * 0.0004 + sun * 0.0003 * (1 - snowIntensity)
	z.depth = math.clamp(z.depth + (add - melt) * dt, 0, z.maxDepth)
end
```

## Rendering depth
- **Material blend:** below 0.05 studs, sprinkle (white-tinted MaterialVariant at low intensity). Above that, full snow material ([[Terrain_and_Materials]]).
- **Snow caps:** pre-made thin meshes on rooftops, fences and branches. Raise `Size.Y` or transparency with depth.
- **Terrain:** `Terrain:ReplaceMaterial(region, 4, Grass, Snow)` in chunks over several frames for big seasonal transitions ([[Time_Slicing_and_Frame_Budget]]).
- **Footprints/trails:** pooled decals stamped at feet, fading after some time ([[Object_Pooling]]). EditableImage masks if you need true deformation ([[EditableImage_and_EditableMesh]]).

## Gameplay hooks
Slower walk speed in deep snow (server-side, from zone depth), footprints that reveal players, reduced visibility (Atmosphere `Density`/`Haze` up: [[Atmosphere_Clouds_and_Sky]]).

## Related
[[Weather_System_Architecture]] · [[Rain_and_Precipitation]] · [[Wetness_Puddles_and_Drying]] · [[Particle_Emitters]] · [[Global_Wind]] · [[Terrain_and_Materials]] · [[EditableImage_and_EditableMesh]] · [[Time_Slicing_and_Frame_Budget]] · [[MOC_VFX_and_Weather]]

## Sources
- https://create.roblox.com/docs/effects/particle-emitters · https://create.roblox.com/docs/reference/engine/classes/Terrain#ReplaceMaterial
