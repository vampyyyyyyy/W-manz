---
aliases: [Cooldowns, Ability cooldowns, Server cooldowns, Debounce]
tags:
  - roblox-dev
  - systems/combat
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Server-Authoritative Cooldowns

> **TL;DR:** Store **"ready at" timestamps** on the server (`readyAt[player][ability] = now + cd`) and reject early casts. The client shows its own predicted cooldown for UI, and the server's copy is the truth. Use server time (`workspace:GetServerTimeNow()`, or `time()` under server authority), never client timestamps ([[Exploit_Threat_Model]]).

## Pattern
```luau
--!strict
local readyAt: { [Player]: { [string]: number } } = {}
const LATENCY_GRACE = 0.08       -- tolerate early-by-a-hair requests from laggy clients

local function tryUse(player: Player, ability: string, cooldown: number): boolean
	local now = workspace:GetServerTimeNow()
	local t = readyAt[player]
	if not t then t = {}; readyAt[player] = t end
	local ready = t[ability] or 0
	if now + LATENCY_GRACE < ready then return false end     -- still cooling down
	t[ability] = now + cooldown
	return true
end

game.Players.PlayerRemoving:Connect(function(p) readyAt[p] = nil end)
```
Send `readyAt` back to the client (or the cooldown start) so the UI ring matches exactly ([[Cooldown_and_Ability_UI]]).

## Debounce vs cooldown vs rate limit
| Tool | Purpose |
| --- | --- |
| **Debounce** (a bool flag) | Prevent re-entry while a yielding action is in progress (e.g. a door animation) |
| **Cooldown** (timestamp) | Game rule: "Fireball every 5 s" |
| **Rate limit** (token bucket) | Anti-spam: cap request frequency regardless of rules ([[Remote_Rate_Limiting]]) |
Use all three where appropriate. They solve different problems.

## Extras
- **Charges:** store `{ charges, nextChargeAt }` for "2 dashes, recharge 3 s each".
- **Cooldown reduction stats:** compute at cast time from server-side stats.
- **Global cooldown** between abilities prevents macro bursts. Combine with the combat FSM ([[Combat_State_Machine]]).

## Related
[[Combat_State_Machine]] · [[Remote_Rate_Limiting]] · [[Cooldown_and_Ability_UI]] · [[Status_Effects]] · [[Hit_Validation]] · [[Exploit_Threat_Model]] · [[Custom_Movement_Abilities]] · [[Server_Authority_Model]] · [[MOC_Combat_Systems]]

## Sources
- https://create.roblox.com/docs/scripting/debounce · https://create.roblox.com/docs/scripting/security/client-server-boundary
