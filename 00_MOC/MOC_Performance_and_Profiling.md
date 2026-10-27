---
aliases: [Performance MOC, Optimization hub, Profiling hub]
tags:
  - roblox-dev
  - moc/performance
type: moc
last_updated: 2026-10-27
status: complete
---
# MOC: Performance & Profiling

> **TL;DR:** Making games **fast on the weakest target device**: measure first (MicroProfiler, Script Profiler, Developer Console, memory categories, heap snapshots, Scene Analysis), then fix the real bottleneck: scripts (micro-optimizations, time slicing, Parallel Luau), memory (leaks, connections), streaming (StreamingEnabled, SLIM), rendering and physics.

*22 notes in this domain.*

## Start here
1. [[Performance_Optimization_Workflow]]: measure → hypothesize → fix → verify
2. [[MicroProfiler]]: where every millisecond of a frame goes
3. [[Memory_Leaks]]: the most common long-session killer
4. [[StreamingEnabled]]: memory and join time at scale
5. [[Parallel_Luau]]: using multiple cores safely
6. [[Mobile_and_Low_End_Optimization]]: your real audience's hardware

## Measure
- **Profilers & consoles:** [[Performance_Optimization_Workflow]] · [[MicroProfiler]] · [[Script_Profiler]] · [[Developer_Console]] · [[Scene_Analysis_Tool]] · [[Benchmarking_Methodology]]
- **Memory analysis:** [[Memory_Categories]] · [[Luau_Heap_Analysis]]

## Scripts & memory
- **CPU:** [[Luau_Micro_Optimizations]] · [[Time_Slicing_and_Frame_Budget]]
- **Memory:** [[Memory_Leaks]] · [[Connection_Management]]
- **Parallelism:** [[Parallel_Luau]] · [[Actors_and_Messaging]] · [[SharedTable]]

## Streaming, rendering & physics
- **Streaming:** [[StreamingEnabled]] · [[Model_Streaming_Modes]] · [[SLIM_and_Frustum_Streaming]]
- **Rendering & physics:** [[Draw_Calls_and_Instancing]] · [[Rendering_Optimization]] · [[Physics_Optimization]]
- **Devices:** [[Mobile_and_Low_End_Optimization]]

## Cross-domain
[[Home]] · [[Learning_Path]] · [[Native_Code_Generation]] · [[MOC_Luau_Core_and_Compiler]] · [[MOC_Engine_and_DataModel]] · [[UI_Performance]]

## Sources
- Each linked note cites its own primary sources. See [[Trusted_Sources]] for the ranking policy.
