---
aliases: [MicroProfiler, Ctrl+F6, debug.profilebegin, Profiler labels, Frame profiler]
tags:
  - roblox-dev
  - performance/profiling
type: api
last_updated: 2026-10-27
status: complete
---
# MicroProfiler

> **TL;DR:** The MicroProfiler shows **where every millisecond of every frame goes**: engine tasks (render, physics, networking, scripts) as nested scopes on a timeline. Open it with **Ctrl+F6** (⌘F6) in Studio or in-game, pause with **Ctrl+P**, and wrap your own code with `debug.profilebegin("Label")` / `debug.profileend()` so it shows up by name. Use **server profiling** from the Developer Console for server lag.

## Workflow
1. Open (Ctrl+F6). Watch the frame-time bar graph for spikes.
2. **Pause** on a spiky frame (Ctrl+P) and drill into the widest scopes.
3. Toggle modes (detailed and timeline views) ([[Performance_Optimization_Workflow]]).
4. **Dump** frames to HTML for sharing or deeper analysis.
5. **Server:** Developer Console ▸ MicroProfiler tab ▸ start a server profile (dumps are captured from the live server).

## Label your own code
```luau
local RunService = game:GetService("RunService")
RunService.Heartbeat:Connect(function(dt)
	debug.profilebegin("AI.Think")
	AI.thinkAll(dt)
	debug.profileend()

	debug.profilebegin("Combat.ResolveHits")
	Combat.resolve()
	debug.profileend()
end)
```
Keep labels coarse (systems, not every function), and **always pair** begin and end (early `return`s are the classic mismatch).

## Scopes worth knowing
| Scope | Meaning |
| --- | --- |
| `physicsStepped` → `worldStep` (`- Adaptive`) → `LDLPGSSolver::solve` | Physics solver. Hover for island counts ([[Adaptive_Timestepping]]) |
| `ProcessPackets` | Incoming network: remote invocations, property changes ([[Network_Bandwidth_Budget]]) |
| `Allocate Bandwidth and Run Senders` | Outgoing replication (server) |
| `Render` / `Prepare` / `Perform` | GPU and CPU render work ([[Rendering_Optimization]]) |
| Script scopes (`LuaGc`, script names, your labels) | Luau time and GC assists ([[Garbage_Collection]]) |
| Parallel worker lanes | [[Parallel_Luau]] work across threads |

## Tips
- Compare frames **before and after** a fix at the same scene and player count ([[Benchmarking_Methodology]]).
- Repeating spikes at regular intervals usually mean an autosave, GC, or a periodic system without time-slicing ([[Time_Slicing_and_Frame_Budget]]).
- Long red script bars with your label make it clear which system to move into Actors or native code ([[Native_Code_Generation]]).

## Related
[[Performance_Optimization_Workflow]] · [[Script_Profiler]] · [[Developer_Console]] · [[Task_Scheduler]] · [[Adaptive_Timestepping]] · [[Network_Bandwidth_Budget]] · [[Parallel_Luau]] · [[Rendering_Optimization]] · [[Time_Slicing_and_Frame_Budget]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://create.roblox.com/docs/performance-optimization/microprofiler · https://create.roblox.com/docs/performance-optimization/microprofiler/use-microprofiler
