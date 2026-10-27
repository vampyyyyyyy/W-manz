---
aliases: [Memory leak, Leaks, Growing memory, Server memory leak]
tags:
  - roblox-dev
  - performance/memory
type: concept
last_updated: 2026-10-27
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

## Prevention architecture
Give every system an **owner object** with `Destroy()` that tears down its connections, instances and table entries. Destroy owners on lifecycle events (player leaves, character dies, round ends) ([[OOP_Class_Patterns]], [[Single_Script_Architecture]]).

## Related
[[Connection_Management]] · [[Luau_Heap_Analysis]] · [[Memory_Categories]] · [[Garbage_Collection]] · [[Cleanup_Libraries_Trove_Maid_Janitor]] · [[Instance_Lifecycle_and_Destroy]] · [[Player_and_Character_Lifecycle]] · [[Weak_Tables]] · [[Object_Pooling]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://create.roblox.com/docs/studio/optimization/memory-usage · https://create.roblox.com/docs/performance-optimization/improve#memory-usage
