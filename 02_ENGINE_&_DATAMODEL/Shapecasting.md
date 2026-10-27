---
aliases: [Blockcast, Spherecast, Shapecast, Swept collision]
tags:
  - roblox-dev
  - engine/spatial-queries
type: api
last_updated: 2026-10-27
status: complete
---
# Shapecasting (`Blockcast`, `Spherecast`, `Shapecast`)

> **TL;DR:** Shapecasts **sweep a volume** along a direction and return the first hit as a `RaycastResult`: `workspace:Blockcast(cframe, size, direction, params)`, `workspace:Spherecast(position, radius, direction, params)`, `workspace:Shapecast(part, direction, params)`. Use them for thick bullets, sword swings and character sweeps where a thin ray would miss. They **ignore parts the shape starts inside**, and the max distance is **1,024 studs**.

## Example: a swept melee arc segment
```luau
--!strict
local params = RaycastParams.new()
params.FilterType = Enum.RaycastFilterType.Exclude
params.FilterDescendantsInstances = { attacker }

local function sweepBlade(prevCF: CFrame, curCF: CFrame, bladeSize: Vector3): RaycastResult?
	local delta = curCF.Position - prevCF.Position
	if delta.Magnitude < 1e-3 then return nil end
	return workspace:Blockcast(prevCF, bladeSize, delta, params)
end
```
Call it each frame between the blade's previous and current CFrame for continuous detection. Combine with an **overlap query at the start** to catch targets already inside the blade, since shapecasts skip initial intersections ([[Spatial_Queries_Overlap]]).

## When to choose what
| Query | Thickness | Returns | Best for |
| --- | --- | --- | --- |
| `Raycast` | none | first hit | Hitscan, LOS, ground checks ([[Raycasting]]) |
| `Spherecast` | sphere | first hit | Thick projectiles, camera collision, character sweeps |
| `Blockcast` | box | first hit | Blades, shields, vehicle bumpers |
| `Shapecast` | any part's shape | first hit | Custom hitbox meshes (cost scales with complexity) |
| `GetPartBoundsInBox`/`Radius`/`GetPartsInPart` | volume | **all** overlapping | AoE, multi-target hitboxes ([[Spatial_Queries_Overlap]]) |

## Gotchas
- **First hit only.** For piercing attacks, repeat from the hit point while excluding hit models, or use overlaps.
- Fast swings at low FPS can skip arcs between frames. Subdivide the sweep (e.g. 3 intermediate CFrames) when the angular delta is large ([[Hitbox_Detection_Methods]]).
- Shapecasts cost more than rays, so budget them on servers with many players ([[Time_Slicing_and_Frame_Budget]]).

## Related
[[Raycasting]] · [[Spatial_Queries_Overlap]] · [[Hitbox_Detection_Methods]] · [[Raycast_Hitbox_Module]] · [[Projectile_Systems]] · [[Collision_Groups_and_Filtering]] · [[Camera_System]] · [[Hit_Validation]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/WorldRoot#Blockcast
- https://create.roblox.com/docs/workspace/raycasting
