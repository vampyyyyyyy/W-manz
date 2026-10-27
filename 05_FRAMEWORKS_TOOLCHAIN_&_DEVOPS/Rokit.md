---
aliases: [Rokit, rokit.toml, Toolchain manager, Aftman, Foreman]
tags:
  - roblox-dev
  - toolchain/setup
type: framework
last_updated: 2026-10-27
status: complete
---
# Rokit

> **TL;DR:** Rokit is the **recommended toolchain manager** for Roblox projects (it replaces Aftman and Foreman, and is drop-in compatible with their configs). It pins CLI tool versions per project (`rokit.toml`), so everyone, including CI, runs the same Rojo, Wally, Selene, StyLua, Lune, Blink and darklua versions.

## Install (per the README)
```bash
# macOS / Linux
curl -sSf https://raw.githubusercontent.com/rojo-rbx/rokit/main/scripts/install.sh | bash
# Windows PowerShell
Invoke-RestMethod https://raw.githubusercontent.com/rojo-rbx/rokit/main/scripts/install.ps1 | Invoke-Expression
```
⚠️ These pipe a remote script into your shell. Read it first if you're cautious, or download `rokit.exe` from the releases page.

## Use
```bash
cd my-game              # project root
rokit init              # creates rokit.toml
rokit add rojo-rbx/rojo
rokit add UpliftGames/wally
rokit add Kampfkarren/selene
rokit add JohnnyMorganz/StyLua
rokit add lune-org/lune
rokit add 1Axen/blink
rokit install           # on a fresh clone / in CI
rokit self-update
```
`rokit.toml` gets committed. Tools resolve to the pinned versions inside the project folder.

## Related
[[Rojo]] · [[Wally]] · [[Pesde]] · [[Selene]] · [[StyLua]] · [[Lune]] · [[Blink_IDL]] · [[Darklua]] · [[GitHub_Actions_CI_CD]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://github.com/rojo-rbx/rokit
