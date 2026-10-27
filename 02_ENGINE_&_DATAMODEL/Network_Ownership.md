---
aliases: [SetNetworkOwner, Physics ownership, Distributed physics, SetNetworkOwnershipAuto]
tags:
  - roblox-dev
  - engine/physics
type: api
last_updated: 2026-10-27
status: complete
---
# Network Ownership

> **TL;DR:** Roblox distributes physics: the **owner** (server or one client) simulates an unanchored assembly and replicates the results. Clients automatically get ownership of parts near their character, which makes interaction responsive but **trusts that client's physics**. Anchored parts are always server-owned. Override with `BasePart:SetNetworkOwner(player | nil)` on the server.

## Rules
- Default owner is the server, but **auto-assignment** hands unanchored parts near a player's character to that client (based on proximity and hardware).
- **Anchored** parts are always server-owned, and their ownership can't be set.
- Setting ownership on one assembly in a mechanism with no anchored parts applies to **every assembly in the mechanism**.
- Anchoring then unanchoring **resets** to automatic ownership.
- `part:SetNetworkOwner(nil)` makes the server own it. `part:SetNetworkOwnershipAuto()` returns to automatic. `part:GetNetworkOwner()` and `part:CanSetNetworkOwnership()` query it.

## Vehicle example (official pattern)
```luau
local seat = script.Parent :: VehicleSeat
seat:GetPropertyChangedSignal("Occupant"):Connect(function()
	local hum = seat.Occupant
	local player = hum and game.Players:GetPlayerFromCharacter(hum.Parent)
	if player then
		seat:SetNetworkOwner(player)        -- the driver simulates the car (responsive steering)
	else
		seat:SetNetworkOwnershipAuto()
	end
end)
```
Without this, a passenger who sat down first owns the car and the driver steers with lag.

## Debug view
Studio viewport ▸ Visualization options ▸ **Network owners**: green = you own it, red = buffer zone (your client simulates it but doesn't own it), white/grey = server or another client, black = no owner (no physics).

## Security (critical)
The server **can't verify** physics a client owns. Owners can teleport, noclip or fling parts, replicate NaN CFrames, and fake or suppress `Touched` ([[Exploit_Threat_Model]], [[Client_Triggered_Instance_Security]]). Mitigations: server ownership for gameplay-critical objects, anchored interactables, [[Movement_Validation]], and ultimately the [[Server_Authority_Model]], which keeps objects server-owned while clients predict.

## Related
[[Physics_Engine_and_Assemblies]] · [[Replication_Model]] · [[Movement_Validation]] · [[Server_Authority_Model]] · [[Exploit_Threat_Model]] · [[Client_Triggered_Instance_Security]] · [[Knockback_and_Ragdoll]] · [[Physics_Optimization]] · [[Projectile_Systems]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/physics/network-ownership
- https://create.roblox.com/docs/scripting/security/network-ownership
