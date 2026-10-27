---
aliases: [fastcall, imports, GETIMPORT, builtin functions, localizing globals]
tags:
  - roblox-dev
  - luau/compiler
type: concept
last_updated: 2026-10-27
status: complete
---
# Builtin Fastcalls & Imports

> **TL;DR:** Luau resolves global chains like `math.max` **once at load time** ("imports") and calls many builtins through a **fastcall** path with no stack frame. The old Lua trick `local max = math.max` is therefore mostly unnecessary. Both optimizations require a **pure environment**, and `getfenv`, `setfenv` or `loadstring` break them.

## Imports
`math.max(a, b)` would normally need two table lookups per call. Luau's compiler emits an import that resolves `math.max` when the script loads (2025: `GET_CACHED_IMPORT` in native code keeps blocks linear). It's invalidated by environment tampering ([[Globals_G_shared_and_getfenv]]).

## Fastcall builtins (non-exhaustive, per Luau docs)
`assert`, `type`, `typeof`, `rawget`/`rawset`/`rawequal`/`rawlen`, `getmetatable`/`setmetatable`, `tonumber`/`tostring`, **all of `math`** (except `noise`, `random`, `randomseed`), **all of `bit32`**, parts of `string` and `table`, `buffer.*`, `vector.*`, `select(n, ...)` (O(1) with `...`).
- `assert(cond)` with an unused result and a truthy condition is near-free.
- `bit32.extract` with constant field and width is extra fast.
- `math.floor` and friends may use SSE4.1 when available.

## Rules for hitting the fast path
```luau
local n = math.abs(x)           -- ✅ direct builtin call
local abs = math.abs; abs(x)    -- ✅ localized also works
local b = string.byte(s, 1)     -- ✅ function form
local b2 = s:byte(1)            -- ❌ method call: no fastcall
local f = cond and math.max or math.min; f(a, b)  -- ❌ indirect call
math.abs("5")                   -- ❌ falls back (string→number coercion path)
```

## Method calls on Roblox objects
`obj:Method()` on Instances uses **namecall**, a fast reflected dispatch. Caching `local getChildren = workspace.GetChildren` buys little in Luau and isn't recommended by the Luau team.

## Related
[[Luau_Compiler_Optimizations]] · [[Native_Code_Generation]] · [[Globals_G_shared_and_getfenv]] · [[Luau_Micro_Optimizations]] · [[Math_Library]] · [[Bitwise_Operations_bit32]] · [[Vector_Library]] · [[Buffer_Library]] · [[String_Library_and_Patterns]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://luau.org/performance#importing-global-access-chains · https://luau.org/performance#specialized-builtin-function-calls
