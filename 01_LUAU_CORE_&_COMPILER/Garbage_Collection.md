---
aliases: [GC, Garbage collector, Incremental GC, gcinfo, collectgarbage]
tags:
  - roblox-dev
  - luau/memory
type: concept
last_updated: 2026-10-27
status: complete
---
# Garbage Collection

> **TL;DR:** Luau uses an **incremental, paced** garbage collector (mark → atomic → sweep) that interleaves small steps with your code ("GC assists"). It frees anything **unreachable**. Your job is to make sure dead objects actually become unreachable: disconnect connections, clear tables, drop references to destroyed Instances. There are no finalizers (`__gc` is unsupported).

## How it works (Luau team summary)
- **Incremental mark** traverses live objects a bit at a time, so the world never stops for a full traversal.
- **Atomic step:** a short indivisible phase. Luau shrinks it with a "remark" pass, incremental coroutine marking (inactive threads aren't rescanned), and shrinkable weak tables (`__mode` with `s`).
- **Paged sweeper:** objects of the same size sit in 16 KB pages, so sweeping is cache-friendly.
- **Pacing:** a PID controller targets heap size as a % of live data. Allocation-heavy code makes your script pay "assists" (CPU time spent helping the GC).

## What you can observe on Roblox
- `gcinfo()` / `collectgarbage("count")`: current Luau heap in KB. Only `"count"` is allowed. You **can't** force a full collection from scripts.
- Developer Console ▸ Memory ▸ `LuaHeap`, plus per-script memory categories ([[Memory_Categories]]). The Luau heap snapshot tool shows *what* is alive ([[Luau_Heap_Analysis]]).

## Why "garbage" stays alive (Roblox edition)
| Leak | Why it's reachable | Fix |
| --- | --- | --- |
| `RBXScriptConnection` never disconnected | Engine signal → your closure → upvalues | `:Disconnect()`, `Once`, or destroy the instance ([[Connection_Management]]) |
| Tables keyed by `Player`/`Instance` | Your table references them forever | Remove on `PlayerRemoving`/`Destroying` ([[Memory_Leaks]]) |
| Destroyed Instances still referenced | Lua reference keeps the object alive (in a destroyed state) | Nil out references after `Destroy()` ([[Instance_Lifecycle_and_Destroy]]) |
| Caches without bounds | Growing tables | LRU, TTL or [[Weak_Tables]] |
| Threads stuck yielding forever | Each holds its stack | Avoid infinite `WaitForChild` without timeout ([[Player_and_Character_Lifecycle]]) |

## Writing GC-friendly hot code
Avoid temporary tables, closures and strings in per-frame loops. Reuse buffers and tables (`table.clear`), use native `vector`/`Vector3` math (no GC allocation for vectors), and pool objects ([[Object_Pooling]], [[Luau_Micro_Optimizations]]).

## Related
[[Weak_Tables]] · [[Memory_Leaks]] · [[Connection_Management]] · [[Memory_Categories]] · [[Luau_Heap_Analysis]] · [[Instance_Lifecycle_and_Destroy]] · [[Object_Pooling]] · [[Luau_Micro_Optimizations]] · [[Closures_and_Upvalues]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://luau.org/performance#improved-garbage-collector-pacing · https://luau.org/performance#reduced-garbage-collector-pauses
