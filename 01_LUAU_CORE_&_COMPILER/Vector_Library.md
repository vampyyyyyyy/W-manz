---
aliases: [vector, vector library, native vector, vector.create]
tags:
  - roblox-dev
  - luau/libraries
type: api
last_updated: 2026-10-27
status: complete
---
# Vector Library (native `vector`)

> **TL;DR:** Luau has a native 3-component float32 **value type**, the same one that backs Roblox's `Vector3`. Since 2025 there's a built-in `vector` library (`vector.create`, `dot`, `cross`, `normalize`, `lerp`…) with **fastcalls, constant folding and native-code lowering** (e.g. `vector.dot` → a CPU dot-product instruction). Vectors live inside the value slot: **no heap allocation, no GC pressure**.

## API (Roblox, 14 functions + constants)
`vector.create(x, y, z?)` (`z` defaults to 0) · `magnitude` · `normalize` · `cross` · `dot` · `angle(a, b, axis?)` · `floor` · `ceil` · `abs` · `sign` · `clamp(v, min, max)` · `lerp(a, b, t)` · `max(...)` · `min(...)` · constants `vector.zero`, `vector.one`.

Operators work natively: `+ - * / //` (component-wise, or with a scalar), unary `-`, `==`. Components: `v.x`/`v.X` etc. Vectors are **immutable**, so `v.x = 1` is an error.

## Example: hot math without allocations
```luau
--!strict
--!native
local function steer(pos: vector, vel: vector, target: vector, maxSpeed: number, dt: number): (vector, vector)
	local desired = vector.normalize(target - pos) * maxSpeed
	local newVel = vector.lerp(vel, desired, math.min(1, dt * 4))
	return pos + newVel * dt, newVel
end
```
Annotating `vector`/`Vector3` parameters lets [[Native_Code_Generation]] emit vector-specialized code instead of generic table checks.

## Gotchas
- `vector.normalize(vector.zero)` returns **NaN components**. Guard zero-length vectors, especially with player-supplied directions ([[NaN_and_Infinity_Exploits]]).
- `vector.clamp` errors if any `min` component is greater than `max`.
- Precision is **float32**. See [[Numbers_and_Floating_Point]].
- `Vector3` methods (`:Dot`, `:Cross`, `.Unit`, `:Lerp`, `:FuzzyEq`) still work. The `vector.*` functions are the fastcall-optimized path for hot loops ([[Builtin_Fastcalls_and_Imports]]).

## Related
[[Math_Library]] · [[CFrame_Math]] · [[Native_Code_Generation]] · [[Builtin_Fastcalls_and_Imports]] · [[Numbers_and_Floating_Point]] · [[Steering_and_Flocking]] · [[Luau_Micro_Optimizations]] · [[Typeof_vs_type]] · [[Quantization]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://create.roblox.com/docs/reference/engine/libraries/vector
- https://rfcs.luau.org/vector-library.html · https://rfcs.luau.org/function-vector-lerp.html
- https://luau.org/news/2025-12-19-luau-recap-runtime-2025
