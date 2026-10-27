---
aliases: [BanAsync, Ban API, Consequence ladder, UnbanAsync]
tags:
  - roblox-dev
  - security/enforcement
type: api
last_updated: 2026-10-27
status: complete
---
# Ban API & the Consequence Ladder

> **TL;DR:** `Players:BanAsync` bans users across your universe, propagates to suspected alt accounts by default, and can block the device. Use it at the **top** of an escalation ladder, after silent logging, quiet mitigation and temporary restrictions, never as a reflex to a single heuristic hit.

## API
| Member | Notes |
| --- | --- |
| `Players:BanAsync(config)` | **Server only.** `config`: `UserIds` (array), `Duration` (seconds; `-1` for permanent), `DisplayReason` (shown to user, max **400** chars, text-filtered), `PrivateReason` (internal), `ExcludeAltAccounts` (default `false` = alts *are* banned too), `ApplyToUniverse` (default `true`), `ApplyDeviceBlock`. |
| `Players:UnbanAsync(config)` | Unban only clears bans of the **same scope**: a universe unban doesn't clear a place ban, and vice versa. Lifting a device block only works through this method. |
| `Players:GetBanHistoryAsync(userId)` | Returns `BanHistoryPages`. **Production servers only** (not Studio, not clients). |
| `Players.BanningEnabled` | Toggle in Studio. Methods error when disabled. |
| Creator Hub ▸ Moderation ▸ **Bans** | Dashboard to view, add or remove bans and see history. Also available via the **User Restrictions** Open Cloud API ([[Open_Cloud_APIs]]). |

Banning in the **start place** effectively locks the user out of the universe even with `ApplyToUniverse = false`. Studio and Team Test calls are accepted, but the bans don't apply to production.

```luau
--!strict
local Players = game:GetService("Players")

local function tempBan(userId: number, hours: number, publicReason: string, evidence: string)
	local ok, err = pcall(function()
		Players:BanAsync({
			UserIds = { userId },
			Duration = hours * 3600,
			DisplayReason = publicReason, -- keep factual; it is shown to the player
			PrivateReason = evidence,     -- your detection rule + version + values
			ExcludeAltAccounts = false,
			ApplyToUniverse = true,
		})
	end)
	if not ok then warn("BanAsync failed:", err) end -- HTTP-backed: can fail, retry later
end
```

## The consequence ladder (Roblox guidance)
1. **Silent logging:** build evidence with no player impact.
2. **Quiet mitigation:** drop requests, clamp values, rubber-band ([[Movement_Validation]]).
3. **Temporary restrictions:** no trading, leaderboards or ranked matchmaking.
4. **Visible enforcement:** kick → temp ban → permanent ban.

Delay visible consequences, match severity to the harm, prefer **reversible** actions when confidence is low, publish your rules, and offer an appeal path. The ban guidelines expect this.

## Related
[[Server_Side_Detection_Heuristics]] · [[Honeypot_Remotes]] · [[Exploit_Threat_Model]] · [[Auto_Farm_and_Remote_Spam_Exploits]] · [[Open_Cloud_APIs]] · [[Script_Capabilities]] (`Consequences` capability) · [[Text_Filtering_Compliance]] · [[Defensive_Design]] · [[MOC_Anti_Exploit]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/Players#BanAsync
- https://create.roblox.com/docs/production/bans
- https://create.roblox.com/docs/scripting/security/server-side-detection#applying-consequences
