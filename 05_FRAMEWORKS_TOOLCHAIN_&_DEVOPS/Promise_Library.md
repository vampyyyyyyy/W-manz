---
aliases: [Promise, roblox-lua-promise, evaera Promise, Promises in Luau]
tags:
  - roblox-dev
  - framework/async
type: framework
last_updated: 2026-10-27
status: complete
---
# Promise Library (evaera/roblox-lua-promise)

> **TL;DR:** Promises represent async work as objects you can **chain, combine, cancel and time out**: `Promise.new`, `:andThen`, `:catch`, `:finally`, `Promise.all`, `Promise.race`, `:timeout`, `:cancel`. They make "do these 5 HTTP calls concurrently, then continue" and "cancel if the player leaves" clean. The library is stable (last updated 2023) and used by Lapis and older Knit code.

## Core usage
```luau
local Promise = require(ReplicatedStorage.Packages.Promise)

local function fetchProduct(id: number)
	return Promise.new(function(resolve, reject, onCancel)
		local ok, info = pcall(MarketplaceService.GetProductInfoAsync, MarketplaceService, id, Enum.InfoType.Product)
		if ok then resolve(info) else reject(info) end
	end)
end

Promise.all({ fetchProduct(1), fetchProduct(2), fetchProduct(3) })
	:timeout(10)
	:andThen(function(infos) Shop.render(infos) end)
	:catch(function(err) warn("shop load failed", tostring(err)) end)
```
`Promise.new` runs its executor in a new thread (`Promise.defer` defers it). `:await()` / `:expect()` yield back into synchronous style when you need it.

## When to use (vs plain yielding)
- ✅ Concurrency, cancellation tied to lifetimes (`onCancel` cleans up), timeouts, composition in libraries.
- ❌ Simple linear code. `task.spawn` + `pcall` is clearer for most game logic ([[task_Library]], [[Error_Handling_pcall_xpcall]]).
- Unhandled rejections print warnings. Always `:catch` at the end of chains.

## Related
[[task_Library]] · [[Coroutines]] · [[Error_Handling_pcall_xpcall]] · [[Lapis]] · [[Knit]] · [[Signal_Libraries]] · [[Wally]] · [[Community_Modules_Index]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://github.com/evaera/roblox-lua-promise · https://eryn.io/roblox-lua-promise/
