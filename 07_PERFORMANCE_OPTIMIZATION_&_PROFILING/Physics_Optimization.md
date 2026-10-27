---
aliases: [Physics performance, CollisionFidelity, CanTouch, Assembly count, Physics lag]
tags:
  - roblox-dev
  - performance/physics
type: concept
last_updated: 2026-10-27
status: complete
---
# Physics Optimization

> **TL;DR:** Physics cost scales with **awake assemblies, contacts, constraint complexity and collision geometry**. Anchor what doesn't move (anchor only the **root part** of a static assembly), turn off `CanTouch`/`CanQuery`/`CanCollide` where unused, simplify `CollisionFidelity` (Box or Hull), let things **sleep**, use **Adaptive** timestepping, and keep NPC counts and Humanoid complexity in check.

## Levers
| Lever | Effect |
| --- | --- |
| `Anchored` (root part only for static assemblies) | Removes simulation entirely. Anchoring every part creates more assemblies ([[Physics_Engine_and_Assemblies]]) |
| `CanCollide = false` on decor | Fewer contacts |
| `CanTouch = false` | No Touched event processing (default on, so turn it off broadly) |
| `CanQuery = false` | Skipped by raycasts and overlaps (faster queries, fewer filter lists) ([[Raycasting]]) |
| `CollisionFidelity` = `Box`/`Hull` on meshes | Much cheaper than `Default`/`PreciseConvexDecomposition` |
| `Workspace.PhysicsSteppingMethod = Adaptive` | Up to 2.5× faster solver ([[Adaptive_Timestepping]]) |
| Sleep-friendly design | Don't poke resting assemblies every frame ([[Physics_Sleep_System]]) |
| Network ownership | Distribute simulation to clients where safe, and keep critical objects server-owned ([[Network_Ownership]]) |
| Fewer constraints in big mechanisms | Each joint adds solver work ([[Mechanical_Constraints]]) |
| Lightweight NPCs | Humanoids are expensive. Use simplified rigs, controllers, or client-rendered crowds ([[Humanoid_and_Character_Model]]) |
| Batch moves | `workspace:BulkMoveTo` for many anchored parts per frame |

## Diagnosing
MicroProfiler `physicsStepped`/`worldStep` scopes and island counts, the Server Stats physics numbers, the [[Memory_Categories]] `PhysicsCollision`/`PhysicsParts`, and the Studio **Assemblies** visualization ([[MicroProfiler]]).

## Related
[[Physics_Engine_and_Assemblies]] · [[Adaptive_Timestepping]] · [[Physics_Sleep_System]] · [[Network_Ownership]] · [[Mechanical_Constraints]] · [[Raycasting]] · [[MicroProfiler]] · [[Humanoid_and_Character_Model]] · [[Memory_Categories]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://create.roblox.com/docs/performance-optimization/improve#physics · https://create.roblox.com/docs/physics/adaptive-timestepping
