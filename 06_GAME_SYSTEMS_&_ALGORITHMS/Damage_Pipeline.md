---
aliases: [Damage system, Damage calculation, Damage events, Armor, Crits, TakeDamage]
tags:
  - roblox-dev
  - systems/combat
type: architecture
last_updated: 2026-10-27
status: complete
---
# Damage Pipeline

> **TL;DR:** All damage goes through **one server function**: `Damage.apply(source, target, baseInfo)`. It runs ordered stages (validate → immunity/i-frames → block/parry → modifiers (buffs, armor, crits) → apply health → status effects and knockback → events and analytics) and returns a result. One choke point makes balance changes, logging, anti-cheat and feedback consistent ([[Defensive_Design]]).

## Stage order
```text
DamageRequest{ source, target, attackId, hitPart, position, kind = "Melee"|"Projectile"|"Environment" }
 1. Validate      target alive, not same team, source state legal          (Hit_Validation)
 2. Immunity      i-frames, spawn protection, ForceField, invulnerable states
 3. Defense       block (chip %), parry (negate + stagger attacker), guard break
 4. Modifiers     +attacker buffs, crit (server RNG), -armor/resist, headshot multipliers, clamp
 5. Apply         health -= final; record lastHitBy for kill credit
 6. Effects       stun/slow/bleed (Status_Effects), knockback impulse (Knockback_and_Ragdoll)
 7. Broadcast     HitConfirmed(target, amount, crit, position) → clients (numbers, VFX, sounds)
 8. Telemetry     counters for balance (dmg per weapon), suspicion signals (impossible DPS)
```

## Skeleton
```luau
--!strict
export type DamageResult = { applied: number, blocked: boolean, parried: boolean, crit: boolean, killed: boolean }

local Damage = {}
local rng = Random.new()

function Damage.apply(source: Model, target: Model, attack: { damage: number, critChance: number? }, info: { headshot: boolean? }): DamageResult?
	local hum = target:FindFirstChildOfClass("Humanoid")
	if not hum or hum.Health <= 0 then return nil end
	if StatusEffects.has(target, "IFrames") then return nil end
	local result: DamageResult = { applied = 0, blocked = false, parried = false, crit = false, killed = false }

	if StatusEffects.has(target, "Parrying") then
		result.parried = true
		StatusEffects.add(source, "Stunned", 0.8)            -- punish the attacker
		return result
	end
	local amount = attack.damage * Stats.outgoingMultiplier(source)
	if StatusEffects.has(target, "Blocking") then
		result.blocked = true
		amount *= 0.15                                        -- chip damage
	end
	if attack.critChance and rng:NextNumber() < attack.critChance then
		result.crit = true
		amount *= 1.5
	end
	if info.headshot then amount *= 1.25 end
	amount *= 1 - Stats.armor(target)                         -- 0..0.8
	amount = math.max(0, math.floor(amount + 0.5))

	hum.Health -= amount
	result.applied = amount
	result.killed = hum.Health <= 0
	CombatEvents.hit:Fire(source, target, result)             -- one place for VFX, numbers, analytics, kill feed
	return result
end
return Damage
```
Use `Humanoid.Health -= x` (or your own health attribute for custom rigs). `Humanoid:TakeDamage` skips damage when a `ForceField` is present, which is handy but implicit.

## Rules
- **Never** take damage values from clients. Only an `attackId` the server looks up ([[Combat_System_Architecture]]).
- Server RNG only (crits, procs).
- Rate-of-damage heuristics catch modified clients that slip past validation ([[Server_Side_Detection_Heuristics]]).

## Related
[[Combat_System_Architecture]] · [[Hit_Validation]] · [[Block_Parry_and_IFrames]] · [[Status_Effects]] · [[Knockback_and_Ragdoll]] · [[Damage_Numbers_and_Hit_Markers]] · [[Server_Side_Detection_Heuristics]] · [[Humanoid_and_Character_Model]] · [[Defensive_Design]] · [[MOC_Combat_Systems]]

## Sources
- https://create.roblox.com/docs/scripting/security/defensive-design (server computes damage)
