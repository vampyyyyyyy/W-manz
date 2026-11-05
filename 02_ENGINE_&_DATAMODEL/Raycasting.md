---
aliases: [workspace:Raycast, RaycastParams, RaycastResult, Ray casting]
tags:
  - roblox-dev
  - engine/spatial-queries
type: api
last_updated: 2026-11-05
status: complete
---
# Raycasting

> **TL;DR:** `workspace:Raycast(origin, direction, params)` returns the first hit along a line as a `RaycastResult` (`Instance`, `Position`, `Normal`, `Material`, `Distance`) or `nil`. The ray's **length is the magnitude of `direction`** (max **15,000 studs**). It's the workhorse for hit detection, ground checks, line of sight, grapple anchors and rain occlusion.

## Usage
```luau
--!strict
local params = RaycastParams.new()
params.ExcludeInstances = { character, workspace.Effects } -- replaces FilterType + FilterDescendantsInstances
params.IgnoreWater = true
-- params.CollisionGroup = "Projectiles"                -- respect collision group rules
-- params.RespectCanCollide = true                      -- skip CanCollide=false parts

local origin = camera.CFrame.Position
local result = workspace:Raycast(origin, camera.CFrame.LookVector * 300, params)
if result then
	print(result.Instance:GetFullName(), result.Position, result.Normal, result.Material, result.Distance)
end
```
- **Reuse `RaycastParams`** objects. Creating them per cast allocates. Update the filter lists only when the set changes.
- Parts with `CanQuery = false` are invisible to rays.
- Terrain hits return `Instance = workspace.Terrain` plus the voxel `Material`, which is great for footstep sounds and wetness ([[Wetness_Puddles_and_Drying]]).

## Filters: `ExcludeInstances` / `IncludeInstances` (live since about Apr 2026)
`RaycastParams` and `OverlapParams` both have them. The API reference says they **supersede** `FilterType` + `FilterDescendantsInstances` (the old pair isn't deprecated and still works). Release Notes 714 described them as faster, with quicker lookups and less memory churn when lists change often.
- **Use both at once** for mixed filtering: include `workspace.Map` but exclude `workspace.Map.GlassPanes`. If the same instance is in both, **exclusion wins** (API reference). A staff reply adds that across different ancestor levels the **deepest** match decides.
- ⚠️ **`IncludeInstances = nil` includes everything. `IncludeInstances = {}` includes nothing.** A list that gets emptied at runtime (all targets died) silently turns your query into a no-op.
- Don't mix the new lists with `FilterDescendantsInstances` on the same params object. Their interaction isn't documented.

## Thick rays: `Margin` (Oct 2026)
`params.Margin = 0.25` makes `Raycast` behave as a **spherecast of that radius**. That stops hitscan slipping through seams between parts and gives "aim assist"-style forgiveness. Roblox's shapecast upgrade post says a thin spherecast now costs roughly the same as a raycast. Like any spherecast it probably ignores parts the ray starts inside (inferred, not stated for `Raycast`). See [[Shapecasting]] for `SizeGradient`.

## Common recipes
| Need | Approach |
| --- | --- |
| Ground check | Short ray down from the root: `-up * (hipHeight + 0.5)` |
| Line of sight | Ray from eye to target, Include filter = static map ([[Hit_Validation]]) |
| Wall-run / ledge detect | Rays to the sides and forward ([[Custom_Movement_Abilities]]) |
| Grapple anchor | Camera ray → hit position + normal ([[Grappling_Hook_Physics]]) |
| Is a player under a roof? | Ray up for rain occlusion ([[Rain_and_Precipitation]]) |
| Bullet with travel time | Many short segment casts per frame ([[Projectile_Systems]]) |

## Gotchas
- A ray **starting inside** a part doesn't hit that part.
- Rays are infinitely thin and can slip through cracks between parts. Use [[Shapecasting]] for volume.
- Under [[Parallel_Luau]], `workspace:Raycast` is safe to call in desynchronized code, which makes it great for batch AI sensing.

## Related
[[Shapecasting]] · [[Spatial_Queries_Overlap]] · [[Collision_Groups_and_Filtering]] · [[Hitbox_Detection_Methods]] · [[Hit_Validation]] · [[Projectile_Systems]] · [[Grappling_Hook_Physics]] · [[Rain_and_Precipitation]] · [[Parallel_Luau]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/reference/engine/datatypes/RaycastParams (ExcludeInstances, IncludeInstances, Margin, SizeGradient; Creator Docs repo @ 2026-11-05)
- https://devforum.roblox.com/t/new-spatial-query-filters/4563575 · https://devforum.roblox.com/t/upgrading-shapecasts-margins-size-gradients-optimizations-and-more/4963119 (read via search excerpts)
- https://create.roblox.com/docs/workspace/raycasting · https://create.roblox.com/docs/reference/engine/datatypes/RaycastParams
