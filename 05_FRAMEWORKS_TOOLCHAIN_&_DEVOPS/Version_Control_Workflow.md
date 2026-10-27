---
aliases: [Git workflow Roblox, Source control, Branching strategy, Team Create vs Git, Drafts mode]
tags:
  - roblox-dev
  - devops/version-control
type: architecture
last_updated: 2026-10-27
status: complete
---
# Version Control Workflow

> **TL;DR:** Put **code in Git** (via [[Script_Sync]] or [[Rojo]]), keep **world/assets in Studio** (Team Create, place version history, [[Packages_and_Asset_Reuse]]), and connect them with CI ([[GitHub_Actions_CI_CD]]). Inside Studio, choose **Live Scripting** (default, real-time co-editing) or **Drafts Mode** (local drafts with commit/merge). On a Git-based team, file sync replaces both for code.

## What lives where
| Artifact | Source of truth | Why |
| --- | --- | --- |
| Luau code | Git (files) | Diffs, review, branches, blame, CI |
| Remote/IDL schemas | Git ([[Blink_IDL]], [[Zap_IDL]]) | Generated code must match the schema |
| Maps, models, UI layout | Place file + Team Create + Packages | Binary/instance data diffs poorly |
| Config/tuning | Configs service or Git modules | Live tuning without deploys ([[Configs_Remote_Configuration]]) |
| Secrets | Secrets store / CI secrets, **never Git** | [[HttpService_and_Secrets_Store]] |

## Branching that fits Roblox
- `main` = what's live. Feature branches → PR → review → CI green → merge → deploy ([[Open_Cloud_Place_Publishing]]).
- Tag releases with the place version the publish returned, so you can bisect bugs to a place version.
- Long-lived world changes: develop in a **separate test place/universe** and promote with packages or a publish ([[Access_Control_and_Confidentiality]]).

## Studio-native collaboration
- **Live Scripting:** shared cursors and real-time edits, auto-saved every 5 minutes, logged in Script History.
- **Drafts Mode** (Experience Settings ▸ Enable Drafts Mode): edits stay local until **Commit**, with **Compare With Server** / **Merge From Server** and a three-way choice (Draft / Server / Other). Restore deleted scripts from the Drafts window.
- **Version history:** save/publish with version notes and restore previous versions. Activity History logs config, monetization and permission changes.

## .gitignore essentials
```gitignore
*.rbxl
*.rbxlx
*.rbxl.lock
*.rbxlx.lock
sourcemap.json
Packages/
DevPackages/
ServerPackages/
```
(Commit `wally.lock` / `pesde.lock` so installs are reproducible: [[Wally]], [[Pesde]].)

## Gotchas
- Script Sync doesn't sync scripts that carry attributes or tags. Move that metadata to a parent or config module ([[Attributes]], [[CollectionService_Tags]]).
- Two sources of truth for the same script (Studio edits + file edits) cause lost work. Pick one per script tree.
- Agents editing code ([[Roblox_Studio_MCP_Server]]): commit before large AI changes so `git diff` is your review surface.

## Related
[[Script_Sync]] · [[Rojo]] · [[GitHub_Actions_CI_CD]] · [[Open_Cloud_Place_Publishing]] · [[Packages_and_Asset_Reuse]] · [[Wally]] · [[Pesde]] · [[Roblox_Studio_MCP_Server]] · [[HttpService_and_Secrets_Store]] · [[Access_Control_and_Confidentiality]] · [[Configs_Remote_Configuration]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://create.roblox.com/docs/projects/collaboration · https://create.roblox.com/docs/projects/version-history
- https://create.roblox.com/docs/projects/external-tools · https://create.roblox.com/docs/ai/coding-harness
