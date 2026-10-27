---
aliases: [Hit registration, Server hit validation, Shot validation, Melee validation]
tags:
  - roblox-dev
  - security/combat
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Hit Validation

> **TL;DR:** For responsive combat, the **client detects** the hit (instant feedback) and the **server validates** it with tolerances for latency. The client sends *where it shot from* and *what it thinks it hit*. The server checks origin, target position, line of sight, fire rate, ammo, team and state, then computes damage itself.

## What the client sends
`origin: Vector3, direction: Vector3, hitInstance: Instance?, hitPosition: Vector3, shotTime: number` (optional, for [[Lag_Compensation]]). **Never** send damage, health, or "I killed X".

## Server checklist (from Roblox's weapon-targeting guidance)
1. **Origin near shooter**: `(origin - root.Position).Magnitude <= ORIGIN_TOLERANCE` (latency slack).
2. **Hit near target**: `hitPosition` is reasonably close to the hit part's *server* position, or the rewound position under [[Lag_Compensation]].
3. **No static obstruction**: raycast origin → hitPosition against **static geometry only**. Dynamic objects differ between client and server, and checking them causes false rejects ([[Raycasting]]).
4. **Rate**: shots no faster than the weapon's fire rate ([[Server_Authoritative_Cooldowns]]).
5. **Ammo** tracked on the server.
6. **Target is valid**: enemy (not teammate), alive, hittable (not in i-frames: [[Block_Parry_and_IFrames]]).
7. **Shooter state allows firing**: not reloading, stunned or sprinting ([[Combat_State_Machine]]).

```luau
--!strict
local V = require(game.ReplicatedStorage.Shared.Validate)
local ORIGIN_TOL, TARGET_TOL, MAX_RANGE = 8, 6, 500
local staticParams = RaycastParams.new()
staticParams.FilterType = Enum.RaycastFilterType.Include
staticParams.FilterDescendantsInstances = { workspace.Map } -- static level geometry only

FireRemote.OnServerEvent:Connect(function(player: Player, origin: unknown, hitPos: unknown, hitPart: unknown)
	if not (V.vector3(origin) and V.vector3(hitPos)) then return end
	local o, h = origin :: Vector3, hitPos :: Vector3
	local root = player.Character and player.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
	if not root or (o - root.Position).Magnitude > ORIGIN_TOL then return end
	if (h - o).Magnitude > MAX_RANGE then return end
	if not Weapons.canFire(player) then return end -- rate + ammo + state, server-side
	Weapons.consumeAmmo(player)

	if not V.instance(hitPart, "BasePart", workspace) then return end -- a miss still costs ammo
	local part = hitPart :: BasePart
	local victim = part:FindFirstAncestorOfClass("Model")
	local hum = victim and victim:FindFirstChildOfClass("Humanoid")
	if not hum or hum.Health <= 0 then return end
	if (part.Position - h).Magnitude > TARGET_TOL + part.Size.Magnitude / 2 then return end
	if workspace:Raycast(o, h - o, staticParams) then return end -- shot through a wall
	Damage.apply(player, hum, Weapons.damageFor(player, part)) -- server-side stats
end)
```

## Melee variant
Validate **distance** (attacker root ↔ victim root ≤ weapon reach + slack), an **angle cone** (`root.CFrame.LookVector:Dot(dirToVictim) > cos(maxAngle)`), timing against the server's swing window ([[Animation_Events_and_Markers]]), and one hit per victim per swing ([[Hitbox_Detection_Methods]]).

## Tuning
Tolerances are a fairness knob. Too tight and laggy players' real hits vanish. Too loose and aimbots get headroom. Log rejection reasons per rule ([[Server_Side_Detection_Heuristics]]) and tune from data.

## Related
[[Lag_Compensation]] · [[Hitbox_Detection_Methods]] · [[Projectile_Systems]] · [[Damage_Pipeline]] · [[Combat_System_Architecture]] · [[Raycasting]] · [[Server_Side_Validation]] · [[Server_Authoritative_Cooldowns]] · [[Block_Parry_and_IFrames]] · [[Server_Side_Detection_Heuristics]] · [[MOC_Combat_Systems]] · [[MOC_Anti_Exploit]]

## Sources
- https://create.roblox.com/docs/scripting/security/client-server-boundary#weapon-targeting
