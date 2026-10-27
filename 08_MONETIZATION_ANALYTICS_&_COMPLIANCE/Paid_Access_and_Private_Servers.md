---
aliases: [Paid access, Private servers, VIP servers, Paid private servers, PrivateServerId]
tags:
  - roblox-dev
  - monetization/access
type: concept
last_updated: 2026-10-27
status: complete
---
# Paid Access & Private Servers

> **TL;DR:** **Paid access** charges to *enter* the game: Robux **25–1,000** (no refunds, 7-day escrow), or local currency at **$9.99 / $29.99 / $49.99** with **50% / 60% / 70%** revenue share (buy on desktop/web via Tipalti payouts). **Private servers** are a monthly subscription for a personal server. You **can't enable paid access and private servers together**. Changing the private-server price **cancels all active subscriptions**, and **Roblox Plus** subscribers get paid private servers free (you earn up to 100 Robux per subscriber who spends 60+ min/month in them).

## Choosing
| Model | Fit | Watch out |
| --- | --- | --- |
| Paid access | Premium, finished, niche games (story, horror, sims) | Big hit to discovery and conversion. Creator Rewards still apply |
| Private servers | Social/grind games, competitive practice, content creators | Price changes cancel subs. Design server-owner tools |
| Free + reserved servers | Your own "private match" logic via `TeleportService:ReserveServerAsync` | You build the access control ([[TeleportService_and_Reserved_Servers]]) |

## Detecting private servers
```luau
if game.PrivateServerId ~= "" then
	local isVip = game.PrivateServerOwnerId ~= 0     -- 0 for reserved servers
	-- unlock owner commands only for game.PrivateServerOwnerId
end
```
Owner commands still go through server permission checks ([[Cmdr]], [[Server_Side_Validation]]).

## Related
[[Subscriptions]] · [[TeleportService_and_Reserved_Servers]] · [[Creator_Rewards]] · [[Developer_Exchange_DevEx]] · [[MarketplaceService]] · [[Price_Optimization_and_Regional_Pricing]] · [[Cmdr]] · [[Server_Side_Validation]] · [[Monetization_Design_Principles]] · [[MOC_Monetization_Analytics_and_Compliance]]

## Sources
- https://create.roblox.com/docs/production/monetization/paid-access-robux · https://create.roblox.com/docs/production/monetization/paid-access-local-currency · https://create.roblox.com/docs/production/monetization/private-servers · https://create.roblox.com/docs/production/monetization/roblox-plus
