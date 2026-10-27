---
aliases: [Legacy code, Code smells, Deprecated APIs, Old Roblox patterns, Refactor checklist]
tags:
  - roblox-dev
  - community/legacy
type: concept
last_updated: 2026-10-27
status: complete
---
# Legacy Code Smells

> **TL;DR:** A scan list for old or AI-generated Roblox code. Each smell maps to its modern replacement. Fix the **security smells** first (client-trusted damage/currency, unvalidated remotes, `InvokeClient`), then **reliability** (`SetAsync` for player data, no session lock, legacy `wait`), then **deprecations** (BodyMovers, `Humanoid:LoadAnimation`, `FindPartOnRay`, legacy chat, `LoadCharacter`).

## Security & architecture
| Smell | Why bad | Replace with |
| --- | --- | --- |
| Client sends damage/coins/position as truth | Exploitable | Intent-only remotes + server validation ([[Server_Side_Validation]], [[Hit_Validation]]) |
| `RemoteFunction:InvokeClient` | A client can yield or error your server thread | RemoteEvents with timeouts ([[RemoteEvents_and_RemoteFunctions]]) |
| One giant `Remote` with a `"action"` string and no checks | Unauditable attack surface | Typed IDL remotes ([[Blink_IDL]], [[Remote_Architecture_Patterns]]) |
| Free-model scripts with `require(assetId)` | Backdoors | Remove, audit, sandbox ([[Third_Party_Code_and_Backdoors]]) |

## Reliability
| Smell | Replace with |
| --- | --- |
| `SetAsync(player.UserId, data)` on leave only | Session-locked profiles + autosave + `BindToClose` ([[Session_Locking]], [[ProfileStore]]) |
| `while true do wait() end` | Event-driven code or `RunService` / `task.wait` ([[Deprecated_wait_spawn_delay]]) |
| `spawn` / `delay` | `task.spawn` / `task.delay` ([[task_Library]]) |
| Connections never disconnected | Trove/Janitor ([[Cleanup_Libraries_Trove_Maid_Janitor]], [[Memory_Leaks]]) |
| `_G` as a module system | `require` modules ([[Globals_G_shared_and_getfenv]]) |

## Deprecated / superseded APIs
| Old | New |
| --- | --- |
| BodyVelocity, BodyGyro, BodyPosition | LinearVelocity, AlignOrientation, AlignPosition ([[Mover_Constraints]]) |
| `Humanoid:LoadAnimation` | `Animator:LoadAnimation` ([[Animation_System]]) |
| `Workspace:FindPartOnRay*` | `Workspace:Raycast` ([[Raycasting]]) |
| `Player:LoadCharacter` | `LoadCharacterAsync` ([[Player_and_Character_Lifecycle]]) |
| `GetProductInfo` | `GetProductInfoAsync` ([[MarketplaceService]]) |
| Legacy chat (Chat service) | `TextChatService` (required for chat) ([[Age_Checks_and_Chat_Safety]]) |
| `Lighting.Technology` | `LightingStyle` + `PrioritizeLightingQuality` ([[Rendering_Pipeline_and_Lighting_Technology]]) |
| `Instance:Remove()`, `:connect` | `:Destroy()`, `:Connect` ([[Instance_Lifecycle_and_Destroy]]) |
| `Instance.new("Part", parent)` then set props | Set props, **then** `Parent` last (fewer replication/property events) |
| Roact, Knit, TestEZ | React Lua / Fusion / Vide, plain modules, Jest Lua ([[Roact_Legacy]], [[Knit]], [[Testing_Frameworks]]) |

## Related
[[Server_Side_Validation]] · [[Session_Locking]] · [[Deprecated_wait_spawn_delay]] · [[Mover_Constraints]] · [[Animation_System]] · [[Raycasting]] · [[Third_Party_Code_and_Backdoors]] · [[Cleanup_Libraries_Trove_Maid_Janitor]] · [[Community_Modules_Index]] · [[Release_Notes_and_Change_Tracking]] · [[MOC_Resource_Hub_and_Community]]

## Sources
- https://create.roblox.com/docs/reference/engine (deprecation notices) · https://create.roblox.com/docs/scripting/security/security-tactics
