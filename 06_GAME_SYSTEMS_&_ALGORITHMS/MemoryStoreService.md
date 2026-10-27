---
aliases: [MemoryStore, MemoryStores, Cross-server memory, Ephemeral storage]
tags:
  - roblox-dev
  - systems/cross-server
type: api
last_updated: 2026-10-27
status: complete
---
# MemoryStoreService

> **TL;DR:** MemoryStores are **fast, ephemeral, cross-server** data structures: sorted maps, queues and hash maps, where every item has a TTL. Use them for matchmaking queues, global leaderboards that update in real time, server lists, cross-server locks and rate limits, and live event state. They're **not** for permanent data. Quotas scale with players: memory **64 KB + 1.2 KB × users**, requests **1000 + 120 × CCU units/min** (game-level).

## Quotas and limits (Oct 2026)
| Limit | Value |
| --- | --- |
| Memory size quota | 64 KB + 1.2 KB × users (drops only after an **8-day** look-back) |
| Request units | 1000 + 120 × concurrent users per minute (game-wide) |
| Range reads | Cost = items returned (min 1). Queue reads add 1 unit per 2 s waiting |
| Per sorted map or queue | 1,000,000 items, 100 MB total |
| Per partition | Throttling starts around **30,000 units/min**. Sorted maps and queues live on **one** partition |
| Hash map per item key | ~5,000 write / 15,000 read units per minute |
| Errors | `PartitionRequestsOverLimit` (shard it), quota errors when memory is full (writes that grow memory fail) |
Observe usage in the MemoryStore **observability** dashboard.

## When to use what
| Need | Structure |
| --- | --- |
| Ranked data, scans by score or key | **Sorted map** |
| Work items, matchmaking tickets | **Queue** (with invisibility timeout + `RemoveAsync` on success) |
| Large keyed state spread across many keys | **Hash map** (spreads across partitions, scales best) |
| Persistent data | **DataStore**, not MemoryStore ([[DataStoreService]]) |

## Design rules
- Always set a sensible **expiration**. Expired items free quota automatically.
- **Shard hot structures** (e.g. `Queue_1..8`) because sorted maps and queues are single-partition ([[MemoryStore_Data_Structures]]).
- Treat every call as fallible: `pcall`, backoff, and degrade gracefully ([[Error_Handling_pcall_xpcall]]).
- Use `UpdateAsync` on sorted maps and hash maps for atomic changes (same transform rules as DataStores) ([[UpdateAsync_Patterns]]).

## Related
[[MemoryStore_Data_Structures]] · [[MessagingService_Cross_Server]] · [[Matchmaking_Customization]] · [[TeleportService_and_Reserved_Servers]] · [[Ordered_DataStores_and_Leaderboards]] · [[DataStoreService]] · [[UpdateAsync_Patterns]] · [[Error_Handling_pcall_xpcall]] · [[MOC_Game_Systems_and_Algorithms]]

## Sources
- https://create.roblox.com/docs/cloud-services/memory-stores · https://create.roblox.com/docs/cloud-services/memory-stores/per-partition-limits
- https://create.roblox.com/docs/cloud-services/data-stores-vs-memory-stores
