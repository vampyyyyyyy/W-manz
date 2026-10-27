---
aliases: [ECS, Entity Component System, Data-oriented design, Components and systems]
tags:
  - roblox-dev
  - systems/architecture
type: architecture
last_updated: 2026-10-27
status: complete
---
# Entity Component System (ECS) Pattern

> **TL;DR:** **Entities** are ids, **components** are plain data attached to ids (`Health`, `Velocity`, `Burning`), and **systems** are functions that run each tick over every entity with a given component set. It's data-oriented: cache-friendly, easy to parallelize, and it replaces deep OOP hierarchies. On Roblox, mature ECS libraries ([[ECS_Libraries_Jecs_and_Matter]]) handle storage and queries. You map entities to Instances when they need to render.

## Shape of the code
```luau
-- conceptual (library APIs differ; see ECS_Libraries_Jecs_and_Matter)
local world = ECS.World.new()
local Position, Velocity, Health, Burning = ECS.component(), ECS.component(), ECS.component(), ECS.component()

local e = world:entity()
world:set(e, Position, vector.create(0, 5, 0))
world:set(e, Velocity, vector.create(0, 0, -10))
world:set(e, Health, 100)
world:set(e, Burning, { dps = 5, untilT = 10 })

-- system: movement
for id, pos, vel in world:query(Position, Velocity) do
	world:set(id, Position, pos + vel * dt)
end
-- system: burning damage
for id, hp, burn in world:query(Health, Burning) do
	world:set(id, Health, hp - burn.dps * dt)
end
```

## When ECS shines on Roblox
- **Thousands** of similar things: projectiles, NPC crowds, resource nodes, status-effected entities ([[Projectile_Systems]], [[Status_Effects]]).
- Systems that compose: anything with `Burning` + `Wet` → extinguish, without class gymnastics ([[Wetness_Puddles_and_Drying]]).
- Replication by component diffs (send changed components only) ([[Packet_Compression]]).
- Parallel processing of independent systems ([[Parallel_Luau]]).

## When it doesn't
Small games, UI-heavy games, or teams new to it, where plain modules + [[CollectionService_Tags]] + [[Attributes]] is simpler. Tags + attributes are a lightweight "ECS on Instances".

## Related
[[ECS_Libraries_Jecs_and_Matter]] · [[CollectionService_Tags]] · [[Attributes]] · [[OOP_Class_Patterns]] · [[Spatial_Partitioning]] · [[Parallel_Luau]] · [[Status_Effects]] · [[Projectile_Systems]] · [[Single_Script_Architecture]] · [[MOC_Game_Systems_and_Algorithms]]

## Sources
- https://github.com/Ukendio/jecs · https://github.com/matter-ecs/matter
