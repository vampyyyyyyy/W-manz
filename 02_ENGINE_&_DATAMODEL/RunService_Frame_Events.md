---
aliases: [RunService, Heartbeat, PreRender, RenderStepped, PreSimulation, Stepped, PostSimulation, BindToRenderStep]
tags:
  - roblox-dev
  - engine/scheduler
type: api
last_updated: 2026-10-27
status: complete
---
# RunService Frame Events

> **TL;DR:** Use `PreRender` (client, camera and visuals), `PreSimulation` (drive physics or Motor6D), `PostSimulation`/`Heartbeat` (game logic after physics). `BindToRenderStep(name, priority, fn)` gives ordered render-step callbacks. The older `RenderStepped`/`Stepped` still work, but the newer names map clearly onto the [[Task_Scheduler]].

## Events & methods (Oct 2026)
| Member | When | Arg | Side |
| --- | --- | --- | --- |
| `PreRender` / `RenderStepped` | Before the frame renders | `dt` | Client |
| `BindToRenderStep(name, priority, fn)` / `UnbindFromRenderStep(name)` | PreRender, ordered by `Enum.RenderPriority` values | `dt` | Client |
| `PreAnimation` / `BindToAnimation` | Before Animators update | `dt` | Both |
| `PreSimulation` / `Stepped` | Before physics | `dt` (Stepped: `time, dt`) | Both |
| `PostSimulation` | After physics | `dt` | Both |
| `Heartbeat` | After physics + task resumptions | `dt` | Both |
| `BindToSimulation(fn)` | Fixed-rate simulation, independent of frame rate | `dt` | Both ([[Server_Authority_Model]]) |
| `Misprediction`, `Rollback` | Server authority prediction events | | Client |
| `SetPredictionMode`, `GetPredictionStatus`, `IsResimulating` | Prediction control and debug | | |
| `IsServer()`, `IsClient()`, `IsStudio()`, `IsRunning()` | Environment checks | | |

## Patterns
```luau
--!strict
local RunService = game:GetService("RunService")

-- Camera follow: after input, before render, with explicit priority
RunService:BindToRenderStep("CombatCamera", Enum.RenderPriority.Camera.Value + 1, function(dt)
	CameraController.update(dt)
end)

-- Frame-rate independent movement
local conn = RunService.Heartbeat:Connect(function(dt)
	projectile.Position += projectile.Velocity * dt
end)
```

## Rules
- **Always use `dt`.** Frame rates range from 30 to 240+ (players can uncap FPS). Logic that assumes 60 FPS breaks for them ([[Fixed_Timestep_and_Tick_Rate]]).
- Keep per-frame callbacks **few and cheap**. Many tiny `Heartbeat` connections cost more than one dispatcher looping over a list ([[Time_Slicing_and_Frame_Budget]]).
- Disconnect when done ([[Connection_Management]]).
- Server `Heartbeat` runs at the server's frame rate (~60 Hz), not the client's.

## Related
[[Task_Scheduler]] · [[task_Library]] · [[Deferred_Events_and_SignalBehavior]] · [[Camera_System]] · [[Fixed_Timestep_and_Tick_Rate]] · [[Server_Authority_Model]] · [[Connection_Management]] · [[Time_Slicing_and_Frame_Budget]] · [[Mover_Constraints]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/RunService
