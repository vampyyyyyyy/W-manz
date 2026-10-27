---
aliases: [Experience subscriptions, In-game subscriptions, Recurring purchases, GetUserSubscriptionStatusAsync]
tags:
  - roblox-dev
  - monetization/subscriptions
type: api
last_updated: 2026-10-27
status: complete
---
# Subscriptions

> **TL;DR:** Monthly, auto-renewing benefits. Up to **50 per game**, single-tier (no mutually exclusive tiers), priced in **Robux (≥ 49, regional pricing forced on, 70% payout)** or **local currency ($2.99/$4.99/$7.99/$9.99/$14.99; 70% first month then 100%; requires ID/phone-verified account; unavailable in some countries)**. Check status on the **server** with `GetUserSubscriptionStatusAsync(player, subscriptionId)` and react to `Players.UserSubscriptionStatusChanged`.

## Server check
```luau
local function refresh(player: Player)
	local ok, status = pcall(MarketplaceService.GetUserSubscriptionStatusAsync, MarketplaceService, player, SUB_ID)
	player:SetAttribute("SubActive", ok and status.IsSubscribed or false)
end
Players.PlayerAdded:Connect(refresh)
Players.UserSubscriptionStatusChanged:Connect(function(player, subscriptionId)
	if subscriptionId == SUB_ID then refresh(player) end
end)
```
The client may prompt (`PromptSubscriptionPurchase`), but **benefits are granted by the server** from the status check.

## Rules (official guidelines)
- Clear names, price and duration in the merch. The same benefits on every platform.
- Honor benefits for the full term, and never revoke them silently.
- Don't gate paid benefits behind extra tasks (e.g., "post on social media").
- Deleting a local-currency subscription forces refunds. Prefer **Take Off Sale**, and choose whether existing subscribers keep renewing.
- `PolicyService.IsEligibleToPurchaseSubscription` must be respected ([[PolicyService_Compliance]]).

## Good subscription design
Recurring *value*, not just recurring *cost*: daily login currency, monthly cosmetic drops, a battle-pass track, a server-wide perk. Measure churn and retention lift with experiments ([[Experiments_and_AB_Testing]], [[Retention_and_Engagement_Metrics]]).

## Related
[[MarketplaceService]] · [[Game_Passes]] · [[Paid_Access_and_Private_Servers]] · [[PolicyService_Compliance]] · [[Price_Optimization_and_Regional_Pricing]] · [[Experiments_and_AB_Testing]] · [[Retention_and_Engagement_Metrics]] · [[Monetization_Design_Principles]] · [[Attributes]] · [[MOC_Monetization_Analytics_and_Compliance]]

## Sources
- https://create.roblox.com/docs/production/monetization/subscriptions
