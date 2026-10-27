---
aliases: [GetMarkerReachedSignal, Animation events, Keyframe markers, Hit frames]
tags:
  - roblox-dev
  - engine/animation
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Animation Events & Markers

> **TL;DR:** Put **named event markers** in the Animation Editor timeline ("WindupEnd", "HitStart", "HitEnd", "Footstep") and listen with `track:GetMarkerReachedSignal("Name")`. This lines up hitboxes, VFX, sounds and camera shake with the animator's intent, so you don't need hardcoded `task.wait(0.27)` timers that drift when you retime the animation.

## Pattern: animation-driven hit window (client feel + server truth)
```luau
--!strict
local function playSwing(track: AnimationTrack, onWindowOpen: () -> (), onWindowClose: () -> ())
	local conns = {
		track:GetMarkerReachedSignal("HitStart"):Connect(onWindowOpen),
		track:GetMarkerReachedSignal("HitEnd"):Connect(onWindowClose),
	}
	track.Stopped:Once(function()
		for _, c in conns do c:Disconnect() end
		onWindowClose()                        -- always close, even if interrupted (stun, cancel)
	end)
	track:Play(0.05)
end
```
Markers can carry a **parameter string** (`GetMarkerReachedSignal("Footstep"):Connect(function(param) ... end)`), for example `"left"`/`"right"` or a surface hint.

## Server-side timing (don't trust client markers)
Markers fire wherever the animation plays. On the client that's ideal for **feel**: VFX, sound, client-side hit detection. The server should derive the **valid hit window from data**, e.g. `HitStart = 0.18 s`, `HitEnd = 0.32 s` stored in a frozen attack table that's exported alongside the animation, and check hit timestamps against it ([[Hit_Validation]], [[Combat_State_Machine]]).

## Gotchas
- `KeyframeReached` (named keyframes) is the legacy mechanism. Prefer markers.
- If the track's `Speed` changes (haste, slow), marker times scale accordingly, so update server windows the same way.
- Markers inside a short fade-out may never fire if the track is stopped early. Handle `Stopped` as above.
- Disconnect marker connections per play, or connect once per cached track. Never connect per play without cleanup ([[Connection_Management]]).

## Related
[[Animation_System]] · [[Combat_State_Machine]] · [[Hitbox_Detection_Methods]] · [[Hit_Validation]] · [[VFX_Composition_and_Timing]] · [[Hitstop_and_Impact_Feel]] · [[Camera_Shake]] · [[Connection_Management]] · [[MOC_Combat_Systems]]

## Sources
- https://create.roblox.com/docs/animation/events
- https://create.roblox.com/docs/reference/engine/classes/AnimationTrack#GetMarkerReachedSignal
