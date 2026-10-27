---
aliases: [CFrame, Coordinate frame, ToObjectSpace, lookAt, CFrame lerp]
tags:
  - roblox-dev
  - engine/math
type: concept
last_updated: 2026-10-27
status: complete
---
# CFrame Math

> **TL;DR:** A `CFrame` is a position + rotation (a 3×4 matrix). Multiply to **compose** transforms (`parent * offset`), use `:Inverse()`/`ToObjectSpace` to get **relative** transforms, `CFrame.lookAt(from, to)` to aim, and `:Lerp` for interpolation. Remember that `a * b ≠ b * a`. Most "my part spins weird" bugs come from multiplication order.

## Essentials
```luau
local cf = CFrame.new(0, 5, 0) * CFrame.Angles(0, math.rad(90), 0)   -- move, then rotate about local axes
local aim = CFrame.lookAt(gun.Position, target.Position)              -- face target (optional up vector)
local offset = root.CFrame:ToObjectSpace(part.CFrame)                 -- part relative to root
local world = root.CFrame:ToWorldSpace(offset)                        -- back to world (== root.CFrame * offset)
local localPoint = root.CFrame:PointToObjectSpace(worldPoint)         -- is the target in front? (Z < 0 is forward)
local mid = a:Lerp(b, 0.5)                                            -- interpolate position + rotation
local rx, ry, rz = cf:ToOrientation()                                 -- YXZ Euler (radians)
```

## Mental model
- `A * B` = "apply B **in A's local space**". `CFrame.new(pos) * CFrame.Angles(...)` rotates in place at `pos`. `CFrame.Angles(...) * CFrame.new(pos)` orbits around the origin.
- `cf.LookVector` (-Z), `cf.RightVector` (+X), `cf.UpVector` (+Y) are unit direction vectors.
- `CFrame.identity` is the identity. `CFrame.fromMatrix(pos, right, up, back?)` builds one from axes.
- Components are **float32**, so precision drops far from the origin ([[Numbers_and_Floating_Point]]).

## Game recipes
| Need | Expression |
| --- | --- |
| Point in front of a character | `root.CFrame * CFrame.new(0, 0, -5)` |
| Is the target within a 60° cone? | `root.CFrame.LookVector:Dot((t - root.Position).Unit) > math.cos(math.rad(30))` ([[Hit_Validation]]) |
| Yaw-only facing | `CFrame.lookAt(pos, Vector3.new(t.X, pos.Y, t.Z))` |
| Smoothly turn toward a target | `cf:Lerp(targetCF, 1 - math.exp(-k * dt))` ([[Math_Library]]) |
| Camera shake offset | `camera.CFrame *= CFrame.Angles(pitchNoise, yawNoise, 0)` ([[Camera_Shake]]) |
| Weapon at a hand attachment | `hand.CFrame * gripOffset` |

## Performance
CFrame math is native C++ userdata, so it's fast, but each operation allocates a new CFrame. In massive per-frame loops (thousands of entities), keep math in `vector`s and build CFrames once at the end ([[Vector_Library]], [[Luau_Micro_Optimizations]]).

## Related
[[Vector_Library]] · [[Math_Library]] · [[Numbers_and_Floating_Point]] · [[Quantization]] · [[Camera_System]] · [[Camera_Shake]] · [[Hit_Validation]] · [[TweenService]] · [[Lag_Compensation]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/workspace/cframes · https://create.roblox.com/docs/reference/engine/datatypes/CFrame
