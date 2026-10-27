---
aliases: [math, math.lerp, math.map, math.isfinite, math.noise, math.random, math.clamp]
tags:
  - roblox-dev
  - luau/libraries
type: api
last_updated: 2026-10-27
status: complete
---
# Math Library

> **TL;DR:** Beyond Lua's basics, Luau's `math` has `clamp`, `sign`, `round`, `noise` (Perlin), and since 2025 **`lerp`, `map`, `isnan`, `isinf`, `isfinite`**. Almost all `math` functions are fastcall builtins (except `noise` and `random`), and constant calls fold at compile time.

## Notable functions (37 total on Roblox)
| Function | Notes |
| --- | --- |
| `math.clamp(x, min, max)` | Errors if `min > max` |
| `math.lerp(a, b, t)` | `a + (b - a) * t`, `t` unbounded. Lowers to fused multiply-add in codegen |
| `math.map(x, inMin, inMax, outMin, outMax)` | Linear remap. Doesn't clamp |
| `math.isfinite/isnan/isinf(x)` | **Use `isfinite` on every client number** ([[NaN_and_Infinity_Exploits]]) |
| `math.round(x)` | Half away from zero (`-0.5 → -1`) |
| `math.sign(x)` | -1, 0, 1 |
| `math.noise(x, y?, z?)` | Perlin noise, *usually* in [-1, 1] (can exceed, so clamp). Integer inputs return 0 ([[Noise_Functions]]) |
| `math.random(m?, n?)` | PCG-based. For independent, seedable streams use the `Random` datatype |
| `math.pi`, `math.huge` | Constants (folded) |

## Recipes
```luau
-- Frame-rate independent smoothing (exponential decay), better than lerp(a, b, 0.1) per frame
local function damp(a: number, b: number, lambda: number, dt: number): number
	return math.lerp(a, b, 1 - math.exp(-lambda * dt))
end

-- Health bar fill from 0..1
local fill = math.clamp(math.map(hp, 0, maxHp, 0, 1), 0, 1)

-- Seeded procedural randomness (deterministic per seed)
local rng = Random.new(12345)
local x = rng:NextNumber(-10, 10)
```

## Gotchas
- `math.random` is a global stream shared by all scripts in that VM. For procedural generation, replays and loot rolls you want to reproduce, use `Random.new(seed)` ([[Procedural_Generation]]).
- `math.noise` at integer coordinates returns 0. Scale inputs by a non-integer frequency.
- `math.floor(-0.5) == -1`, while `//` floors too. Don't confuse floor with truncation.

## Related
[[Numbers_and_Floating_Point]] · [[Vector_Library]] · [[NaN_and_Infinity_Exploits]] · [[Noise_Functions]] · [[Procedural_Generation]] · [[Builtin_Fastcalls_and_Imports]] · [[UI_Animation_and_Springs]] · [[Camera_Shake]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://create.roblox.com/docs/reference/engine/libraries/math
- https://rfcs.luau.org/function-math-lerp.html · https://rfcs.luau.org/function-math-map.html · https://rfcs.luau.org/math-isnan-isfinite-isinf.html
