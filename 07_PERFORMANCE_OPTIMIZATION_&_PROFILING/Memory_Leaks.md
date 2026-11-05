---
aliases: [Memory leak, Leaks, Growing memory, Server memory leak]
tags:
  - roblox-dev
  - performance/memory
type: concept
last_updated: 2026-11-05
status: complete
---
# Memory Leaks (Roblox edition)

> **TL;DR:** Luau has a garbage collector, so "leaks" mean **references you forgot about**: live connections, tables keyed by players or instances, destroyed-but-referenced Instances, unbounded caches, stuck threads, and VFX that never gets cleaned up. Servers that run for hours are where leaks become crashes. Find them with heap snapshots, and prevent them with ownership and cleanup patterns.

## Top leak sources & fixes
| # | Leak | Fix |
| --- | --- | --- |
| 1 | `Connect` on long-lived signals (`Heartbeat`, `PlayerAdded`, a service) never disconnected | Store and `:Disconnect()`, use `Once`, or a Trove/Maid ([[Connection_Management]], [[Cleanup_Libraries_Trove_Maid_Janitor]]) |
| 2 | `local data = {}` keyed by `Player`/`Model` never cleared | `PlayerRemoving` / `Destroying` → `data[x] = nil` |
| 3 | Instances removed with `Parent = nil` (connections kept) instead of `Destroy()` | `Destroy()` (or pool deliberately) ([[Instance_Lifecycle_and_Destroy]]) |
| 4 | Per-character objects created on each respawn without cleanup | Tie lifetime to the character (CharacterRemoving / `Destroying`) ([[Player_and_Character_Lifecycle]]) |
| 5 | Infinite `WaitForChild` / waiting threads | Timeouts. Cancel with `task.cancel` ([[task_Library]]) |
| 6 | Unbounded caches (thumbnails, paths, names) | LRU/TTL caps, or [[Weak_Tables]] for Lua-object keys |
| 7 | Animation tracks loaded per play | Load once per Animator and reuse ([[Animation_System]]) |
| 8 | VFX without Debris/cleanup | `task.delay(t, inst.Destroy, inst)` or pooling ([[Object_Pooling]]) |
| 9 | UI screens cloned per open | Toggle `Enabled`/`Visible` instead ([[UI_Performance]]) |

## Detecting
- Memory tab: **PlaceScriptMemory**/`LuaHeap` climbing steadily while player count is stable ([[Memory_Categories]]).
- **Heap snapshot diffs** ([[Luau_Heap_Analysis]]) and the **Scene Analysis** unparented-instances mode ([[Scene_Analysis_Tool]]).
- Server uptime tests: run bots or a long playtest and chart memory per hour.

## Last-resort valve: `DataModel.ServerLowMemoryWarning` (new, Nov 2026)
A server-only event that fires when Roblox detects the server is **under memory pressure**. Per the API reference, it's a *best-effort* chance to shed nonessential memory. It **can fire repeatedly** while pressure lasts, handlers must be **idempotent and cheap**, and it **doesn't guarantee** the server will or won't shut down. It's a valve, not a fix: a leak still needs finding.
```luau
--!strict
-- ServerScriptService: shed caches when the engine says memory is tight
local lastTrim = 0
game.ServerLowMemoryWarning:Connect(function()
	local now = os.clock()
	if now - lastTrim < 10 then return end       -- idempotent + throttled: it may fire many times
	lastTrim = now
	ProjectilePool.trimTo(32)                     -- your own modules: drop idle pooled VFX parts
	LeaderboardCache.clear()                      -- rebuildable data only, never player saves
	warn("[memory] low-memory warning: trimmed pools and caches")  -- log it so you can correlate in analytics
end)
```
Only drop what you can **rebuild** (pools, caches, cosmetic debris). Never touch session data or anything that a save depends on ([[Object_Pooling]], [[Session_Locking]]). If this fires in production, take a heap snapshot on a test server under the same load ([[Luau_Heap_Analysis]]).

## Prevention architecture
Give every system an **owner object** with `Destroy()` that tears down its connections, instances and table entries. Destroy owners on lifecycle events (player leaves, character dies, round ends) ([[OOP_Class_Patterns]], [[Single_Script_Architecture]]).

## Related
[[Connection_Management]] · [[Luau_Heap_Analysis]] · [[Memory_Categories]] · [[Garbage_Collection]] · [[Cleanup_Libraries_Trove_Maid_Janitor]] · [[Instance_Lifecycle_and_Destroy]] · [[Player_and_Character_Lifecycle]] · [[Weak_Tables]] · [[Object_Pooling]] · [[Session_Locking]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/DataModel#ServerLowMemoryWarning (added to the Creator Docs repo Oct 30–Nov 5, 2026)
- https://create.roblox.com/docs/studio/optimization/memory-usage · https://create.roblox.com/docs/performance-optimization/improve#memory-usage
