---
aliases: [Script Sync, InstanceFileSyncService, Studio file sync, External editor sync]
tags:
  - roblox-dev
  - toolchain/sync
type: framework
last_updated: 2026-10-27
status: complete
---
# Script Sync (Roblox Studio, native)

> **TL;DR:** Studio's built-in **Script Sync** mirrors selected folders (and their Scripts, LocalScripts, ModuleScripts and Folders) to `.luau` files on disk. Edit in VS Code, Cursor or any editor, and changes flow both ways. It works **with Team Create**, and it's the backbone of Roblox's official "coding harness" setup (editor + AI agent + MCP + Git). It's still flagged as a beta in places, so enable it under *File ▸ Beta Features* if you don't see it.

## Setup
1. Explorer → right-click a folder or service (e.g. `ServerScriptService`) → **Sync to…** → choose a directory.
2. Repeat for `ReplicatedStorage`, `StarterPlayerScripts`… Choosing a **top-level project folder** whose subfolders are already named after services auto-matches them.
3. Open that folder in your editor. Install **Luau LSP + Luau Language Server Companion plugin**, plus selene and StyLua (official recommendation) ([[Luau_LSP]], [[Selene]], [[StyLua]]).
4. Verify: `game:GetService("InstanceFileSyncService"):GetStatus(instance)`.

## File naming rules
| On disk | In Studio |
| --- | --- |
| `name.luau` | ModuleScript |
| `name.server.luau` | Script, `RunContext = Server` |
| `name.client.luau` | Script, `RunContext = Client` |
| `name.local.luau` | LocalScript |
| `name.legacy.luau` | Script, `RunContext = Legacy` |
| `name.plugin.luau` | Script, `RunContext = Plugin` |
| `name/` | Folder |
| `name/init.*.luau` | Script with children (type from suffix) |

## Limits & gotchas (official)
- Up to **10,000 scripts per top-level synced instance** and **128 top-level synced instances**.
- Only scripts and folders sync. Other instances in synced folders are ignored, so **don't sync folders that mix scripts with parts or models**.
- **Don't sync scripts that use attributes or tags.** Script Sync ignores them, which can cause data loss on create, delete or resync.
- File-system-safe, unique names required. Studio errors on duplicates or illegal characters.
- Conflict dialog on resume: **Keep Studio** vs **Keep Disk**, with a detailed diff. The default setting is "Do not resume" on conflict.
- Team Create: avoid two people syncing and editing the same script simultaneously.
- The Studio **debugger can't be controlled** from the external editor.
- Settings (Alt+S): auto-resume, conflict policy, keep files after stop, file extension.

## Related
[[Rojo]] · [[Roblox_Studio_MCP_Server]] · [[Luau_LSP]] · [[Selene]] · [[StyLua]] · [[Version_Control_Workflow]] · [[Script_Types_and_RunContext]] · [[Roblox_Assistant_and_AI_Tools]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://create.roblox.com/docs/scripting/sync · https://create.roblox.com/docs/ai/coding-harness
