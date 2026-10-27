---
aliases: [Buffs, Debuffs, Stun, Slow, Burn, Bleed, DoT, Status effect system]
tags:
  - roblox-dev
  - systems/combat
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Status Effects (Buffs/Debuffs)

> **TL;DR:** Store effects as **server-side records** `{ id, source, stacks, expiresAt, tickEvery, nextTick }` keyed per target. Advance them in **one** Heartbeat loop, not one thread per effect. Define stacking rules (refresh, extend, stack, ignore). Replicate a compact view (attributes or bitflags) for client visuals. Put immunities and diminishing returns in from day one.

## Data model
```luau
--!strict
type Effect = {
	id: string,             -- "Stunned", "Burn", "Slow", "IFrames", "SuperArmor"
	source: Model?,
	stacks: number,
	expiresAt: number,      -- server time
	tickEvery: number?,     -- DoT/HoT period
	nextTick: number?,
	magnitude: number,      -- slow %, burn dps, etc.
}
local effects: { [Model]: { [string]: Effect } } = {}

local RULES = table.freeze({
	Stunned = { stacking = "refresh_longest", dr = true },     -- diminishing returns per window
	Burn    = { stacking = "stack", maxStacks = 5, tick = 0.5 },
	Slow    = { stacking = "strongest" },
	IFrames = { stacking = "refresh_longest" },
})
```

## One loop to rule them
```luau
game:GetService("RunService").Heartbeat:Connect(function()
	local now = workspace:GetServerTimeNow()
	for target, list in effects do
		for id, e in list do
			if e.tickEvery and e.nextTick and now >= e.nextTick then
				e.nextTick += e.tickEvery
				Damage.applyDot(e.source, target, id, e.magnitude * e.stacks)     -- through the pipeline
			end
			if now >= e.expiresAt then
				list[id] = nil
				StatusEffects.onExpired(target, id)
			end
		end
		if next(list) == nil then effects[target] = nil end      -- no leaks
	end
end)
```
Clean up on the target's `Destroying` or death ([[Memory_Leaks]]).

## Replicating for visuals
Set a bitmask attribute (`Status = bit32.bor(STUNNED, BURNING)`) or individual attributes. Clients show icons, tints, particles and animations ([[Bitwise_Operations_bit32]], [[Attributes]], [[Cooldown_and_Ability_UI]]).

## Gameplay rules worth stealing
- **Diminishing returns** on hard CC: each stun within 10 s lasts 50% as long. Prevents stun-lock infinites ([[Combo_Systems_and_Input_Buffering]]).
- **Tenacity/immunity windows** after CC ends.
- **Movement effects** apply server-side (WalkSpeed or controller params) and are validated by [[Movement_Validation]] budgets.

## Related
[[Damage_Pipeline]] · [[Combat_State_Machine]] · [[Block_Parry_and_IFrames]] · [[Server_Authoritative_Cooldowns]] · [[Bitwise_Operations_bit32]] · [[Attributes]] · [[Cooldown_and_Ability_UI]] · [[task_Library]] · [[Memory_Leaks]] · [[MOC_Combat_Systems]]

## Sources
- Pattern; timing via https://create.roblox.com/docs/reference/engine/classes/Workspace#GetServerTimeNow
