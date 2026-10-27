---
aliases: [Lightning, Lightning bolt, Midpoint displacement, Thunder, Storm VFX]
tags:
  - roblox-dev
  - systems/weather
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Lightning Generation

> **TL;DR:** A convincing strike is **geometry + light + sound + timing**. Generate a jagged path with **recursive midpoint displacement** (plus random branches), draw it with Beams or thin neon parts for 50–150 ms with a flicker, flash the scene (PointLight + exposure/ColorCorrection pulse), then play **thunder delayed by distance / speed of sound**. The server decides *where and when* (it may damage). Clients render.

## Path generation
```luau
--!strict
local function bolt(a: Vector3, b: Vector3, depth: number, displacement: number, rng: Random, out: { Vector3 })
	if depth == 0 then
		table.insert(out, b)
		return
	end
	local mid = (a + b) / 2
	local dir = (b - a).Unit
	local perp = dir:Cross(Vector3.yAxis)
	if perp.Magnitude < 1e-3 then perp = dir:Cross(Vector3.xAxis) end
	perp = perp.Unit
	local perp2 = dir:Cross(perp)
	mid += (perp * rng:NextNumber(-1, 1) + perp2 * rng:NextNumber(-1, 1)) * displacement
	bolt(a, mid, depth - 1, displacement / 2, rng, out)
	bolt(mid, b, depth - 1, displacement / 2, rng, out)
end

local function makeBoltPoints(top: Vector3, ground: Vector3, seed: number): { Vector3 }
	local pts = { top }
	bolt(top, ground, 6, (top - ground).Magnitude * 0.15, Random.new(seed), pts) -- 64 segments
	return pts
end
```
- Send only `seed + endpoints` from the server, and every client builds the **same** bolt deterministically ([[Client_Side_VFX_Replication]], [[Procedural_Generation]]).
- Branches: at a few random segments, recurse a shorter bolt from that point at an angle with lower depth.

## Rendering
- **Beams** between attachments at each point: neon white-blue, `LightEmission = 1`, width tapering toward branches ([[Beams_and_Trails]]). Thin neon parts work too, but pool them ([[Object_Pooling]]).
- **Flicker:** visible 60 ms → hidden 40 ms → visible 50 ms → fade.
- **Flash:** a big PointLight at the strike (Brightness 5–10, Range 60) plus a short `ColorCorrection.Brightness` and `Lighting.ExposureCompensation` pulse ([[Lighting_and_Post_Processing]], [[Light_Sources_and_Highlights]]).
- **Sky-only lightning:** flash clouds (`Clouds.Color` brighten) with no bolt for distant strikes ([[Atmosphere_Clouds_and_Sky]]).

## Thunder timing
`delay = distance_studs × (1 stud ≈ 0.28 m) / 343 m/s`. Close strikes get a sharp crack immediately. Far ones get a delayed low rumble with low-pass filtering ([[Audio_API]]).

## Gameplay (server)
Choose a strike point (random within the storm, or attracted to the highest part or a player holding metal), warn with a ground decal for 1 s, then damage within a radius via [[Spatial_Queries_Overlap]] and the [[Damage_Pipeline]].

## Related
[[Weather_System_Architecture]] · [[Beams_and_Trails]] · [[Light_Sources_and_Highlights]] · [[Lighting_and_Post_Processing]] · [[Atmosphere_Clouds_and_Sky]] · [[Audio_API]] · [[Client_Side_VFX_Replication]] · [[Procedural_Generation]] · [[Camera_Shake]] · [[MOC_VFX_and_Weather]]

## Sources
- Midpoint displacement is a standard procedural technique; Roblox APIs per https://create.roblox.com/docs/effects/beams
