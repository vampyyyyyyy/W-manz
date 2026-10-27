---
aliases: [Atmosphere, Clouds, Sky, Haze, Fog, Skybox]
tags:
  - roblox-dev
  - engine/environment
type: api
last_updated: 2026-10-27
status: complete
---
# Atmosphere, Clouds & Sky

> **TL;DR:** `Atmosphere` (in `Lighting`) scatters light for distance fog, haze, glare and horizon color. `Clouds` (in `Workspace.Terrain`) renders dynamic volumetric clouds that move with [[Global_Wind]]. `Sky` sets the skybox, sun and moon. All three replicate and are cheap to animate, so they're the backbone of weather transitions ([[Weather_System_Architecture]]).

## Atmosphere
| Property | Effect |
| --- | --- |
| `Density` | How much atmosphere blocks distant objects (fog amount) |
| `Offset` | Light transmission between camera and sky (horizon silhouette) |
| `Haze` | Hazy look at distance (storms, humidity) |
| `Color` | Haze tint (with `Haze` > 0) |
| `Glare` | Glow around the sun (needs `Haze` > 0) |
| `Decay` | Color away from the sun (sunset gradients) |

## Clouds (`Terrain.Clouds`)
`Cover` (0–1, how much sky is clouded), `Density` (0–1, thickness and darkness), `Color`. Clouds drift with `Workspace.GlobalWind`. Roblox's weather sample lerps clear→storm values for `Cover`, `Density` and `Color` while ramping wind ([[Rain_and_Precipitation]]).

## Sky
`Sky` in `Lighting`: six skybox faces (`SkyboxBk`…), `SunTextureId`/`MoonTextureId`, `SunAngularSize`, `CelestialBodiesShown`, `StarCount`. Swap or tween between sky instances for dramatic weather or day/night ([[Day_Night_Cycle]]).

## Transition recipe (server-driven, replicated)
```luau
-- intensity 0..1 from your weather state machine; write at ~15 Hz, not every frame
local function applySky(clouds: Clouds, air: Atmosphere, intensity: number)
	clouds.Cover = math.lerp(0.35, 0.95, intensity)
	clouds.Density = math.lerp(0.25, 0.85, intensity)
	clouds.Color = Color3.fromRGB(255, 255, 255):Lerp(Color3.fromRGB(120, 125, 135), intensity)
	air.Haze = math.lerp(0.5, 2.5, intensity)
	air.Density = math.lerp(0.3, 0.45, intensity)
end
```
Throttling replicated writes to a fixed rate (Roblox's sample uses 15 Hz) avoids flooding replication ([[Network_Bandwidth_Budget]]).

## Related
[[Global_Wind]] · [[Lighting_and_Post_Processing]] · [[Rendering_Pipeline_and_Lighting_Technology]] · [[Weather_System_Architecture]] · [[Rain_and_Precipitation]] · [[Day_Night_Cycle]] · [[Lightning_Generation]] · [[Terrain_and_Materials]] · [[MOC_VFX_and_Weather]]

## Sources
- https://create.roblox.com/docs/environment/atmosphere · https://create.roblox.com/docs/environment/clouds · https://create.roblox.com/docs/environment/skybox
- https://github.com/Roblox/resources/tree/main/experiences/weather-island (SkyState.luau)
