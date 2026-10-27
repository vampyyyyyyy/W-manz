---
aliases: [luau-lsp, Luau Language Server, VS Code Luau, Luau Language Server Companion, sourcemap]
tags:
  - roblox-dev
  - toolchain/editor
type: framework
last_updated: 2026-10-27
status: complete
---
# Luau Language Server (luau-lsp)

> **TL;DR:** `luau-lsp` (JohnnyMorganz) brings Studio-grade autocomplete, type checking, go-to-definition, hover docs and diagnostics to **VS Code and other editors**. It preloads Roblox type definitions, understands **require-by-string**, and resolves the DataModel via **Rojo sourcemaps** or the **Luau Language Server Companion** Studio plugin (for [[Script_Sync]]). It's the officially recommended editor extension for Script Sync.

## Setup paths
| Workflow | How luau-lsp knows your instance tree |
| --- | --- |
| [[Rojo]] (v7.3+) | `rojo sourcemap --watch -o sourcemap.json` (the extension can autogenerate it) |
| [[Script_Sync]] | **Luau Language Server Companion** Studio plugin streams the DataModel to the extension |
| Pure Luau / [[Lune]] | `luau-lsp.types.definitionFiles` for custom globals, plus `.luaurc` aliases |

## CI type checking
```bash
luau-lsp analyze --sourcemap=sourcemap.json --definitions=globalTypes.d.luau --base-luaurc=.luaurc src/
```
Fail the build on type errors in `--!strict` files ([[GitHub_Actions_CI_CD]], [[Type_Checking_Modes]]). Keep the solver setting consistent with Studio ([[New_Type_Solver]]).

## Tips
- Nightly builds ship daily if you need fresh Luau features (type functions, new syntax) before a stable release.
- Pair with [[Selene]] (lints) and [[StyLua]] (format) for the full quality stack.
- AI coding agents (Claude Code, etc.) benefit too: diagnostics from the LSP give the agent ground truth while it edits ([[Roblox_Studio_MCP_Server]]).

## Related
[[Rojo]] · [[Script_Sync]] · [[Selene]] · [[StyLua]] · [[Type_Checking_Modes]] · [[New_Type_Solver]] · [[Require_and_Module_Resolution]] · [[GitHub_Actions_CI_CD]] · [[Roblox_Studio_MCP_Server]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://github.com/JohnnyMorganz/luau-lsp · https://create.roblox.com/docs/scripting/sync#set-up-a-language-server
