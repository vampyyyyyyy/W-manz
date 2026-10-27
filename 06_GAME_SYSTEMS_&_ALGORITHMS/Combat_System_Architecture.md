---
aliases: [Combat system, Combat framework, Melee system architecture, Fighting game architecture]
tags:
  - roblox-dev
  - systems/combat
type: architecture
last_updated: 2026-10-27
status: complete
---
# Combat System Architecture

> **TL;DR:** A production Roblox combat system is a pipeline: **Input → client prediction (anim + VFX + local hit detection) → intent remote → server state machine + validation → server damage resolution → replicated results → every client's feedback**. The client makes it *feel* instant. The server makes it *true*. Keep both sides reading the **same data tables** (attack definitions) so timing, ranges and damage never drift.

## Data flow
```text
CLIENT (attacker)                                  SERVER                                       CLIENTS (all)
input (IAS/UIS) ─► ComboBuffer ─► StateMachine ─► play anim, trail, swing SFX (predicted)
                    │ hit window opens (anim marker)
                    ├─► local hitbox query (instant hit sparks, hitstop)
                    └─► Net.Attack(attackId, seq, aimDir) ─────► rate limit + validate state/cooldown
                         Net.HitClaim(seq, targets, t) ──────────► validate: distance, angle, window, LoS,
                                                                    i-frames, team; rewind if needed
                                                                   ─► DamagePipeline (armor, crits, block)
                                                                   ─► apply: Health, status effects, knockback
                                                                   ─► Net.HitConfirmed(...) ─────────────► damage numbers, hit react anim,
                                                                                                           VFX/SFX at confirmed position
```

## Components
| Component | Runs on | Responsibility |
| --- | --- | --- |
| Attack definitions (frozen tables) | Shared | `windup`, `active` window, `recovery`, range, hitbox size, damage, stun, knockback, cancel rules |
| [[Combat_State_Machine]] | Both (server authoritative) | Idle/Windup/Active/Recovery/Stunned/Blocking/Dashing. Who can do what, when |
| [[Combo_Systems_and_Input_Buffering]] | Client (+ server checks) | Buffer inputs during recovery, chain strings |
| Hit detection ([[Hitbox_Detection_Methods]]) | Client for feel, server for validation | Overlap or shapecast during the active window |
| [[Hit_Validation]] + [[Lag_Compensation]] | Server | Accept or reject claims with tolerances |
| [[Damage_Pipeline]] | Server | Modifiers, block and parry, armor, crits, events |
| [[Status_Effects]] | Server (replicated) | Stun, slow, bleed, i-frames, super-armor |
| Feedback ([[Hitstop_and_Impact_Feel]], [[Camera_Shake]], [[Damage_Numbers_and_Hit_Markers]]) | Clients | Juice, readability |
| Networking ([[Remote_Architecture_Patterns]]) | Both | Few typed remotes, sequence numbers, batching |

## Failure modes & exploits considered
- **Damage spoofing:** the server computes damage, so the client never sends numbers ([[Defensive_Design]]).
- **Speed attacks / animation cancels:** the server state machine enforces windup and recovery using server time ([[Server_Authoritative_Cooldowns]]).
- **Reach hacks:** distance and angle validation with latency slack ([[Hit_Validation]]).
- **Hit claims for out-of-window swings:** the server tracks each swing's `seq`, open window, and already-hit targets.
- **Lag-switch abuse:** cap rewind and reject stale claims ([[Lag_Compensation]]).
- **Desync of state:** replicate key state via attributes (`State`, `Stunned`), and under [[Server_Authority_Model|server authority]] put it in the simulation.

## Implementation notes
```luau
--!strict
-- Shared/Attacks.luau (frozen): single source of truth for client feel AND server validation
export type Attack = {
	read id: string, read anim: string,
	read windup: number, read active: number, read recovery: number,
	read range: number, read hitbox: Vector3, read damage: number,
	read stun: number, read knockback: number, read cancelInto: { string },
}
return table.freeze({
	Light1 = table.freeze({ id = "Light1", anim = "rbxassetid://0", windup = 0.12, active = 0.10, recovery = 0.22,
		range = 7, hitbox = Vector3.new(6, 5, 6), damage = 8, stun = 0.35, knockback = 6, cancelInto = { "Light2", "Dash" } }),
})
```

## Related
[[Combat_State_Machine]] · [[Hitbox_Detection_Methods]] · [[Hit_Validation]] · [[Damage_Pipeline]] · [[Combo_Systems_and_Input_Buffering]] · [[Status_Effects]] · [[Block_Parry_and_IFrames]] · [[Knockback_and_Ragdoll]] · [[Hitstop_and_Impact_Feel]] · [[Animation_Events_and_Markers]] · [[Lag_Compensation]] · [[MOC_Combat_Systems]]

## Sources
- https://create.roblox.com/docs/scripting/security/client-server-boundary#weapon-targeting
- https://create.roblox.com/docs/scripting/security/defensive-design
