---
aliases: [Knit, Knit framework, Services and Controllers]
tags:
  - roblox-dev
  - framework/architecture
type: framework
last_updated: 2026-10-27
status: complete
---
# Knit (archived)

> **TL;DR:** Knit (Sleitnick) was the most popular Roblox game framework: server **Services** and client **Controllers**, auto-wired networking (`Client` tables become remotes), and a `Knit.Start()` lifecycle (`KnitInit` → `KnitStart`). **It's archived and no longer maintained** (repo last updated July 2024). Existing Knit games keep working, but new projects should use a lightweight [[Single_Script_Architecture]] module loader plus explicit networking ([[Remote_Architecture_Patterns]], [[Networking_Libraries_Comparison]]).

## What Knit looked like
```lua
-- Server
local Knit = require(ReplicatedStorage.Packages.Knit)
local PointsService = Knit.CreateService({ Name = "PointsService", Client = {} })
function PointsService.Client:GetPoints(player) return self.Server:GetPoints(player) end
function PointsService:KnitStart() --[[ runs after all KnitInit ]] end
Knit.Start():catch(warn)        -- returns a Promise
```

## Why teams moved on
- **Implicit networking:** every `Client` method is a remote. That makes it easy to forget validation and rate limits ([[Server_Side_Validation]]).
- **Promise-heavy APIs** and string-keyed service lookup hurt type inference.
- Archival means no fixes for engine changes (deferred events, type solver updates).

## Migrating off Knit (incremental)
1. Keep the services as plain ModuleScripts with `init()` and `start()` functions.
2. Replace `Knit.GetService("X")` with direct `require`s (typed).
3. Replace `Client` methods with explicit remotes through your Net layer, adding validation and rate limiting as you go.
4. Swap Knit's bundled utilities for their standalone packages (Trove, Signal, Comm in RbxUtil) ([[Cleanup_Libraries_Trove_Maid_Janitor]], [[Signal_Libraries]]).

## Related
[[Single_Script_Architecture]] · [[Remote_Architecture_Patterns]] · [[Networking_Libraries_Comparison]] · [[Promise_Library]] · [[Signal_Libraries]] · [[Cleanup_Libraries_Trove_Maid_Janitor]] · [[Server_Side_Validation]] · [[Legacy_Code_Smells]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://github.com/Sleitnick/Knit (README: "No Longer Maintained", ARCHIVAL.md)
