---
aliases: [Developer Console, F9 console, Dev console, Server Stats, Log]
tags:
  - roblox-dev
  - performance/profiling
type: api
last_updated: 2026-10-27
status: complete
---
# Developer Console

> **TL;DR:** Press **F9** (or type `/console` in chat) in any live server you have permission in. It has tabs for **Log** (client and server output), **Memory**, **Network**, **Scripts**, **Server Stats** (incl. average data ping), **MicroProfiler** (server captures), **LuauHeap**, and more. It's your window into production behavior, where Studio can't reproduce real load.

## Tabs that matter
| Tab | Use |
| --- | --- |
| **Log** | Client vs server output. Errors with stack traces from live servers |
| **Memory** | Real-time categories (CoreMemory, PlaceMemory, PlaceScriptMemory, UntrackedMemory…) ([[Memory_Categories]]) |
| **LuauHeap** | Heap snapshots: graph, object tags, memory categories, classes, unparented instances ([[Luau_Heap_Analysis]]) |
| **Network** | Data in/out per category ([[Network_Bandwidth_Budget]]) |
| **Scripts** | Per-script activity/rate |
| **Server Stats** | Server FPS, physics, average **data ping** of all players |
| **MicroProfiler** | Capture server frame profiles from production ([[MicroProfiler]]) |
| **Action Bindings / Server Jobs** etc. | Input bindings and engine job timing |
Also useful: **Shift+F3** (network debug stats incl. per-client data ping), **Shift+F5** (render/perf stats), and **Ctrl+F6** (MicroProfiler).

## Production debugging workflow
1. Join a live server when the issue happens (or use a test universe with real players).
2. Check **Server Stats** + **Memory** for growth. Snapshot LuauHeap twice, a few minutes apart, and compare.
3. Capture a server MicroProfiler dump during a spike.
4. Correlate with your own logged events ([[AnalyticsService_Events]]).

## Related
[[Memory_Categories]] · [[Luau_Heap_Analysis]] · [[MicroProfiler]] · [[Network_Bandwidth_Budget]] · [[Memory_Leaks]] · [[Performance_Optimization_Workflow]] · [[Studio_Debugger]] · [[Scene_Analysis_Tool]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://create.roblox.com/docs/studio/developer-console · https://create.roblox.com/docs/studio/optimization/memory-usage
