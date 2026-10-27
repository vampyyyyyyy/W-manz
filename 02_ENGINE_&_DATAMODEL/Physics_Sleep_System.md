---
aliases: [Sleep system, Sleeping parts, Physics sleep thresholds]
tags:
  - roblox-dev
  - engine/physics
type: concept
last_updated: 2026-10-27
status: complete
---
# Physics Sleep System

> **TL;DR:** Assemblies that stop moving **fall asleep** and cost nothing until something wakes them. That's a huge performance win, and also the reason a slow-moving platform or a constraint target sometimes just *stops*. Know the thresholds and the wake triggers.

## States
- **Awake:** simulated.
- **Sleeping:** linear velocity < **0.33 studs/s**, rotational velocity < **0.42**, and accelerations below **0.24 studs/s²** (linear and rotational). Not simulated.
- **Sleep-checking:** a non-moving assembly connected by a constraint to an awake neighbor. It wakes if its own acceleration crosses the wake thresholds or a neighbor moves faster than the neighbor thresholds (e.g. **0.48 studs/s** linear).

## Wake triggers
Changing velocity, CFrame or physical properties from script, applying impulses, a collision with an awake assembly, constraint property changes, and ownership changes. See the docs' "additional wake situations" for the full list.

## Common bugs and fixes
| Symptom | Cause | Fix |
| --- | --- | --- |
| Slow conveyor or elevator stops | Below the velocity threshold | Move kinematically (anchored + CFrame) or keep the speed above the threshold |
| Object hangs mid-air at the top of a toss | Velocity ~0 (acceleration check usually prevents this) | Apply an impulse / let gravity act. Avoid manually zeroing velocity |
| Constraint target "doesn't respond" | Sleeping assembly not woken by an attachment move | Nudge it awake (tiny impulse) after retargeting |

## Performance angle
Large piles of debris settle and sleep, so let them. Don't run per-frame scripts that write to sleeping parts, because each write wakes them ([[Physics_Optimization]]).

## Related
[[Physics_Engine_and_Assemblies]] · [[Adaptive_Timestepping]] · [[Physics_Optimization]] · [[Mover_Constraints]] · [[Mechanical_Constraints]] · [[Network_Ownership]] · [[Object_Pooling]] · [[Engine_Quirks_and_Gotchas]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/physics/sleep-system
