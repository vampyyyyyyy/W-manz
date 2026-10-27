---
aliases: [Steering behaviors, Boids, Flocking, Crowd simulation, Local avoidance]
tags:
  - roblox-dev
  - systems/ai
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Steering & Flocking

> **TL;DR:** **Steering behaviors** compute a desired velocity per agent (seek, flee, arrive, wander, separate, align, cohere) and blend them with weights. **Boids** are just separation + alignment + cohesion. Great for birds, fish, swarms and crowd avoidance on top of [[Pathfinding]]. Run the math in **native `vector`s** with spatial hashing for neighbors, and render with anchored parts or bones.

## Core behaviors
```luau
--!strict
--!native
local function seek(pos: vector, vel: vector, target: vector, maxSpeed: number): vector
	return vector.normalize(target - pos) * maxSpeed - vel
end
local function arrive(pos: vector, vel: vector, target: vector, maxSpeed: number, slowRadius: number): vector
	local offset = target - pos
	local dist = vector.magnitude(offset)
	if dist < 1e-3 then return -vel end
	local speed = maxSpeed * math.min(1, dist / slowRadius)
	return offset / dist * speed - vel
end
local function separation(pos: vector, neighbors: { vector }, radius: number): vector
	local force = vector.zero
	for _, n in neighbors do
		local d = pos - n
		local m = vector.magnitude(d)
		if m > 0 and m < radius then force += d / (m * m) end   -- stronger when closer
	end
	return force
end
-- boid step: steer = 1.5*sep + 1.0*align + 1.0*cohere + 0.5*seek(goal); vel = clampMag(vel + steer*dt, maxSpeed)
```

## Making it scale
- **Neighbor queries** via a uniform grid (spatial hash) rebuilt each tick, so per-agent work is O(k) not O(n) ([[Spatial_Partitioning]]).
- **Native codegen** for the integration loop ([[Native_Code_Generation]], [[Vector_Library]]).
- **Rendering** hundreds of agents: anchored MeshParts moved with `workspace:BulkMoveTo(parts, cframes, Enum.BulkMoveMode.FireCFrameChanged)` on clients. The server simulates coarse positions and clients interpolate ([[Client_Prediction_and_Reconciliation]]).
- Cosmetic flocks (birds, fish) can be **client-only**, so there's zero network cost ([[Client_Side_VFX_Replication]]).

## Related
[[Pathfinding]] · [[NPC_Behavior_Trees]] · [[Spatial_Partitioning]] · [[Vector_Library]] · [[Native_Code_Generation]] · [[Parallel_Luau]] · [[Procedural_Generation]] · [[Client_Side_VFX_Replication]] · [[MOC_Game_Systems_and_Algorithms]]

## Sources
- Craig Reynolds' steering behaviors (classic reference); Roblox BulkMoveTo per https://create.roblox.com/docs/reference/engine/classes/WorldRoot#BulkMoveTo
