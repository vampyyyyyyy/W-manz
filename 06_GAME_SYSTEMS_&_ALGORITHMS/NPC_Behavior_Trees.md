---
aliases: [Behavior trees, NPC AI, Enemy AI, Utility AI, AI decision making]
tags:
  - roblox-dev
  - systems/ai
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# NPC Behavior Trees (and when to use FSMs/Utility AI)

> **TL;DR:** A **behavior tree** evaluates a tree of nodes each AI tick: **Selector** (try children until one succeeds), **Sequence** (run children until one fails), **Conditions** and **Actions** that return `Success`/`Failure`/`Running`. It scales better than FSMs when NPCs have many prioritized behaviors (combat, flee, patrol, investigate). Tick AI at **2–10 Hz**, staggered, on the server.

## Tiny BT runtime
```luau
--!strict
export type Status = "Success" | "Failure" | "Running"
export type Node = (ctx: any) -> Status

local BT = {}
function BT.Selector(children: { Node }): Node
	return function(ctx)
		for _, child in children do
			local s = child(ctx)
			if s ~= "Failure" then return s end
		end
		return "Failure"
	end
end
function BT.Sequence(children: { Node }): Node
	return function(ctx)
		for _, child in children do
			local s = child(ctx)
			if s ~= "Success" then return s end
		end
		return "Success"
	end
end
function BT.Condition(pred: (any) -> boolean): Node
	return function(ctx) return if pred(ctx) then "Success" else "Failure" end
end

-- Enemy brain: flee when low, fight when target in range, chase if seen, else patrol
local brain = BT.Selector({
	BT.Sequence({ BT.Condition(function(c) return c.hp < 0.2 end), Actions.flee }),
	BT.Sequence({ BT.Condition(function(c) return c.target and c.dist < 8 end), Actions.attack }),
	BT.Sequence({ BT.Condition(function(c) return c.target ~= nil end), Actions.chase }),
	Actions.patrol,
})
```
`Actions.*` return `"Running"` while in progress (moving along a path, winding up an attack). Store per-NPC state in `ctx` (the **blackboard**).

## FSM vs BT vs Utility
| Approach | Best for |
| --- | --- |
| [[Finite_State_Machines]] | Few clear states (door, simple mob, boss phases) |
| Behavior tree | Many prioritized, reusable behaviors |
| Utility AI (score each action, pick the max) | Emergent, nuanced choices (hunger vs threat vs loot). Scores are easy to tune |
Bosses often combine them: an FSM for phases, a BT inside each phase.

## Perception & performance
- Sensing: distance checks via [[Spatial_Partitioning]], line-of-sight [[Raycasting]], hearing from events (gunshots broadcast to nearby NPCs).
- **Stagger ticks:** `nextThink = now + 1/rate + random jitter`. Hundreds of NPCs × 10 Hz is fine if each tick is cheap ([[Time_Slicing_and_Frame_Budget]]).
- Expensive work (pathfinding, sensing) can run in [[Parallel_Luau]] Actors. Writes to Instances happen after `task.synchronize()`.

## Related
[[Finite_State_Machines]] · [[Pathfinding]] · [[Steering_and_Flocking]] · [[Spatial_Partitioning]] · [[Raycasting]] · [[Time_Slicing_and_Frame_Budget]] · [[Parallel_Luau]] · [[Entity_Component_System_Pattern]] · [[Combat_State_Machine]] · [[MOC_Game_Systems_and_Algorithms]]

## Sources
- Standard game-AI patterns; Roblox perception APIs per https://create.roblox.com/docs/workspace/raycasting
