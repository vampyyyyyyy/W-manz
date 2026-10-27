---
aliases: [Combat states, Attack phases, Windup Active Recovery, Combat FSM]
tags:
  - roblox-dev
  - systems/combat
type: architecture
last_updated: 2026-10-27
status: complete
---
# Combat State Machine

> **TL;DR:** Every attack moves through **Windup → Active → Recovery**, in frame-like timings defined in data. Defensive and disruptive states (**Blocking, Parrying, Dashing, Stunned, Knocked, Dead**) gate what's legal. The **server's** FSM is authoritative and enforces timings with **server time**. The client runs the same FSM for instant feel and gets corrected if it disagrees.

## States & legal transitions
| From → To | Idle | Windup | Active | Recovery | Block | Parry | Dash | Stunned |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Idle** | | ✔ | | | ✔ | ✔ | ✔ | forced |
| **Windup** | (feint) | | ✔ (auto) | | | | cancel? | forced |
| **Active** | | | | ✔ (auto) | | | | forced |
| **Recovery** | ✔ (auto) | ✔ (combo window) | | | | | ✔ (cancel window) | forced |
| **Block** | ✔ | | | | | ✔ (if parry tech) | | guard-break |
| **Stunned** | ✔ (timer) | | | | | | | refresh |
"forced" = hit stun from the [[Damage_Pipeline]], which overrides the transition table.

## Server enforcement (sketch)
```luau
--!strict
local Attacks = require(game.ReplicatedStorage.Shared.Attacks)
type Fighter = { state: string, stateUntil: number, attackId: string?, swingSeq: number, hitList: { [Model]: boolean } }

local function startAttack(f: Fighter, attackId: string, seq: number): boolean
	local atk = Attacks[attackId]
	local now = workspace:GetServerTimeNow()
	if not atk then return false end
	if f.state == "Recovery" then
		-- allow chaining only inside the combo window (end of recovery) and only into listed moves
		local current = f.attackId and Attacks[f.attackId]
		if not (current and table.find(current.cancelInto, attackId) and now >= f.stateUntil - 0.12) then return false end
	elseif f.state ~= "Idle" then
		return false
	end
	f.state, f.attackId, f.swingSeq = "Windup", attackId, seq
	f.stateUntil = now + atk.windup
	table.clear(f.hitList)
	return true
end

-- per Heartbeat: advance Windup→Active→Recovery→Idle using stateUntil; accept hit claims only in Active (+ small slack)
```

## Client/server split
- The client transitions immediately (anim, trail, SFX) and sends `Attack(attackId, seq)`.
- The server accepts or rejects. On reject, it sends a correction and the client snaps back to Idle (rare when the inputs are honest).
- Replicate `State` and `StunUntil` as attributes so other clients can show reactions (stagger anims, i-frame flashes) ([[Attributes]]).

## Edge cases that bite
- **Death/stun mid-windup** must cancel pending hit windows. Always clean up on exit ([[Animation_Events_and_Markers]]).
- **Lag:** give hit-claim acceptance a small grace window after Active ends (~0.1 s), with rewind ([[Lag_Compensation]]).
- **Simultaneous hits** (trades): decide on a policy (both land vs priority) and keep it deterministic.

## Related
[[Finite_State_Machines]] · [[Combat_System_Architecture]] · [[Combo_Systems_and_Input_Buffering]] · [[Damage_Pipeline]] · [[Block_Parry_and_IFrames]] · [[Status_Effects]] · [[Server_Authoritative_Cooldowns]] · [[Hit_Validation]] · [[Animation_Events_and_Markers]] · [[MOC_Combat_Systems]]

## Sources
- Pattern synthesized from Roblox security guidance (server-side state validation) and fighting-game frame-data conventions
- https://create.roblox.com/docs/scripting/security/security-tactics · https://create.roblox.com/docs/animation/events · https://luau.org/types/basic-types
