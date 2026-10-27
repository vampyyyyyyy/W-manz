---
aliases: [LinearVelocity, AlignPosition, AlignOrientation, VectorForce, AngularVelocity, Torque, LineForce, BodyMovers]
tags:
  - roblox-dev
  - engine/physics
type: api
last_updated: 2026-10-27
status: complete
---
# Mover Constraints

> **TL;DR:** Mover constraints apply force or torque through `Attachment`s (or animated `Bone`s). They're the modern replacement for the deprecated `BodyVelocity`/`BodyPosition`/`BodyGyro`. Pick by intent: **target velocity** → `LinearVelocity`/`AngularVelocity`, **target pose** → `AlignPosition`/`AlignOrientation`, **raw force** → `VectorForce`/`Torque`/`LineForce`.

## Cheat sheet
| Constraint | Drives | Key properties | Typical use |
| --- | --- | --- | --- |
| `LinearVelocity` | Velocity along a line, plane or vector | `VelocityConstraintMode` (Line/Plane/Vector), `VectorVelocity`, `MaxForce` (or `ForceLimitMode`), `RelativeTo` | Dashes, conveyors, hover movement ([[Custom_Movement_Abilities]]) |
| `AngularVelocity` | Spin rate | `AngularVelocity`, `MaxTorque` | Turrets, spinning hazards |
| `AlignPosition` | Move to a position | `Mode` (OneAttachment/TwoAttachment), `Responsiveness`, `MaxForce`, `MaxVelocity`, `RigidityEnabled` | Carried objects, grapple pull ([[Grappling_Hook_Physics]]) |
| `AlignOrientation` | Rotate to an orientation | `Mode`, `Responsiveness`, `MaxTorque`, `PrimaryAxisOnly`, `RigidityEnabled` | Keep upright, face direction |
| `VectorForce` | Constant force | `Force`, `RelativeTo` (World/Attachment0/1), `ApplyAtCenterOfMass` | Thrusters, anti-gravity (`Force = mass * gravity`) |
| `Torque` | Constant torque | `Torque`, `RelativeTo` | Flywheels |
| `LineForce` | Force along the line between two attachments | `Magnitude`, `InverseSquareLaw`, `MaxForce` | Magnets, tethers, ODM reel pull |

## Example: anti-gravity + controlled thrust
```luau
local att = Instance.new("Attachment")
att.Parent = root
local vf = Instance.new("VectorForce")
vf.Attachment0 = att
vf.RelativeTo = Enum.ActuatorRelativeTo.World
vf.ApplyAtCenterOfMass = true
vf.Force = Vector3.new(0, root.AssemblyMass * workspace.Gravity, 0) -- cancels gravity for this assembly
vf.Parent = root
```
Recompute `AssemblyMass` if the assembly changes (equipping tools, ragdolling).

## Tips
- `RigidityEnabled = true` makes Align* as strong as possible. It's snappy, but it can fight other constraints and look robotic.
- Set movers from **PreSimulation**, and change properties rather than re-creating instances every frame ([[Task_Scheduler]]).
- Movers on **client-owned** assemblies run on that client, which is the normal case for character abilities ([[Network_Ownership]]).
- Under the [[Server_Authority_Model]], movers inside `BindToSimulation` are predicted and rolled back like everything else.

## Related
[[Mechanical_Constraints]] · [[Physics_Engine_and_Assemblies]] · [[Grappling_Hook_Physics]] · [[ODM_Gear_System]] · [[Custom_Movement_Abilities]] · [[Character_Controllers_and_ControllerManager]] · [[Knockback_and_Ragdoll]] · [[Task_Scheduler]] · [[Network_Ownership]] · [[MOC_Engine_and_DataModel]] · [[MOC_Movement_and_ODM]]

## Sources
- https://create.roblox.com/docs/physics/mover-constraints · https://create.roblox.com/docs/physics/constraints/linear-velocity
