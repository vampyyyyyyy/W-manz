---
aliases: [SharedTable, Shared state, SharedTableRegistry, Cross-actor data]
tags:
  - roblox-dev
  - performance/parallel
type: api
last_updated: 2026-10-27
status: complete
---
# SharedTable

> **TL;DR:** `SharedTable` is a table-like structure that **multiple actors can read and update concurrently**, with atomic per-key updates. Sending one to another actor **doesn't copy it**: everyone sees the same data immediately. Use it for big shared world state (grid occupancy, influence maps, spatial indexes) that parallel workers consult. Use `SharedTableRegistry` to publish it under a name.

## Usage
```luau
local SharedTableRegistry = game:GetService("SharedTableRegistry")

-- serial setup (any script)
local grid = SharedTable.new()
SharedTableRegistry:SetSharedTable("NavGrid", grid)

-- inside an actor (parallel phase)
local navGrid = SharedTableRegistry:GetSharedTable("NavGrid")
navGrid["12,40"] = 1                                     -- plain writes are per-key atomic
SharedTable.increment(navGrid, "visits", 1)              -- atomic numeric increment
SharedTable.update(navGrid, "danger", function(old)      -- atomic read-modify-write
	return (old or 0) + 0.5
end)
local snapshot = SharedTable.clone(navGrid, false)       -- efficient structural-sharing clone
```

## Rules
- **Keys:** strings or non-negative integers < 2^32 only. **Values:** booleans, numbers, vectors, strings, nested `SharedTable`s, or serializable Roblox data types. No functions or plain Luau tables (build nested SharedTables instead; `SharedTable.new(t)` constructs one from a table).
- Distinct SharedTables never compare equal. `SharedTable.cloneAndFreeze` makes a read-only copy. Other helpers: `clear`, `size`, `isFrozen`.
- Iteration while others write gives a consistent per-key view but not a global snapshot. Clone first if you need a stable picture.
- Prefer **fewer, coarser** updates: atomic ops still synchronize. Writing every cell per frame across 16 actors can contend.
- Read-mostly data shared by many workers is the sweet spot.

## Related
[[Parallel_Luau]] · [[Actors_and_Messaging]] · [[Spatial_Partitioning]] · [[NPC_Behavior_Trees]] · [[Procedural_Generation]] · [[Buffer_Library]] · [[Table_Library]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://create.roblox.com/docs/scripting/multithreading#shared-table · https://create.roblox.com/docs/reference/engine/datatypes/SharedTable
