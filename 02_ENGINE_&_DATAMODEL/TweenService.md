---
aliases: [Tween, TweenInfo, TweenService:Create, SmoothDamp, Easing]
tags:
  - roblox-dev
  - engine/animation
type: api
last_updated: 2026-10-27
status: complete
---
# TweenService (incl. `SmoothDamp`)

> **TL;DR:** `TweenService:Create(instance, TweenInfo, goals)` animates properties with easing. `TweenService:GetValue(alpha, style, dir)` gives you easing curves for custom code. **`TweenService:SmoothDamp(current, target, velocity, smoothTime, maxSpeed?, dt?)`** is a built-in **critically damped spring** that returns `(newValue, newVelocity)`. Tween on the **client**: server tweens replicate the property every frame and jitter ([[Network_Bandwidth_Budget]]).

## Tweens
```luau
local TweenService = game:GetService("TweenService")
local info = TweenInfo.new(0.35, Enum.EasingStyle.Quint, Enum.EasingDirection.Out, 0, false, 0)
-- (time, style, direction, repeatCount, reverses, delayTime)
local tween = TweenService:Create(frame, info, { Size = UDim2.fromScale(0.3, 0.1), BackgroundTransparency = 0 })
tween:Play()
tween.Completed:Once(function(state) print(state) end)    -- Enum.PlaybackState
```
- Tweenable types include number, bool, `CFrame`, `Vector3`, `Vector2`, `UDim2`, `UDim`, `Color3`, `Rect`, `EnumItem` (snaps).
- Starting a new tween on the same property **overrides** the old one (the old one cancels).
- `GetValue` for custom interpolation: `local a = TweenService:GetValue(t / duration, Enum.EasingStyle.Back, Enum.EasingDirection.Out)`.

## SmoothDamp (springy follow without a spring module)
```luau
local velocity = Vector3.zero
RunService.PreRender:Connect(function(dt)
	local newPos, newVel = TweenService:SmoothDamp(follower.Position, target.Position, velocity, 0.12, math.huge, dt)
	follower.Position = newPos
	velocity = newVel            -- keep the returned velocity (don't shadow it with a new local)
end)
```
It works on numbers, vectors and other supported value types. It's used in the server-authority docs to smooth mispredicted objects ([[Server_Authority_Model]]), and it's great for cameras, UI followers and damage-number drift ([[UI_Animation_and_Springs]]).

## Rules of thumb
- UI and VFX motion: tween on the client. World objects everyone must see in sync (doors, platforms): server sets the *state*, clients tween visually, or use physics with anchored CFrame updates.
- Don't create a tween per frame. Reuse it, or use SmoothDamp or springs for continuous targets.
- Anchored part tweens + characters: players standing on tweened (anchored) platforms don't inherit movement automatically. Use physics movers or prismatic constraints for rideable platforms ([[Mover_Constraints]]).

## Related
[[UI_Animation_and_Springs]] · [[Camera_System]] · [[Server_Authority_Model]] · [[Network_Bandwidth_Budget]] · [[Client_Side_VFX_Replication]] · [[Mover_Constraints]] · [[Lighting_and_Post_Processing]] · [[Math_Library]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/TweenService
- https://create.roblox.com/docs/projects/server-authority/techniques#position-smoothing
