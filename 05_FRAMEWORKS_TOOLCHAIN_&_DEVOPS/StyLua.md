---
aliases: [StyLua, Formatter, .stylua.toml, Code formatting]
tags:
  - roblox-dev
  - toolchain/quality
type: framework
last_updated: 2026-10-27
status: complete
---
# StyLua (formatter)

> **TL;DR:** StyLua is a **deterministic formatter** (prettier-style) for Lua and Luau. It reprints your code from scratch, following the Roblox Lua Style Guide with a few deviations. Format on save in your editor and enforce it in CI with `stylua --check`, and style debates disappear from code review.

## Setup
```toml
# .stylua.toml
syntax = "Luau"
column_width = 120
indent_type = "Tabs"
indent_width = 4
quote_style = "AutoPreferDouble"
call_parentheses = "Always"
```
```bash
rokit add JohnnyMorganz/StyLua
stylua src/            # format
stylua --check src/    # CI: fail if unformatted
```
Prebuilt release binaries include all syntax variants. There's a `stylua-action` for GitHub Actions ([[GitHub_Actions_CI_CD]]).

## Tips
- Add a `.styluaignore` for generated code (Blink or Zap output, vendored packages).
- `-- stylua: ignore` above a statement keeps hand-aligned tables (frame data, lookup tables).
- Run StyLua **before** selene in hooks so lint line numbers match committed code ([[Selene]]).

## Related
[[Selene]] · [[Luau_LSP]] · [[Rokit]] · [[GitHub_Actions_CI_CD]] · [[Script_Sync]] · [[Rojo]] · [[Version_Control_Workflow]] · [[Blink_IDL]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://github.com/JohnnyMorganz/StyLua
