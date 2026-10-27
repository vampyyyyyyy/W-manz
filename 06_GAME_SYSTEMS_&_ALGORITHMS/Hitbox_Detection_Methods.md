---
aliases: [Hitboxes, Melee hitbox, Hit detection, Hitbox methods, Spatial query hitbox]
tags:
  - roblox-dev
  - systems/combat
type: concept
last_updated: 2026-10-27
status: complete
---
# Hitbox Detection Methods

> **TL;DR:** Pick by attack shape. **Overlap boxes** (`GetPartBoundsInBox`) per frame during the active window are robust and forgiving, and the most common choice for melee. **Shapecasts/raycast arrays** along the weapon's path catch fast swings precisely. **`Touched`** is unreliable and exploitable, so avoid it for damage. Run detection on the **attacker's client** for instant feedback, and **validate on the server** ([[Hit_Validation]]).

## Method comparison
| Method | How | Pros | Cons |
| --- | --- | --- | --- |
| **Spatial overlap box/sphere** | `GetPartBoundsInBox(root.CFrame * offset, size, params)` each frame in the active window | Simple, forgiving, multi-target, cheap | Bounding-box imprecision, and it can miss very thin fast swings at low FPS |
| **Shapecast sweep** | `Blockcast`/`Spherecast` from last frame's pose to this frame's | Continuous (no tunneling), precise | First hit only. Skips targets already overlapping at the start ([[Shapecasting]]) |
| **Raycast points on the weapon** (RaycastHitbox style) | Attachments along the blade, rays from previous to current positions | Matches the animation exactly | Many rays. Gaps between points. Animation-dependent |
| **Magnitude/angle check** | Distance + dot-product cone to each nearby enemy | Very cheap, great for the server side | Coarse, ignores geometry |
| `Touched` | Physics contact events | Easy | Unreliable at speed, network-ownership dependent, spoofable ([[Client_Triggered_Instance_Security]]) |

## Robust melee frame loop
```luau
--!strict
local function runHitWindow(attacker: Model, attack, onHit: (Model) -> ())
	local root = attacker:FindFirstChild("HumanoidRootPart") :: BasePart
	local params = OverlapParams.new()
	params.FilterType = Enum.RaycastFilterType.Exclude
	params.FilterDescendantsInstances = { attacker }
	local hitThisSwing: { [Model]: boolean } = {}
	local t0 = os.clock()
	while os.clock() - t0 < attack.active do
		local cf = root.CFrame * CFrame.new(0, 0, -attack.range / 2)
		for _, part in workspace:GetPartBoundsInBox(cf, attack.hitbox, params) do
			local model = part:FindFirstAncestorOfClass("Model")
			local hum = model and model:FindFirstChildOfClass("Humanoid")
			if model and hum and hum.Health > 0 and not hitThisSwing[model] then
				hitThisSwing[model] = true                      -- one hit per target per swing
				onHit(model)
			end
		end
		task.wait()                                            -- every frame (Heartbeat)
	end
end
```
At low client FPS or for very fast weapons, **also sweep** between frames, or subdivide the box positions along the swing arc ([[Shapecasting]]).

## Tuning for feel
- Hitboxes a bit **larger than the visual** feel fair to the attacker. Match the server tolerance to the same generosity.
- Debug-draw hitboxes (a transparent part, client-only) while tuning. Strip it in production.
- Put hitbox size and offset per attack in data, not code ([[Combat_System_Architecture]]).

## Related
[[Spatial_Queries_Overlap]] · [[Shapecasting]] · [[Raycasting]] · [[Raycast_Hitbox_Module]] · [[Hit_Validation]] · [[Combat_System_Architecture]] · [[Animation_Events_and_Markers]] · [[Lag_Compensation]] · [[Collision_Groups_and_Filtering]] · [[MOC_Combat_Systems]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/WorldRoot · https://create.roblox.com/docs/workspace/raycasting
