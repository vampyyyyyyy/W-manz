---
aliases: [pesde, pesde.toml, Luau package manager]
tags:
  - roblox-dev
  - toolchain/packages
type: framework
last_updated: 2026-10-27
status: complete
---
# pesde

> **TL;DR:** pesde is a **Luau package manager designed to avoid runtime lock-in**. It supports Roblox and standalone Luau runtimes like [[Lune]], and it's inspired by npm, pnpm, Wally and Cargo. It's actively developed (commits Oct 26, 2026). Consider it when your code targets several runtimes or you want features beyond [[Wally]]. Check ecosystem coverage for the packages you need.

## What it is / maintenance status
- Repo: https://github.com/pesde-pkg/pesde. Docs: docs.pesde.dev.
- Install with a toolchain manager (the README recommends mise-en-place). [[Rokit]] users can usually add it too.
- Can consume Wally packages (check the docs for current interop), so migration can be gradual.

## When to choose pesde vs Wally
| Situation | Pick |
| --- | --- |
| Pure Roblox game, team already on Wally, packages available there | [[Wally]] |
| Shared Luau libraries used in Roblox **and** Lune scripts or CLI tools | pesde |
| You want pnpm-like workflows and runtime targets | pesde |

## Related
[[Wally]] · [[Rokit]] · [[Lune]] · [[Rojo]] · [[Luau_LSP]] · [[Community_Modules_Index]] · [[Third_Party_Code_and_Backdoors]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://github.com/pesde-pkg/pesde · https://docs.pesde.dev
