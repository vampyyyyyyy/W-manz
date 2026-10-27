---
aliases: [Game passes, Passes, Gamepass, VIP pass, UserOwnsGamePassAsync]
tags:
  - roblox-dev
  - monetization/products
type: api
last_updated: 2026-10-27
status: complete
---
# Game Passes

> **TL;DR:** Passes are **one-time, permanent** purchases (VIP, 2× XP, extra loadout slot, cosmetic packs). On join, check `UserOwnsGamePassAsync(userId, passId)` server-side and apply perks. On an in-session purchase, grant from `PromptGamePassPurchaseFinished(player, passId, wasPurchased)`, re-verifying ownership on the server. **Listed** passes sell outside the game too, and you can opt passes into the **Buy Robux page** promotion (price must be 50–800 Robux).

## Server pattern
```luau
local function applyPasses(player: Player)
	for passId, perk in PASS_PERKS do
		local ok, owns = pcall(MarketplaceService.UserOwnsGamePassAsync, MarketplaceService, player.UserId, passId)
		if ok and owns then perk(player) end            -- concurrent calls are transparently batched
	end
end
Players.PlayerAdded:Connect(applyPasses)

MarketplaceService.PromptGamePassPurchaseFinished:Connect(function(player, passId, purchased)
	if purchased and PASS_PERKS[passId] then PASS_PERKS[passId](player) end
end)
```
Keep perks **data-driven** (passId → function) so every server code path grants the same way.

## Notes
- Personalize the store with `RankProductsAsync` (strict rate limit, so call once at join) or `RecommendTopProductsAsync`.
- Passes can't be paid random items in Buy Robux promotions, and they need a thumbnail.
- Cross-game pass sales have been disabled since May 30, 2026.
- Passes are regionally priced by default under Managed Pricing ([[Price_Optimization_and_Regional_Pricing]]).
- PvP-affecting passes hurt retention and fairness, so prefer QoL and cosmetics ([[Monetization_Design_Principles]]).

## Related
[[MarketplaceService]] · [[Developer_Products]] · [[Subscriptions]] · [[Price_Optimization_and_Regional_Pricing]] · [[Monetization_Design_Principles]] · [[Paid_Random_Items_Policy]] · [[Player_and_Character_Lifecycle]] · [[Server_Side_Validation]] · [[Analytics_Dashboard_and_Metrics]] · [[MOC_Monetization_Analytics_and_Compliance]]

## Sources
- https://create.roblox.com/docs/production/monetization/passes
