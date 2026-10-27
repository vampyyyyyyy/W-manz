---
aliases: [require, ModuleScript, require by string, "@self", "@game", .luaurc aliases, cyclic require]
tags:
  - roblox-dev
  - luau/modules
type: api
last_updated: 2026-10-27
status: complete
---
# `require` & Module Resolution

> **TL;DR:** `require(moduleScript)` runs a ModuleScript **once per VM side** and returns its cached value. That's how state is shared within the server or within one client. On Roblox, `require` also accepts **string paths** (`"./Sibling"`, `"../Shared/Util"`, `"@self/Child"`, `"@game/ReplicatedStorage/Net"`). String requires don't wait for missing modules.

## Instance require (classic)
```luau
local Net = require(game:GetService("ReplicatedStorage"):WaitForChild("Net"))
```
- **Cached per side:** a module in `ReplicatedStorage` required by both a Script and a LocalScript runs **twice** (once on the server, once on each client) and returns *different* tables ([[Container_Services_and_Replication_Scope]]).
- The first `require` executes the module. If it errors, the require errors. A module that yields at top level blocks every requirer until it returns.
- **Cyclic requires** error ("loop or previous error loading module"). Break cycles with dependency injection or lazy requires inside functions.

## Require by string (Roblox semantics)
| Prefix | Starts at |
| --- | --- |
| `./` | `script.Parent` |
| `../` | `script.Parent.Parent` |
| `@self/` | `script` itself (children of this module) |
| `@game/` | `game` |
| `@rbx/…` | Roblox-provided packages, e.g. `require("@rbx/AvatarAbilities")` in the [[Character_Controllers_and_ControllerManager|Character Controller Library]] |
Each path component is a **child name**. `..` goes up. It's **non-blocking**: if the target doesn't exist yet, it errors immediately. Pair it with streaming- and replication-safe placement.

Outside Roblox ([[Lune]], CLI, [[Rojo]] with luau-lsp), `.luaurc` / `.config.luau` **aliases** like `"@shared/Net"` and `init.luau` directory modules follow the Luau require-by-string RFCs ([[Luau_LSP]]).

## Asset-id require (server only)
`require(1234567)` loads a published `MainModule`. It's the #1 backdoor vector, gated by the `LoadUnownedAsset` capability. Avoid it entirely in production ([[Third_Party_Code_and_Backdoors]]).

## Module design rules
- Return a table or function. **No side effects** at require time beyond setup (no infinite loops, no long yields).
- Keep server-only modules in `ServerScriptService`/`ServerStorage`. Modules in `ReplicatedStorage` get decompiled ([[Access_Control_and_Confidentiality]]).
- `export type` from modules so consumers get types ([[Type_Annotations_and_Casts]]).

## Related
[[Single_Script_Architecture]] · [[Container_Services_and_Replication_Scope]] · [[Access_Control_and_Confidentiality]] · [[Third_Party_Code_and_Backdoors]] · [[Rojo]] · [[Luau_LSP]] · [[Lune]] · [[Globals_G_shared_and_getfenv]] · [[Type_Annotations_and_Casts]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://create.roblox.com/docs/reference/engine/globals/LuaGlobals#require
- https://rfcs.luau.org/new-require-by-string-semantics.html · https://rfcs.luau.org/require-by-string-aliases.html
