---
aliases: [Luau C API, lua_State, Embedding Luau, luau_load, Luau VM]
tags:
  - roblox-dev
  - luau/c-api
type: api
last_updated: 2026-10-27
status: complete
---
# Luau C API & Embedding

> **TL;DR:** Luau is an MIT-licensed C++ library (`luau-lang/luau`) you can embed in any program: compile source with `luau_compile`, load bytecode with `luau_load`, and drive it through a Lua 5.1-style stack API (`lua_State`). Roblox devs touch this through **tools built on it**: [[Lune]], [[Luau_LSP]], [[Darklua]], and the `luau` CLI ([[Luau_CLI_Tools]]). It's also why Roblox-only APIs need type definition files outside Studio.

## Architecture
```text
source ──Luau.Compiler──► bytecode ──luau_load──► VM (lua_State) ──► optional CodeGen (x64/arm64)
         Luau.Analysis (type checker, linter)      Luau.Require (require-by-string, 2025)
```
- Components: `Ast`, `Compiler`, `Analysis`, `VM`, `CodeGen`, `Require`. Use only what you need.
- `luaL_sandbox` / `luaL_sandboxthread` apply the readonly-globals model ([[Luau_Sandboxing]]).

## 2025 C API additions (Luau runtime recap)
- `lua_newuserdatataggedwithmetatable`: about 3x faster creation of small tagged userdata (colors, matrices).
- 16-byte alignment guarantee for userdata (with a compatible allocator).
- `lua_rawgetp`/`lua_rawsetp` (+ tagged variants) for lightuserdata keys.
- `luaL_callyieldable`: yieldable C functions can call other yieldable functions.
- Stackless `pcall`/`xpcall` in yieldable contexts. Better OOM robustness (`lua_checkstack` reports failure, `luau_load` doesn't throw on OOM, `lua_cpcall` is back).
- `lua_clonetable`, `lua_tolstringatom`.

## Minimal embed (C++ sketch)
```cpp
#include "lua.h"
#include "lualib.h"
#include "luacode.h"

size_t size = 0;
char* bytecode = luau_compile(src, srcLen, nullptr, &size);
lua_State* L = luaL_newstate();
luaL_openlibs(L);
luaL_sandbox(L);                         // freeze builtins
lua_State* T = lua_newthread(L);
luaL_sandboxthread(T);                   // per-script global table
if (luau_load(T, "=chunk", bytecode, size, 0) == 0)
    lua_pcall(T, 0, 0, 0);
free(bytecode);
```

## Related
[[Luau_CLI_Tools]] · [[Luau_Sandboxing]] · [[Lune]] · [[Luau_LSP]] · [[Darklua]] · [[Native_Code_Generation]] · [[Require_and_Module_Resolution]] · [[Luau_Overview]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://github.com/luau-lang/luau · https://luau.org/api
- https://luau.org/news/2025-12-19-luau-recap-runtime-2025
