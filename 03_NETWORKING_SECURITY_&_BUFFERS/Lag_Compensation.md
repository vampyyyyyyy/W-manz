---
aliases: [Server rewind, Backwards reconciliation, Favor the shooter, Position history]
tags:
  - roblox-dev
  - networking/netcode
type: concept
last_updated: 2026-10-27
status: complete
---
# Lag Compensation (Server Rewind)

> **TL;DR:** When a client says "I hit them", it saw targets as they were roughly one round trip ago. Lag compensation keeps a short **position history** per character on the server, then checks the hit against where the target *was* at the shooter's view time. Clamp the rewind window so high-ping players can't shoot around corners indefinitely.

## Why it's needed
Client view = server state from about `RTT/2` ago + **interpolation delay** (other players are rendered slightly in the past to smooth jitter). Without rewind, [[Hit_Validation]] against *current* positions rejects real hits on moving targets, and players feel "I clearly hit that!".

## Implementation sketch
```luau
--!strict
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local HISTORY_SECONDS, MAX_REWIND = 1.0, 0.25

type Sample = { t: number, cf: CFrame }
local history: { [Model]: { Sample } } = {}

RunService.Heartbeat:Connect(function()
	local now = workspace:GetServerTimeNow()
	for _, p in Players:GetPlayers() do
		local char = p.Character
		local root = char and char:FindFirstChild("HumanoidRootPart") :: BasePart?
		if char and root then
			local h = history[char] or {}
			table.insert(h, { t = now, cf = root.CFrame })
			while #h > 0 and now - h[1].t > HISTORY_SECONDS do table.remove(h, 1) end
			history[char] = h
		end
	end
end)

-- Position of `char` at server time `t` (clamped), linearly interpolated
local function rewind(char: Model, t: number): CFrame?
	local h = history[char]
	if not h or #h == 0 then return nil end
	local now = workspace:GetServerTimeNow()
	t = math.clamp(t, now - MAX_REWIND, now)
	for i = #h, 2, -1 do
		local a, b = h[i - 1], h[i]
		if a.t <= t and t <= b.t then
			return a.cf:Lerp(b.cf, (t - a.t) / math.max(b.t - a.t, 1e-6))
		end
	end
	return h[#h].cf
end
```
The client stamps shots with `workspace:GetServerTimeNow()`. The server **doesn't trust** that stamp blindly. It clamps it to `MAX_REWIND`, and you can also cross-check it against measured ping (`player:GetNetworkPing()`).

## Trade-offs
- **Favor the shooter** (rewind) vs **favor the target** (no rewind). Rewind causes "I got shot behind cover" moments for the victim. Cap the window (150–250 ms is common) and accept some loss for very high pings.
- Ring buffers are cheaper than `table.remove(h, 1)` for many characters ([[Luau_Micro_Optimizations]]).
- Rewinding full hitbox geometry is expensive. Usually you rewind the root CFrame and rebuild a simple box or capsule ([[Hitbox_Detection_Methods]]).
- Under the [[Server_Authority_Model]] the engine handles *movement* prediction and rollback for you. Hit rewind for shooters is still a game-level design decision.

## Related
[[Hit_Validation]] · [[Client_Prediction_and_Reconciliation]] · [[Server_Authority_Model]] · [[Fixed_Timestep_and_Tick_Rate]] · [[Hitbox_Detection_Methods]] · [[Projectile_Systems]] · [[UnreliableRemoteEvent]] · [[Combat_System_Architecture]] · [[CFrame_Math]] · [[MOC_Combat_Systems]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/Workspace#GetServerTimeNow
- https://create.roblox.com/docs/reference/engine/classes/Player#GetNetworkPing
