---
aliases: [Luau, Roblox Lua, Luau language]
tags:
  - roblox-dev
  - luau/language
type: concept
last_updated: 2026-10-27
status: complete
---
# Luau Overview

> **TL;DR:** Luau is Roblox's open-source language derived from **Lua 5.1**. It adds gradual typing, a fast interpreter with an optimizing compiler, optional native code generation, sandboxing, and modern syntax (`const`, string interpolation, `continue`, `+=`, if-expressions, generalized iteration, attributes). It's developed in the open at `luau-lang/luau`, with language changes going through RFCs ([[Luau_RFC_Process]]).

## What makes Luau different from Lua
| Area | Luau | Notes |
| --- | --- | --- |
| Types | Gradual, structural types with `--!strict` | [[Luau_Type_System]], [[Type_Checking_Modes]], [[New_Type_Solver]] |
| Syntax | `const`, `continue`, compound ops, `if … then … else` expressions, backtick strings, `//`, attributes | [[Luau_Syntax_Extensions]], [[Const_Bindings]], [[String_Interpolation]], [[Luau_Attributes]] |
| Iteration | `for k, v in t do`, plus the `__iter` metamethod | [[Generalized_Iteration]] |
| Performance | Tuned interpreter, compiler `-O2`, fastcalls, imports, inline caching, opt-in JIT | [[Luau_Compiler_Optimizations]], [[Builtin_Fastcalls_and_Imports]], [[Native_Code_Generation]] |
| Value types | Native `vector`, `buffer` | [[Vector_Library]], [[Buffer_Library]] |
| Safety | Sandboxed: no `io`, no `debug` internals, no bytecode loading, deprecated `getfenv`/`setfenv` | [[Luau_Sandboxing]], [[Globals_G_shared_and_getfenv]] |
| Missing on purpose | `goto`, integers/bitwise operators (use `bit32`), `__gc`, `<close>` | [[Luau_Lua_Compatibility]], [[Bitwise_Operations_bit32]] |

## The modern Luau checklist (2026)
```luau
--!strict
const MAX_HP = 100                                       -- const binding (2025)
type Fighter = { read name: string, hp: number }         -- read-only property modifier

local function damage(f: Fighter, amount: number): Fighter
	f.hp = math.clamp(f.hp - amount, 0, MAX_HP)
	return f
end

local roster: { Fighter } = { { name = "Ari", hp = 100 } }
for _, f in roster do                                    -- generalized iteration
	damage(f, 15)
	print(`{f.name} has {f.hp} HP`)                      -- string interpolation
end
local alive = if roster[1].hp > 0 then "yes" else "no"   -- if-expression
```

## Where Luau runs
Roblox (client, server, Studio plugins), standalone (`luau` CLI, [[Lune]]), other engines and products (it's MIT-licensed and embeddable: [[Luau_C_API_and_Embedding]]). The language core is the same everywhere. Roblox adds its own globals and types (`Instance`, `Vector3`, `task`, `game`).

## Related
[[Luau_Lua_Compatibility]] · [[Luau_Type_System]] · [[Luau_Syntax_Extensions]] · [[Native_Code_Generation]] · [[Luau_Compiler_Optimizations]] · [[Luau_Sandboxing]] · [[Luau_CLI_Tools]] · [[Luau_RFC_Tracker]] · [[Legacy_Code_Smells]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://luau.org (docs) · https://github.com/luau-lang/luau · https://rfcs.luau.org
- https://create.roblox.com/docs/luau
