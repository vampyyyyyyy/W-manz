---
aliases: [Animator, AnimationTrack, LoadAnimation, Animation priority, Animation Graph Editor, AnimationGraphDefinition]
tags:
  - roblox-dev
  - engine/animation
type: api
last_updated: 2026-10-27
status: complete
---
# Animation System

> **TL;DR:** `Animator:LoadAnimation(animation)` returns an `AnimationTrack` you can `Play`, `Stop`, `AdjustSpeed`, `AdjustWeight` and blend by `Priority`. Animations **played by a client on its own character replicate** to everyone through the `Animator`. Anything else must be played on the server. 2026 adds the **Animation Graph Editor**: node graphs and **state machines** (`AnimationGraphDefinition`) driven at runtime by `AnimationTrack:SetParameter`.

## Core API
```luau
local animator = humanoid:WaitForChild("Animator") :: Animator
local track = animator:LoadAnimation(script.Slash1)   -- Animation instance with AnimationId
track.Priority = Enum.AnimationPriority.Action        -- Core < Idle < Movement < Action < Action2..4
track.Looped = false
track:Play(0.05, 1, 1.15)                              -- fadeTime, weight, speed
track.Stopped:Once(function() --[[ back to idle ]] end)
track:GetMarkerReachedSignal("Hit"):Connect(onHitFrame) -- see Animation_Events_and_Markers
```
- `Humanoid:LoadAnimation` is deprecated. Use the `Animator`.
- **Cache tracks per Animator** (load once, replay many times). Loading the same animation repeatedly leaks tracks. Under [[Server_Authority_Model|server authority]], don't hold tracks across rollbacks. Query `Animator:GetTrackByAnimationId()` or `GetPlayingAnimationTracks()` instead.
- `TimePosition`, `Length`, `IsPlaying`, `Speed`, `WeightCurrent` are readable. `AdjustSpeed(0)` freezes on a frame (hitstop: [[Hitstop_and_Impact_Feel]]).

## Replication rules
- A client's `Animator` replicates tracks **for its own character** (and other client-owned rigs it controls).
- NPC animations must be played **on the server** to replicate. Alternatively, play them on clients from a replicated state (cheaper for crowds).
- `Animator` must exist on the server **and** replicate, otherwise nothing replicates.

## Animation Graph Editor (2026)
- Build graphs of **clip**, **blend** (e.g. `Blend1DNode` over `Speed`) and **state machine** nodes. Transitions use expressions (`not Grounded`) or "Finished" with `BeforeFinished` timing, plus blend lengths and curves.
- Publishing creates an **`AnimationGraphDefinition`** asset. Load it like any animation and drive it with `track:SetParameter("humanoidSpeed", speed)` every frame.
- Replaces hand-written "which animation should play" spaghetti in locomotion and combat stance code ([[Finite_State_Machines]]).

## Procedural layers
Edit `Motor6D.Transform` in **PreSimulation** (after Animators write, before physics) for aim offsets, head look and recoil ([[Task_Scheduler]]). IK: `IKControl` for foot planting and hand targets.

## Related
[[Animation_Events_and_Markers]] · [[Humanoid_and_Character_Model]] · [[Combat_State_Machine]] · [[Hitstop_and_Impact_Feel]] · [[Finite_State_Machines]] · [[Server_Authority_Model]] · [[Task_Scheduler]] · [[Replication_Model]] · [[VFX_Composition_and_Timing]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/animation/using · https://create.roblox.com/docs/reference/engine/classes/Animator
- https://create.roblox.com/docs/animation/graph-editor · https://create.roblox.com/docs/animation/graph-editor-state-machine
