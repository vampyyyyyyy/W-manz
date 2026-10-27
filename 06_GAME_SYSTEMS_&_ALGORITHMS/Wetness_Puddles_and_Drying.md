---
aliases: [Wet surfaces, Puddles, Drying, Surface wetness, Wetness system]
tags:
  - roblox-dev
  - systems/weather
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Wetness, Puddles & Drying

> **TL;DR:** Model wetness as a **per-zone (or per-surface) value 0..1** that rises with rain intensity and exposure, then **dries over time** (faster in sun and wind, slower in shade). Render it on clients by swapping or blending **MaterialVariants** (darker albedo, lower roughness), adding reflective puddle decals or meshes in low spots, and drips under edges. Gameplay can read the same value (slippery surfaces, extinguishing fire).

## The model
```luau
--!strict
-- Server or client: wetness per zone, integrated each tick
type Zone = { wetness: number, exposure: number }   -- exposure 0 (indoors) .. 1 (open sky)
local WET_RATE, DRY_RATE = 0.08, 0.015               -- per second at full intensity / dry conditions

local function stepZone(z: Zone, rainIntensity: number, sun: number, wind: number, dt: number)
	local wetting = rainIntensity * z.exposure * WET_RATE
	local drying = DRY_RATE * (0.5 + sun) * (1 + wind / 50) * (1 - rainIntensity)
	z.wetness = math.clamp(z.wetness + (wetting - drying) * dt, 0, 1)
end
```
- **Exposure** comes from roof raycasts, the same idea as rain shelter ([[Rain_and_Precipitation]]). Bake it per zone once, because roofs rarely move.
- `sun` can come from `Lighting.ClockTime` and cloud cover. `wind` from `GlobalWind.Magnitude` ([[Day_Night_Cycle]], [[Global_Wind]]).
- Puddles **lag** surface wetness: they fill after wetness passes about 0.6 and drain last. That gives believable "after the storm" scenes.

## Rendering wet surfaces (client)
| Technique | How | Cost |
| --- | --- | --- |
| **MaterialVariant swap** | `Cobblestone` → `Cobblestone_Wet` (darker color map, lower roughness, stronger normals) per part or zone at thresholds | Cheap. Discrete steps, so fade them with a short darkening tween |
| **Color/Reflectance nudge** | Lerp `Color` darker and `Reflectance` up slightly with wetness | Very cheap, subtle |
| **Puddle decals/meshes** | Pre-placed in low areas. Tween transparency with puddle fill. Use a reflective, smooth material | Cheap, art-directed |
| **EditableImage masks** | Paint wetness or puddle masks at runtime | Flexible, memory-heavy ([[EditableImage_and_EditableMesh]]) |
| **Terrain** | `Terrain:SetMaterialColor` darkening during storms, plus water level tricks | Global, coarse ([[Terrain_and_Materials]]) |

## Details that sell it
- Drips: tiny emitters under roof edges, enabled while wetness > 0.3 and for a while after rain.
- Footsteps: switch to splash sounds and particles when the floor zone is wet (`Humanoid.FloorMaterial` + zone wetness).
- Characters: a subtle sheen and darkening on clothing while exposed. Dry them under cover.
- Steam: brief mist when sun returns over hot surfaces (art choice).

## Related
[[Rain_and_Precipitation]] · [[Weather_System_Architecture]] · [[Terrain_and_Materials]] · [[EditableImage_and_EditableMesh]] · [[Day_Night_Cycle]] · [[Global_Wind]] · [[Raycasting]] · [[Particle_Emitters]] · [[Snow_Accumulation]] · [[MOC_VFX_and_Weather]]

## Sources
- https://create.roblox.com/docs/parts/materials (MaterialVariants)
- Design pattern; see [[Showcase_Breakdown_Method]] for capturing community implementations
