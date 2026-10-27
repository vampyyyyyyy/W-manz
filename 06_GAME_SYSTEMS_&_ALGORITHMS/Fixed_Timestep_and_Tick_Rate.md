---
aliases: [Fixed timestep, Tick rate, Accumulator, Deterministic simulation, UseFixedSimulation]
tags:
  - roblox-dev
  - systems/simulation
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Fixed Timestep & Tick Rate

> **TL;DR:** Frame rates vary (30–240+ FPS on clients, about 60 on servers). Gameplay simulation that must match across machines (prediction, replays, deterministic projectiles) should run at a **fixed tick** (e.g. 30 or 60 Hz) using an **accumulator**, with rendering interpolated between ticks. Roblox's `RunService:BindToSimulation` + `Workspace.UseFixedSimulation` gives you an engine fixed step under the [[Server_Authority_Model]].

## Accumulator pattern
```luau
--!strict
local RunService = game:GetService("RunService")
const TICK = 1 / 60
local acc = 0
local prevState, state = initialState(), initialState()

RunService.Heartbeat:Connect(function(dt)
	acc += math.min(dt, 0.25)                -- clamp: avoid the "spiral of death" after hitches
	while acc >= TICK do
		prevState = state
		state = simulate(state, TICK)        -- deterministic step
		acc -= TICK
	end
	local alpha = acc / TICK                 -- render interpolation factor
	render(prevState, state, alpha)          -- lerp positions for smooth visuals
end)
```

## Choosing a tick rate
| System | Typical tick |
| --- | --- |
| Character movement (engine physics) | Engine (240 Hz physics, or adaptive) ([[Adaptive_Timestepping]]) |
| Custom combat/simulation logic | 30–60 Hz |
| Network snapshots (other entities) | 10–20 Hz + interpolation ([[Client_Prediction_and_Reconciliation]]) |
| AI decisions | 2–10 Hz, staggered across NPCs ([[Time_Slicing_and_Frame_Budget]]) |
| Weather / sky writes | ~15 Hz (Roblox weather sample) ([[Weather_System_Architecture]]) |

## Rules
- Use **one clock** for simulation: `time()` under server authority, otherwise your own accumulated tick count. Not `os.clock()` deltas spread across systems.
- Never multiply by frame `dt` *inside* a fixed step. Use `TICK`.
- Seeded `Random.new(seed)` per simulation for reproducibility ([[Math_Library]]).
- Under server authority: `task.spawn` inside sim callbacks keeps sim restrictions and `task.defer` escapes them. Only "Simulation Access" APIs are allowed in `BindToSimulation`.

## Related
[[Client_Prediction_and_Reconciliation]] · [[Server_Authority_Model]] · [[Task_Scheduler]] · [[RunService_Frame_Events]] · [[Adaptive_Timestepping]] · [[Time_Slicing_and_Frame_Budget]] · [[Projectile_Systems]] · [[Weather_System_Architecture]] · [[MOC_Movement_and_ODM]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/RunService#BindToSimulation
- https://create.roblox.com/docs/projects/server-authority#simulation-sync
