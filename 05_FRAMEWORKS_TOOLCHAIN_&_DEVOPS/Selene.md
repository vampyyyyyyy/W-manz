---
aliases: [selene, Luau linter, selene.toml]
tags:
  - roblox-dev
  - toolchain/quality
type: framework
last_updated: 2026-10-27
status: complete
---
# selene (linter)

> **TL;DR:** selene is a fast Rust-based **Lua/Luau linter** with a Roblox standard library definition. It catches unused variables, shadowing, suspicious patterns, deprecated APIs and more, with the goal that "diagnostics are never wrong". Run it in your editor (VS Code extension) and in CI. It's recommended by Roblox's Script Sync docs.

## Setup
```toml
# selene.toml (project root)
std = "roblox"

[lints]
shadowing = "allow"          # tune per team taste
unused_variable = "warn"
```
```bash
rokit add Kampfkarren/selene
selene src/                  # lint
selene generate-roblox-std   # refresh Roblox API definitions when needed
```

## What it catches that Studio's analyzer may not
Unbalanced `pcall` result handling patterns, `if x == nil then` on always-truthy expressions, unused `local function`s, empty `if` blocks, deprecated globals (`wait`, `spawn`, `delay`) ([[Deprecated_wait_spawn_delay]]), mixed-table constructors, and more (see the selene docs).

## Fit in the toolchain
- **Type errors** → [[Luau_LSP]] / `luau-lsp analyze` (or Studio Script Analysis).
- **Lint and style smells** → selene.
- **Formatting** → [[StyLua]].
- Gate merges with all three in [[GitHub_Actions_CI_CD]].

## Related
[[StyLua]] · [[Luau_LSP]] · [[Rokit]] · [[GitHub_Actions_CI_CD]] · [[Script_Sync]] · [[Rojo]] · [[Deprecated_wait_spawn_delay]] · [[Type_Checking_Modes]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://github.com/Kampfkarren/selene · https://kampfkarren.github.io/selene/
