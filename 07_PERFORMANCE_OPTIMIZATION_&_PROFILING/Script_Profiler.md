---
aliases: [Script Profiler, Luau profiler, Function profiling, <native> annotation]
tags:
  - roblox-dev
  - performance/profiling
type: api
last_updated: 2026-10-27
status: complete
---
# Script Profiler

> **TL;DR:** Studio's **Script Profiler** samples Luau execution and shows **which functions** consume CPU time (call tree + flat list, client or server). Use it once the [[MicroProfiler]] tells you scripts are the problem. Natively compiled functions show **`<native>`**, which is how you confirm `@native` is working ([[Native_Code_Generation]]).

## Workflow
1. Studio ▸ View/Window ▸ **Script Profiler** (Client or Server context).
2. Start recording, reproduce the heavy scenario for 10–30 s, then stop.
3. Sort by total and self time. Expand the call tree to find the hot path.
4. Fix it, then re-record under the same conditions ([[Benchmarking_Methodology]]).

## Reading results
- **Self time** high = the function's own work (loops, math, allocations).
- **Total time** high but self low = it's calling something expensive. Follow the children.
- Functions marked `<native>` run as machine code. If one you marked `@native` isn't marked, look for deopts: `getfenv`, mismatched argument types, breakpoints ([[Luau_Attributes]]).
- Many small anonymous functions from connections = event spam. Consider batching or throttling ([[Signals_and_Connections]]).

## Complements
- [[MicroProfiler]]: frame timeline across engine systems.
- `luau --profile` for pure-Luau algorithms outside Studio ([[Luau_CLI_Tools]]).
- [[Luau_Heap_Analysis]] when the cost is allocation and GC rather than computation.

## Related
[[MicroProfiler]] · [[Native_Code_Generation]] · [[Luau_Attributes]] · [[Luau_Micro_Optimizations]] · [[Benchmarking_Methodology]] · [[Luau_Heap_Analysis]] · [[Luau_CLI_Tools]] · [[Performance_Optimization_Workflow]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://create.roblox.com/docs/studio/optimization/scriptprofiler · https://create.roblox.com/docs/luau/native-code-gen#script-profiler
