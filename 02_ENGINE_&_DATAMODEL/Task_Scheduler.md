---
aliases: [Task scheduler, Frame order, Engine frame, Frame pipeline]
tags:
  - roblox-dev
  - engine/scheduler
type: architecture
last_updated: 2026-10-27
status: complete
---
# Task Scheduler (the engine frame)

> **TL;DR:** Each frame the engine runs a fixed sequence: **input → PreRender → (render) → legacy waits → PreAnimation → animation → PreSimulation → physics → PostSimulation → task resumptions → Heartbeat → replication**. Knowing where your code runs in this pipeline explains jitter, one-frame-late bugs and "my Motor6D change got overwritten" ([[RunService_Frame_Events]]).

## Order (resumption points, per Roblox docs)
```text
1. Input processing                (UserInputService / ContextActionService handlers, per input)
2. PreRender  (RenderStepped, BindToRenderStep)   ← camera, view-model, UI that must match the frame (client)
   ── frame is rendered ──
3. Legacy wait()/spawn()/delay() resumption       ← throttled; avoid
4. PreAnimation  (BindToAnimation)                ← before Animators update
5. Animation step (Animators write Motor6D.Transform)
6. PreSimulation (Stepped)                        ← set velocities/forces, Motor6D.Transform overrides
7. Physics simulation (may substep; adaptive timestepping, up to 240 Hz)
8. PostSimulation                                 ← read physics results
9. task.wait/task.delay/task.spawn resumptions
10. Heartbeat                                     ← general per-frame game logic
11. Network send / replication (server: "Allocate Bandwidth and Run Senders")
```
With `Workspace.SignalBehavior = Deferred`, event handlers queued since the last point run at each of these resumption points ([[Deferred_Events_and_SignalBehavior]]).

## Practical consequences
- **Camera and view-model** go in PreRender or `BindToRenderStep` (after input, before draw). Putting them in Heartbeat shows last frame's camera, so you get jitter ([[Camera_System]]).
- **Physics inputs** (`AssemblyLinearVelocity`, `VectorForce`) go in **PreSimulation**. Reactions to physics results go in **PostSimulation**/Heartbeat ([[Mover_Constraints]]).
- **Procedural animation** (`Motor6D.Transform`) goes in **PreSimulation**, otherwise Animators overwrite it next frame ([[Animation_System]]).
- **Server authority** adds fixed-rate simulation via `BindToSimulation`, plus `Rollback`/`Misprediction` events ([[Server_Authority_Model]]).
- Heavy work in any step delays the whole frame. Spread it out ([[Time_Slicing_and_Frame_Budget]]) or go parallel ([[Parallel_Luau]]).

## Overload symptoms
Custom rigs, manual part animation, physics-heavy scenes and frequent replication are the documented overload sources. Diagnose with the [[MicroProfiler]] (each step has labeled scopes).

## Related
[[RunService_Frame_Events]] · [[task_Library]] · [[Deferred_Events_and_SignalBehavior]] · [[Adaptive_Timestepping]] · [[Animation_System]] · [[Camera_System]] · [[Server_Authority_Model]] · [[MicroProfiler]] · [[Time_Slicing_and_Frame_Budget]] · [[Fixed_Timestep_and_Tick_Rate]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/performance-optimization/microprofiler/task-scheduler
- https://create.roblox.com/docs/scripting/events/deferred#resumption-points
