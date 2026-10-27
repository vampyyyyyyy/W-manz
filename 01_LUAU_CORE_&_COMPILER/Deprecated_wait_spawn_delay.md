---
aliases: [wait(), spawn(), delay(), tick(), deprecated globals]
tags:
  - roblox-dev
  - luau/legacy
type: concept
last_updated: 2026-10-27
status: complete
---
# Deprecated: `wait`, `spawn`, `delay` (and friends)

> **TL;DR:** The legacy globals `wait()`, `spawn()` and `delay()` run on an old **throttled** scheduler. `wait()`, `spawn()` and `delay()` all have a **minimum 29 ms** delay that can stretch arbitrarily under load or throttling. All three are officially tagged Deprecated. Replace them with `task.wait`, `task.spawn`/`task.defer` and `task.delay` ([[task_Library]]). Also prefer `os.clock()` and `workspace:GetServerTimeNow()` over `tick()`. `tick()` isn't officially deprecated, but it can be off by up to 1 s and is inconsistent across time zones and OSes.

## Replacement table
| Legacy | Modern | Why |
| --- | --- | --- |
| `wait(t)` | `task.wait(t)` | Resumes on the next Heartbeat after `t`, no throttling. Returns actual elapsed time |
| `wait()` in loops | `RunService.Heartbeat:Wait()`, or an event-driven design | Polling loops waste CPU ([[RunService_Frame_Events]]) |
| `spawn(f)` | `task.spawn(f)` (now) / `task.defer(f)` (end of cycle) | No hidden start delay. Errors keep their stack trace |
| `delay(t, f)` | `task.delay(t, f)` | Cancellable via `task.cancel` |
| `tick()` | `os.clock()` (benchmarks), `workspace:GetServerTimeNow()` (synced), `DateTime.now()`/`os.time()` (wall clock), `time()` (game time; synced under [[Server_Authority_Model|server authority]]) | Off by up to 1 s; inconsistent across time zones/OSes |
| `game.Players.LocalPlayer.Character` busy-waits | `player.CharacterAdded:Wait()` | [[Player_and_Character_Lifecycle]] |

## The classic loop, modernized
```luau
-- legacy (2018-2022 era scripts)
spawn(function()
	while true do
		doThing()
		wait()
	end
end)

-- modern: explicit cadence, cancellable, no throttled scheduler
local thread = task.spawn(function()
	while true do
		doThing()
		task.wait(0.1)
	end
end)
-- later: task.cancel(thread)
```
Better still, react to events (`Changed`, `GetAttributeChangedSignal`, signals) instead of polling ([[Signals_and_Connections]]).

## Related
[[task_Library]] · [[Task_Scheduler]] · [[RunService_Frame_Events]] · [[Coroutines]] · [[Legacy_Code_Smells]] · [[Globals_G_shared_and_getfenv]] · [[Signals_and_Connections]] · [[Player_and_Character_Lifecycle]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://create.roblox.com/docs/reference/engine/libraries/task
- https://create.roblox.com/docs/reference/engine/globals/RobloxGlobals (deprecated globals)
