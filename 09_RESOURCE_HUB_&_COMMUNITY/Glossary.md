---
aliases: [Glossary, Terms, Roblox dev vocabulary, Definitions]
tags:
  - roblox-dev
  - community/glossary
type: concept
last_updated: 2026-10-27
status: complete
---
# Glossary

> **TL;DR:** Short definitions of the terms used across this vault, each pointing to its main note. Use the alphabetical sections, or search (Ctrl/Cmd+O) for a term's alias.

## A–D
- **Actor:** container whose scripts can run in parallel. See [[Actors_and_Messaging]], [[Parallel_Luau]].
- **Assembly:** rigidly connected parts simulated as one body. See [[Physics_Engine_and_Assemblies]].
- **AuthorityMode (Server):** server-authoritative simulation with prediction and rollback (full release, 2026). See [[Server_Authority_Model]].
- **Bitpacking:** fitting several values into fewer bits. See [[Bitpacking]], [[Buffer_Library]].
- **CCU / DAU:** concurrent users / daily active users, which scale DataStore budgets and analytics. See [[DataStore_Limits_and_Error_Codes]], [[Analytics_Dashboard_and_Metrics]].
- **Deferred events:** handlers queued to resumption points instead of running immediately. See [[Deferred_Events_and_SignalBehavior]].
- **DevEx:** cashing out Earned Robux. See [[Developer_Exchange_DevEx]].

## E–L
- **ECS:** Entity-Component-System data architecture. See [[Entity_Component_System_Pattern]], [[ECS_Libraries_Jecs_and_Matter]].
- **Fastcall:** a builtin call the VM handles without a normal function call. See [[Builtin_Fastcalls_and_Imports]].
- **FilteringEnabled (FE):** the historical name for the client/server boundary that's now always on. See [[Replication_Model]].
- **Hitbox:** a query volume used to detect hits. See [[Hitbox_Detection_Methods]].
- **Hitstop:** a brief freeze on impact for weight. See [[Hitstop_and_Impact_Feel]].
- **IDL:** a schema language that generates networking code. See [[Blink_IDL]], [[Zap_IDL]].
- **I-frames:** invulnerability frames. See [[Block_Parry_and_IFrames]].
- **Idempotent:** safe to apply more than once (receipts!). See [[ProcessReceipt_Idempotency]].
- **Lag compensation:** judging hits at the shooter's perceived time. See [[Lag_Compensation]].

## M–R
- **MCP:** Model Context Protocol, how AI agents drive Studio. See [[Roblox_Studio_MCP_Server]].
- **Native codegen:** compiling Luau to machine code (`--!native`). See [[Native_Code_Generation]].
- **Network owner:** the machine simulating an assembly's physics. See [[Network_Ownership]].
- **ODM:** omni-directional mobility gear (grapple-swing movement). See [[ODM_Gear_System]].
- **Quantization:** reducing precision to save bandwidth. See [[Quantization]].
- **Reconciliation:** correcting client prediction to server state. See [[Client_Prediction_and_Reconciliation]].
- **RTBF:** right to be forgotten (data erasure). See [[Right_to_Erasure_GDPR]].
- **RunContext:** where a Script runs (Server/Client/Legacy/Plugin). See [[Script_Types_and_RunContext]].

## S–Z
- **Session lock:** guarantee that only one server owns a player's data. See [[Session_Locking]].
- **SharedTable:** a table shareable across Actors. See [[SharedTable]].
- **SLIM:** simplified low-detail model streaming. See [[SLIM_and_Frustum_Streaming]].
- **StreamingEnabled:** the client only receives nearby parts of the world. See [[StreamingEnabled]].
- **Token bucket:** a rate-limiting algorithm. See [[Remote_Rate_Limiting]].
- **Type function:** a type-level function written in Luau. See [[User_Defined_Type_Functions]].
- **Upvalue:** a variable captured by a closure. See [[Closures_and_Upvalues]].
- **Weak table:** a table whose references don't prevent GC. See [[Weak_Tables]].

## Related
[[Home]] · [[Learning_Path]] · [[Trusted_Sources]] · [[Engine_Quirks_and_Gotchas]] · [[Community_Modules_Index]] · [[MOC_Resource_Hub_and_Community]]

## Sources
- Definitions summarize the linked notes, which cite official documentation.
