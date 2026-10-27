---
aliases: [Screen shake, Camera shake, Trauma shake, Camera punch]
tags:
  - roblox-dev
  - systems/game-feel
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Camera Shake

> **TL;DR:** Use **trauma-based, noise-driven, additive** shake. Events add "trauma" (0..1), shake intensity is `trauma²`, trauma decays every frame, and offsets come from smooth noise (`math.noise`), not `math.random` (which looks like jitter). Apply it as the **last multiplication** on the camera CFrame in PreRender, and scale it down for **Reduce Motion** users.

## Implementation
```luau
--!strict
local CameraShake = {}
local trauma = 0
local seed = math.random() * 1000
const MAX_ANGLE = math.rad(4)
const MAX_OFFSET = 0.6
const DECAY = 1.6                  -- trauma per second

function CameraShake.add(amount: number)
	trauma = math.min(1, trauma + amount)
end

local t = 0
function CameraShake.offset(dt: number): CFrame
	t += dt
	trauma = math.max(0, trauma - DECAY * dt)
	if trauma <= 0 then return CFrame.identity end
	local s = trauma * trauma                                   -- perceptual curve
	local f = 18                                                -- noise frequency
	local pitch = MAX_ANGLE * s * math.noise(seed, t * f)
	local yaw   = MAX_ANGLE * s * math.noise(seed + 10, t * f)
	local roll  = MAX_ANGLE * 0.5 * s * math.noise(seed + 20, t * f)
	local ox = MAX_OFFSET * s * math.noise(seed + 30, t * f)
	local oy = MAX_OFFSET * s * math.noise(seed + 40, t * f)
	return CFrame.new(ox, oy, 0) * CFrame.Angles(pitch, yaw, roll)
end
return CameraShake
```
Use it in the camera update: `cam.CFrame = baseCF * CameraShake.offset(dt)` ([[Camera_System]]).

## Directional "punch"
For hits, add a short **directional kick** opposite the hit direction (spring back with `TweenService:SmoothDamp`) in addition to the trauma shake. It reads as impact rather than an earthquake ([[TweenService]]).

## Tuning table
| Event | Trauma |
| --- | --- |
| Light hit landed | 0.12 |
| Heavy hit / parry | 0.3 |
| Explosion nearby | 0.4–0.7 by distance falloff |
| Landing from ODM swing / big fall | 0.2 |
| Lightning strike nearby | 0.35 ([[Lightning_Generation]]) |

## Accessibility
Scale by a user setting, and reduce shake heavily when **`GuiService.ReducedMotionEnabled`** is true (the player's Reduce Motion setting). `GuiService.PreferredTransparency` and `PreferredTextSize` are the related accessibility signals ([[Responsive_UI_and_Safe_Areas]]). Never shake UI text.

## Related
[[Camera_System]] · [[Hitstop_and_Impact_Feel]] · [[Noise_Functions]] · [[Math_Library]] · [[TweenService]] · [[Lightning_Generation]] · [[ODM_Gear_System]] · [[VFX_Composition_and_Timing]] · [[MOC_Combat_Systems]]

## Sources
- Trauma-based shake is a widely used game-dev technique; noise per https://create.roblox.com/docs/reference/engine/libraries/math#noise
