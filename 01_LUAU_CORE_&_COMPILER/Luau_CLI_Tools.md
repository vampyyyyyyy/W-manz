---
aliases: [luau CLI, luau-analyze, luau-compile, Luau profiler]
tags:
  - roblox-dev
  - luau/tooling
type: framework
last_updated: 2026-10-27
status: complete
---
# Luau CLI Tools

> **TL;DR:** The `luau-lang/luau` releases ship command-line tools. `luau` runs scripts (with `--profile` for flamegraphs, `-O2`, `--codegen`), `luau-analyze` type-checks and lints, and `luau-compile` dumps bytecode, remarks or native IR/asm. Flags were verified against `CLI/src/*.cpp` in Oct 2026. They're great for benchmarking pure-Luau algorithms outside Studio, and for seeing *why* code is slow. For Roblox projects, [[Luau_LSP]] and [[Lune]] wrap the same engine with Roblox types.

## Tools
| Tool | Use |
| --- | --- |
| `luau file.luau` | Run a script (standard library only, no Roblox APIs) |
| `luau -O2 file.luau` | Match Roblox live-game optimization level ([[Luau_Compiler_Optimizations]]) |
| `luau --codegen file.luau` | Run with native code generation ([[Native_Code_Generation]]) |
| `luau --profile file.luau` | Sampling profiler → `profile.out`, then convert to a flamegraph with the repo's `tools/perfgraph.py`. Also prints GC time breakdown (mark/atomic/sweep) |
| `luau-analyze file.luau` | Type check + lint (`--mode=strict`, `--solver=new` or `--solver=old`, `--formatter=plain`/`gnu`, `--annotate`) |
| `luau-compile --remarks file.luau` | Shows compiler decisions (inlining, unrolling) |
| `luau-compile --text file.luau` | Human-readable bytecode (`-O2` to match live games) |
| `luau-compile --codegenir` / `--codegenasm file.luau` | Native codegen IR or assembly, to see what `@native` actually produced |
| `luau --coverage` / `--counters` | Coverage and VM counters for tests and benchmarks |

## Workflow: optimize a hot algorithm
1. Extract the pure-Luau part (no Instances) into a module.
2. Benchmark with `luau -O2` and `--codegen`, then profile ([[Benchmarking_Methodology]]).
3. Read `--remarks` to confirm inlining happened.
4. Port back and verify in Studio's [[Script_Profiler]] / [[MicroProfiler]].

## Install
GitHub releases of `luau-lang/luau`, or via a toolchain manager ([[Rokit]]: `rokit add luau-lang/luau`).

## Related
[[Luau_C_API_and_Embedding]] · [[Luau_Compiler_Optimizations]] · [[Native_Code_Generation]] · [[Benchmarking_Methodology]] · [[Luau_LSP]] · [[Lune]] · [[Rokit]] · [[Script_Profiler]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://luau.org/profile · https://github.com/luau-lang/luau/releases
