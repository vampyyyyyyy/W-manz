---
aliases: [Spatial hash, Grid partitioning, Octree, Broadphase, Neighbor queries]
tags:
  - roblox-dev
  - systems/algorithms
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Spatial Partitioning

> **TL;DR:** When you need "who is near X?" for **many** entities every tick (AI perception, flocking, AoE auras, interest management for custom replication), don't loop all pairs (O(n²)). Bucket entities into a **uniform grid / spatial hash** (O(1) insert, query just the neighboring cells) or an octree for very uneven distributions. For physical parts, Roblox's own spatial queries already use engine acceleration structures ([[Spatial_Queries_Overlap]]).

## Spatial hash (2D on XZ)
```luau
--!strict
--!native
local CELL = 32
local grid: { [number]: { any } } = {}

local function key(x: number, z: number): number
	-- pack two signed cell coords into one number key (fits well within 2^53)
	return (x // CELL + 32768) * 65536 + (z // CELL + 32768)
end

local function insert(e: any, pos: vector)
	local k = key(pos.x, pos.z)
	local bucket = grid[k]
	if not bucket then bucket = {}; grid[k] = bucket end
	table.insert(bucket, e)
end

local function queryRadius(pos: vector, r: number, out: { any })
	local minX, maxX = (pos.x - r) // CELL, (pos.x + r) // CELL
	local minZ, maxZ = (pos.z - r) // CELL, (pos.z + r) // CELL
	for cx = minX, maxX do
		for cz = minZ, maxZ do
			local bucket = grid[(cx + 32768) * 65536 + (cz + 32768)]
			if bucket then
				for _, e in bucket do
					if vector.magnitude(e.pos - pos) <= r then table.insert(out, e) end
				end
			end
		end
	end
end
-- rebuild each tick: table.clear(grid) then insert all (cheap for thousands), or update on cell change
```

## Uses
- AI sensing and flocking neighbors ([[Steering_and_Flocking]], [[NPC_Behavior_Trees]]).
- **Interest management:** which players should receive which entity updates in custom replication ([[Packet_Compression]]).
- Status auras and proximity triggers without `Touched` ([[Client_Triggered_Instance_Security]]).
- Chunk loading for procedural worlds ([[Procedural_Generation]]).

## Choosing cell size
About 1–2× the typical query radius. Too small means many cells per query. Too large means many entities per cell.

## Related
[[Spatial_Queries_Overlap]] · [[Steering_and_Flocking]] · [[NPC_Behavior_Trees]] · [[Entity_Component_System_Pattern]] · [[Procedural_Generation]] · [[Native_Code_Generation]] · [[Vector_Library]] · [[Packet_Compression]] · [[MOC_Game_Systems_and_Algorithms]]

## Sources
- Classic broadphase technique; engine queries per https://create.roblox.com/docs/reference/engine/classes/WorldRoot
