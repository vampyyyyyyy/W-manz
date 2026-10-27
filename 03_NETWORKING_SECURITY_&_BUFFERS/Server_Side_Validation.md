---
aliases: [Input validation, Remote validation, Sanity checks, Never trust the client]
tags:
  - roblox-dev
  - security/validation
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Server-Side Validation

> **TL;DR:** Every value that crosses from client to server goes through three gates before it touches game state. **Type and structure** (is it really a `Vector3`, or a table pretending to be an Instance?). **Value** (finite, in range, integer where needed). **Context and permission** (is this player alive, close enough, allowed, off cooldown?). Rejections should be cheap and silent, and they feed your detection score.

## The three layers (Roblox security guide)
1. **Context/permission:** needed for anything that grants rewards, touches progression, affects other players, or has distance/timing rules. Is the character alive? Near the shop? Does the player own the key?
2. **Type and structure:** exploiters send valid-looking but oversized or malformed data. Huge strings, deep tables, or **tables impersonating Instances** like `{ClassName = "NumberValue", Value = 0}`.
3. **Value:** quantities > 0, real item ids, integers where integers are expected, and **NaN/inf rejected** with `math.isfinite` ([[NaN_and_Infinity_Exploits]]).

## Reusable validators
```luau
--!strict
-- ReplicatedStorage/Shared/Validate.luau (pure functions; safe to share)
local V = {}

function V.finite(x: unknown): boolean
	return typeof(x) == "number" and math.isfinite(x)
end

function V.int(x: unknown, min: number, max: number): boolean
	return V.finite(x) and (x :: number) % 1 == 0 and (x :: number) >= min and (x :: number) <= max
end

function V.vector3(v: unknown, maxMagnitude: number?): boolean
	if typeof(v) ~= "Vector3" then return false end
	local vec = v :: Vector3
	if not (math.isfinite(vec.X) and math.isfinite(vec.Y) and math.isfinite(vec.Z)) then return false end
	return maxMagnitude == nil or vec.Magnitude <= maxMagnitude
end

function V.unitVector(v: unknown): boolean
	return V.vector3(v) and math.abs((v :: Vector3).Magnitude - 1) < 1e-3
end

-- Real Instance (not a spoofed table) of the right class, inside the expected container
function V.instance(x: unknown, className: string, ancestor: Instance?): boolean
	if typeof(x) ~= "Instance" then return false end
	local inst = x :: Instance
	return inst:IsA(className) and (ancestor == nil or inst:IsDescendantOf(ancestor))
end

-- Bounded, valid UTF-8 string (DataStores reject invalid UTF-8)
function V.string(x: unknown, maxLen: number): boolean
	if typeof(x) ~= "string" or #x > maxLen then return false end
	return utf8.len(x) ~= nil
end

-- Flat array of at most n elements, each passing `each`
function V.array(x: unknown, n: number, each: (unknown) -> boolean): boolean
	if typeof(x) ~= "table" then return false end
	local t = x :: { [unknown]: unknown }
	local count = 0
	for k, v in t do
		count += 1
		if count > n or typeof(k) ~= "number" or not each(v) then return false end
	end
	return count == #t -- rejects holes/mixed keys
end

return V
```
Use them at the top of every handler. Fail fast, return early, and never `error()` inside a handler on bad input.

## Context checks that catch the most cheats
- **Distance:** `(root.Position - target.Position).Magnitude <= MAX + latencySlack` ([[Hit_Validation]]).
- **State:** alive, not stunned, not in a cutscene, correct [[Combat_State_Machine]] state.
- **Ownership:** the item is in *their* server-side inventory ([[Inventory_Systems]]), not "an item that exists".
- **Timing:** the server stamps cooldowns ([[Server_Authoritative_Cooldowns]]). Client timestamps are untrusted.
- **Line of sight:** a server [[Raycasting|raycast]] against *static* geometry only, so latency doesn't cause false rejects.

## Pitfalls
- `type()` returns `"userdata"` for every Roblox type. Use `typeof()` ([[Typeof_vs_type]]).
- Range checks alone are bypassed by NaN, so **always** check finiteness first.
- Validate **every key and value** of incoming tables before saving them. NaN or nil indices and invalid UTF-8 break DataStore writes and enable dupes ([[Data_Duplication_and_Trade_Exploits]]).
- Don't validate on the client and skip the server. Client checks are for responsiveness only ([[Exploit_Threat_Model]]).
- Runtime type-checker libraries are popular for this, notably `t` by osyrisrblx. IDL tools ([[Blink_IDL]], [[Zap_IDL]]) generate the checks for you.

## Related
[[RemoteEvents_and_RemoteFunctions]] · [[NaN_and_Infinity_Exploits]] · [[Remote_Rate_Limiting]] · [[Exploit_Threat_Model]] · [[Hit_Validation]] · [[Movement_Validation]] · [[Client_Triggered_Instance_Security]] · [[Defensive_Design]] · [[Data_Duplication_and_Trade_Exploits]] · [[Typeof_vs_type]] · [[MOC_Anti_Exploit]]

## Sources
- https://create.roblox.com/docs/scripting/security/client-server-boundary#validating-remote-inputs
- https://create.roblox.com/docs/scripting/security/security-tactics
