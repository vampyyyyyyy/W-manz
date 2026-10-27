---
aliases: [ODM gear, ODM, 3D maneuver gear, Omni-directional mobility gear, Grapple swinging system, AoT movement]
tags:
  - roblox-dev
  - systems/movement
type: architecture
last_updated: 2026-10-27
status: complete
---
# ODM Gear System (Attack-on-Titan-style movement)

> **TL;DR:** ODM = **two independent grapple hooks** (left/right) that anchor to world geometry from camera-aimed raycasts, a **reel/pull force** toward the anchors, **pendulum swinging** constrained by rope length, **gas boosts** (a resource) for thrust, and **orbit/strafe** control around anchors. It's client-owned physics for responsiveness, with server-side **budgets** for speed and gas, and ideally [[Server_Authority_Model|server authority]] prediction for competitive play.

## Components
| Component | Runs on | Responsibility |
| --- | --- | --- |
| Hook aim + fire | Client | Camera/crosshair raycast (max range ~150–250 studs), hook travel time, attach to the hit point and normal ([[Raycasting]]) |
| Hook state ×2 | Client (state replicated) | `Idle → Firing → Attached → Reeling → Released`, with anchor position (+ moving-target attachment) |
| Rope physics | Client (owner) | `RopeConstraint` (max length + winch) **or** a custom spring force. One per hook ([[Grappling_Hook_Physics]]) |
| Pull / reel | Client | Force toward the anchor midpoint, scaled by input and gas |
| Swing control | Client | Tangential force from WASD relative to the camera, for orbit and strafe |
| Gas | **Server** truth, client predicted | Boost thrust, reel strength. Refill at stations ([[Server_Authoritative_Cooldowns]]) |
| Visuals | All clients | Cables as Beams with sag, hook models, gas puffs, wind lines, FOV kick ([[Beams_and_Trails]], [[Camera_System]]) |
| Validation | **Server** | Speed budget raised while attached or boosting, hook range and LOS checks, gas accounting ([[Movement_Validation]]) |

## Physics model (per frame, PreSimulation)
```text
for each attached hook h:
   d = anchor_h - rootPos;  dist = |d|;  dir = d / dist
   rope constraint: if dist > ropeLen_h then remove outward radial velocity (pendulum)
   reel:            if reeling then ropeLen_h -= reelSpeed * dt  and  F += dir * reelForce
pull = Σ F;  if both hooks attached, aim pull at the midpoint for stable "slingshot" lines
steer = camera-relative input projected onto the plane ⟂ to the rope (tangential) * steerForce
boost = if boosting and gas > 0: camera.LookVector * boostForce; gas -= rate * dt
apply: VectorForce / LinearVelocity, or AssemblyLinearVelocity += (pull + steer + boost)/mass * dt
```
Remove gravity partially while reeling (gameplay choice) and clamp max speed for control and validation.

## Feel checklist
- **Hook travel time** (0.05–0.15 s) plus an audible "thunk" on attach. Rope tension sound scaling with speed.
- **FOV kick** on boost and release, **camera roll** into swings, light shake on hard landings ([[Camera_Shake]]).
- **Speed lines / wind particles** around the camera above a speed threshold ([[Particle_Emitters]]).
- **Release momentum** is the skill expression: keep tangential velocity when letting go.
- **Animation layers:** a swing pose blended by speed and rope angle, and leg tuck when reeling ([[Animation_System]]).
- **Mobile:** two hook buttons + aim assist toward valid surfaces ([[Cross_Platform_UI_Input]]).

## Networking & anti-cheat
- Replicate hook **state and anchor positions** (an UnreliableRemoteEvent at ~20 Hz plus reliable attach/detach events) so other clients draw cables ([[UnreliableRemoteEvent]]).
- The server checks the anchor is within range and line of sight of the player's server position at fire time. It deducts gas and raises the movement budget only while hooks are validly attached ([[Movement_Validation]]).
- Competitive ODM PvP: move hook logic into `BindToSimulation` under the server authority beta, or the CCL with deterministic callbacks ([[Character_Controllers_and_ControllerManager]]).

## Related
[[Grappling_Hook_Physics]] · [[Custom_Movement_Abilities]] · [[Movement_Validation]] · [[Mover_Constraints]] · [[Mechanical_Constraints]] · [[Camera_System]] · [[Beams_and_Trails]] · [[Server_Authority_Model]] · [[Character_Controllers_and_ControllerManager]] · [[Client_Prediction_and_Reconciliation]] · [[MOC_Movement_and_ODM]]

## Sources
- Engine APIs: https://create.roblox.com/docs/physics/constraints/rope · https://create.roblox.com/docs/physics/mover-constraints
- Design synthesized for this vault; add community showcase breakdowns via [[Showcase_Breakdown_Method]]
