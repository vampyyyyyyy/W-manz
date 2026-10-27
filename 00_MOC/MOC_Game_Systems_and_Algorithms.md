---
aliases: [Game systems MOC, Gameplay hub, Systems hub]
tags:
  - roblox-dev
  - moc/game-systems
type: moc
last_updated: 2026-10-27
status: complete
---
# MOC: Game Systems & Algorithms

> **TL;DR:** The **gameplay layer**: persistence (DataStores, session locking, MemoryStores, cross-server messaging, teleports, matchmaking), combat (state machines, hitboxes, damage, feel), movement (prediction, ODM, grapples), weather and environment simulation, AI and procedural generation, and reusable patterns (pooling, inventories, spatial partitioning, ECS).

*47 notes in this domain.*

## Start here
1. [[Session_Locking]]: why player data needs a lock, and how to take one
2. [[Combat_System_Architecture]]: the server-authoritative combat blueprint
3. [[Client_Prediction_and_Reconciliation]]: responsive and authoritative at once
4. [[ODM_Gear_System]]: grapple-swing movement from first principles
5. [[Weather_System_Architecture]]: a believable, performant weather simulation
6. [[VFX_Composition_and_Timing]]: effects that read well and run well

## Persistence & services
- **DataStores:** [[DataStoreService]] · [[DataStore_Limits_and_Error_Codes]] · [[UpdateAsync_Patterns]] · [[Session_Locking]] · [[Data_Versioning_and_Schema_Migration]] · [[Ordered_DataStores_and_Leaderboards]]
- **Live services:** [[MemoryStoreService]] · [[MemoryStore_Data_Structures]] · [[MessagingService_Cross_Server]] · [[TeleportService_and_Reserved_Servers]] · [[Matchmaking_Customization]]

## Combat
- **Architecture:** [[Combat_System_Architecture]] · [[Finite_State_Machines]] · [[Combat_State_Machine]] · [[Combo_Systems_and_Input_Buffering]] · [[Server_Authoritative_Cooldowns]]
- **Hits & damage:** [[Hitbox_Detection_Methods]] · [[Raycast_Hitbox_Module]] · [[Projectile_Systems]] · [[Damage_Pipeline]] · [[Status_Effects]] · [[Block_Parry_and_IFrames]] · [[Knockback_and_Ragdoll]]
- **Feel:** [[Hitstop_and_Impact_Feel]] · [[Camera_Shake]]

## Movement & netcode
- **Movement:** [[ODM_Gear_System]] · [[Grappling_Hook_Physics]] · [[Custom_Movement_Abilities]]
- **Simulation:** [[Client_Prediction_and_Reconciliation]] · [[Fixed_Timestep_and_Tick_Rate]]

## Environment & VFX
- **Weather:** [[Weather_System_Architecture]] · [[Rain_and_Precipitation]] · [[Wetness_Puddles_and_Drying]] · [[Snow_Accumulation]] · [[Lightning_Generation]] · [[Day_Night_Cycle]]
- **VFX:** [[Client_Side_VFX_Replication]] · [[VFX_Composition_and_Timing]]

## AI & procedural
- **Agents:** [[Pathfinding]] · [[NPC_Behavior_Trees]] · [[Steering_and_Flocking]]
- **Generation:** [[Procedural_Generation]] · [[Noise_Functions]]

## Reusable patterns
- **Patterns:** [[Object_Pooling]] · [[Inventory_Systems]] · [[Spatial_Partitioning]] · [[Entity_Component_System_Pattern]]

## Cross-domain
[[Home]] · [[Learning_Path]] · [[MOC_Combat_Systems]] · [[MOC_Movement_and_ODM]] · [[MOC_VFX_and_Weather]] · [[MOC_Anti_Exploit]]

## Sources
- Each linked note cites its own primary sources. See [[Trusted_Sources]] for the ranking policy.
