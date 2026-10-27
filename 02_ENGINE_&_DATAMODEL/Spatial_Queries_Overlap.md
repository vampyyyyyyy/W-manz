---
aliases: [GetPartBoundsInBox, GetPartBoundsInRadius, GetPartsInPart, OverlapParams, Overlap queries]
tags:
  - roblox-dev
  - engine/spatial-queries
type: api
last_updated: 2026-10-27
status: complete
---
# Spatial Queries (Overlap)

> **TL;DR:** Overlap queries return **every part** in a volume: `GetPartBoundsInBox(cframe, size, params)` and `GetPartBoundsInRadius(pos, r, params)` (fast, **bounding-box** tests), and `GetPartsInPart(part, params)` (exact geometry, slower). Configure them with `OverlapParams`. They're the backbone of AoE attacks, melee hitbox frames, pickups and "who's in this zone".

## Usage
```luau
--!strict
local params = OverlapParams.new()
params.FilterType = Enum.RaycastFilterType.Exclude
params.FilterDescendantsInstances = { attacker }
params.MaxParts = 64                 -- cap work (0 = unlimited)
-- params.CollisionGroup = "Hitboxes"; params.RespectCanCollide = false

local parts = workspace:GetPartBoundsInBox(root.CFrame * CFrame.new(0, 0, -4), Vector3.new(6, 5, 7), params)

local victims: { [Model]: Humanoid } = {}
for _, p in parts do
	local model = p:FindFirstAncestorOfClass("Model")
	local hum = model and model:FindFirstChildOfClass("Humanoid")
	if model and hum and hum.Health > 0 then victims[model] = hum end   -- dedupe by model
end
```

## Precision vs cost
| Method | Test | Cost |
| --- | --- | --- |
| `GetPartBoundsInBox` | Axis/oriented **bounding boxes** of parts vs your box | Cheap |
| `GetPartBoundsInRadius` | Bounding boxes vs sphere | Cheap |
| `GetPartsInPart` | True geometry of a part | Higher (mesh complexity matters) |
| `ArePartsTouchingOthers(parts, overlapIgnored?)` | Boolean | Cheap check |

A rotated thin part has a big bounding box, so bounding-box queries can return parts that aren't really inside. For melee, that slack is usually fine (forgiving hitboxes feel good). For precise checks, follow up with `GetPartsInPart`.

## Patterns
- **Melee hit frames:** run a box query during the active window from [[Animation_Events_and_Markers]], dedupe per swing ([[Hitbox_Detection_Methods]]).
- **AoE:** radius query, then line-of-sight [[Raycasting|raycasts]] to avoid hitting through walls.
- **Zones:** poll a few times per second instead of relying on `Touched` ([[Client_Triggered_Instance_Security]]).

## Related
[[Raycasting]] · [[Shapecasting]] · [[Hitbox_Detection_Methods]] · [[Collision_Groups_and_Filtering]] · [[Animation_Events_and_Markers]] · [[Client_Triggered_Instance_Security]] · [[Spatial_Partitioning]] · [[Damage_Pipeline]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/WorldRoot#GetPartBoundsInBox
- https://create.roblox.com/docs/reference/engine/datatypes/OverlapParams
