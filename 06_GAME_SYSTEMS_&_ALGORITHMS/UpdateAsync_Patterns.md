---
aliases: [UpdateAsync, Atomic update, Read-modify-write, Transform function]
tags:
  - roblox-dev
  - systems/persistence
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# UpdateAsync Patterns

> **TL;DR:** `UpdateAsync(key, function(old, keyInfo) return new, userIds?, metadata? end)` reads the **latest** value and lets you transform it. If another server wrote in between, your function **re-runs** with the newer value. Return `nil` to **cancel**. The transform must be **fast, pure and non-yielding**. That makes it the primitive for counters, session locks and idempotent saves.

## Rules for the transform function
- **No yielding** (`task.wait`, other `*Async` calls). Compute from `old` only.
- **May run multiple times**, so no side effects (don't grant items, fire remotes or log inside it). Do side effects **after** a successful return.
- Return `nil` to abort without writing. Use this for lock conflicts and validation failures.
- `keyInfo` (DataStoreKeyInfo) exposes `Version`, `CreatedTime`, `UpdatedTime`, `:GetMetadata()` and `:GetUserIds()`. Return metadata as the 3rd value to keep or update it (session locks live there: [[Session_Locking]]).

## Pattern: idempotent save with a version stamp
```luau
--!strict
local function save(store: DataStore, key: string, data: { [string]: any }, sessionId: string): boolean
	local ok, err = pcall(function()
		store:UpdateAsync(key, function(old: any, keyInfo: DataStoreKeyInfo?)
			local meta = if keyInfo then keyInfo:GetMetadata() else {}
			if meta.LockId and meta.LockId ~= sessionId then
				return nil                          -- someone else owns this profile: abort
			end
			data.SaveVersion = ((old and old.SaveVersion) or 0) + 1
			return data, nil, meta                  -- keep metadata (incl. our LockId)
		end)
	end)
	if not ok then warn("save failed", err) end
	return ok
end
```

## Pattern: global counter / shared pool
```luau
store:UpdateAsync("EventPool", function(old)
	local pool = old or { remaining = 1000 }
	if pool.remaining <= 0 then return nil end   -- sold out: cancel
	pool.remaining -= 1
	return pool
end)
```
For high-contention shared counters, prefer `IncrementAsync`, MemoryStore, or sharded keys, because one hot key hits per-key throughput limits ([[DataStore_Limits_and_Error_Codes]], [[MemoryStoreService]]).

## Gotchas
- Returning the **same table** you received is fine, but mutating `old` and then returning `nil` doesn't write anything.
- `UpdateAsync` costs a read **and** a write from the budget.
- Don't call `GetAsync` and then `SetAsync` "to be safe". That's exactly the race `UpdateAsync` exists to prevent ([[Data_Duplication_and_Trade_Exploits]]).

## Related
[[DataStoreService]] · [[Session_Locking]] · [[DataStore_Limits_and_Error_Codes]] · [[Data_Versioning_and_Schema_Migration]] · [[ProcessReceipt_Idempotency]] · [[Data_Duplication_and_Trade_Exploits]] · [[Error_Handling_pcall_xpcall]] · [[ProfileStore]] · [[MOC_Game_Systems_and_Algorithms]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/GlobalDataStore#UpdateAsync
- https://create.roblox.com/docs/cloud-services/data-stores/best-practices#prefer-updateasync-over-setasync
