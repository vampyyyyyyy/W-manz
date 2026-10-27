---
aliases: [Learning path, Curriculum, Roadmap, Where to start]
tags:
  - roblox-dev
  - moc/learning
type: moc
last_updated: 2026-10-27
status: complete
---
# Learning Path

> **TL;DR:** A staged route from "I can script" to "I ship production systems", aimed at combat, VFX, weather and movement-heavy games. Each stage has a goal, the notes to read, and a **prove-it** mini-project. Don't skip stage 3 (client/server security): it's what separates games that survive exploiters from games that don't.

## Stage 0: Pro workflow (1–2 days)
**Goal:** code on disk, in Git, with an AI agent connected to Studio.
[[Script_Sync]] or [[Rojo]] · [[Rokit]] · [[StyLua]] · [[Selene]] · [[Luau_LSP]] · [[Version_Control_Workflow]] · [[Roblox_Studio_MCP_Server]]
**Prove it:** the agent creates a script through Script Sync, playtests via MCP, and reads the output.

## Stage 1: Luau fluency
[[Luau_Overview]] · [[Luau_Type_System]] · [[Type_Checking_Modes]] · [[Metatables]] · [[Closures_and_Upvalues]] · [[Coroutines]] · [[task_Library]] · [[Error_Handling_pcall_xpcall]] · [[Generalized_Iteration]]
**Prove it:** a `--!strict` typed inventory module with zero type errors.

## Stage 2: The engine model
[[DataModel_and_Instance_Hierarchy]] · [[Task_Scheduler]] · [[RunService_Frame_Events]] · [[Deferred_Events_and_SignalBehavior]] · [[Replication_Model]] · [[Network_Ownership]] · [[Physics_Engine_and_Assemblies]]
**Prove it:** explain in your own words why a server-side tween stutters on clients, then fix it.

## Stage 3: Client/server security (do not skip)
[[Exploit_Threat_Model]] · [[RemoteEvents_and_RemoteFunctions]] · [[Server_Side_Validation]] · [[Remote_Rate_Limiting]] · [[NaN_and_Infinity_Exploits]] · [[Server_Authoritative_Cooldowns]]
**Prove it:** a dash ability with a server-validated cooldown, rate limits and NaN-safe arguments.

## Stage 4: Data that never dupes
[[DataStoreService]] · [[DataStore_Limits_and_Error_Codes]] · [[Session_Locking]] · [[ProfileStore]] · [[ProcessReceipt_Idempotency]]
**Prove it:** a currency system that survives a server crash mid-purchase without duping or losing coins.

## Stage 5: Combat
[[MOC_Combat_Systems]]: [[Combat_State_Machine]] → [[Hitbox_Detection_Methods]] → [[Hit_Validation]] → [[Damage_Pipeline]] → [[Hitstop_and_Impact_Feel]]
**Prove it:** a 3-hit combo with block/parry, validated hits, and hitstop that feels good at 150 ms of simulated ping ([[Studio_Testing_Modes]]).

## Stage 6: Movement & ODM
[[MOC_Movement_and_ODM]]: [[Mover_Constraints]] → [[Grappling_Hook_Physics]] → [[ODM_Gear_System]] → [[Movement_Validation]]
**Prove it:** a grapple swing with a gas economy and server-side speed and teleport checks.

## Stage 7: VFX & weather
[[MOC_VFX_and_Weather]]: [[VFX_Composition_and_Timing]] → [[Client_Side_VFX_Replication]] → [[Weather_System_Architecture]] → [[Wetness_Puddles_and_Drying]]
**Prove it:** rain that ramps up, shelters correctly, wets surfaces and dries afterward, at 60 FPS on a mid-range phone.

## Stage 8: UI
[[Roblox_UI_Fundamentals]] · [[UI_Styling_StyleSheets]] · [[Fusion]] or [[Vide]] · [[Custom_HUD_Design]] · [[Cooldown_and_Ability_UI]] · [[Game_UI_Art_Direction]]
**Prove it:** a HUD with ability cooldowns driven by server timestamps that works with touch and gamepad.

## Stage 9: Performance
[[Performance_Optimization_Workflow]] · [[MicroProfiler]] · [[Memory_Leaks]] · [[StreamingEnabled]] · [[Parallel_Luau]] · [[Mobile_and_Low_End_Optimization]]
**Prove it:** find and fix one real frame spike and one leak in your project, with before/after numbers.

## Stage 10: Ship & grow
[[GitHub_Actions_CI_CD]] · [[Analytics_Dashboard_and_Metrics]] · [[Retention_and_Engagement_Metrics]] · [[Monetization_Design_Principles]] · [[Content_Maturity_Labels]] · [[PolicyService_Compliance]]
**Prove it:** publish through CI, then run one experiment on onboarding and read the D1 results.

## Related
[[Home]] · [[Glossary]] · [[Trusted_Sources]] · [[MOC_Resource_Hub_and_Community]]

## Sources
- Curriculum assembled from this vault's notes, which cite official documentation.
