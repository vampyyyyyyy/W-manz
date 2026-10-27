---
aliases: [--!optimize, O2, Constant folding, Inlining, Loop unrolling, Bytecode compiler]
tags:
  - roblox-dev
  - luau/compiler
type: concept
last_updated: 2026-10-27
status: complete
---
# Luau Compiler Optimizations

> **TL;DR:** Luau compiles source → AST → bytecode with a multi-pass optimizing compiler. Roblox uses **`--!optimize 1` in Studio testing and `--!optimize 2` in live games**. O2 adds **function inlining, loop unrolling** and aggressive builtin constant folding. That's why a micro-benchmark in Studio can differ from production ([[Benchmarking_Methodology]]).

## What the compiler does
| Optimization | Level | Effect |
| --- | --- | --- |
| Deep **constant folding** across locals and functions | 1+ | `local A = 2; local B = A * 3` → constant 6. 2025: folds `string.char`/`sub`, string concatenation and interpolation, vector math, vector constants |
| Upvalue capture-by-value | always | Cheap closures ([[Closures_and_Upvalues]]) |
| **Imports** (`math.max` resolved at load) | always (pure envs) | [[Builtin_Fastcalls_and_Imports]] |
| Fastcall emission for builtins | always | [[Builtin_Fastcalls_and_Imports]] |
| Table shape prediction (`{}` then `v.x = …`) | always | Pre-sized tables ([[Table_Library]]) |
| **Function inlining** (local functions, non-recursive) | **2** | Cost model is per-call and aware of constant args (2025), so big functions with constant args can collapse |
| **Loop unrolling** (`for i = 1, 4`) | **2** | Constant bounds only |
| Builtin calls with constant args folded (`math.sqrt(16)`) | **2** | |
| `const * var` → `var * const` with typed numbers | 2025 | One instruction instead of two |

Inlining is **disabled for modules using `getfenv`/`setfenv`** ([[Globals_G_shared_and_getfenv]]).

## Write code the optimizer likes
```luau
--!strict
local DEBUG = false                 -- constant local: dead branches cost nothing (2025 cost model)
local SCALE = 0.5

local function scaled(x: number): number   -- small local function: inlining candidate at O2
	if DEBUG then print("scaled", x) end
	return x * SCALE
end
```
- Prefer `local function` for helpers. Only locals can be inlined.
- Keep "config" values as never-reassigned locals or [[Const_Bindings]] so they fold.
- Don't micro-inline by hand. Let O2 do it, then profile ([[Luau_Micro_Optimizations]]).

## Directive
`--!optimize 0|1|2` per script. Roblox recommends the defaults ([[Type_Checking_Modes]] lists all directives).

## Related
[[Builtin_Fastcalls_and_Imports]] · [[Native_Code_Generation]] · [[Luau_Micro_Optimizations]] · [[Closures_and_Upvalues]] · [[Const_Bindings]] · [[Globals_G_shared_and_getfenv]] · [[Table_Library]] · [[Benchmarking_Methodology]] · [[Luau_CLI_Tools]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://luau.org/performance#optimizing-compiler · https://create.roblox.com/docs/luau/comments#comment-directives
- https://luau.org/news/2025-12-19-luau-recap-runtime-2025
