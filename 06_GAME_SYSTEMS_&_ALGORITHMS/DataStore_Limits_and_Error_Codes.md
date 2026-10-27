---
aliases: [DataStore limits, DataStore throttling, DataStore budget, Error 301-306, Storage limit]
tags:
  - roblox-dev
  - systems/persistence
type: api
last_updated: 2026-10-27
status: complete
---
# DataStore Limits & Error Codes (2026)

> **TL;DR:** Budgets are **experience-level and shared with Open Cloud**: reads `300 + 40×CCU`/min, writes `300 + 20×CCU`/min, lists `300 + 2×CCU`/min, removes `300 + 40×CCU`/min. Each key has throughput caps (**read 25 MB/min, write 4 MB/min**). Storage is capped at **500 MB + 1 MB per lifetime user** (compressed, latest versions only). Over-budget requests queue (30 per queue) and then fail with **301–306**.

## Data limits
| Item | Max |
| --- | --- |
| Data store name, key, scope | 50 characters each |
| Value (serialized JSON) | 4,194,304 characters per key |
| Metadata | 300 characters total (keys ≤ 50, values ≤ 250) |

## Throughput (per key, rolling 60 s, all servers)
| Type | Calls | Limit |
| --- | --- | --- |
| Read | `GetAsync`, `GetVersionAsync`, `GetVersionAtTimeAsync`, `ListVersionsAsync`, `UpdateAsync` | **25 MB/min** |
| Write | `SetAsync`, `IncrementAsync`, `UpdateAsync`, `RemoveAsync` | **4 MB/min** |
Throughput rounds **up to the next KB per request** (800 B + 1.2 KB = 3 KB counted). Many tiny writes to one key add up.

## Request budgets (per minute, experience-wide, shared with Open Cloud)
| Store | Read | Write | List | Remove |
| --- | --- | --- | --- | --- |
| Standard | 300 + CCU×40 | 300 + CCU×20 | 300 + CCU×2 | 300 + CCU×40 |
| Ordered | 300 + CCU×40 (incl. `BatchGetAsync`) | 300 + CCU×20 | 300 + CCU×2 (`GetSortedAsync`) | 300 + CCU×40 |
`UpdateAsync` consumes **both** read and write. Open Cloud scripts (admin panels, bots) can starve live servers, so rate-limit them (leaky bucket) ([[Open_Cloud_APIs]]). In-game, use `DataStoreService:SetRateLimitForRequestType()` / `GetRequestBudgetForRequestType()` to reserve headroom for critical saves.

## Storage
`500 MB + 1 MB × lifetime users`, measured on the **compressed** latest version of each key. **Don't pre-compress**, because Roblox compresses for you and pre-compression wastes CPU and can hurt the ratio. Old versions and deleted keys don't count during retention.

## Throttling and queues
Over-limit requests go to one of four queues (**Set, Ordered set, Get, Ordered get**), served in order while your call yields. Each queue holds **30** requests. Beyond that, calls fail with codes in the **301–306** range (dropped). A throttled *key* is temporarily skipped in its queue.

## Practical budget math
30 players → reads 1,500/min and writes 900/min **for the whole experience**, shared across servers. An autosave every 60 s for 30 players uses 30 `UpdateAsync` = 30 reads + 30 writes per minute. That's fine. Saving on every coin pickup isn't.

## Related
[[DataStoreService]] · [[UpdateAsync_Patterns]] · [[Session_Locking]] · [[Error_Handling_pcall_xpcall]] · [[Open_Cloud_APIs]] · [[Custom_Serialization]] · [[ProfileStore]] · [[Remote_Rate_Limiting]] · [[MOC_Game_Systems_and_Algorithms]]

## Sources
- https://create.roblox.com/docs/cloud-services/data-stores/error-codes-and-limits (Oct 2026)
