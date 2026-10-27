---
aliases: [Jecs, Matter ECS, ECS library, Entity relationships]
tags:
  - roblox-dev
  - framework/ecs
type: framework
last_updated: 2026-10-27
status: complete
---
# ECS Libraries: Jecs & Matter

> **TL;DR:** **Jecs** (Ukendio) is the performance leader: archetype/SoA storage, **entity relationships** as first-class citizens, a type-safe Luau API, zero dependencies, and "800,000 entities at 60 FPS" per the README. It's actively developed (Oct 2026). **Matter** (matter-ecs, formerly evaera/matter) is mature and approachable, with a debugger and hot-reload-friendly loop, but it's quieter (last commit Nov 2024, v0.8.x). Choose Jecs for scale and new projects, Matter if your team already knows it.

## Jecs sketch
```luau
local jecs = require(ReplicatedStorage.Packages.jecs)
local world = jecs.World.new()

local Position = world:component() :: jecs.Entity<vector>
local Velocity = world:component() :: jecs.Entity<vector>
local Burning = world:component() :: jecs.Entity<number>   -- dps

local e = world:entity()
world:set(e, Position, vector.create(0, 0, 0))
world:set(e, Velocity, vector.create(0, 0, -10))

local function moveSystem(dt: number)
	for id, pos, vel in world:query(Position, Velocity) do
		world:set(id, Position, pos + vel * dt)
	end
end
```
Relationships (`pair(ChildOf, parent)`) model hierarchies, targets, inventories and "attached to" without bespoke tables. See `how_to/` in the repo for the design walkthrough.

## Matter sketch
A `World` plus `Loop` scheduling systems on RunService events, components created with `Matter.component("Name")`, queries with `world:query(A, B)`, and a built-in debugger panel. Install via Wally: `Matter = "matter-ecs/matter@0.8.4"`.

## Integration tips
- Bind entities to Instances (a `Renderable = Model` component). Systems update Instances in a dedicated render system on the client.
- Replication: send component diffs from server to clients (your own net layer or the library ecosystem) ([[Packet_Compression]]).
- Pair hot systems with `--!native` and [[Parallel_Luau]] where data is independent.

## Related
[[Entity_Component_System_Pattern]] · [[Native_Code_Generation]] · [[Parallel_Luau]] · [[Packet_Compression]] · [[Spatial_Partitioning]] · [[User_Defined_Type_Functions]] · [[Wally]] · [[Community_Modules_Index]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://github.com/Ukendio/jecs · https://github.com/matter-ecs/matter
