---
aliases: [Floating point, Doubles, Float precision, 2^53, Floating point origin]
tags:
  - roblox-dev
  - luau/numbers
type: concept
last_updated: 2026-10-27
status: complete
---
# Numbers & Floating Point

> **TL;DR:** Luau has **one** number type: a 64-bit IEEE-754 double. It's exact for integers up to 2^53 (~9×10^15). But Roblox **positions, `Vector3` and `CFrame` components are 32-bit floats** (~7 significant digits), so precision degrades far from the world origin. Never compare floats with `==` after arithmetic, and validate NaN and inf from clients.

## Facts to remember
| Thing | Precision | Consequence |
| --- | --- | --- |
| Luau `number` | double, 53-bit mantissa | Currency up to ~9e15 is exact. Beyond that, integers round |
| `Vector3`, `CFrame`, part positions | **float32** | At 10,000 studs from origin, steps are about 0.001 studs. At 100,000, about 0.008. Physics and animation jitter get visible far out |
| native `vector` | float32 × 3 | Same as `Vector3` ([[Vector_Library]]) |
| `buffer.writef32` | float32 | Lossy for doubles ([[Buffer_Library]]) |
| `0.1 + 0.2 == 0.3` | `false` | Use an epsilon: `math.abs(a - b) < 1e-6` |

## Practical rules
- **Big worlds:** keep gameplay near the origin, or shift the world ("floating origin" techniques), because characters 50k+ studs out get jitter. Roblox's own docs and the community recommend staying within reasonable bounds.
- **Big currency:** for idle and simulator games beyond 2^53, store mantissa + exponent (e.g. `{m = 1.23, e = 45}`) or use a big-number library. Don't let numbers silently lose integer precision.
- **Integer checks:** `x % 1 == 0` or `math.floor(x) == x` (validate finiteness first: [[NaN_and_Infinity_Exploits]]).
- **Rounding:** `math.round` (half away from zero), `math.floor`/`ceil`, `//` for floor division ([[Math_Library]]).
- **Formatting:** `string.format("%.2f", x)` for UI. `tostring` prints the shortest round-trip representation.

## NaN and inf
`0/0` is NaN, and `1/0` is `math.huge`. NaN fails every comparison and poisons arithmetic, so reject it at trust boundaries with `math.isfinite` ([[NaN_and_Infinity_Exploits]]). DataStores shouldn't store inf or NaN ([[DataStoreService]]).

## Related
[[Math_Library]] · [[NaN_and_Infinity_Exploits]] · [[Vector_Library]] · [[Buffer_Library]] · [[Quantization]] · [[CFrame_Math]] · [[Bitwise_Operations_bit32]] · [[DataStoreService]] · [[Luau_Syntax_Extensions]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://luau.org/syntax#number-literals · https://create.roblox.com/docs/luau/numbers
