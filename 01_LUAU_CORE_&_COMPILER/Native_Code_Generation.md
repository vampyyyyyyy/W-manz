---
aliases: [Native codegen, --!native, JIT, NCG, Luau native code]
tags:
  - roblox-dev
  - luau/compiler
type: concept
last_updated: 2026-10-27
status: complete
---
# Native Code Generation

> **TL;DR:** `--!native` (whole script) or `@native` (one function) compiles Luau to **x64/arm64 machine code** instead of bytecode. On Roblox this applies to **server scripts**. It speeds up **compute-heavy Luau** (math, buffers, tight loops) by multiples, but does little for code dominated by Roblox API calls. There's a per-game native code size limit, so apply it surgically and measure.

## Enable
```luau
--!native                 -- top of a Script: all functions (and top-level if profitable)
@native local function hot(x: number) return x * x end   -- or per function
```
Behavior is identical with or without it. Only speed changes.

## What benefits
- ✅ Numeric loops, physics integration, noise generation ([[Noise_Functions]]), pathfinding grids, ECS systems ([[ECS_Libraries_Jecs_and_Matter]]), buffer serialization ([[Buffer_Library]]), vector math ([[Vector_Library]]).
- ❌ Code that mostly calls engine APIs (`Instance.new`, raycasts, property sets). The time is spent in C++, not Luau.
- ❌ Top-level code that runs once.

## Make it effective
- **Annotate types**, especially `Vector3`/`vector` params. Codegen specializes on annotated argument types (skipping tag checks on unmodified typed args, 2025). A wrong-typed call falls back to slower paths.
- Avoid **deoptimizers**: `getfenv`/`setfenv`, builtins called with wrong types (e.g. `math.asin("1")`) ([[Globals_G_shared_and_getfenv]]).
- Breakpoints disable native execution for that function while debugging ([[Studio_Debugger]]).

## Verify and measure
- [[Script_Profiler]] shows `<native>` next to natively running functions.
- The Luau heap view shows `[native]` memory ([[Luau_Heap_Analysis]]).
- `debug.dumpcodesize()` in the Command Bar (Server view) prints native code size per script and function vs the limit.

## Limits & errors
| Message | Meaning |
| --- | --- |
| `exceeded single code block instruction limit` | A block over 64K instructions. Split the function |
| `exceeded function code block limit` | Over 32K internal blocks. Simplify control flow |
| `exceeded total module instruction limit` | 1M instructions per script. Move big functions out or use targeted `@native` |
| `Memory allocation limit reached for native code generation` | Game-wide native memory budget hit. Remove `--!native` from big scripts |
| `internal lowering failure` | Split complex expressions, and file a bug |

## 2025 improvements (Luau recap)
Android support. `vector` ops lowered (dot → dot-product instruction, `lerp` → FMA). Load-store propagation for vectors, buffers, upvalues and userdata. Branch-free equality and `type(x) == "number"` checks. Integer instructions for buffer/`bit32` math. Longer linear basic blocks.

## Related
[[Luau_Attributes]] · [[Luau_Compiler_Optimizations]] · [[Builtin_Fastcalls_and_Imports]] · [[Luau_Micro_Optimizations]] · [[Script_Profiler]] · [[Benchmarking_Methodology]] · [[Parallel_Luau]] · [[Buffer_Library]] · [[Vector_Library]] · [[MOC_Luau_Core_and_Compiler]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://create.roblox.com/docs/luau/native-code-gen
- https://luau.org/news/2025-12-19-luau-recap-runtime-2025 · https://luau.org/performance
