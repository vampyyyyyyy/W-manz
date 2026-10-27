---
aliases: [Time slicing, Frame budget, Work spreading, Budgeted loops, Staggering]
tags:
  - roblox-dev
  - performance/scheduling
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Time-Slicing & Frame Budgets

> **TL;DR:** Spread big jobs across frames with a **per-frame time budget** (e.g. 1–2 ms) or an **item budget** (N per frame), and **stagger** periodic work across entities so it doesn't all land on the same frame. Roblox's weather sample does exactly this: ≤ 32 rain cells built per frame, and roof re-checks round-robin with credit-based budgets.

## Budgeted queue (time-based)
```luau
--!strict
local RunService = game:GetService("RunService")
local queue: { () -> () } = {}
const BUDGET = 0.002   -- 2 ms per frame

RunService.Heartbeat:Connect(function()
	local start = os.clock()
	while #queue > 0 and os.clock() - start < BUDGET do
		local job = table.remove(queue)   -- LIFO is cheapest (no shifting); use a head index for FIFO
		job()
	end
end)

local function schedule(job: () -> ()) table.insert(queue, job) end
```

## Credit-based round-robin (from the official RoofShelter module)
```luau
-- revisit every entry once per SWEEP_SECONDS, spending fractional credit each frame
local sweepCredit, cursor = 0, 1
local function step(dt: number, entries: { any }, SWEEP_SECONDS: number, refresh: (any) -> ())
	sweepCredit = math.min(sweepCredit + #entries * dt / SWEEP_SECONDS, #entries)
	local budget = math.floor(sweepCredit)
	sweepCredit -= budget
	for _ = 1, budget do
		if cursor > #entries then cursor = 1 end
		refresh(entries[cursor])
		cursor += 1
	end
end
```

## Staggering periodic work
- Give each NPC or system a random phase: `nextThink = now + interval * math.random()`. Then they spread out naturally ([[NPC_Behavior_Trees]]).
- Autosaves: jitter per player so 30 saves don't fire in one frame ([[DataStoreService]]).
- **Throttle replicated writes** (e.g. 15 Hz for sky and clock) ([[Weather_System_Architecture]]).

## When slicing isn't enough
Move heavy compute to [[Parallel_Luau]], or precompute offline (bake data into modules).

## Related
[[Task_Scheduler]] · [[RunService_Frame_Events]] · [[Parallel_Luau]] · [[NPC_Behavior_Trees]] · [[Weather_System_Architecture]] · [[Procedural_Generation]] · [[Coroutines]] · [[Fixed_Timestep_and_Tick_Rate]] · [[MicroProfiler]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://github.com/Roblox/resources/tree/main/experiences/weather-island (RainField.luau, RoofShelter.luau)
