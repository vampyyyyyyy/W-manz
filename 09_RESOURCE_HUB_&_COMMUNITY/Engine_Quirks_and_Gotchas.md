---
aliases: [Engine quirks, Gotchas, Roblox pitfalls, Common bugs that aren't bugs]
tags:
  - roblox-dev
  - community/quirks
type: concept
last_updated: 2026-10-27
status: complete
---
# Engine Quirks & Gotchas

> **TL;DR:** Most "Roblox is broken" moments are documented behavior. This is a checklist of the ones that bite production games most: replication edge cases, event timing, physics signals, streaming, serialization and lifecycle. When debugging, check this list **before** assuming an engine bug ([[Studio_Debugger]]).

## Replication & networking
- Remote args: **mixed tables and nil holes break**, non-string keys become strings, metatables are stripped, functions → nil, non-replicated instances → nil ([[RemoteEvents_and_RemoteFunctions]]).
- `UnreliableRemoteEvent` payloads **> 1000 bytes are dropped** and ordering isn't guaranteed ([[UnreliableRemoteEvent]]).
- Server `TweenService` on replicated parts replicates **every frame**. Tween on clients instead ([[TweenService]], [[Network_Bandwidth_Budget]]).
- Client-owned physics ⇒ client authority over position. Exploiters abuse it ([[Network_Ownership]]).
- With **StreamingEnabled**, client-side instances can be **missing**. Never assume `workspace.Map.Door` exists on the client ([[StreamingEnabled]]).

## Events & timing
- `SignalBehavior.Default` is **Immediate today**, and Deferred changes handler timing (and fixes re-entrancy) ([[Deferred_Events_and_SignalBehavior]]).
- `Changed` / `GetPropertyChangedSignal` **don't fire for physics-driven CFrame/Position** changes. Poll in a frame event instead ([[RunService_Frame_Events]]).
- `PlayerAdded` can fire before your script connects (Studio especially). Also loop over `Players:GetPlayers()` ([[Player_and_Character_Lifecycle]]).
- `CharacterAdded` fires before the appearance is fully loaded (use `CharacterAppearanceLoaded` when it matters).
- `game:BindToClose` callbacks get a limited window (~30 s) to save ([[Session_Locking]]).
- Legacy `wait()` throttles (29 ms minimum, can delay much longer). Use the `task` library ([[Deprecated_wait_spawn_delay]], [[task_Library]]).

## Data
- DataStores serialize to JSON: **no NaN/inf**, numeric keys become strings for non-arrays, there's a ~4 s `GetAsync` cache, and buffers *are* supported ([[DataStore_Limits_and_Error_Codes]]).
- Attributes can't store Instances (use ObjectValues or IDs) ([[Attributes]]).

## Physics & math
- Far from the origin (tens of thousands of studs), float precision causes jitter, so keep play areas near the origin ([[Numbers_and_Floating_Point]]).
- Parts **sleep** below small velocity thresholds, so a "stuck" unanchored part may just be asleep ([[Physics_Sleep_System]]).
- Raycasts are capped at 15,000 studs, and shapecasts at 1,024 studs (and they ignore initial overlaps) ([[Raycasting]], [[Shapecasting]]).

## UI
- Layout objects override child Position/Size. `ResetOnSpawn = true` by default ([[UI_Flex_and_List_Layouts]], [[Roblox_UI_Fundamentals]]).

## Related
[[Deferred_Events_and_SignalBehavior]] · [[RemoteEvents_and_RemoteFunctions]] · [[StreamingEnabled]] · [[Network_Ownership]] · [[DataStore_Limits_and_Error_Codes]] · [[Physics_Sleep_System]] · [[Numbers_and_Floating_Point]] · [[Player_and_Character_Lifecycle]] · [[Historical_Bugs_and_Outages]] · [[Legacy_Code_Smells]] · [[Studio_Debugger]] · [[MOC_Resource_Hub_and_Community]]

## Sources
- https://create.roblox.com/docs/scripting/events/remote · https://create.roblox.com/docs/scripting/events/deferred · https://create.roblox.com/docs/cloud-services/data-stores/error-codes-and-limits
