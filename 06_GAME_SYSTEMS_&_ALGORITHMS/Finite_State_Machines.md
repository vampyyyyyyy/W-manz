---
aliases: [FSM, State machine, State pattern, Hierarchical state machine]
tags:
  - roblox-dev
  - systems/architecture
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Finite State Machines

> **TL;DR:** An FSM says "the thing is in exactly one state, and only these transitions are legal". It's the cure for boolean soup (`isAttacking and not isStunned and not isDashing...`). Use **typed singleton states**, **explicit transition tables**, and **enter/exit/update hooks**. FSMs power combat ([[Combat_State_Machine]]), movement ([[Custom_Movement_Abilities]]), weather ([[Weather_System_Architecture]]), UI flows and AI ([[NPC_Behavior_Trees]] for complex AI).

## Minimal typed FSM
```luau
--!strict
export type StateName = "Idle" | "Windup" | "Active" | "Recovery" | "Stunned" | "Dashing"

type StateDef = {
	enter: ((ctx: any, from: StateName?) -> ())?,
	exit: ((ctx: any, to: StateName) -> ())?,
	update: ((ctx: any, dt: number) -> StateName?)?,   -- return a state to transition
	allowed: { [StateName]: boolean },                  -- legal next states
}

local function createFSM(defs: { [StateName]: StateDef }, initial: StateName, ctx: any)
	local current: StateName = initial
	local fsm = {}
	function fsm.get(): StateName return current end
	function fsm.can(to: StateName): boolean return defs[current].allowed[to] == true end
	function fsm.go(to: StateName): boolean
		if not fsm.can(to) then return false end
		local from = current
		local exitFn = defs[from].exit
		if exitFn then exitFn(ctx, to) end
		current = to
		local enterFn = defs[to].enter
		if enterFn then enterFn(ctx, from) end
		return true
	end
	function fsm.update(dt: number)
		local u = defs[current].update
		local nextState = u and u(ctx, dt)
		if nextState then fsm.go(nextState) end
	end
	return fsm
end
```

## Design tips
- **Transitions as data** make illegal moves impossible and easy to audit ("can Stunned go to Dashing?").
- **Forced transitions** (stun, death) can bypass `allowed` through a separate `force()` that still runs exit and enter hooks.
- **Hierarchical FSMs:** `Combat` (Idle/Attacking/Blocking) inside `Alive`, inside `Character`. Or run parallel FSMs (locomotion + combat + status) that consult each other.
- Replicate only the **state name** (an attribute) and let clients drive visuals from it ([[Attributes]]).
- For data-driven ability conflicts, the [[Character_Controllers_and_ControllerManager|CCL]] (labels, Blocks/Stops/Suspends, ExclusiveGroup) is effectively a declarative state system.

## Related
[[Combat_State_Machine]] · [[NPC_Behavior_Trees]] · [[Custom_Movement_Abilities]] · [[Weather_System_Architecture]] · [[Character_Controllers_and_ControllerManager]] · [[Attributes]] · [[Type_Refinements]] · [[Luau_Type_System]] · [[MOC_Game_Systems_and_Algorithms]]

## Sources
- Pattern reference; Luau singleton types per https://luau.org/types/basic-types
