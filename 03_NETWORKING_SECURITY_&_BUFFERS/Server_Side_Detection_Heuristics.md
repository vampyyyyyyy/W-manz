---
aliases: [Cheat detection, Suspicion score, Heuristics, Anti-cheat heuristics]
tags:
  - roblox-dev
  - security/detection
type: concept
last_updated: 2026-10-27
status: complete
---
# Server-Side Detection Heuristics

> **TL;DR:** Validation stops *impossible* requests. Heuristics catch *improbable* ones: things a human could technically do but almost never does. Treat each heuristic as a **signal**, add it to a decaying **suspicion score**, and only act when several independent signals line up.

## The three classic heuristics (Roblox security guide)
| Heuristic | Measures | Example |
| --- | --- | --- |
| **Fastest completion time** | Task time vs theoretical optimum (best path × max speed) | Obby record is 30 s, a run finishes in 5 s → teleport/speed |
| **Rate of gain** | Resource income vs max legit rate for their upgrades | 100 coins/min is max, but +10,000 in 1 s |
| **Action cadence** | Variance of intervals between repeated inputs | 100 casts at exactly 2.500 s → macro/bot ([[Auto_Farm_and_Remote_Spam_Exploits]]) |

Game-specific additions: impossible accuracy streaks, hits through walls on [[Hit_Validation]], ability usage while stunned, speed-bucket overflows from [[Movement_Validation]], [[Honeypot_Remotes]] hits (near-certain).

## Suspicion score pattern
```luau
--!strict
-- ServerScriptService/Suspicion.luau
local Players = game:GetService("Players")
local HALF_LIFE = 300 -- seconds; old signals fade
local THRESHOLDS = { log = 10, restrict = 40, kick = 80 }

type Entry = { score: number, last: number, reasons: { string } }
local entries: { [Player]: Entry } = {}

local Suspicion = {}

function Suspicion.add(player: Player, reason: string, weight: number)
	local now = os.clock()
	local e = entries[player] or { score = 0, last = now, reasons = {} }
	e.score *= 0.5 ^ ((now - e.last) / HALF_LIFE) -- exponential decay
	e.score += weight
	e.last = now
	table.insert(e.reasons, reason)
	if #e.reasons > 20 then table.remove(e.reasons, 1) end
	entries[player] = e
	if e.score >= THRESHOLDS.kick then
		-- correlate before acting: require >= 2 distinct reason types
		local kinds = {}
		for _, r in e.reasons do kinds[string.split(r, ":")[1]] = true end
		local n = 0
		for _ in kinds do n += 1 end
		if n >= 2 then player:Kick("Unexpected client behavior") end
	end
end

Players.PlayerRemoving:Connect(function(p) entries[p] = nil end)
return Suspicion
```

## Philosophy (official guidance)
- **The server decides.** Never ban on client-side detections alone. They're trivially spoofed ([[Exploit_Threat_Model]]).
- **Prevent harm first.** Rubber-band a speeder instead of kicking, and drop a malformed request instead of punishing.
- **Be proportional and reversible.** Assume false positives (lag spikes, legit shortcuts, skilled players).
- **Design > detection.** Detection supplements [[Server_Side_Validation]] and [[Defensive_Design]]. It doesn't replace them.

## Operational tips
- Log reasons with timestamps and send aggregate counts to analytics ([[AnalyticsService_Events]]) so you can see which rule fires the most and tune it.
- **Version your detection rules.** If a new rule suddenly flags 5% of players, it's broken, not a cheat wave.
- **Delay consequences** so cheaters can't bisect your rules ([[Ban_API_and_Consequences]]).

## Related
[[Ban_API_and_Consequences]] · [[Honeypot_Remotes]] · [[Auto_Farm_and_Remote_Spam_Exploits]] · [[Movement_Validation]] · [[Hit_Validation]] · [[Remote_Rate_Limiting]] · [[Defensive_Design]] · [[Exploit_Threat_Model]] · [[MOC_Anti_Exploit]]

## Sources
- https://create.roblox.com/docs/scripting/security/server-side-detection
