---
aliases: [Perlin noise, math.noise, fBm, Fractal noise, Octaves, Domain warping]
tags:
  - roblox-dev
  - systems/procedural
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Noise Functions (Perlin, fBm, warping)

> **TL;DR:** `math.noise(x, y?, z?)` returns smooth Perlin noise, usually in [-1, 1]. It **can exceed** that, so clamp. It's **0 at integer coordinates**, so scale inputs by non-integer frequencies. Stack octaves (**fBm**) for natural detail, **ridged** noise for mountains, and **domain warping** for organic shapes. Seed it by offsetting coordinates.

## Recipes
```luau
--!strict
--!native
local Noise = {}

-- seed by offsetting into a different region of noise space
function Noise.seeded(seed: number): (number, number) -> number
	local ox, oz = (seed % 1000) * 13.37, (seed // 1000) * 7.77
	return function(x, z) return math.noise(x + ox, z + oz) end
end

-- fractal Brownian motion: sum octaves of increasing frequency, decreasing amplitude
function Noise.fbm(x: number, z: number, octaves: number, lacunarity: number?, gain: number?): number
	local l, g = lacunarity or 2.0, gain or 0.5
	local sum, amp, freq, norm = 0, 1, 1, 0
	for _ = 1, octaves do
		sum += amp * math.noise(x * freq, z * freq)
		norm += amp
		amp *= g
		freq *= l
	end
	return math.clamp(sum / norm, -1, 1)
end

-- ridged: sharp crests (mountain ranges)
function Noise.ridged(x: number, z: number, octaves: number): number
	local n = 1 - math.abs(Noise.fbm(x, z, octaves))
	return n * n
end

-- domain warp: feed noise into the coordinates of noise (swirly, organic)
function Noise.warped(x: number, z: number): number
	local wx = Noise.fbm(x + 5.2, z + 1.3, 3) * 4
	local wz = Noise.fbm(x + 9.7, z + 2.8, 3) * 4
	return Noise.fbm(x + wx, z + wz, 5)
end
return Noise
```

## Uses beyond terrain
Camera shake (1D noise over time: [[Camera_Shake]]), wind gust variation ([[Global_Wind]]), cloud cover fluctuation, flicker of fire lights, wobble in VFX, NPC wander targets.

## Performance
`math.noise` is a builtin but not a fastcall (per Luau docs). Thousands of samples per frame belong in `--!native` code with cached results per chunk ([[Native_Code_Generation]], [[Procedural_Generation]]).

## Related
[[Procedural_Generation]] · [[Math_Library]] · [[Camera_Shake]] · [[Terrain_and_Materials]] · [[Native_Code_Generation]] · [[Global_Wind]] · [[Weather_System_Architecture]] · [[Builtin_Fastcalls_and_Imports]] · [[MOC_Game_Systems_and_Algorithms]]

## Sources
- https://create.roblox.com/docs/reference/engine/libraries/math#noise · https://luau.org/performance (fastcall list excludes noise)
