---
aliases: [Price optimization, Regional pricing, Managed pricing, Dynamic pricing, GetUsersPriceLevelsAsync]
tags:
  - roblox-dev
  - monetization/pricing
type: concept
last_updated: 2026-10-27
status: complete
---
# Price Optimization & Regional Pricing (Managed Pricing)

> **TL;DR:** **Managed Pricing** unifies **price optimization** (automatic A/B price tests; applied only if total revenue rises; needs about **60k transactions/30 days**; reruns at least every **90 days**) and **regional pricing** (prices scaled by *economic location*, never more than **70% below** and never **above** your default). It only works if your UI reads prices **dynamically** from `MarketplaceService`. Protect trades and gifts from regional arbitrage with `GetUsersPriceLevelsAsync`.

## Dynamic price display (client)
```luau
local ok, info = pcall(MarketplaceService.GetProductInfoAsync, MarketplaceService, PRODUCT_ID, Enum.InfoType.Product)
priceLabel.Text = if ok then `{info.PriceInRobux} R$` else "—"
```
Hard-coded "100 R$" labels break price tests, show wrong prices to regional users, and also misprice **Roblox Plus** discounts ([[MarketplaceService]]). Run the **dynamic price check tool** before enrolling.

## Enrollment facts
- New games and items are enrolled by default (item-level opt-out). Passes are regionally priced by default.
- Subscriptions, private servers and developer servers are regionalized automatically. Subscriptions aren't price-tested.
- Developer products need dynamic prices **and** price-level-aware transfers before enabling.

## Arbitrage guard (trading/gifting)
If player A (lower regional price) can buy and gift to player B, compare price levels first:
```luau
local ok, levels = pcall(MarketplaceService.GetUsersPriceLevelsAsync, MarketplaceService, { giver.UserId, receiver.UserId })
-- disallow gifting from a lower price level to a higher one (or charge the receiver's price)
```
See [[Data_Duplication_and_Trade_Exploits]] for trade-system hardening.

## Related
[[MarketplaceService]] · [[Developer_Products]] · [[Game_Passes]] · [[Subscriptions]] · [[Experiments_and_AB_Testing]] · [[Data_Duplication_and_Trade_Exploits]] · [[Monetization_Design_Principles]] · [[Analytics_Dashboard_and_Metrics]] · [[Inventory_Systems]] · [[MOC_Monetization_Analytics_and_Compliance]]

## Sources
- https://create.roblox.com/docs/production/monetization/managed-pricing · https://create.roblox.com/docs/production/monetization/price-optimization · https://create.roblox.com/docs/production/monetization/regional-pricing
