---
aliases: [Knockback, Ragdoll, Launch, ApplyImpulse knockback, BallSocket ragdoll]
tags:
  - roblox-dev
  - systems/combat
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Knockback & Ragdoll

> **TL;DR:** Knockback = an **impulse or velocity on the victim's assembly**, applied by **whoever owns its physics**. For player characters that's the victim's client, so the server must either tell the victim's client to apply it, or briefly take network ownership. Ragdoll = swap `Motor6D`s for `BallSocketConstraint`s (with limits), disable Humanoid states that fight it, and restore on recovery.

## Ownership is the whole trick
| Victim | Who simulates | How to knock back |
| --- | --- | --- |
| NPC (server-owned) | Server | `root:ApplyImpulse(dir * force * root.AssemblyMass)` on the server |
| Player character (client-owned) | That player's client | Server sends `Knockback(dir, force)` to the victim, who applies it locally. The server validates the resulting movement budget ([[Movement_Validation]]). Or, for big launches, temporarily `SetNetworkOwner(nil)` and apply it on the server, then hand ownership back |
| Under [[Server_Authority_Model]] | Server (predicted) | Apply inside the simulation, and it's predicted and rolled back correctly |

```luau
-- victim client: apply replicated knockback
KnockbackRemote.OnClientEvent:Connect(function(dir: Vector3, force: number, upward: number)
	local root = player.Character and player.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
	if not root then return end
	local impulse = (dir.Unit * force + Vector3.yAxis * upward) * root.AssemblyMass
	root:ApplyImpulse(impulse)
end)
```
For consistent distances regardless of current motion, set velocity instead: `root.AssemblyLinearVelocity = dir * speed + up * lift`, or drive a short-lived `LinearVelocity` ([[Mover_Constraints]]).

## Ragdoll recipe (R15)
1. For each `Motor6D` joint: create two attachments at `C0`/`C1`, a `BallSocketConstraint` (`LimitsEnabled`, `UpperAngle` ~45–90, `TwistLimitsEnabled`), then disable the motor (`Enabled = false`).
2. `humanoid:ChangeState(Enum.HumanoidStateType.Physics)` (or `Ragdoll`), and disable `GettingUp` while ragdolled.
3. Turn on limb collisions (`CanCollide = true` on limbs), and add `NoCollisionConstraint`s between adjacent parts to avoid jitter ([[Mechanical_Constraints]], [[Collision_Groups_and_Filtering]]).
4. Recover: re-enable the Motor6Ds, destroy the sockets, set state to `GettingUp`.
Prebuild the constraints **disabled** at spawn and toggle them, which is cheaper than creating them on every hit. For "active ragdoll" hit reactions, look at `AnimationConstraint`.

## Feel
Brief hitstop before the launch, then a camera punch, a dust trail (Trail on root), and a landing impact with a small shake ([[Hitstop_and_Impact_Feel]], [[Camera_Shake]], [[Beams_and_Trails]]).

## Related
[[Network_Ownership]] · [[Physics_Engine_and_Assemblies]] · [[Mover_Constraints]] · [[Mechanical_Constraints]] · [[Damage_Pipeline]] · [[Movement_Validation]] · [[Humanoid_and_Character_Model]] · [[Server_Authority_Model]] · [[Hitstop_and_Impact_Feel]] · [[MOC_Combat_Systems]]

## Sources
- https://create.roblox.com/docs/physics/assemblies · https://create.roblox.com/docs/physics/constraints/ball-socket
