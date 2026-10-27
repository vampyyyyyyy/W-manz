---
aliases: [MarketplaceService, Purchases API, PromptProductPurchase, UserOwnsGamePassAsync, OpenShop]
tags:
  - roblox-dev
  - monetization/api
type: api
last_updated: 2026-10-27
status: complete
---
# MarketplaceService

> **TL;DR:** `MarketplaceService` is the hub for every in-game purchase: **prompts** (`PromptProductPurchase`, `PromptGamePassPurchase`, `PromptSubscriptionPurchase`, `PromptRobloxSubscriptionPurchase`, `PromptRobuxTransferAsync`, `OpenShop`), **ownership checks** (`UserOwnsGamePassAsync`, `GetUserSubscriptionStatusAsync`), **product data** (`GetProductInfoAsync`, `GetDeveloperProductsAsync`, `RankProductsAsync`, `RecommendTopProductsAsync`, `GetUsersPriceLevelsAsync`) and **receipt processing** (`ProcessReceipt` or the newer `BindReceiptHandler`). Grant value only from receipts or ownership checks on the **server**.

## Map
| Product | Prompt | Grant via | Note |
| --- | --- | --- | --- |
| [[Developer_Products]] (consumable) | `PromptProductPurchase` | `BindReceiptHandler` / `ProcessReceipt` | Must be idempotent ([[ProcessReceipt_Idempotency]]) |
| [[Game_Passes]] (one-time) | `PromptGamePassPurchase` | `UserOwnsGamePassAsync` on join + `PromptGamePassPurchaseFinished` | Ownership is permanent |
| [[Subscriptions]] | `PromptSubscriptionPurchase` | `GetUserSubscriptionStatusAsync` + `Players.UserSubscriptionStatusChanged` | Check on the server |
| Robux transfers (Plus) | `PromptRobuxTransferAsync` (server) | `BindReceiptHandler(RobuxTransferSender/Receiver)` | 10–500 Robux per transfer |
| Roblox Plus sign-ups | `PromptRobloxSubscriptionPurchase` | Payout from Roblox | Up to 750 Robux per new subscriber you drive |
| Native Shop | `OpenShop` | — | Shows Listed passes and products ([[Monetization_Design_Principles]]) |

## Production rules
- **Never hard-code prices** in UI. Read `GetProductInfoAsync` on the client so Managed Pricing, regional prices and Plus discounts display correctly ([[Price_Optimization_and_Regional_Pricing]]).
- Concurrent `GetProductInfoAsync` / `UserOwnsGamePassAsync` calls are **transparently batched**, so firing them in parallel at join is fine. Still wrap every async call in `pcall`.
- `Prompt*Finished` events mean "the prompt closed", **not** "payment succeeded" for products. Never grant products from them.
- Cross-game product and pass sales were **disabled May 30, 2026**. Use Robux transfers if you relied on them.
- Policy gates: `PolicyService` fields such as `ArePaidRandomItemsRestricted` and `IsEligibleToPurchaseSubscription` ([[PolicyService_Compliance]]).

## Related
[[Developer_Products]] · [[Game_Passes]] · [[Subscriptions]] · [[ProcessReceipt_Idempotency]] · [[Price_Optimization_and_Regional_Pricing]] · [[PolicyService_Compliance]] · [[Paid_Random_Items_Policy]] · [[Monetization_Design_Principles]] · [[Server_Side_Validation]] · [[DataStore_Limits_and_Error_Codes]] · [[MOC_Monetization_Analytics_and_Compliance]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/MarketplaceService · https://create.roblox.com/docs/production/monetization/developer-products
