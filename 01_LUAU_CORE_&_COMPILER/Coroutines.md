---
aliases: [coroutine, threads, coroutine.wrap, coroutine.close, yield]
tags:
  - roblox-dev
  - luau/concurrency
type: api
last_updated: 2026-10-27
status: complete
---
# Coroutines

> **TL;DR:** Coroutines are cooperative threads: they run until they `yield`, then resume later. On Roblox you rarely call `coroutine.resume` directly. The [[task_Library]] (`task.spawn`, `task.defer`, `task.wait`) schedules threads for you. Raw coroutines are still great for **generators**, state machines and stepping algorithms across frames.

## API
| Function | Notes |
| --- | --- |
| `coroutine.create(fn)` → thread | Not started yet |
| `coroutine.resume(co, ...)` → `ok, ...` | Errors are **caught** and returned as `false, err` |
| `coroutine.wrap(fn)` → function | Calling it resumes. Errors **propagate** to the caller |
| `coroutine.yield(...)` | Returns values to the resumer |
| `coroutine.status(co)` | `"suspended" | "running" | "normal" | "dead"` |
| `coroutine.isyieldable()` | Whether the current thread can yield |
| `coroutine.running()` | Current thread |
| `coroutine.close(co)` | Kills a suspended or dead coroutine, returns `true` or `false, err` (Lua 5.4 feature) |

## Generator example (time-sliced work)
```luau
--!strict
local function chunked<T>(items: { T }, perStep: number)
	return coroutine.wrap(function()
		for i, item in items do
			coroutine.yield(item)
			if i % perStep == 0 then coroutine.yield(nil) end -- nil = "pause this frame"
		end
	end)
end
```
See [[Time_Slicing_and_Frame_Budget]] for the production version.

## Roblox interplay
- `task.wait`, `WaitForChild` and every `*Async` call **yield the current thread**. The engine resumes it later, which is why they only work in yieldable contexts.
- **Don't** `coroutine.resume` a thread that's waiting on an engine yield (`task.wait`), or you'll get confusing double-resume behavior. Use `task.spawn`/`task.defer`/`task.cancel` for engine-managed threads ([[task_Library]]).
- Errors inside `task.spawn`ed threads are **reported to Output** with a stack trace. Errors inside `coroutine.resume` are **swallowed** unless you check the return value. That's a classic "silent failure" bug ([[Error_Handling_pcall_xpcall]]).
- Many suspended coroutines raise GC atomic-step cost a little. Luau marks inactive coroutines incrementally to mitigate this ([[Garbage_Collection]]).

## Related
[[task_Library]] · [[Task_Scheduler]] · [[Error_Handling_pcall_xpcall]] · [[Deprecated_wait_spawn_delay]] · [[Time_Slicing_and_Frame_Budget]] · [[Promise_Library]] · [[Garbage_Collection]] · [[Closures_and_Upvalues]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://create.roblox.com/docs/reference/engine/libraries/coroutine · https://rfcs.luau.org/function-coroutine-close.html
