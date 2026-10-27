---
aliases: [Movement MOC, ODM MOC, Traversal hub, Grapple hub]
tags:
  - roblox-dev
  - moc/movement
type: moc
last_updated: 2026-10-27
status: complete
---
# MOC: Movement & ODM

> **TL;DR:** Great movement is **physics you can predict plus input you can trust**. Model grapples as constraints or forces on the character assembly, keep the client responsive (it owns its character, or predicts under Server Authority), and validate on the server with tolerant, leaky-bucket checks. ODM gear (anchor raycasts, reel force, gas economy, swing arcs, momentum) is the flagship case.

## Core mechanics
[[ODM_Gear_System]] · [[Grappling_Hook_Physics]] · [[Custom_Movement_Abilities]] · [[Character_Controllers_and_ControllerManager]] · [[Humanoid_and_Character_Model]]

## Physics building blocks
[[Physics_Engine_and_Assemblies]] · [[Mover_Constraints]] · [[Mechanical_Constraints]] · [[Adaptive_Timestepping]] · [[Physics_Sleep_System]] · [[CFrame_Math]] · [[Vector_Library]]

## Sensing the world
[[Raycasting]] · [[Shapecasting]] · [[Spatial_Queries_Overlap]] · [[Collision_Groups_and_Filtering]]

## Netcode & authority
[[Network_Ownership]] · [[Client_Prediction_and_Reconciliation]] · [[Fixed_Timestep_and_Tick_Rate]] · [[Server_Authority_Model]] · [[Movement_Validation]]

## Input, camera & feel
[[Input_Action_System]] · [[Camera_System]] · [[Camera_Shake]] · [[Beams_and_Trails]] · [[Cooldown_and_Ability_UI]] · [[Custom_HUD_Design]]

## Performance
[[Physics_Optimization]] · [[Luau_Micro_Optimizations]] · [[Native_Code_Generation]]

## Related hubs
[[Home]] · [[MOC_Game_Systems_and_Algorithms]] · [[MOC_Engine_and_DataModel]] · [[MOC_Combat_Systems]] · [[MOC_Anti_Exploit]]

## Sources
- Each linked note cites its own primary sources. See [[Trusted_Sources]].
