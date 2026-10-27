---
aliases: [Benchmarking, Benchmark, os.clock timing, Performance testing, Microbenchmarks]
tags:
  - roblox-dev
  - performance/methodology
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Benchmarking Methodology

> **TL;DR:** Benchmarks lie unless you control for **optimization level** (Studio playtests use `-O1`, live games `-O2`), **warm-up**, **GC noise**, **dead-code elimination** and **variance**. Run many iterations, take the median, compare in the same environment, and finally validate in the real game with the [[MicroProfiler]] or [[Script_Profiler]].

## Harness
```luau
--!strict
--!optimize 2          -- match live-game optimization level when benchmarking in Studio
local function bench(name: string, fn: () -> (), iterations: number, runs: number)
	for _ = 1, 3 do fn() end                         -- warm-up
	local times = table.create(runs)
	for r = 1, runs do
		local t0 = os.clock()
		for _ = 1, iterations do fn() end
		times[r] = (os.clock() - t0) / iterations
	end
	table.sort(times)
	local median = times[(runs + 1) // 2]
	print(string.format("%-24s median %.3f µs  (min %.3f, max %.3f)", name, median * 1e6, times[1] * 1e6, times[runs] * 1e6))
end

local sink = 0                                     -- consume results so work isn't optimized away
bench("vector.dot", function() sink += vector.dot(vector.create(1, 2, 3), vector.create(4, 5, 6)) end, 100000, 15)
```

## Rules
1. **Same conditions:** same device, same place state, no other heavy scripts, and Studio on battery vs plugged in matters on laptops.
2. **Optimization level:** add `--!optimize 2` or test in a published test place. Studio defaults to O1 ([[Luau_Compiler_Optimizations]]).
3. **Constant folding traps:** benchmarks over constants can be folded at compile time. Use values from inputs.
4. **Native code:** benchmark with and without `@native`. Only keep it where it wins ([[Native_Code_Generation]]).
5. **Statistics:** median of ≥ 10 runs. Report min and max. Distrust differences under ~5%.
6. **End-to-end check:** a micro win that doesn't show in frame time doesn't matter ([[Performance_Optimization_Workflow]]).
7. Pure-Luau algorithms can be benchmarked outside Studio with `luau -O2 --codegen` ([[Luau_CLI_Tools]]).

## Related
[[Performance_Optimization_Workflow]] · [[MicroProfiler]] · [[Script_Profiler]] · [[Luau_Micro_Optimizations]] · [[Luau_Compiler_Optimizations]] · [[Native_Code_Generation]] · [[Luau_CLI_Tools]] · [[Testing_Frameworks]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://create.roblox.com/docs/luau/comments#comment-directives (optimize levels) · https://luau.org/profile
