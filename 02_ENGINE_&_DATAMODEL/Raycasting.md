---
aliases: [workspace:Raycast, RaycastParams, RaycastResult, Ray casting]
tags:
  - roblox-dev
  - engine/spatial-queries
type: api
last_updated: 2026-10-27
status: complete
---
# Raycasting

> **TL;DR:** `workspace:Raycast(origin, direction, params)` returns the first hit along a line as a `RaycastResult` (`Instance`, `Position`, `Normal`, `Material`, `Distance`) or `nil`. The ray's **length is the magnitude of `direction`** (max **15,000 studs**). It's the workhorse for hit detection, ground checks, line of sight, grapple anchors and rain occlusion.

## Usage
```luau
--!strict
local params = RaycastParams.new()
params.FilterType = Enum.RaycastFilterType.Exclude      -- or Include (whitelist)
params.FilterDescendantsInstances = { character, workspace.Effects }
params.IgnoreWater = true
-- params.CollisionGroup = "Projectiles"                -- respect collision group rules
-- params.RespectCanCollide = true                      -- skip CanCollide=false parts

local origin = camera.CFrame.Position
local result = workspace:Raycast(origin, camera.CFrame.LookVector * 300, params)
if result then
	print(result.Instance:GetFullName(), result.Position, result.Normal, result.Material, result.Distance)
end
```
- **Reuse `RaycastParams`** objects. Creating them per cast allocates. Update `FilterDescendantsInstances` only when the set changes (it copies the array on assignment). `params:AddToFilter(inst)` appends.
- Parts with `CanQuery = false` are invisible to rays.
- Terrain hits return `Instance = workspace.Terrain` plus the voxel `Material`, which is great for footstep sounds and wetness ([[Wetness_Puddles_and_Drying]]).

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
- https://create.roblox.com/docs/workspace/raycasting · https://create.roblox.com/docs/reference/engine/datatypes/RaycastParams
