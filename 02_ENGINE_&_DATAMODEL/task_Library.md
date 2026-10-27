---
aliases: [task, task.spawn, task.defer, task.delay, task.wait, task.cancel]
tags:
  - roblox-dev
  - engine/scheduler
type: api
last_updated: 2026-10-27
status: complete
---
# `task` Library

> **TL;DR:** The modern scheduling API: `task.spawn` (run now), `task.defer` (run at the end of the current resumption cycle), `task.delay` (run later), `task.wait` (yield), `task.cancel` (kill a thread), plus `task.desynchronize`/`synchronize` for [[Parallel_Luau]]. No throttling, errors keep their stack traces, and it replaces `wait`/`spawn`/`delay` ([[Deprecated_wait_spawn_delay]]).

## API
| Function | Behavior |
| --- | --- |
| `task.spawn(fnOrThread, ...)` | Resumes **immediately** through the scheduler. Returns the thread |
| `task.defer(fnOrThread, ...)` | Resumes at the **end of the current resumption point** (same frame). `defer(print, "A"); print("B")` prints B then A |
| `task.delay(t, fnOrThread, ...)` | Resumes on the first **Heartbeat** after `t` seconds (`t = 0` means next step) |
| `task.wait(t?)` | Yields, resumes on the Heartbeat after `t`. Returns the actual elapsed time |
| `task.cancel(thread)` | Stops a thread that hasn't finished (including delayed/waiting ones) |
| `task.desynchronize()` / `task.synchronize()` | Switch the current thread to parallel or serial execution inside an [[Actors_and_Messaging|Actor]] |

## Idioms
```luau
-- run many yielding jobs concurrently (and let transparent batching group HTTP calls)
for _, id in productIds do
	task.spawn(fetchProductInfo, id)
end

-- cancellable timer (e.g. buff expiry)
local expiry = task.delay(10, removeBuff, character)
-- refreshed early? cancel and re-arm
task.cancel(expiry)

-- defer work until the current event burst settles
task.defer(recomputeLeaderboard)
```
Concurrent `task.spawn`s of supported Marketplace and Avatar API calls get **transparently batched** into fewer HTTP requests by the engine ([[MarketplaceService]]).

## Gotchas
- `task.spawn` inside `RunService:BindToSimulation()` **keeps simulation restrictions**, because it runs immediately. Use `task.defer` to escape them ([[Server_Authority_Model]]).
- `task.cancel` on the **currently running** thread errors. Cancel from elsewhere, or `return`.
- `task.wait()` in a tight loop is a polling smell. Prefer events or [[RunService_Frame_Events]].

## Related
[[Task_Scheduler]] · [[Coroutines]] · [[Deprecated_wait_spawn_delay]] · [[RunService_Frame_Events]] · [[Parallel_Luau]] · [[Actors_and_Messaging]] · [[Server_Authority_Model]] · [[Status_Effects]] · [[MarketplaceService]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/reference/engine/libraries/task · https://create.roblox.com/docs/scripting/scheduler
- https://create.roblox.com/docs/scripting/transparent-batching
