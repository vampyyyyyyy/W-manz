---
aliases: [Wally, wally.toml, Roblox package manager, Wally packages]
tags:
  - roblox-dev
  - toolchain/packages
type: framework
last_updated: 2026-10-27
status: complete
---
# Wally

> **TL;DR:** Wally is the established **package manager for Roblox** (Cargo/npm-inspired): a `wally` CLI plus a public registry. Declare dependencies in `wally.toml`, run `wally install`, and point [[Rojo]] at the generated `Packages/` folder. Most community libraries (Fusion, Promise, Trove, ProfileStore-like modules, Blink runtime pieces) are published here.

## What it is / maintenance status
- Repo: https://github.com/UpliftGames/wally. Active (Oct 2026). Install via [[Rokit]] (`rokit add wally`). Prebuilt binaries for Windows, macOS and Linux (x86_64 + aarch64).

## Manifest
```toml
[package]
name = "yourname/combat-game"
version = "0.1.0"
registry = "https://github.com/UpliftGames/wally-index"
realm = "shared"

[dependencies]
Promise = "evaera/promise@4.0.0"
Trove = "sleitnick/trove@1.1.0"

[server-dependencies]
# server-only packages

[dev-dependencies]
JestGlobals = "jsdotlua/jest-globals@3.10.0"
```
`wally install` creates `Packages/` (shared), `ServerPackages/`, `DevPackages/` and a `wally.lock`. **Commit `wally.toml` and `wally.lock`**, and usually git-ignore the generated folders (CI regenerates them).

## Tips
- Pin exact versions for anything security-sensitive. Review package source before adding it, because it's third-party code running in your game ([[Third_Party_Code_and_Backdoors]]).
- For type checking across packages, run `wally-package-types` or use luau-lsp sourcemaps ([[Luau_LSP]]).
- Alternative: [[Pesde]] (runtime-agnostic Luau package manager).

## Related
[[Rojo]] · [[Rokit]] · [[Pesde]] · [[Luau_LSP]] · [[Community_Modules_Index]] · [[Third_Party_Code_and_Backdoors]] · [[GitHub_Actions_CI_CD]] · [[Version_Control_Workflow]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://github.com/UpliftGames/wally · https://wally.run
