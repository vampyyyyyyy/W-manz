---
aliases: [Procedural generation, Procgen, Seeded generation, Dungeon generation, Infinite terrain]
tags:
  - roblox-dev
  - systems/procedural
type: concept
last_updated: 2026-10-27
status: complete
---
# Procedural Generation

> **TL;DR:** Generate content from **seeded randomness + rules**: noise for terrain, grammars and graphs for dungeons, Poisson disc for scattering. On Roblox the key engineering is **determinism** (the same seed gives the same world on every machine) and **budgeting** (generate in chunks over frames, stream around the player). Send seeds, not geometry, wherever you can.

## Building blocks
| Technique | Use |
| --- | --- |
| `Random.new(seed)` per system | Reproducible streams (worldSeed ⊕ chunkX ⊕ chunkZ). Never the global `math.random` ([[Math_Library]]) |
| Noise (Perlin/fBm via `math.noise`) | Heightmaps, biomes, caves, clouds ([[Noise_Functions]]) |
| Voxel terrain `FillBlock`/`WriteVoxels` | Natural landscapes ([[Terrain_and_Materials]]) |
| Rooms + corridors / BSP / random walk | Dungeons, roguelike floors |
| Wave Function Collapse | Tile-based towns and interiors with adjacency rules |
| Poisson disc sampling | Natural spacing of trees and rocks (no clumping) |
| L-systems | Trees, vines, lightning branches ([[Lightning_Generation]]) |

## Chunked, deterministic world sketch
```luau
--!strict
const CHUNK = 64
const WORLD_SEED = 1337

local function chunkSeed(cx: number, cz: number): number
	return (WORLD_SEED * 73856093 + cx * 19349663 + cz * 83492791) % 2^31
end

local function generateChunk(cx: number, cz: number)
	local rng = Random.new(chunkSeed(cx, cz))
	for x = 0, CHUNK - 1, 4 do
		for z = 0, CHUNK - 1, 4 do
			local wx, wz = cx * CHUNK + x, cz * CHUNK + z
			local h = Noise.fbm(wx * 0.01, wz * 0.01, 5) * 40 + 20
			-- place terrain column / props using rng for scatter decisions
		end
		task.wait()                   -- budget: yield between rows (Time_Slicing_and_Frame_Budget)
	end
end
```

## Networking choices
- **Server-generated, replicated:** simplest and authoritative, but heavy on join and replication. Use StreamingEnabled ([[StreamingEnabled]]).
- **Seed-replicated, client-generated visuals** + server-generated collision/gameplay: tiny bandwidth, but both sides must match (same code version, same seeds).
- **Hybrid:** server places gameplay-relevant objects (loot, enemies). Clients decorate (grass, rocks, particles).

## Related
[[Noise_Functions]] · [[Terrain_and_Materials]] · [[Math_Library]] · [[Time_Slicing_and_Frame_Budget]] · [[StreamingEnabled]] · [[Spatial_Partitioning]] · [[EditableImage_and_EditableMesh]] · [[Lightning_Generation]] · [[Native_Code_Generation]] · [[MOC_Game_Systems_and_Algorithms]]

## Sources
- https://create.roblox.com/docs/reference/engine/datatypes/Random · https://create.roblox.com/docs/reference/engine/classes/Terrain
