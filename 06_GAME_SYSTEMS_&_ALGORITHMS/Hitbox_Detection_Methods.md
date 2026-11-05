---
aliases: [Hitboxes, Melee hitbox, Hit detection, Hitbox methods, Spatial query hitbox]
tags:
  - roblox-dev
  - systems/combat
type: concept
last_updated: 2026-11-05
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
	params.ExcludeInstances = { attacker }
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

## Avatar Settings can change what your queries hit (as of Nov 5, 2026)
In Studio ▸ **Avatar Settings ▸ Movement ▸ Collision ▸ Single Collider** (or the **Consistent Gameplay** preset), a "hit & touch detection" option decides which parts are visible to `Touched` and spatial queries (raycasts, shapecasts, `GetPartBoundsInBox`, `GetPartsInPart`):

| Mode (`Enum.AvatarSettingsHitAndTouchDetectionMode`) | `CanTouch` + `CanQuery` on | Consequence for combat |
| --- | --- | --- |
| `UseParts` (default) | Body parts | Classic behavior. Per-limb hits and headshots work |
| `UseCollider` | The single collision box only | Every avatar is the same box. **Body parts are invisible to queries** |
| `UseHitbox` (added to the API docs Nov 3, 2026) | A separate non-colliding, massless box sized by `HitboxSize` | The hit target is separate from the movement collider. It hangs from the top of the body, reaches the floor, and is removed on death |

- **Why you'd want it:** every player gets the same hittable volume whatever avatar they wear, so tiny or thin avatars stop being an advantage, and you control the size. That's fairer than per-limb boxes for battlegrounds.
- **What breaks under `UseCollider`/`UseHitbox`:** headshot or limb multipliers keyed on `result.Instance.Name == "Head"`, `Touched` on limbs, per-limb raycast modules ([[Raycast_Hitbox_Module]] against body parts), and ragdoll or limb-targeted VFX that find the hit limb through a query. Resolve the **model** first (`FindFirstAncestorOfClass("Model")` + a Humanoid check, as the loop above does), then derive any zone from hit position relative to the root instead of the part name.
- **Unverified:** where the hitbox part is parented (the docs don't say). If it isn't a descendant of the character model, the ancestor lookup fails. Inspect a live character in Studio before switching.
- **Server validation and lag compensation** must use the **same** target volume the client aimed at. Rewind the hitbox or collider size, not the limbs, when the mode isn't `UseParts` ([[Hit_Validation]], [[Lag_Compensation]]).
- It's configured in the Avatar Settings window. There's no documented scripting API (no `AvatarCollisionRules` class page as of Nov 5, 2026). The Studio guide still lists only "parts or colliders", and a duplicate enum `AvatarSettingsTouchAndQueryDetectionMode` with the same values appeared the same week, which looks like a rename in progress.

## Tuning for feel
- Hitboxes a bit **larger than the visual** feel fair to the attacker. Match the server tolerance to the same generosity.
- Debug-draw hitboxes (a transparent part, client-only) while tuning. Strip it in production.
- Put hitbox size and offset per attack in data, not code ([[Combat_System_Architecture]]).

## Related
[[Spatial_Queries_Overlap]] · [[Shapecasting]] · [[Raycasting]] · [[Raycast_Hitbox_Module]] · [[Hit_Validation]] · [[Combat_System_Architecture]] · [[Animation_Events_and_Markers]] · [[Lag_Compensation]] · [[Collision_Groups_and_Filtering]] · [[Humanoid_and_Character_Model]] · [[MOC_Combat_Systems]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/WorldRoot · https://create.roblox.com/docs/workspace/raycasting
- https://create.roblox.com/docs/studio/avatar-settings · https://create.roblox.com/docs/reference/engine/enums/AvatarSettingsHitAndTouchDetectionMode (Creator Docs repo @ 2026-11-05)
