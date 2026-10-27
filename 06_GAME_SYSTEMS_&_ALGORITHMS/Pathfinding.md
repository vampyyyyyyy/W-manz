---
aliases: [PathfindingService, NPC pathfinding, ComputeAsync, PathfindingModifier, PathfindingLink, Navigation mesh]
tags:
  - roblox-dev
  - systems/ai
type: api
last_updated: 2026-10-27
status: complete
---
# Pathfinding (PathfindingService)

> **TL;DR:** `PathfindingService:CreatePath(agentParams)` → `path:ComputeAsync(start, goal)` → follow `path:GetWaypoints()`, and handle `path.Blocked`. Navigation adapts to agent size (`AgentRadius`, `AgentHeight`), jumping and climbing, and **material/region costs** (`Costs` + `PathfindingModifier` labels). **`PathfindingLink`** connects gaps (ladders, teleporters, boats). Recompute sparingly and stagger NPCs, because pathfinding is server CPU.

## Usage
```luau
--!strict
local PathfindingService = game:GetService("PathfindingService")
local path = PathfindingService:CreatePath({
	AgentRadius = 2,
	AgentHeight = 5,
	AgentCanJump = true,
	AgentCanClimb = false,
	WaypointSpacing = 4,
	Costs = { Water = 20, Lava = math.huge, DangerZone = 10 },  -- materials or PathfindingModifier labels
})

local function moveTo(humanoid: Humanoid, root: BasePart, goal: Vector3): boolean
	local ok = pcall(path.ComputeAsync, path, root.Position, goal)
	if not ok or path.Status ~= Enum.PathStatus.Success then return false end
	for _, wp in path:GetWaypoints() do
		if wp.Action == Enum.PathWaypointAction.Jump then humanoid.Jump = true end
		humanoid:MoveTo(wp.Position)
		local reached = humanoid.MoveToFinished:Wait()   -- MoveTo times out after ~8 s per call
		if not reached then return false end              -- stuck: recompute or give up
	end
	return true
end
```
- `path.Blocked:Connect(function(blockedIndex) ... end)` fires when an obstacle appears on the path **ahead**, so recompute from the current position.
- `PathfindingModifier` (in a part or region) with a `Label` + `PassThrough` lets you mark doors as passable or areas as costly.
- `PathfindingLink` with two attachments and a `Label` creates custom traversal. Handle the label's waypoint in your follower (e.g. play a climb animation, teleport).

## Scaling to many NPCs
- **Stagger:** each NPC recomputes at most every 0.5–2 s, offset randomly, and only when the target moved more than a threshold ([[Time_Slicing_and_Frame_Budget]]).
- **Direct chase** when there's line of sight and no obstacles (raycast), and use pathfinding only otherwise ([[Raycasting]]).
- **Shared paths / flow fields** for hordes to one target, with [[Steering_and_Flocking]] for local avoidance.
- Run decision logic in [[Parallel_Luau]] Actors, with movement commands applied in serial.

## Related
[[NPC_Behavior_Trees]] · [[Steering_and_Flocking]] · [[Humanoid_and_Character_Model]] · [[Time_Slicing_and_Frame_Budget]] · [[Raycasting]] · [[Parallel_Luau]] · [[Spatial_Partitioning]] · [[Physics_Optimization]] · [[MOC_Game_Systems_and_Algorithms]]

## Sources
- https://create.roblox.com/docs/characters/pathfinding · https://create.roblox.com/docs/reference/engine/classes/PathfindingService
