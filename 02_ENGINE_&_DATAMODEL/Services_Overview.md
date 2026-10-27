---
aliases: [GetService, Roblox services, Services list]
tags:
  - roblox-dev
  - engine/services
type: concept
last_updated: 2026-10-27
status: complete
---
# Services Overview

> **TL;DR:** Services are singleton Instances under `game` that expose engine systems. Always fetch them with `game:GetService("Name")` at the top of a script. A quick map of which service owns which job saves hours of searching.

## Most-used services by job
| Job | Service(s) | Note |
| --- | --- | --- |
| Players, characters, bans | `Players` | [[Player_and_Character_Lifecycle]], [[Ban_API_and_Consequences]] |
| Frame loop, environment checks | `RunService` | [[RunService_Frame_Events]] |
| Networking containers | `ReplicatedStorage`, `ReplicatedFirst` | [[Container_Services_and_Replication_Scope]] |
| Server-only code & assets | `ServerScriptService`, `ServerStorage` | |
| Input | `UserInputService`, `ContextActionService`, Input Action System | [[Input_Action_System]], [[UserInputService_and_ContextActionService]] |
| Tweens | `TweenService` | [[TweenService]] |
| Tags | `CollectionService` | [[CollectionService_Tags]] |
| Physics groups | `PhysicsService` | [[Collision_Groups_and_Filtering]] |
| Persistence | `DataStoreService`, `MemoryStoreService` | [[DataStoreService]], [[MemoryStoreService]] |
| Cross-server | `MessagingService`, `TeleportService` | [[MessagingService_Cross_Server]], [[TeleportService_and_Reserved_Servers]] |
| Money | `MarketplaceService`, `BadgeService` | [[MarketplaceService]], [[Badges]] |
| Analytics & policy | `AnalyticsService`, `PolicyService` | [[AnalyticsService_Events]], [[PolicyService_Compliance]] |
| HTTP & secrets | `HttpService` | [[HttpService_and_Secrets_Store]] |
| Text & chat | `TextService`, `TextChatService` | [[Text_Filtering_Compliance]] |
| Navigation | `PathfindingService` | [[Pathfinding]] |
| Audio | `SoundService` (+ Audio API objects) | [[Audio_API]] |
| Debris timer | `Debris` | `AddItem(obj, seconds)` |

## Pattern
```luau
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
```
`GetService` creates the service if it hasn't been created yet, whereas `game.ServiceName` indexing can fail for services that aren't instantiated or are renamed. Some services are server-only (`ServerStorage` contents, `DataStoreService`, `MessagingService`). Calling them on the client errors or returns nothing.

## Related
[[DataModel_and_Instance_Hierarchy]] · [[Container_Services_and_Replication_Scope]] · [[Script_Types_and_RunContext]] · [[RunService_Frame_Events]] · [[DataStoreService]] · [[MarketplaceService]] · [[HttpService_and_Secrets_Store]] · [[Input_Action_System]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/scripting/services
