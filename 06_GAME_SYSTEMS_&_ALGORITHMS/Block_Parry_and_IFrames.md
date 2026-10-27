---
aliases: [Blocking, Parry, Perfect block, I-frames, Invincibility frames, Guard break, Posture]
tags:
  - roblox-dev
  - systems/combat
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Block, Parry & I-Frames

> **TL;DR:** **Block** reduces damage while held (it costs a guard/posture meter, and heavies guard-break). **Parry** is a short timing window at block start (or a separate input) that negates the hit and staggers the attacker. **I-frames** are temporary immunity (dodges, rolls, bursts). All three are **server-side states with timestamps**. Lag makes timing windows tricky, so be explicit about whose timeline decides.

## Server model
```luau
--!strict
type Defense = { blockingSince: number?, posture: number, iframesUntil: number, lastParryAt: number }
const PARRY_WINDOW = 0.18           -- seconds after block start
const PARRY_COOLDOWN = 0.9          -- prevents spam-parry
const BLOCK_POSTURE_COST = 12

local function resolveDefense(d: Defense, attackKind: "Light" | "Heavy" | "Unblockable", hitTime: number): "IFrame" | "Parry" | "Block" | "GuardBreak" | "Hit"
	if hitTime < d.iframesUntil then return "IFrame" end
	if d.blockingSince and attackKind ~= "Unblockable" then
		if hitTime - d.blockingSince <= PARRY_WINDOW and hitTime - d.lastParryAt > PARRY_COOLDOWN then
			d.lastParryAt = hitTime
			return "Parry"
		end
		if attackKind == "Heavy" then
			d.posture -= BLOCK_POSTURE_COST * 2
		else
			d.posture -= BLOCK_POSTURE_COST
		end
		if d.posture <= 0 then return "GuardBreak" end
		return "Block"
	end
	return "Hit"
end
```
The result feeds the [[Damage_Pipeline]] (chip damage, stagger, posture regen).

## Latency and fairness
- The **defender** pressed block on *their* screen before the hit landed there. Under classic netcode, use the **server receive time** of the block request minus a bounded latency estimate (`player:GetNetworkPing()`), capped (e.g. ≤ 150 ms), to judge parries ([[Lag_Compensation]]).
- Always use the **same timeline rule** for both players, and document it for your team. Inconsistent rules feel like "parry doesn't work".
- Under [[Server_Authority_Model|server authority]], inputs are simulated on aligned frames, so parry windows become frame-exact on the server.

## I-frames in practice
- Dodge: `iframesUntil = now + 0.25` starting slightly after the dodge begins (no instant panic button), with a cooldown ([[Server_Authoritative_Cooldowns]]).
- Visual: flash or desaturate the character (client) while the replicated `IFrames` status is active ([[Status_Effects]]).
- Respawn protection: i-frames until first action or N seconds.

## Feedback
Parry: big spark, hitstop on both, distinct SFX, attacker stagger anim. Block: smaller sparks and pushback. Guard break: unique sound, stun, camera punch ([[Hitstop_and_Impact_Feel]], [[Camera_Shake]], [[VFX_Composition_and_Timing]]).

## Related
[[Damage_Pipeline]] · [[Combat_State_Machine]] · [[Status_Effects]] · [[Lag_Compensation]] · [[Server_Authoritative_Cooldowns]] · [[Hitstop_and_Impact_Feel]] · [[Combo_Systems_and_Input_Buffering]] · [[Server_Authority_Model]] · [[MOC_Combat_Systems]]

## Sources
- Pattern; ping API https://create.roblox.com/docs/reference/engine/classes/Player#GetNetworkPing
