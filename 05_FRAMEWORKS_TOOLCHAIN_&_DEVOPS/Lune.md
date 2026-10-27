---
aliases: [Lune, Standalone Luau runtime, Lune scripts, roblox library lune]
tags:
  - roblox-dev
  - toolchain/runtime
type: framework
last_updated: 2026-10-27
status: complete
---
# Lune (standalone Luau runtime)

> **TL;DR:** Lune runs Luau **outside Roblox** like Node runs JS. It has filesystem, networking, process, serde and stdio APIs, a 1-to-1 port of the **task scheduler**, and an optional **`roblox` library to read and write place and model files** and their Instances. Use it for build scripts, asset pipelines, CI tasks, data migrations, unit tests of pure logic, and Open Cloud tooling, all in the language you already know.

## What it is / maintenance status
- Repo: https://github.com/lune-org/lune (active, Oct 2026). About a 5 MB executable. Docs bundled for editors.
- Install via [[Rokit]]: `rokit add lune-org/lune`.

## Example: bump a version attribute in a place file during CI
```luau
-- scripts/stamp-version.luau   (run: lune run scripts/stamp-version 1.4.2)
local fs = require("@lune/fs")
local process = require("@lune/process")
local roblox = require("@lune/roblox")

local version = process.args[1] or "dev"
local game = roblox.deserializePlace(fs.readFile("build/game.rbxl"))
local ws = game:GetService("Workspace")
ws:SetAttribute("BuildVersion", version)
fs.writeFile("build/game.rbxl", roblox.serializePlace(game))
print("stamped", version)
```

## Good uses
- Pre-publish steps in [[GitHub_Actions_CI_CD]] (stamping, validation, asset manifests).
- Calling [[Open_Cloud_APIs]] (DataStore admin, MessagingService announcements, place publishing) with typed Luau.
- Testing pure modules (combat math, serializers, migrations) fast without Studio ([[Testing_Frameworks]], [[Data_Versioning_and_Schema_Migration]]).
- **Non-goal:** running full Roblox games outside Roblox.

## Related
[[Rokit]] · [[Pesde]] · [[GitHub_Actions_CI_CD]] · [[Open_Cloud_APIs]] · [[Testing_Frameworks]] · [[Luau_CLI_Tools]] · [[Luau_C_API_and_Embedding]] · [[Rojo]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://github.com/lune-org/lune · https://lune-org.github.io/docs
