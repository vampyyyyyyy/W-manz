---
aliases: [Speed hack detection, Teleport detection, Fly detection, Noclip detection, Anti speed]
tags:
  - roblox-dev
  - security/anti-exploit
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Movement Validation (Server-Side)

> **TL;DR:** Clients own their character's physics, so the server *observes* movement instead of simulating it ([[Network_Ownership]]). Validate the **distance travelled over time** with a burst-tolerant **leaky bucket**, project to the right plane, exempt your own teleports and abilities, and **rubber-band** instead of kicking. For competitive games, the real fix is the [[Server_Authority_Model]] (full release in 2026).

## Problem
Exploiters can teleport, fly, noclip, or set `WalkSpeed` locally **without firing any event your scripts could see**. Naive `distance > speed * dt` checks false-flag laggy players, because positions arrive in bursts. They also break for knockback, vehicles, launch pads and movement tech like [[ODM_Gear_System|ODM]] or [[Custom_Movement_Abilities|dashes]].

## Solution: leaky-bucket accumulator on the XZ plane
```luau
--!strict
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")

local CHECK_INTERVAL = 0.25
local BUCKET_CAPACITY = 40   -- studs of "excess" tolerated (lag bursts)
type Track = { lastPos: Vector3, lastValid: CFrame, excess: number, graceUntil: number }
local tracks: { [Player]: Track } = {}

-- Abilities register their legit max speed; default = WalkSpeed with slack
local function allowedSpeed(player: Player, hum: Humanoid): number
	local bonus = (player:GetAttribute("MoveBonusSpeed") :: number?) or 0 -- set by server-side ability code
	return hum.WalkSpeed * 1.25 + bonus
end

-- Call this from YOUR server teleports/knockbacks so they aren't flagged
local function grantGrace(player: Player, seconds: number)
	local t = tracks[player]
	if t then t.graceUntil = os.clock() + seconds end
end

local acc = 0
RunService.Heartbeat:Connect(function(dt)
	acc += dt
	if acc < CHECK_INTERVAL then return end
	local elapsed = acc
	acc = 0
	for _, player in Players:GetPlayers() do
		local char = player.Character
		local root = char and char:FindFirstChild("HumanoidRootPart") :: BasePart?
		local hum = char and char:FindFirstChildOfClass("Humanoid")
		if not (root and hum and hum.Health > 0) then continue end
		local t = tracks[player]
		if not t then
			tracks[player] = { lastPos = root.Position, lastValid = root.CFrame, excess = 0, graceUntil = 0 }
			continue
		end
		local delta = root.Position - t.lastPos
		local horizontal = Vector3.new(delta.X, 0, delta.Z).Magnitude -- XZ projection
		local budget = allowedSpeed(player, hum) * elapsed
		-- leak, then add overflow
		t.excess = math.max(0, t.excess - budget * 0.5) + math.max(0, horizontal - budget)
		if os.clock() < t.graceUntil then t.excess = 0 end
		if t.excess > BUCKET_CAPACITY or not math.isfinite(root.Position.X) then
			root.CFrame = t.lastValid -- rubber-band (server write replicates to the owner)
			root.AssemblyLinearVelocity = Vector3.zero
			t.excess = 0
			-- Suspicion.add(player, "speed:bucket", 10)
		else
			t.lastValid = root.CFrame
		end
		t.lastPos = root.Position
	end
end)
Players.PlayerRemoving:Connect(function(p) tracks[p] = nil end)
```

## Extending it
- **Noclip:** [[Raycasting|raycast]] from `lastPos` to the new position against **static, anchored** geometry only ([[Collision_Groups_and_Filtering|filter]] out dynamic parts). A hit through a solid wall is a strong signal. Use a small tolerance at corners.
- **Fly:** track continuous airtime with no falling velocity, using `Humanoid:GetState()` or floor raycasts. Exempt swimming, climbing, gliders and grapples.
- **Vertical:** validate separately. Gravity sets a maximum *rise* rate given your jump power and launchers.
- **Ability-aware budgets:** dashes, grapples and launch pads must raise the budget **server-side** (attribute or grace window set by server code), never because the client asked.

## Pitfalls
- Validation tuned for walking breaks physics-heavy games (vehicles, ragdoll, [[Knockback_and_Ragdoll]]). Profile real play sessions before enforcing.
- Rubber-banding a laggy player too eagerly feels awful. The bucket capacity is your fairness knob.
- Don't run per-frame raycasts for every player on big servers. Time-slice them ([[Time_Slicing_and_Frame_Budget]]).

## Related
[[Network_Ownership]] · [[Server_Authority_Model]] · [[Client_Prediction_and_Reconciliation]] · [[Server_Side_Detection_Heuristics]] · [[Remote_Rate_Limiting]] · [[Exploit_Threat_Model]] · [[Humanoid_and_Character_Model]] · [[ODM_Gear_System]] · [[Custom_Movement_Abilities]] · [[Raycasting]] · [[MOC_Movement_and_ODM]] · [[MOC_Anti_Exploit]]

## Sources
- https://create.roblox.com/docs/scripting/security/network-ownership#movement-validation
- https://create.roblox.com/docs/projects/server-authority
