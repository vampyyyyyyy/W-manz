---
aliases: [Developer products, Dev products, Consumables, IAP Roblox]
tags:
  - roblox-dev
  - monetization/products
type: api
last_updated: 2026-10-27
status: complete
---
# Developer Products

> **TL;DR:** Developer products are **repeatable purchases** (currency packs, revives, boosts) priced from **1 to 1,000,000,000 Robux**. Prompt with `MarketplaceService:PromptProductPurchase(player, id)` and grant **only** from a receipt handler (`BindReceiptHandler` or `ProcessReceipt`) that's idempotent and saves before acknowledging. **Listed** products can be sold *outside* your game (homepage, search, post-Robux-purchase), but only while your receipt handling stays correct.

## Lifecycle
1. Create in Creator Hub ▸ Monetization ▸ Developer Products (name, icon, price). Add a custom icon for external surfaces.
2. Display: `GetProductInfoAsync(id, Enum.InfoType.Product)` or `GetDeveloperProductsAsync()` on the client for live prices.
3. Prompt: `PromptProductPurchase` (client or server).
4. Grant: receipt handler → award → persist `PurchaseId` → return `Processed` / `PurchaseGranted` ([[ProcessReceipt_Idempotency]]).

## 2026 changes to know
- **Cross-game sales disabled (May 30, 2026).** Products only sell in their own universe. Robux transfers replace cross-game patterns.
- **External sales:** Roblox continuously audits receipt handling. Broken products are flagged (banner in Monetization ▸ Shop) and **removed from external surfaces** until fixed, though in-game sales continue.
- **Rewarded video rewards** are developer products granted through the receipt flow with `ProductPurchaseChannel.AdReward` ([[Rewarded_Video_Ads]]).
- **Managed Pricing** (price tests + regional prices) needs *dynamically scripted* prices ([[Price_Optimization_and_Regional_Pricing]]).

## Design notes
- Consumables that affect PvP balance are a fairness problem. Prefer convenience, cosmetics and time-savers ([[Monetization_Design_Principles]]).
- Paid random outcomes (crates, spins) trigger odds-disclosure and per-user restrictions ([[Paid_Random_Items_Policy]]).
- Log purchases as economy *sources* for the dashboard ([[AnalyticsService_Events]]).

## Related
[[MarketplaceService]] · [[ProcessReceipt_Idempotency]] · [[Game_Passes]] · [[Rewarded_Video_Ads]] · [[Price_Optimization_and_Regional_Pricing]] · [[Paid_Random_Items_Policy]] · [[Monetization_Design_Principles]] · [[AnalyticsService_Events]] · [[Session_Locking]] · [[MOC_Monetization_Analytics_and_Compliance]]

## Sources
- https://create.roblox.com/docs/production/monetization/developer-products
