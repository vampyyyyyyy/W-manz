---
aliases: [Blockcast, Spherecast, Shapecast, Swept collision]
tags:
  - roblox-dev
  - engine/spatial-queries
type: api
last_updated: 2026-11-05
status: complete
---
# Shapecasting (`Blockcast`, `Spherecast`, `Shapecast`)

> **TL;DR:** Shapecasts **sweep a volume** along a direction and return the first hit as a `RaycastResult`: `workspace:Blockcast(cframe, size, direction, params)`, `workspace:Spherecast(position, radius, direction, params)`, `workspace:Shapecast(part, direction, params)`. Use them for thick bullets, sword swings and character sweeps where a thin ray would miss. They **ignore parts the shape starts inside**. The max distance is **1,024 studs** and the max shape size is **512 studs**. **Oct 2026 upgrade:** all shapecasts run on a faster, more accurate implementation with no code change, and `RaycastParams` gained **`Margin`** (inflate or round the shape) and **`SizeGradient`** (grow or shrink it along the cast).

## Example: a swept melee arc segment
```luau
--!strict
local params = RaycastParams.new()
params.ExcludeInstances = { attacker } -- see Raycasting for the new filter lists

local function sweepBlade(prevCF: CFrame, curCF: CFrame, bladeSize: Vector3): RaycastResult?
	local delta = curCF.Position - prevCF.Position
	if delta.Magnitude < 1e-3 then return nil end
	return workspace:Blockcast(prevCF, bladeSize, delta, params)
end
```
Call it each frame between the blade's previous and current CFrame for continuous detection. Combine with an **overlap query at the start** to catch targets already inside the blade, since shapecasts skip initial intersections ([[Spatial_Queries_Overlap]]).

## `Margin` and `SizeGradient` (official, Oct 2026)
| Property | Range | Effect |
| --- | --- | --- |
| `Margin` | ≥ 0 (default 0) | Expands the shape uniformly in every direction. On `Raycast` it turns the ray into a **spherecast** of that radius. The **expanded** shape counts against the 512-stud limit, so a large margin can make a valid cast throw |
| `SizeGradient` | ≥ −1 (default 0) | The shape starts at its size and ends at `size × (1 + SizeGradient)`: `0.5` ends 50% larger, `-0.5` at half size, `-1` shrinks to nothing. It scales the shape, **not** the margin, except on `Spherecast`, where radius and margin scale together |

**Widening sweep** (shotgun blast, breath attack, "fat" projectile that gets more forgiving with range). It returns the first hit only, as usual:
```luau
--!strict
local coneParams = RaycastParams.new()
coneParams.SizeGradient = 7        -- radius grows from 0.5 to 0.5 * (1 + 7) = 4 studs at the end

local function coneSweep(attacker: Model, origin: Vector3, look: Vector3, range: number): RaycastResult?
	coneParams.ExcludeInstances = { attacker } -- one shared params object: set the exclusion per call
	return workspace:Spherecast(origin, 0.5, look.Unit * range, coneParams)
end
```
For **every** target in a cone, run an overlap first (`GetPartBoundsInRadius`), then filter by angle and line of sight. Shapecasts stop at the first hit ([[Spatial_Queries_Overlap]]).

**Server-side tolerance:** hit validation can replay the client's swing as a slightly inflated cast (`Margin` = your tolerance) instead of hand-rolled distance slop ([[Hit_Validation]]).

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
- Shapecasts used to cost much more than rays. After the Oct 2026 upgrade, Roblox says a **thin spherecast costs roughly the same as a raycast**. Large or complex shapes (`Shapecast` on a detailed mesh) still cost more, so budget them on full servers ([[Time_Slicing_and_Frame_Budget]]). No published benchmark numbers yet.

## Related
[[Raycasting]] · [[Spatial_Queries_Overlap]] · [[Hitbox_Detection_Methods]] · [[Raycast_Hitbox_Module]] · [[Projectile_Systems]] · [[Collision_Groups_and_Filtering]] · [[Camera_System]] · [[Hit_Validation]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/WorldRoot#Blockcast
- https://create.roblox.com/docs/workspace/raycasting · https://create.roblox.com/docs/reference/engine/datatypes/RaycastParams (Creator Docs repo @ 2026-11-05)
- https://devforum.roblox.com/t/upgrading-shapecasts-margins-size-gradients-optimizations-and-more/4963119 (staff announcement, late Oct 2026; read via search excerpts)
