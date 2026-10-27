---
aliases: [Collision groups, PhysicsService, CollisionGroup, CanCollide filtering]
tags:
  - roblox-dev
  - engine/physics
type: api
last_updated: 2026-10-27
status: complete
---
# Collision Groups & Filtering

> **TL;DR:** Collision groups decide which sets of parts physically collide. Register groups with `PhysicsService:RegisterCollisionGroup`, set pairs with `CollisionGroupSetCollidable`, and assign `BasePart.CollisionGroup = "Name"`. The same group names drive **raycast and overlap filtering** (`RaycastParams.CollisionGroup`), so one setup serves physics and queries.

## Setup (server, once)
```luau
local PhysicsService = game:GetService("PhysicsService")
for _, g in { "Players", "Projectiles", "Debris", "Hitboxes" } do
	PhysicsService:RegisterCollisionGroup(g)
end
PhysicsService:CollisionGroupSetCollidable("Players", "Players", false)       -- no player blocking
PhysicsService:CollisionGroupSetCollidable("Projectiles", "Projectiles", false)
PhysicsService:CollisionGroupSetCollidable("Debris", "Players", false)        -- debris never trips players
PhysicsService:CollisionGroupSetCollidable("Hitboxes", "Default", false)      -- query-only parts

local function setGroup(model: Instance, group: string)
	for _, d in model:GetDescendants() do
		if d:IsA("BasePart") then d.CollisionGroup = group end
	end
end
```
Groups can be predefined in Studio (Collision Groups editor), and there's a limit on the number of groups (check the `PhysicsService` reference for the current value).

## Filtering beyond physics
- `RaycastParams.CollisionGroup = "Projectiles"` makes a ray respect that group's collidability ([[Raycasting]]).
- `CanQuery = false` removes a part from raycasts and overlaps entirely. Use it for VFX and decor ([[Spatial_Queries_Overlap]]).
- `CanTouch = false` removes `Touched` events (cheaper physics).
- `NoCollisionConstraint` disables collision for one specific pair ([[Mechanical_Constraints]]).

## Patterns
- **Ghost teammates:** a group per team, with teammate collisions disabled.
- **Ragdoll self-collision:** disable collisions within the ragdoll group, or use NoCollisionConstraints between neighbors ([[Knockback_and_Ragdoll]]).
- **Hitbox parts** used only for overlap queries: `CanCollide = false`, `CanTouch = false`, `CanQuery = true`, and their own group.

## Related
[[Physics_Engine_and_Assemblies]] · [[Raycasting]] · [[Shapecasting]] · [[Spatial_Queries_Overlap]] · [[Mechanical_Constraints]] · [[Hitbox_Detection_Methods]] · [[Knockback_and_Ragdoll]] · [[Physics_Optimization]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/workspace/collisions · https://create.roblox.com/docs/reference/engine/classes/PhysicsService
