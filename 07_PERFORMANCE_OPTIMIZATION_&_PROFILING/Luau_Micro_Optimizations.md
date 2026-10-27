---
aliases: [Micro optimizations, Luau performance tips, Fast Luau, Hot loop optimization]
tags:
  - roblox-dev
  - performance/luau
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Luau Micro-Optimizations (what actually matters in 2026)

> **TL;DR:** Most "Lua speed tricks" are **obsolete in Luau** (localizing globals, caching methods). What still matters in hot paths: **avoid allocations** (tables, closures, strings) per iteration, **preallocate** (`table.create`), use **direct builtin calls** (fastcalls), keep **table shapes consistent**, use `vector`/buffer types, annotate types for native codegen, and above all **fix the algorithm**. Measure everything ([[Benchmarking_Methodology]]).

## Still worth it ✅
| Do | Why |
| --- | --- |
| Hoist closures out of loops (`table.sort` comparators, callbacks) | Avoid per-iteration allocation ([[Closures_and_Upvalues]]) |
| `table.create(n)` + indexed writes | Preallocated array part ([[Table_Library]]) |
| Build records in **one literal** | Table templates ([[Luau_Compiler_Optimizations]]) |
| `table.concat` instead of `..` in loops | O(n) vs O(n²) ([[String_Library_and_Patterns]]) |
| Reuse scratch tables with `table.clear` | Less GC ([[Garbage_Collection]]) |
| Swap-remove for unordered arrays | O(1) vs O(n) `table.remove(t, 1)` |
| `string.byte(s, i)` over `s:byte(i)` | Fastcall vs method call ([[Builtin_Fastcalls_and_Imports]]) |
| `vector`/`Vector3` math instead of `{x, y, z}` tables | No heap allocation ([[Vector_Library]]) |
| Typed params + `@native` on proven-hot functions | Specialized machine code ([[Native_Code_Generation]]) |
| Cache `GetChildren()`/`GetDescendants()` results when iterating every frame | Each call allocates a new array |
| Avoid `getfenv`/`setfenv`/`loadstring` | They deoptimize imports, fastcalls and inlining ([[Globals_G_shared_and_getfenv]]) |

## Obsolete or myth ❌
| Myth | Reality in Luau |
| --- | --- |
| `local max = math.max` for speed | Imports resolve `math.max` at load. Tiny or no gain |
| Caching `workspace.FindFirstChild` method locally | Namecall is already optimized |
| `ipairs` is faster than `pairs` (or vice versa) | Both specialized. Generalized `for k, v in t` is recommended ([[Generalized_Iteration]]) |
| `#t` is slow | Almost always O(1) in Luau (cached length) |
| Manual inlining | O2 inlines small local functions in live games ([[Luau_Compiler_Optimizations]]) |

## The real wins are usually higher level
Event-driven instead of polling, spatial partitioning instead of O(n²) scans ([[Spatial_Partitioning]]), time-slicing ([[Time_Slicing_and_Frame_Budget]]), parallel actors ([[Parallel_Luau]]), and not replicating what you don't need ([[Network_Bandwidth_Budget]]).

## Related
[[Benchmarking_Methodology]] · [[Native_Code_Generation]] · [[Luau_Compiler_Optimizations]] · [[Builtin_Fastcalls_and_Imports]] · [[Garbage_Collection]] · [[Table_Library]] · [[Vector_Library]] · [[Spatial_Partitioning]] · [[Time_Slicing_and_Frame_Budget]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://luau.org/performance (official optimization notes)
