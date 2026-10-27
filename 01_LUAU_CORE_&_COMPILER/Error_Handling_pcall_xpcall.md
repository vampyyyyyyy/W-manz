---
aliases: [pcall, xpcall, error handling, error(), debug.traceback, retries]
tags:
  - roblox-dev
  - luau/errors
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Error Handling (`pcall`, `xpcall`, `error`)

> **TL;DR:** Wrap anything that **talks to a backend** (DataStores, MarketplaceService, HttpService, TeleportService, BadgeService) in `pcall` and retry with backoff. Use `xpcall(fn, debug.traceback)` when you need the stack trace. Don't wrap normal game logic in `pcall` to hide bugs. In Luau, `pcall` is **yieldable** and, since 2025, stackless in yieldable contexts.

## Basics
```luau
local ok, result = pcall(DataStore.GetAsync, DataStore, key)   -- method form: pass self explicitly
if not ok then warn("GetAsync failed:", result) end

local ok2, err = xpcall(riskyFunction, function(e)
	return debug.traceback(tostring(e), 2)                    -- capture full stack
end, arg1, arg2)

error("Invalid state", 2)                                    -- level 2 blames the caller
error({ code = "NO_FUNDS", need = 50 })                      -- error objects can be tables
```

## Retry with exponential backoff (backend calls)
```luau
--!strict
local function retry<T...>(attempts: number, fn: () -> T...): (boolean, ...any)
	local delay = 1
	for i = 1, attempts do
		local result = table.pack(pcall(fn))
		if result[1] then return table.unpack(result, 1, result.n) end
		if i < attempts then
			task.wait(delay + math.random() * 0.5)     -- jitter avoids thundering herds
			delay *= 2
		else
			return false, result[2]
		end
	end
	return false, "unreachable"
end

local ok, data = retry(4, function() return store:GetAsync("player_" .. userId) end)
```
Roblox recommends exponential backoff for DataStores and HTTP ([[DataStore_Limits_and_Error_Codes]], [[HttpService_and_Secrets_Store]]).

## Where errors go
- Uncaught errors in a Script, LocalScript or `task.spawn`ed thread **print to Output with a traceback** and kill that thread only.
- Errors inside `coroutine.resume` are **returned, not printed**. Check them ([[Coroutines]]).
- `ScriptContext.Error` fires for uncaught errors, so you can feed it into analytics ([[AnalyticsService_Events]]).

## Anti-patterns
- `pcall` around everything: it hides bugs and makes stack traces useless.
- Retrying **non-idempotent** operations blindly (granting currency twice). Make the operation idempotent first ([[ProcessReceipt_Idempotency]], [[UpdateAsync_Patterns]]).
- Erroring inside remote handlers on bad client input. Return early instead ([[Server_Side_Validation]]).

## Related
[[Coroutines]] · [[task_Library]] · [[DataStore_Limits_and_Error_Codes]] · [[UpdateAsync_Patterns]] · [[HttpService_and_Secrets_Store]] · [[ProcessReceipt_Idempotency]] · [[Promise_Library]] · [[Studio_Debugger]] · [[Varargs_and_Tuples]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://create.roblox.com/docs/reference/engine/globals/LuaGlobals#pcall
- https://luau.org/news/2025-12-19-luau-recap-runtime-2025 (stackless pcall)
