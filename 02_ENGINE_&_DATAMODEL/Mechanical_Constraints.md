---
aliases: [RopeConstraint, SpringConstraint, HingeConstraint, BallSocketConstraint, WeldConstraint, Motor6D, RigidConstraint, NoCollisionConstraint, AnimationConstraint]
tags:
  - roblox-dev
  - engine/physics
type: api
last_updated: 2026-10-27
status: complete
---
# Mechanical Constraints

> **TL;DR:** Mechanical constraints model joints between attachments: ropes, springs, hinges, ball sockets, sliders, rigid welds. They're the building blocks of ragdolls, grapples, vehicles, doors and destructible structures. Most support **limits** and some have **actuators** (motor or servo).

## Reference
| Constraint | Degrees of freedom | Notable properties | Use |
| --- | --- | --- | --- |
| `WeldConstraint` | 0 (rigid) | Keeps the current offset | Gluing props, attaching hitboxes |
| `RigidConstraint` | 0 (rigid, attachment-based) | Works with Bones | Attaching to animated bones |
| `Motor6D` | Animated by `Transform` | `C0`, `C1`, `Transform` | Character joints ([[Animation_System]]) |
| `BallSocketConstraint` | 3 rotation | `LimitsEnabled`, `UpperAngle`, `TwistLimitsEnabled`, `MaxFrictionTorque` | **Ragdolls** ([[Knockback_and_Ragdoll]]) |
| `HingeConstraint` | 1 rotation | `ActuatorType` (None/Motor/Servo), `LimitsEnabled`, `TargetAngle`, `AngularSpeed` | Doors, wheels, turrets |
| `PrismaticConstraint` | 1 translation | Actuator, limits | Elevators, pistons |
| `CylindricalConstraint` | 1 rot + 1 trans | Both actuators | Suspension struts |
| `SpringConstraint` | Spring-damper | `Stiffness`, `Damping`, `FreeLength`, limits | Suspension, bouncy tethers |
| `RopeConstraint` | Max distance (slack) | `Length`, `CurrentDistance` (read), `WinchEnabled`, `WinchTarget`, `WinchSpeed`, `WinchForce`, `WinchResponsiveness`, `Restitution`, `Thickness` | **Grapple lines**, cranes ([[Grappling_Hook_Physics]]) |
| `RodConstraint` | Fixed distance | `Length`, limits | Pendulums, chains |
| `TorsionSpringConstraint` | Rotational spring | `Stiffness`, `Damping` | Springy doors |
| `UniversalConstraint` | 2 rotation | Limits | Drive shafts |
| `PlaneConstraint` | Keep on a plane | | 2D gameplay |
| `NoCollisionConstraint` | — | Disables collision between two parts | Avoid self-collision in ragdolls |
| `AnimationConstraint` | Animated, physics-aware joint | `Transform`, `IsKinematic`, `LinearStrength`/`AngularStrength`, `LinearDamping`/`AngularDamping`, `MaxForce`, `MaxTorque` | Physically simulated animation (active ragdoll, hit reactions) |

## Example: winch-able grapple rope
```luau
local rope = Instance.new("RopeConstraint")
rope.Attachment0 = handAttachment
rope.Attachment1 = hitAttachment          -- created at the raycast hit point
rope.Length = (hitPos - hand.Position).Magnitude
rope.WinchEnabled = true
rope.WinchTarget = 4                      -- reel to 4 studs
rope.WinchSpeed = 60
rope.WinchForce = 40000
rope.Visible = false                      -- draw your own Beam for style (Beams_and_Trails)
rope.Parent = hand
```

## Debugging
Studio's constraint visualization (Model tab) shows attachments and limits. The **Assemblies** visualization shows which parts actually form rigid bodies.

## Related
[[Mover_Constraints]] · [[Physics_Engine_and_Assemblies]] · [[Grappling_Hook_Physics]] · [[Knockback_and_Ragdoll]] · [[Animation_System]] · [[ODM_Gear_System]] · [[Beams_and_Trails]] · [[Physics_Sleep_System]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/physics/mechanical-constraints · https://create.roblox.com/docs/physics/constraints/rope
