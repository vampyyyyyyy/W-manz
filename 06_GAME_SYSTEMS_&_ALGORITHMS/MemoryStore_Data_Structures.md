---
aliases: [MemoryStoreSortedMap, MemoryStoreQueue, MemoryStoreHashMap, Matchmaking queue]
tags:
  - roblox-dev
  - systems/cross-server
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# MemoryStore Data Structures

> **TL;DR:** **Sorted map**: ordered by key or sort key, range reads, atomic `UpdateAsync`. Good for leaderboards and server browsers. **Queue**: `AddAsync`, `ReadAsync` with invisibility timeout, then `RemoveAsync` to acknowledge. Good for matchmaking and job queues. **Hash map**: unordered, scales across partitions. Good for large keyed state. Everything expires, everything can throttle, and hot single-partition structures must be sharded.

## Sorted map: live global leaderboard
```luau
local MemoryStoreService = game:GetService("MemoryStoreService")
local board = MemoryStoreService:GetSortedMap("WeeklyKills")

-- add score atomically (sortKey orders entries; value can be a table)
board:UpdateAsync(tostring(userId), function(old)
	local kills = (old and old.kills or 0) + 1
	return { kills = kills, name = playerName }, kills      -- value, sortKey
end, 7 * 24 * 3600)                                         -- expiration (seconds)

local top = board:GetRangeAsync(Enum.SortDirection.Descending, 10)  -- costs ~10 units
```

## Queue: matchmaking tickets (at-least-once processing)
```luau
local queue = MemoryStoreService:GetQueue("Ranked_EU", 30)        -- 30 s invisibility timeout
queue:AddAsync({ userId = id, mmr = mmr, t = os.time() }, 300)    -- item, expiration
-- matchmaker server:
local items, readId = queue:ReadAsync(10, false, 5)               -- count, allOrNothing, waitTimeout
if items and #items >= 2 then
	-- build matches; reserve a server via TeleportService; then acknowledge:
	queue:RemoveAsync(readId)
end
-- if we crash before RemoveAsync, items reappear after the invisibility timeout (retry-safe)
```
Process items **idempotently**, because a ticket can be read twice after a timeout ([[ProcessReceipt_Idempotency]] uses the same mindset).

## Hash map: scalable keyed state
`GetHashMap("Parties")`: `SetAsync`, `GetAsync`, `UpdateAsync`, `RemoveAsync`, `ListItemsAsync`. Items spread across partitions. Per-key limits are about 5k writes and 15k reads per minute.

## Sharding
Single-partition structures (sorted maps, queues) throttle at about 30k units/min. Split by region, mode or hash: `Ranked_EU_1..4`. Aggregate reads (top-N from each shard, then merge) ([[MemoryStoreService]]).

## Related
[[MemoryStoreService]] · [[Matchmaking_Customization]] · [[TeleportService_and_Reserved_Servers]] · [[Ordered_DataStores_and_Leaderboards]] · [[MessagingService_Cross_Server]] · [[UpdateAsync_Patterns]] · [[ProcessReceipt_Idempotency]] · [[Spatial_Partitioning]] · [[MOC_Game_Systems_and_Algorithms]]

## Sources
- https://create.roblox.com/docs/cloud-services/memory-stores/sorted-map · https://create.roblox.com/docs/cloud-services/memory-stores/queue
- https://create.roblox.com/docs/cloud-services/memory-stores/hash-map
