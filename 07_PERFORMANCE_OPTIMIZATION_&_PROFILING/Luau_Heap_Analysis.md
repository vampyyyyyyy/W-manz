---
aliases: [Luau heap, Heap snapshot, LuauHeap, Unparented instances]
tags:
  - roblox-dev
  - performance/memory
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Luau Heap Analysis

> **TL;DR:** Developer Console ▸ **LuauHeap** ▸ *Create Snapshot* captures everything your scripts keep alive. The **Graph** view shows the shortest path from `registry` to each object, which answers "**who** is holding this?". **Unparented Instances** / **Unique References** show Instances that are out of the DataModel but still reachable by scripts, the classic leak. Diff two snapshots over time to find growth.

## Views
| View | Answers |
| --- | --- |
| **Graph** | Aggregated reference tree from `registry`. Nodes like `Module @Path`, `name:line =Path` (functions), `upvalue`, `env`, `[key]`, `array`, `stack`, `constants`. Size (incl. contents) vs Self. Nodes < 2 KB collapse into `…` |
| **Object Tags** | Totals by Luau type: `table`, `function`, `thread`, `userdata`, `buffer`… |
| **Memory Categories** | Totals by allocation category (script name, or your `debug.setmemorycategory` tag) ([[Memory_Categories]]) |
| **Object Classes** | Which engine classes your Luau holds (`CFrame`, `Animation`, `EnumItem`…), Luau-side only |
| **Unique References / Unparented Instances** | Instances not in the DataModel, kept alive only by scripts, plus the **paths pinning them** |

## Leak hunt procedure
1. Join, play normally for 2 minutes, then take **snapshot A**.
2. Do the suspected action 20 times (respawn, open/close UI, cast an ability), then take **snapshot B**.
3. Compare **Object Tags** and **Memory Categories**. Something that grew linearly with your 20 actions is the leak.
4. In **Graph** or **Unparented Instances**, follow the path: usually `registry → function (connection callback) → upvalue → table → Instance` ([[Closures_and_Upvalues]], [[Memory_Leaks]]).
5. Fix (disconnect, clear tables, nil references) and repeat to confirm a flat line.

## Native code memory
Natively compiled functions appear as `[native]` elements ([[Native_Code_Generation]]).

## Related
[[Memory_Leaks]] · [[Memory_Categories]] · [[Developer_Console]] · [[Garbage_Collection]] · [[Connection_Management]] · [[Closures_and_Upvalues]] · [[Scene_Analysis_Tool]] · [[Weak_Tables]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://create.roblox.com/docs/studio/optimization/memory-usage#luau-heap
