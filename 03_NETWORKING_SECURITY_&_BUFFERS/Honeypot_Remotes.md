---
aliases: [Honeypot, Decoy remote, Directional remote check]
tags:
  - roblox-dev
  - security/detection
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Honeypot Remotes

> **TL;DR:** A honeypot is a remote that **no legitimate client code ever fires**. Any traffic on it comes from someone poking at your networking with an executor, so it's one of the few near-zero-false-positive cheat signals on Roblox. A cousin trick is **directional misuse**: a server→client remote that suddenly fires `OnServerEvent`.

## Problem
Exploiters enumerate `ReplicatedStorage` and probe remotes that look valuable (`GiveCash`, `AdminCommand`, `SetLevel`). Normal detection is probabilistic ([[Server_Side_Detection_Heuristics]]). A honeypot hit is close to proof.

## Solution
```luau
--!strict
-- Server: create decoys that blend in with real remotes (same folder, same naming style)
local Players = game:GetService("Players")
local Net = game.ReplicatedStorage:WaitForChild("Net")

local function flag(player: Player, reason: string)
	warn(("[AC] %s (%d) tripped %s"):format(player.Name, player.UserId, reason))
	-- log to your analytics/webhook pipeline here, then remove them from the session
	player:Kick("Connection error (279)") -- vague on purpose: don't teach the exploiter
end

for _, name in { "UpdateCurrency", "AdminRequest", "SetStat" } do
	local decoy = Instance.new("RemoteEvent")
	decoy.Name = name
	decoy.OnServerEvent:Connect(function(player) flag(player, "honeypot:" .. name) end)
	decoy.Parent = Net
end

-- Directional check: these remotes are only ever FireClient'ed by the server
for _, remote in Net.ServerToClient:GetChildren() do
	if remote:IsA("RemoteEvent") then
		remote.OnServerEvent:Connect(function(player) flag(player, "wrong-direction:" .. remote.Name) end)
	end
end
```

## Why it works
Your own client code never references the decoys, so the legitimate traffic rate is exactly zero. Remote spies show the decoys as tempting targets. Direction misuse works the same way: no LocalScript calls `FireServer` on a server→client channel.

## Variations & pitfalls
- **Refactor risk:** if you rename a real remote and an old client build still fires it during a rolling update, it *looks* like a honeypot hit. Delete real remotes cleanly and test in [[Studio_Testing_Modes]].
- Prefer **kick + log** over an instant permanent ban. Escalate with the [[Ban_API_and_Consequences|Ban API]] once you have repeated evidence.
- **Delay visible consequences** (randomized seconds or minutes later) so exploiters can't easily bisect which remote is the trap.
- Free models and plugins can contain code that fires remotes. Audit them ([[Third_Party_Code_and_Backdoors]]).
- With IDL networking ([[Blink_IDL]], [[Zap_IDL]]) there are fewer named remotes to imitate. Decoys must match whatever your real layout looks like.

## Related
[[Server_Side_Detection_Heuristics]] · [[Ban_API_and_Consequences]] · [[Exploit_Threat_Model]] · [[RemoteEvents_and_RemoteFunctions]] · [[Remote_Architecture_Patterns]] · [[Auto_Farm_and_Remote_Spam_Exploits]] · [[Defensive_Design]] · [[Access_Control_and_Confidentiality]] · [[MOC_Anti_Exploit]]

## Sources
- https://create.roblox.com/docs/scripting/security/server-side-detection#honeypots
