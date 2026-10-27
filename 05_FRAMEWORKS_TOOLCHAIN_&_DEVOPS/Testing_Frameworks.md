---
aliases: [Jest Lua, TestEZ, Unit testing Roblox, Automated tests]
tags:
  - roblox-dev
  - toolchain/testing
type: framework
last_updated: 2026-10-27
status: complete
---
# Testing Frameworks (Jest Lua, TestEZ, Lune, Luau Execution)

> **TL;DR:** **Jest Lua** (jsdotlua) is the modern choice: Jest-style `describe/it/expect`, mocks, and the framework Roblox uses internally. It runs **inside Roblox**. **TestEZ** is the older BDD framework (Roblox, last updated 2023). Pure logic modules can be tested **outside** Roblox with [[Lune]] scripts, and full in-engine tests can run in CI through **Open Cloud Luau Execution** ([[Open_Cloud_APIs]]).

## Jest Lua
```toml
# wally.toml
[dev-dependencies]
Jest = "jsdotlua/jest@3.10.0"
JestGlobals = "jsdotlua/jest-globals@3.10.0"
```
```luau
-- Damage.spec.luau
local JestGlobals = require("@DevPackages/JestGlobals")
local describe, it, expect = JestGlobals.describe, JestGlobals.it, JestGlobals.expect
local Damage = require("../Damage")

describe("Damage.compute", function()
	it("applies block chip damage", function()
		expect(Damage.compute({ base = 100, blocked = true, armor = 0 })).toBe(15)
	end)
	it("never goes negative", function()
		expect(Damage.compute({ base = 5, blocked = false, armor = 0.99 })).toBeGreaterThanOrEqual(0)
	end)
end)
```
(Adjust require paths to your setup. Jest Lua runs via a runner script in Studio or a Luau Execution session.)

## What to test first (highest ROI)
1. **Pure game math:** damage formulas, cooldown logic, combo graphs, loot tables ([[Damage_Pipeline]], [[Combo_Systems_and_Input_Buffering]]).
2. **Serialization:** encode → decode round-trips, malformed input rejection ([[Custom_Serialization]]).
3. **Data migrations** on fixture profiles ([[Data_Versioning_and_Schema_Migration]]).
4. **Validators** for remote input ([[Server_Side_Validation]]).

## CI options
| Approach | Runs | Notes |
| --- | --- | --- |
| [[Lune]] + a small test harness | Outside Roblox | Fast. No engine APIs |
| Open Cloud **Luau Execution** sessions | On Roblox infrastructure against a place version | Real engine. Upload with place publishing first ([[Open_Cloud_Place_Publishing]]) |
| Studio + MCP agent playtests | Your machine | Great for smoke tests driven by an AI agent ([[Roblox_Studio_MCP_Server]]) |

## Related
[[GitHub_Actions_CI_CD]] · [[Lune]] · [[Open_Cloud_APIs]] · [[Open_Cloud_Place_Publishing]] · [[Roblox_Studio_MCP_Server]] · [[Data_Versioning_and_Schema_Migration]] · [[Custom_Serialization]] · [[Wally]] · [[Studio_Testing_Modes]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://github.com/jsdotlua/jest-lua · https://github.com/Roblox/testez
- https://create.roblox.com/docs/cloud-services/http-service (Luau execution endpoints)
