---
aliases: [ReplicatedStorage, ServerStorage, ServerScriptService, ReplicatedFirst, StarterPlayerScripts, Where to put scripts]
tags:
  - roblox-dev
  - engine/replication
type: concept
last_updated: 2026-10-27
status: complete
---
# Container Services & Replication Scope

> **TL;DR:** Where you parent something decides who can see it. **Server-only:** `ServerScriptService`, `ServerStorage`. **Replicated to all clients:** `ReplicatedStorage`, `ReplicatedFirst`, `Workspace` (streamed), `Lighting`, plus per-player copies from `StarterGui`/`StarterPack`/`StarterPlayer`. Put secrets, server logic and unreleased assets in server-only containers ([[Access_Control_and_Confidentiality]]).

## Cheat sheet
| Container | Replicates? | Simulated/rendered? | Typical contents |
| --- | --- | --- | --- |
| `ServerScriptService` | ❌ | — | Server scripts and modules |
| `ServerStorage` | ❌ | ❌ | Server-only assets: maps, NPC templates, loot tables |
| `ReplicatedStorage` | ✔️ all clients | ❌ | Shared modules, remotes, VFX templates, client assets |
| `ReplicatedFirst` | ✔️ first, before the rest | ❌ | Loading screen ([[Loading_Screens_and_ReplicatedFirst]]) |
| `Workspace` | ✔️ (streamed if [[StreamingEnabled]]) | ✔️ | The world |
| `Lighting` | ✔️ | Applies | Sky, Atmosphere, post effects ([[Lighting_and_Post_Processing]]) |
| `StarterGui` | Copied to `PlayerGui` | — | ScreenGuis |
| `StarterPlayer.StarterPlayerScripts` | Copied to `PlayerScripts` | — | Client bootstrap |
| `StarterPlayer.StarterCharacterScripts` | Copied into each character | — | Per-character client logic |
| `Players.<player>` | Partially | — | `PlayerGui`, `Backpack` (client-visible) |

## Rules
- **Client-created instances never replicate to the server** (except things the engine replicates, like physics of owned parts and animations on owned characters) ([[Replication_Model]]).
- Assets the client needs **only sometimes** (big maps, cutscene models) can live in `ServerStorage` and be cloned into `Workspace` or `ReplicatedStorage` when needed. That reduces join time and memory ([[Mobile_and_Low_End_Optimization]]).
- `ReplicatedStorage` size directly affects **join time**, because everything downloads on join ([[Network_Bandwidth_Budget]]).

## Related
[[Replication_Model]] · [[Access_Control_and_Confidentiality]] · [[Script_Types_and_RunContext]] · [[DataModel_and_Instance_Hierarchy]] · [[StreamingEnabled]] · [[Loading_Screens_and_ReplicatedFirst]] · [[Require_and_Module_Resolution]] · [[Network_Bandwidth_Budget]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/projects/data-model#replication · https://create.roblox.com/docs/scripting/locations
