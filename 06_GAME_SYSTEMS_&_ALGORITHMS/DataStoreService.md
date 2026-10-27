---
aliases: [DataStore, DataStores, GetAsync, SetAsync, Player data saving]
tags:
  - roblox-dev
  - systems/persistence
type: api
last_updated: 2026-10-27
status: complete
---
# DataStoreService

> **TL;DR:** DataStores are Roblox's persistent key-value storage. Values are JSON-serialized, up to **4 MB per key**, with versioning (30-day history) and metadata. The proven architecture: **load once per session → keep data in memory → save periodically, on leave and on shutdown → session-lock the key**. Always go through `UpdateAsync` for anything that can race. Most teams use a library ([[ProfileStore]], [[Lapis]]) rather than raw calls.

## Core API
| Method | Use |
| --- | --- |
| `DataStoreService:GetDataStore(name, scope?)` | Get a store handle (create few stores, reuse them) |
| `GetAsync(key, options?)` | Read (cached locally **4 s**; `DataStoreGetOptions.UseCache = false` to bypass) |
| `SetAsync(key, value, userIds?, options?)` | Blind overwrite. Only for new keys or values independent of the old one |
| `UpdateAsync(key, fn)` | Read-modify-write against the **latest** value. Counts against **read and write** budgets |
| `IncrementAsync(key, delta)` | Atomic numeric add |
| `RemoveAsync(key)` | Delete (the version is kept for 30 days) |
| `GetVersionAsync`, `ListVersionsAsync`, `GetVersionAtTimeAsync` | Rollbacks, support tickets, "restore yesterday's save" |
| `ListKeysAsync`, `ListDataStoresAsync` | Admin tooling |
| `GlobalDataStore:BatchGetAsync` | Batched reads (ordered stores per the limits table) |
| `SetRateLimitForRequestType`, `GetRequestBudgetForRequestType` | Per-server control of your shared budget |

## Supported values
nil, booleans, finite numbers (**no inf/NaN**), strings (valid UTF-8), tables of supported types (numeric keys become strings if `#t == 0`), and **buffers**. Instances, functions and metatables aren't supported. Preview the stored form with `HttpService:JSONEncode` ([[Custom_Serialization]]).

## Architecture rules (official best practices)
1. **Few data stores, one or few keys per player** with static key patterns (`"player_" .. userId`).
2. **Buffer in memory.** Mutate the in-memory copy and save on an interval (with jitter), on `PlayerRemoving`, in `BindToClose`, and at critical moments like purchases.
3. **Retry transient failures** with exponential backoff ([[Error_Handling_pcall_xpcall]]).
4. **Prefer `UpdateAsync`** when a write depends on the current value or multiple servers may write ([[UpdateAsync_Patterns]]).
5. **Session lock** player keys ([[Session_Locking]]).
6. **Shard hot keys** read by every server (e.g. `Weather_1..3`), with random initial delays and jittered polling.
7. **Lifecycle:** delete test data, handle right-to-be-forgotten requests ([[Right_to_Erasure_GDPR]]).

## Studio
Enable *Studio Access to API Services* in Experience Settings to test against real stores. Use a separate place or universe for testing so you don't corrupt live data ([[Studio_Testing_Modes]]).

## Related
[[DataStore_Limits_and_Error_Codes]] · [[UpdateAsync_Patterns]] · [[Session_Locking]] · [[Data_Versioning_and_Schema_Migration]] · [[ProfileStore]] · [[DataStore_Libraries_Comparison]] · [[Ordered_DataStores_and_Leaderboards]] · [[ProcessReceipt_Idempotency]] · [[Data_Duplication_and_Trade_Exploits]] · [[MemoryStoreService]] · [[MOC_Game_Systems_and_Algorithms]]

## Sources
- https://create.roblox.com/docs/cloud-services/data-stores · https://create.roblox.com/docs/cloud-services/data-stores/best-practices
- https://create.roblox.com/docs/cloud-services/data-stores/versioning-listing-and-caching
