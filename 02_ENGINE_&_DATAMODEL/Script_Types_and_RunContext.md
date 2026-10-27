---
aliases: [Script, LocalScript, ModuleScript, RunContext, Script types]
tags:
  - roblox-dev
  - engine/scripting
type: concept
last_updated: 2026-10-27
status: complete
---
# Script Types & `RunContext`

> **TL;DR:** **Script** runs on the server, or on the client when `RunContext = Client`. **LocalScript** is legacy client-only, and only runs in specific containers. **ModuleScript** runs only when `require`d. Modern projects use `Script` + `RunContext` and keep almost all logic in ModuleScripts ([[Single_Script_Architecture]]).

## Matrix
| Type | Runs where | Runs from which containers |
| --- | --- | --- |
| `Script` (`RunContext = Legacy`) | Server | `Workspace`, `ServerScriptService` |
| `Script` (`RunContext = Server`) | Server | **Anywhere** it replicates to the server (incl. `ReplicatedStorage`) |
| `Script` (`RunContext = Client`) | Client | **Anywhere** it replicates to the client. Careful: this includes `Workspace`, so it runs once per client |
| `LocalScript` | Client | `StarterPlayerScripts`, `StarterCharacterScripts`, `StarterGui`/`PlayerGui`, `Backpack`/tools, `ReplicatedFirst`, the player's character |
| `ModuleScript` | Whoever `require`s it | Wherever both sides can see it, or server-only containers for server modules |

Script Sync and Rojo map these to file suffixes: `.server.luau`, `.client.luau`, `.local.luau` (LocalScript), `.luau` (module) ([[Script_Sync]], [[Rojo]]).

## Security implications
- Client scripts and **all** replicated ModuleScripts can be decompiled by exploiters ([[Access_Control_and_Confidentiality]]).
- Roblox's list of decompilable types is LocalScripts, `RunContext = Client` Scripts and ModuleScripts. Server-context Scripts aren't on it, but a server Script in `ReplicatedStorage` still replicates as an instance (name, attributes), and any modules it requires there are decompilable. Keep server code in `ServerScriptService`.
- `Disabled`/`Enabled` doesn't hide source from exploiters.

## Practical defaults
- One bootstrap `Script` in `ServerScriptService`, one `LocalScript` (or client-context Script) in `StarterPlayerScripts`. Each requires a list of feature modules ([[Single_Script_Architecture]]).
- UI code lives with UI, but behavior goes in modules ([[Roblox_UI_Fundamentals]]).
- Character-specific client logic goes in `StarterCharacterScripts`, which re-runs every respawn ([[Player_and_Character_Lifecycle]]).

## Related
[[Container_Services_and_Replication_Scope]] · [[Require_and_Module_Resolution]] · [[Single_Script_Architecture]] · [[Access_Control_and_Confidentiality]] · [[Script_Sync]] · [[Rojo]] · [[Player_and_Character_Lifecycle]] · [[Script_Capabilities]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/scripting/locations · https://create.roblox.com/docs/reference/engine/classes/BaseScript#RunContext
