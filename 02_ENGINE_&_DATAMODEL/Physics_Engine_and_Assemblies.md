---
aliases: [Physics engine, Assemblies, AssemblyRootPart, Rigid bodies, ApplyImpulse]
tags:
  - roblox-dev
  - engine/physics
type: concept
last_updated: 2026-10-27
status: complete
---
# Physics Engine & Assemblies

> **TL;DR:** Roblox simulates **assemblies**: groups of parts joined by rigid welds or Motor6Ds that act as one rigid body. That's the unit of mass, velocity, network ownership and sleep. Default rate is **240 Hz** (about 4 worldsteps per 60 FPS frame), with [[Adaptive_Timestepping]] available. Move things with **constraints or impulses**, not by writing CFrames every frame on unanchored parts.

## Assembly facts
- `ApplyImpulse` / `ApplyAngularImpulse` on any part affects the **whole assembly**.
- Assembly properties (same for every part in it): `AssemblyLinearVelocity`, `AssemblyAngularVelocity`, `AssemblyCenterOfMass`, `AssemblyMass` (infinite if anything is anchored), `AssemblyRootPart`.
- **Root part** selection (highest priority first): anchored part → non-`Massless` parts → higher `RootPriority` → size, with multipliers for Seats/VehicleSeats, then parts named `HumanoidRootPart`, then `Torso`. The root part is used for replication and ownership, and it doesn't move when Motor6D transforms update.
- Anchoring **one** part anchors the assembly. Anchoring **two** splits it and deactivates the weld between them. To anchor an assembly, **anchor only its root part**, which performs better than anchoring every part.
- Joints only work inside `Workspace` or a `WorldModel` ([[ViewportFrames]] use WorldModels).

## How to move things (preference order)
1. **Constraints:** `LinearVelocity`, `AlignPosition`, `VectorForce`… ([[Mover_Constraints]]).
2. **Impulses** for instantaneous changes: knockback, jumps ([[Knockback_and_Ragdoll]]).
3. Setting `AssemblyLinearVelocity` directly works but can feel unnatural. Do it in `PreSimulation` ([[Task_Scheduler]]).
4. **Anchored + CFrame** (tweened or scripted) for kinematic objects: doors, platforms. Combine with `Workspace:BulkMoveTo` for many parts.

## Per-part flags that matter
| Property | Effect |
| --- | --- |
| `Anchored` | Not simulated, server-owned |
| `CanCollide` | Participates in collisions |
| `CanTouch` | Fires `Touched`/`TouchEnded` (turn off when unused: perf) |
| `CanQuery` | Hit by raycasts and spatial queries ([[Raycasting]]) |
| `Massless` | Ignored in assembly mass (only when welded to a non-massless part) |
| `CustomPhysicalProperties` | Density, friction, elasticity + weights |
| `CollisionGroup` | [[Collision_Groups_and_Filtering]] |

## Related
[[Adaptive_Timestepping]] · [[Physics_Sleep_System]] · [[Mover_Constraints]] · [[Mechanical_Constraints]] · [[Network_Ownership]] · [[Collision_Groups_and_Filtering]] · [[Physics_Optimization]] · [[Knockback_and_Ragdoll]] · [[Grappling_Hook_Physics]] · [[Task_Scheduler]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/physics/assemblies · https://create.roblox.com/docs/physics
