---
aliases: [Engine MOC, DataModel hub, Engine hub]
tags:
  - roblox-dev
  - moc/engine
type: moc
last_updated: 2026-10-27
status: complete
---
# MOC: Engine & DataModel

> **TL;DR:** How the **Roblox engine** works under your scripts: the Instance tree and services, the task scheduler and frame events, replication and network ownership, the physics solver and constraints, spatial queries, characters and animation, input, camera, and the rendering, lighting and effects pipeline. Every game system sits on these.

*45 notes in this domain.*

## Start here
1. [[DataModel_and_Instance_Hierarchy]]: the tree everything lives in
2. [[Task_Scheduler]]: what runs when inside a frame
3. [[Replication_Model]]: what the server sends and what clients can change
4. [[Network_Ownership]]: who simulates physics, and why exploiters care
5. [[Physics_Engine_and_Assemblies]]: assemblies, solver and constraints
6. [[Server_Authority_Model]]: the 2026 server-authoritative simulation beta

## Core architecture
- **DataModel:** [[DataModel_and_Instance_Hierarchy]] · [[Instance_Lifecycle_and_Destroy]] · [[Services_Overview]] · [[Script_Types_and_RunContext]] · [[Container_Services_and_Replication_Scope]]
- **Data on instances:** [[Attributes]] · [[CollectionService_Tags]]

## Scheduling & events
- **Frame loop:** [[Task_Scheduler]] · [[RunService_Frame_Events]] · [[task_Library]]
- **Signals:** [[Signals_and_Connections]] · [[Deferred_Events_and_SignalBehavior]] · [[Bindable_Events_and_Functions]]

## Networking model
- **Replication:** [[Replication_Model]] · [[Network_Ownership]] · [[Server_Authority_Model]] · [[Player_and_Character_Lifecycle]]

## Physics & spatial queries
- **Simulation:** [[Physics_Engine_and_Assemblies]] · [[Adaptive_Timestepping]] · [[Physics_Sleep_System]] · [[Collision_Groups_and_Filtering]]
- **Constraints:** [[Mover_Constraints]] · [[Mechanical_Constraints]]
- **Queries & math:** [[Raycasting]] · [[Shapecasting]] · [[Spatial_Queries_Overlap]] · [[CFrame_Math]]

## Characters, animation & input
- **Characters:** [[Humanoid_and_Character_Model]] · [[Character_Controllers_and_ControllerManager]]
- **Animation:** [[Animation_System]] · [[Animation_Events_and_Markers]] · [[TweenService]]
- **Input & camera:** [[Input_Action_System]] · [[UserInputService_and_ContextActionService]] · [[Camera_System]]

## Rendering, environment & effects
- **Lighting:** [[Rendering_Pipeline_and_Lighting_Technology]] · [[Lighting_and_Post_Processing]] · [[Atmosphere_Clouds_and_Sky]] · [[Light_Sources_and_Highlights]]
- **World:** [[Terrain_and_Materials]] · [[Global_Wind]] · [[EditableImage_and_EditableMesh]]
- **Effects & audio:** [[Particle_Emitters]] · [[Beams_and_Trails]] · [[Audio_API]]

## Cross-domain
[[Home]] · [[Learning_Path]] · [[MOC_Networking_Security_and_Buffers]] · [[MOC_Game_Systems_and_Algorithms]] · [[MOC_VFX_and_Weather]] · [[MOC_Movement_and_ODM]]

## Sources
- Each linked note cites its own primary sources. See [[Trusted_Sources]] for the ranking policy.
