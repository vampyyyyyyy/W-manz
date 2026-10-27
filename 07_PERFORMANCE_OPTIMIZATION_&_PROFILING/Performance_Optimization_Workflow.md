---
aliases: [Optimization workflow, Performance workflow, Identify improve monitor, Frame budget]
tags:
  - roblox-dev
  - performance/workflow
type: concept
last_updated: 2026-10-27
status: complete
---
# Performance Optimization Workflow

> **TL;DR:** **Measure → isolate → fix → verify → monitor.** Don't optimize from vibes. Find whether you're bound by **script CPU, physics, rendering (GPU), memory, or network**, using the right tool for each. Fix the biggest offender, verify on **real low-end devices**, and keep watching live metrics after launch.

## Budget targets
- 60 FPS = **16.6 ms per frame** for *everything* (input, scripts, animation, physics, render). Mobile players often run at 30 FPS (33 ms), and servers run their simulation at about 60 Hz.
- Memory: low-end phones crash first. Treat client memory as the tightest budget ([[Mobile_and_Low_End_Optimization]]).

## Which tool for which symptom
| Symptom | First tool | Then |
| --- | --- | --- |
| Low FPS, stutter | [[MicroProfiler]] (Ctrl+F6) | Script vs physics vs render scopes |
| Slow Luau functions | [[Script_Profiler]] | [[Luau_Micro_Optimizations]], [[Native_Code_Generation]] |
| Memory growth / crashes | [[Developer_Console]] ▸ Memory, [[Memory_Categories]] | [[Luau_Heap_Analysis]], [[Scene_Analysis_Tool]], [[Memory_Leaks]] |
| Rubber-banding, delayed actions | Data ping vs network ping, `ProcessPackets` scope | [[Network_Bandwidth_Budget]] |
| Long join times | Load time measurement, `ReplicatedStorage`/`ReplicatedFirst` size | [[StreamingEnabled]], asset dedupe |
| Server lag with many players | Server MicroProfiler + Server Stats | [[Parallel_Luau]], [[Time_Slicing_and_Frame_Budget]], [[Physics_Optimization]] |

## The loop
1. **Reproduce** with a test plan: player count, device tier, map area. Use realistic test conditions ([[Studio_Testing_Modes]]).
2. **Measure** a baseline. Capture MicroProfiler dumps and memory snapshots.
3. **Isolate** one hypothesis at a time. Disable systems with flags to confirm the culprit.
4. **Fix** the root cause (algorithmic first: O(n²) → O(n), per-frame → event-driven), then micro-optimizations.
5. **Verify** with the same measurement, and on low-end hardware ([[Mobile_and_Low_End_Optimization]]).
6. **Monitor** live: Creator Hub performance analytics (FPS, memory, crashes) and custom telemetry ([[Analytics_Dashboard_and_Metrics]]).

## Design-time performance
Roblox's docs stress designing for performance up front: streaming-friendly worlds, client-side VFX, instance reuse, and limits on concurrent effects ([[Client_Side_VFX_Replication]], [[Object_Pooling]]).

## Related
[[MicroProfiler]] · [[Script_Profiler]] · [[Developer_Console]] · [[Memory_Categories]] · [[Scene_Analysis_Tool]] · [[Benchmarking_Methodology]] · [[Mobile_and_Low_End_Optimization]] · [[Network_Bandwidth_Budget]] · [[Time_Slicing_and_Frame_Budget]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://create.roblox.com/docs/performance-optimization (design, identify, improve, monitor, test on hardware)
