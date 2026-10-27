---
aliases: [Community modules, Open source Roblox libraries, Library index, Maintenance status]
tags:
  - roblox-dev
  - community/modules
type: concept
last_updated: 2026-10-27
status: complete
---
# Community Modules Index

> **TL;DR:** A status board of the open-source libraries this vault covers, with **last-commit dates checked Oct 2026** (from fresh clones). "Active" = commits within ~3 months. Prefer active, typed, tested libraries. Treat **archived/deprecated** ones as legacy, and pin versions in every case ([[Wally]], [[Pesde]]).

## Toolchain
| Library | Last commit | Status | Note |
| --- | --- | --- | --- |
| Rojo | 2026-10 | Active | [[Rojo]] |
| Wally / pesde | 2026-10 | Active | [[Wally]], [[Pesde]] |
| Rokit | 2026-09 | Active | [[Rokit]] |
| selene / StyLua / luau-lsp | 2026-10 | Active | [[Selene]], [[StyLua]], [[Luau_LSP]] |
| Lune | 2026-10 | Active | [[Lune]] |
| darklua | 2026-07 | Maintained | [[Darklua]] |
| roblox-ts | 2026-10 | Active | [[Roblox_TS]] |
| rbxcloud | 2025-03 | Quiet | [[Open_Cloud_APIs]] |
| studio-rust-mcp-server | 2026-04 | **Not actively developed** (built-in Studio MCP replaces it) | [[Roblox_Studio_MCP_Server]] |

## Runtime libraries
| Library | Last commit | Status | Note |
| --- | --- | --- | --- |
| Knit | 2024-07 | **Archived** | [[Knit]] |
| RbxUtil (Trove, Signal, Comm…) | 2026-07 | Maintained | [[Cleanup_Libraries_Trove_Maid_Janitor]], [[Signal_Libraries]] |
| Janitor / LemonSignal | 2025-10 / 2026-07 | Maintained | [[Cleanup_Libraries_Trove_Maid_Janitor]], [[Signal_Libraries]] |
| ProfileStore | 2025-07 | Stable | [[ProfileStore]] |
| Lapis | 2025-02 | Quiet | [[Lapis]] |
| Promise (evaera) | 2023-10 | Stable/finished | [[Promise_Library]] |
| Blink | 2026-09 | Active | [[Blink_IDL]] |
| Zap | 2026-06 | Rewrite in progress (0.6.x maintained) | [[Zap_IDL]] |
| ByteNet | 2025-08 | Low activity | [[ByteNet]] |
| Jecs | 2026-10 | Active | [[ECS_Libraries_Jecs_and_Matter]] |
| Matter | 2024-11 | Quiet | [[ECS_Libraries_Jecs_and_Matter]] |
| Cmdr | 2026-10 | Active | [[Cmdr]] |
| RaycastHitbox / FastCast | 2021 / 2020 | **Legacy** (still widely referenced) | [[Raycast_Hitbox_Module]], [[Projectile_Systems]] |

## UI & testing
| Library | Last commit | Status | Note |
| --- | --- | --- | --- |
| Fusion | 2026-02 | Maintained (0.3 scoped API) | [[Fusion]] |
| React Lua (jsdotlua) | 2024-12 | Stable | [[React_Lua]] |
| Roact | 2023-12 | **Deprecated** | [[Roact_Legacy]] |
| Vide | 2026-10 | Active | [[Vide]] |
| Charm / Reflex | 2026-09 / 2025-12 | Active / Maintained | [[UI_State_Management]] |
| UI Labs | 2026-08 | Active | [[UI_Labs]] |
| Jest Lua / TestEZ | 2024-12 / 2023-01 | Stable / Legacy | [[Testing_Frameworks]] |

## Choosing a library (checklist)
Typed API? Tests/CI? Recent releases? Issue response? License? Security review of anything that touches remotes or DataStores ([[Third_Party_Code_and_Backdoors]]).

## Related
[[Wally]] · [[Pesde]] · [[Trusted_Sources]] · [[Third_Party_Code_and_Backdoors]] · [[Legacy_Code_Smells]] · [[Knit]] · [[Fusion]] · [[ProfileStore]] · [[Networking_Libraries_Comparison]] · [[DataStore_Libraries_Comparison]] · [[MOC_Resource_Hub_and_Community]]

## Sources
- GitHub repositories of each project (cloned 2026-10-27): rojo-rbx/rojo, UpliftGames/wally, pesde-pkg/pesde, rojo-rbx/rokit, Kampfkarren/selene, JohnnyMorganz/StyLua, JohnnyMorganz/luau-lsp, lune-org/lune, seaofvoices/darklua, roblox-ts/roblox-ts, Sleitnick/rbxcloud, Roblox/studio-rust-mcp-server, Sleitnick/Knit, Sleitnick/RbxUtil, howmanysmall/Janitor, Data-Oriented-House/LemonSignal, MadStudioRoblox/ProfileStore, nezuo/lapis, evaera/roblox-lua-promise, 1Axen/blink, red-blox/zap, ffrostflame/ByteNet, Ukendio/jecs, matter-ecs/matter, evaera/Cmdr, dphfox/Fusion, jsdotlua/react-lua, Roblox/roact, centau/vide, littensy/charm, littensy/reflex, PepeElToro41/ui-labs, jsdotlua/jest-lua, Roblox/testez
