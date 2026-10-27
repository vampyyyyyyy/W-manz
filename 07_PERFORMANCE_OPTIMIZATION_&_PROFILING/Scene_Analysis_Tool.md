---
aliases: [Scene Analysis, Performance Summary, Triangle composition, Instance composition]
tags:
  - roblox-dev
  - performance/profiling
type: api
last_updated: 2026-10-27
status: complete
---
# Scene Analysis Tool

> **TL;DR:** Studio ▸ **Window ▸ Performance Summary ▸ Scene Analysis** shows treemaps of what your **client and server scenes** consume during a playtest. Modes include script memory, unparented instances, instance composition, audio memory, animation memory, and triangle composition. Right-click an item to jump to it in the Explorer. It's the fastest way to find "what's heavy in this place?".

## Modes
| Mode | Finds |
| --- | --- |
| **Script memory** | Which scripts and memory categories hold the most Luau memory ([[Memory_Categories]]) |
| **Unparented instances** | Instances outside the DataModel kept alive by scripts, i.e. leaks ([[Memory_Leaks]]) |
| **Instance composition** | Which classes and models dominate instance counts |
| **Audio memory** | Heavy sounds (long uncompressed SFX, duplicates) ([[Audio_API]]) |
| **Animation memory** | Animation data, including leftover Animation Editor rigs and metadata |
| **Triangle composition** (extended breakdown) | Meshes and models driving triangle counts ([[Rendering_Optimization]]) |

## Workflow
1. Playtest the heaviest area, or after a long session.
2. Walk through each mode. Sort the list under the treemap. Search by name.
3. Jump to offenders, fix (dedupe assets, SLIM, delete leftovers, decimate meshes), and re-run.
4. Cross-check with [[Luau_Heap_Analysis]] for script memory paths and the [[Developer_Console]] in live servers.

## Related
[[Memory_Categories]] · [[Memory_Leaks]] · [[Luau_Heap_Analysis]] · [[Rendering_Optimization]] · [[Draw_Calls_and_Instancing]] · [[Developer_Console]] · [[Performance_Optimization_Workflow]] · [[Audio_API]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://create.roblox.com/docs/performance-optimization/scene-analysis
