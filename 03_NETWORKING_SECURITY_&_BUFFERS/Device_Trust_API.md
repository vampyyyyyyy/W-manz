---
aliases: [Device Trust, IntegrityService, DeviceTrustLevel, EvaluatePlayerDeviceTrust, PlayerDeviceTrustLevel, Device attestation]
tags:
  - roblox-dev
  - networking/security
type: api
last_updated: 2026-11-02
status: complete
---
# Device Trust API (IntegrityService)

> **TL;DR:** Roblox attests each joining player's **device** (real hardware, not an emulator; OS not rooted or tampered with; Roblox app not modified) and exposes the result as `Player.DeviceTrustLevel`: `Pending` → `Unknown` / `None` / `Standard` / `Full`. **Roblox takes no action on it.** You decide: route players to trusted servers, gate features, or reject them through the `IntegrityService.EvaluatePlayerDeviceTrust` callback. As of Oct 29, 2026 only **Android, Chromebook and Meta Quest** are verified. **Web browsers always report `None`**, and iOS, macOS, Windows, Xbox and PlayStation report `Unknown` until supported. It measures how *hard* cheating is on a device, not whether someone *is* cheating, so it never replaces [[Server_Side_Validation]].

## The levels (and what they actually mean)
| Level | Meaning | Treat as |
| --- | --- | --- |
| `Pending` | Still checking. **Everyone starts here.** It can stay here for the whole session if the check never finishes, and it's always `Pending` in Studio | Not trusted for sensitive features |
| `Unknown` | Unsupported platform (**currently Windows, iOS, macOS and consoles**) or a Roblox-side error | **Your call.** Not the same as untrusted: today it's most of your PC and iPhone players |
| `None` | Failed the check, or a platform that can't be verified and is often used for cheating (**web browser**) | Low trust |
| `Standard` | Passed some checks | Trusted |
| `Full` | Passed every check | Trusted |

The property changes **once**, after `Players.PlayerAdded` fires and before the callback runs. Only the server and the player's own client can read it, and **every other client sees `Pending`**. It's tagged `Hidden`, `ReadOnly` and `NotReplicated` in the API reference.

**Never compare levels numerically.** `Unknown` sorts before `None`, so `level.Value > None.Value` silently excludes every Windows and iOS player. Always use an allow-list table.

## Platform coverage (as of Oct 29, 2026)
| Platform | Reports |
| --- | --- |
| Android, Chromebook, Meta Quest | `None` / `Standard` / `Full` (older Android hardware may be unable to reach `Standard`/`Full` even untampered) |
| Web browser | Always `None` ("can't be verified") |
| iOS, macOS, Windows, Xbox, PlayStation | `Unknown` ("coming soon") |

So **today this mainly separates tampered or emulated Android devices from the rest.** PC exploiters on Windows report `Unknown`, the same as legitimate PC players. Re-check this table when Windows support lands, because that changes what an `Unknown` policy means overnight. Browser play from RDC 2026 ([[RDC_2026_Recap]]) will add more `None` players, mostly ordinary web users, so a `None` policy that rejects outright will hit them too.

## Recommended policy for battlegrounds / fighting games
The official genre table recommends **separate servers** for `Unknown` and `None`, and **trusted servers** for `Standard` and `Full`, with `Pending` waiting for a result. In practice, for a combat game:
- **Casual servers: everyone.** Don't reject anyone just for being low trust.
- **Ranked / leaderboard queues:** start with `Standard`, `Full` **and `Unknown`**. Excluding `Unknown` today would lock out every PC, iPhone and console player. Tighten this per platform once more platforms report real levels.
- **Trading and gifting:** block `None` and `Pending` ([[Data_Duplication_and_Trade_Exploits]]).

Check the impact before enforcing anything: Creator Hub ▸ your game ▸ **Safety ▸ Anti-cheat** shows DAU, playtime and revenue split by trust level (owner or "view analytics" permission required).

## Production pattern: gate the ranked queue on the server
```luau
--!strict
-- ServerScriptService/RankedQueue (lobby place)
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TeleportService = game:GetService("TeleportService")

local RANKED_PLACE_ID = 0 -- your ranked place
-- Allow-list, never a numeric comparison. Unknown = currently most PC/iOS/console players.
local RANKED_LEVELS: { [Enum.PlayerDeviceTrustLevel]: boolean } = {
	[Enum.PlayerDeviceTrustLevel.Unknown] = true,
	[Enum.PlayerDeviceTrustLevel.Standard] = true,
	[Enum.PlayerDeviceTrustLevel.Full] = true,
}

local queueRemote = ReplicatedStorage:WaitForChild("Remotes"):WaitForChild("QueueRanked") :: RemoteEvent
local lastRequest: { [Player]: number } = {}

queueRemote.OnServerEvent:Connect(function(player: Player)
	-- Rate limit before doing any work (see Remote_Rate_Limiting)
	local now = os.clock()
	if now - (lastRequest[player] or 0) < 2 then return end
	lastRequest[player] = now

	if not RANKED_LEVELS[player.DeviceTrustLevel] then
		-- Pending lands here too: ask the client to retry in a few seconds
		queueRemote:FireClient(player, "RankedUnavailable", player.DeviceTrustLevel.Name)
		return
	end

	local ok, err = pcall(TeleportService.TeleportAsync, TeleportService, RANKED_PLACE_ID, { player })
	if not ok then
		warn(`Ranked teleport failed for {player.UserId}: {err}`)
	end
end)

game:GetService("Players").PlayerRemoving:Connect(function(player)
	lastRequest[player] = nil
end)
```
Players can reach the ranked place in other ways (joining a friend, a direct link), so **enforce the same policy in the ranked place** with the callback:
```luau
--!strict
-- ServerScriptService/DeviceTrustPolicy (ranked place). Assign the callback in ONE script only.
local IntegrityService = game:GetService("IntegrityService")

local RANKED_LEVELS: { [Enum.PlayerDeviceTrustLevel]: boolean } = {
	[Enum.PlayerDeviceTrustLevel.Unknown] = true,
	[Enum.PlayerDeviceTrustLevel.Standard] = true,
	[Enum.PlayerDeviceTrustLevel.Full] = true,
}

IntegrityService.EvaluatePlayerDeviceTrust = function(player: Player, measures)
	if RANKED_LEVELS[player.DeviceTrustLevel] then
		return { Action = Enum.PlayerDeviceTrustDecision.Accept }
	end
	return {
		Action = Enum.PlayerDeviceTrustDecision.Reject,
		Message = "Ranked isn't available on this device. Casual mode is still open.",
	}
end
```
Players can start playing **before** the callback runs, so the ranked place must not start a match for anyone still at `Pending`. Hold them in a pre-match area until their level resolves ([[Matchmaking_Customization]]).

## Callback rules (official)
- **Server only.** One callback per place, and the **last assignment wins**, so keep it in a single script.
- Called **once per player, as soon as the level is known**. It isn't called if the player leaves first.
- It can yield, but it **times out after about 10 seconds**, and then Roblox **accepts** the player. Avoid several DataStore or HTTP calls inside it.
- It **fails open**: no callback, a `nil` or invalid return, or an **error** all mean Accept. A bug can't lock players out, but it also silently disables your policy, so log callback errors.
- Return `{ Action = Accept | Reject, Message = string? }`. The message is text-filtered, falls back to a default "how to fix your device" message if filtering fails, and is truncated if too long.
- **`measures`** is a table of booleans: `IsPlatformVersionSecure`, `IsPlatformBootSecure`, `IsAppSecure`. A measure reads **`true` when it isn't available**, so passing every measure doesn't mean `Full`. Check the level first and use measures only to spot failures.
- **Don't reject from `PlayerAdded`.** The level usually isn't available yet, so you'd reject trusted players. If you need the level at join (matchmaking), yield the `PlayerAdded` thread and resume it from the callback with a timeout. The docs' "wait for the trust level" sample does this with `coroutine.yield` + `task.defer` and a 10-second cap.

## Testing in Studio
In Studio the level is always `Pending` and the callback never runs. Keep the policy in a pure function of the level, bypass the check when `RunService:IsStudio()` is true, and in Studio loop over `Enum.PlayerDeviceTrustLevel:GetEnumItems()` to print what your policy does for each level ([[Studio_Testing_Modes]]).

## What it does NOT do
- **It doesn't validate gameplay.** Speed hacks, teleporting, remote spam and fake hits from a trusted device still need server checks ([[Movement_Validation]], [[Hit_Validation]], [[Remote_Rate_Limiting]]).
- **It doesn't identify cheaters.** Use it to change the *cost* of cheating in high-value modes, alongside behavioral detection ([[Server_Side_Detection_Heuristics]]) and enforcement ([[Ban_API_and_Consequences]]).
- **It doesn't check the account.** For that, combine it with `Player:IsVerified()`.

## Related
[[Exploit_Threat_Model]] · [[Server_Side_Validation]] · [[Server_Side_Detection_Heuristics]] · [[Ban_API_and_Consequences]] · [[Data_Duplication_and_Trade_Exploits]] · [[Hit_Validation]] · [[Movement_Validation]] · [[Remote_Rate_Limiting]] · [[Matchmaking_Customization]] · [[TeleportService_and_Reserved_Servers]] · [[Studio_Testing_Modes]] · [[Defensive_Design]] · [[MOC_Anti_Exploit]] · [[MOC_Networking_Security_and_Buffers]]

## Sources
- https://create.roblox.com/docs/scripting/security/device-trust (Creator Docs repo @ 2026-10-29)
- https://create.roblox.com/docs/reference/engine/classes/IntegrityService · https://create.roblox.com/docs/reference/engine/classes/Player#DeviceTrustLevel · https://create.roblox.com/docs/reference/engine/enums/PlayerDeviceTrustLevel
- https://en.help.roblox.com/hc/en-us/articles/49648939984916-Android-Remote-Attestation (supported Android devices, player troubleshooting)
- https://devforum.roblox.com/c/updates/announcements/36 (mentioned in "Weekly Recap: October 26–30, 2026"; read via search excerpts)
