---
aliases: [Parallel Luau, Multithreading, task.desynchronize, ConnectParallel, Thread safety]
tags:
  - roblox-dev
  - performance/parallel
type: concept
last_updated: 2026-10-27
status: complete
---
# Parallel Luau

> **TL;DR:** Put scripts under **`Actor`** instances. Code in *different* actors can run **in parallel on multiple cores** after `task.desynchronize()` (or via `Signal:ConnectParallel`), then must `task.synchronize()` before writing to the DataModel. It's great for raycast-heavy validation, AI sensing, procedural generation and heavy math. Respect **thread safety levels**: most reads are fine and most writes aren't.

## Model
- Scripts **in the same actor** always run serially with respect to each other, so you need **many actors** (e.g. one per NPC or per player) to get parallelism.
- **Desynchronize:** `task.desynchronize()` suspends and resumes the coroutine in a parallel phase. `RBXScriptSignal:ConnectParallel(fn)` runs callbacks directly in parallel.
- **Synchronize:** `task.synchronize()` returns to the serial phase to mutate Instances.
- `require()` **isn't allowed** in parallel phases. Require modules up front in serial.

```luau
-- inside a Script under an Actor (one actor per NPC)
local RunService = game:GetService("RunService")
local Brain = require(script.Parent.Brain)         -- require in serial
RunService.Heartbeat:ConnectParallel(function(dt)
	local decision = Brain.think(dt)                 -- raycasts, math, reads: parallel-safe
	task.synchronize()
	Brain.apply(decision)                            -- Humanoid:MoveTo, property writes: serial
end)
```

## Thread safety levels (API reference tags)
| Level | Properties | Functions |
| --- | --- | --- |
| **Unsafe** (default if untagged) | No read or write in parallel | No calls |
| **Read Parallel** | Read OK, no write | — |
| **Local Safe** | Read/write within the same actor, read-only from others | Call within the same actor |
| **Safe** | Read and write | Call (e.g. `workspace:Raycast`) |

## Cross-actor communication
[[Actors_and_Messaging]] (`SendMessage`/`BindToMessageParallel`), [[SharedTable]] (shared mutable state, atomic updates), or data-model properties and attributes (limited by write safety).

## When it pays off (and when not)
- ✅ N independent units each doing meaningful work: NPC AI, per-player hit validation (Roblox's own example), chunk generation, pathing preprocessing.
- ❌ Tiny tasks (overhead dominates), or work that's mostly Instance writes (serial anyway).
- Profile with the [[MicroProfiler]] parallel lanes. Combine with [[Native_Code_Generation]] for compute.

## Related
[[Actors_and_Messaging]] · [[SharedTable]] · [[task_Library]] · [[MicroProfiler]] · [[Native_Code_Generation]] · [[NPC_Behavior_Trees]] · [[Procedural_Generation]] · [[Hit_Validation]] · [[Buffer_Library]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://create.roblox.com/docs/scripting/multithreading
