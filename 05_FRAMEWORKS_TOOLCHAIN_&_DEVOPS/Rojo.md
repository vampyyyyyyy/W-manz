---
aliases: [Rojo, rojo serve, default.project.json, syncback, Filesystem workflow]
tags:
  - roblox-dev
  - toolchain/sync
type: framework
last_updated: 2026-10-27
status: complete
---
# Rojo

> **TL;DR:** Rojo makes the **filesystem the source of truth** for your Roblox project. You edit `.luau` (and `.rbxm`, `.json`, `.toml`, `.model.json`) files in VS Code with Git, and `rojo serve` + the Studio plugin live-syncs them in. `rojo build` produces `.rbxl`/`.rbxm` files for CI. **`rojo syncback`** pulls instances from place files back into the project. Since Roblox added native [[Script_Sync]], pick based on whether you want *everything* or just *scripts* on disk.

## What it is / maintenance status
- Repo: https://github.com/rojo-rbx/rojo (MPL-2.0). Active (commits Oct 2026). Docs: rojo.space.
- Install via [[Rokit]]: `rokit add rojo-rbx/rojo`, plus the Studio plugin (Rojo installs it with `rojo plugin install`).

## Core files
```json
// default.project.json
{
  "name": "MyGame",
  "tree": {
    "$className": "DataModel",
    "ReplicatedStorage": {
      "Shared": { "$path": "src/shared" },
      "Packages": { "$path": "Packages" }
    },
    "ServerScriptService": { "Server": { "$path": "src/server" } },
    "StarterPlayer": { "StarterPlayerScripts": { "Client": { "$path": "src/client" } } },
    "Workspace": { "$properties": { "StreamingEnabled": true } }
  }
}
```
File naming: `init.server.luau` / `init.client.luau` / `init.luau` (folder = script with children), `*.server.luau`, `*.client.luau`, `*.luau` (ModuleScript), `*.model.json`, `*.meta.json` (properties and attributes).

## Commands
`rojo init` · `rojo serve` (live sync; connect from the Studio plugin) · `rojo build -o game.rbxl` · `rojo sourcemap` (for [[Luau_LSP]]) · `rojo syncback` (place → files) · `rojo upload` (legacy publishing; prefer Open Cloud in CI: [[Open_Cloud_Place_Publishing]]).

## Rojo vs Script Sync
| Need | Choose |
| --- | --- |
| Everything in Git (models, configs, packages), CI builds, Wally/pesde | **Rojo** |
| Keep building in Studio, just edit scripts in an external editor (Team Create friendly) | **[[Script_Sync]]** |
| AI agents editing code + driving Studio | Either + the [[Roblox_Studio_MCP_Server]] |

## Related
[[Script_Sync]] · [[Wally]] · [[Pesde]] · [[Rokit]] · [[Luau_LSP]] · [[Selene]] · [[StyLua]] · [[Version_Control_Workflow]] · [[GitHub_Actions_CI_CD]] · [[Open_Cloud_Place_Publishing]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://github.com/rojo-rbx/rojo · https://rojo.space/docs
