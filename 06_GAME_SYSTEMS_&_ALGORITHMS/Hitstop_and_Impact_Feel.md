---
aliases: [Hitstop, Hit pause, Impact frames, Game feel, Juice, Hit feedback]
tags:
  - roblox-dev
  - systems/combat
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Hitstop & Impact Feel

> **TL;DR:** Impact feel comes from **time manipulation + synchronized feedback**. Freeze or slow the attacker's and victim's animations for **2–6 frames** (hitstop), fire a flash plus particle burst at the contact point, punch the camera, layer a crunchy SFX, and show a readable damage number. All of it is client-side and **instant on the attacker's screen** (predicted), then confirmed for everyone else.

## Hitstop on Roblox
```luau
--!strict
-- freeze AnimationTracks briefly (attacker + victim), then restore their speeds
local function hitstop(animators: { Animator }, duration: number)
	local saved: { [AnimationTrack]: number } = {}
	for _, a in animators do
		for _, track in a:GetPlayingAnimationTracks() do
			saved[track] = track.Speed
			track:AdjustSpeed(0.03)            -- near-freeze (0 also works; tiny speed avoids "stuck" look)
		end
	end
	task.delay(duration, function()
		for track, speed in saved do
			if track.IsPlaying then track:AdjustSpeed(speed) end
		end
	end)
end
-- light hit: 0.05 s, heavy: 0.09 s, parry: 0.12 s (scale with damage)
```
- Also pause **trails** (`Enabled = false` briefly) and particle `TimeScale` on the weapon for a crisp freeze ([[Particle_Emitters]]).
- Extend combo windows and hit windows by the hitstop duration so it doesn't eat inputs ([[Combo_Systems_and_Input_Buffering]]).
- Under [[Server_Authority_Model|server authority]], hitstop is a *visual* layer in RenderStepped. Don't alter simulation time.

## The impact stack (≈100 ms)
| t | Layer |
| --- | --- |
| 0 ms | Hitstop starts. White flash on the victim (Highlight fill pulse) ([[Light_Sources_and_Highlights]]) |
| 0 ms | Spark/burst emitters `:Emit()` at the contact point, oriented to the hit normal ([[VFX_Composition_and_Timing]]) |
| 0 ms | SFX: transient + body + tail, pitch-randomized ([[Audio_API]]) |
| 0–80 ms | Camera punch along the hit direction, small FOV pulse ([[Camera_Shake]]) |
| 50 ms | Damage number pops, with crits bigger and different-colored ([[Damage_Numbers_and_Hit_Markers]]) |
| end | Victim hit-react animation, knockback starts ([[Knockback_and_Ragdoll]]) |

## Readability rules
Strong feedback for **confirmed** hits. Lighter predicted feedback until confirmation if your game has many rejects. Distinct shapes and colors per outcome (hit, crit, block, parry). Respect Reduce Motion for shakes.

## Related
[[VFX_Composition_and_Timing]] · [[Camera_Shake]] · [[Damage_Numbers_and_Hit_Markers]] · [[Animation_System]] · [[Particle_Emitters]] · [[Audio_API]] · [[Block_Parry_and_IFrames]] · [[Knockback_and_Ragdoll]] · [[Client_Side_VFX_Replication]] · [[MOC_Combat_Systems]] · [[MOC_VFX_and_Weather]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/AnimationTrack#AdjustSpeed · game-feel conventions
