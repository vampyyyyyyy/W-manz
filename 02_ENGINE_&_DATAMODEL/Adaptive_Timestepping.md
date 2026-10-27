---
aliases: [PhysicsSteppingMethod, Adaptive physics, Solver islands, 240 Hz]
tags:
  - roblox-dev
  - engine/physics
type: concept
last_updated: 2026-10-27
status: complete
---
# Adaptive Timestepping

> **TL;DR:** With `Workspace.PhysicsSteppingMethod = Adaptive`, the solver groups parts into **islands simulated at 240, 120 or 60 Hz** depending on how hard they are to solve. Fast or complex mechanisms stay at 240 Hz, and calm ones drop to 60 Hz. It's up to **2.5× faster physics** and recommended for most games. Use **Fixed (240 Hz)** for racing, destruction or complex mechanisms.

## How it works
- Default physics rate is 240 Hz, about 4 worldsteps per frame at 60 FPS.
- Adaptive assigns islands to `1dt` (240 Hz), `2dt` (120 Hz) or `4dt` (60 Hz) buckets. High velocity, high acceleration and complex mechanisms go to 240 Hz. The exact criteria may change.
- When a 240 Hz island interacts with slower ones, those get **promoted** to 240 Hz, which can erase the gains in scenes where most things are fast.

## Inspect it
- MicroProfiler: `physicsStepped` → `worldStep - Adaptive`. Hover `LDLPGSSolver::solve` to see island counts per bucket ([[MicroProfiler]]).
- Studio Settings ▸ Physics ▸ **Are Timesteps Shown** outlines parts by their current rate.

## Choose a mode
| Game | Mode |
| --- | --- |
| Most games: characters, light props, combat | **Adaptive** |
| Racing, vehicles with suspension, tanks, destruction sims | **Fixed** (stability matters more than CPU) |
| Physics-heavy ODM/grapple games | Test both. Fast-swinging characters land in 240 Hz islands anyway ([[Grappling_Hook_Physics]]) |

## Related
[[Physics_Engine_and_Assemblies]] · [[Physics_Sleep_System]] · [[Physics_Optimization]] · [[Task_Scheduler]] · [[Fixed_Timestep_and_Tick_Rate]] · [[MicroProfiler]] · [[Mechanical_Constraints]] · [[Grappling_Hook_Physics]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/physics/adaptive-timestepping
