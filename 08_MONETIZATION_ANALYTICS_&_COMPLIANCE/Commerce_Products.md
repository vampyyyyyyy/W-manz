---
aliases: [Commerce products, Real-world products, Shopify integration, Merch in game]
tags:
  - roblox-dev
  - monetization/commerce
type: concept
last_updated: 2026-10-27
status: complete
---
# Commerce Products

> **TL;DR:** Commerce lets eligible creators sell **real-world products** (merch, via a linked **Shopify** store) inside their games, optionally bundled with **digital items** as a benefit. Creators must be **18+** (or have written permission from the Shopify store's account holder) and complete business/legal info. Games must be public. Currently **only U.S. users** can buy, and they must be 13+ (Texas excepted). Check `PolicyService.IsEligibleToPurchaseCommerceProduct` per player.

## Implementation checklist
1. Meet creator eligibility (age, Shopify link, Account Information legal and business tabs, group permissions if group-owned).
2. Create commerce products in Creator Hub and link catalog items.
3. In game, show commerce UI only to eligible players ([[PolicyService_Compliance]]).
4. Bundled digital items are granted through Roblox's commerce flow, so don't invent your own grant path. Make the bundled benefit clear before purchase.

## For a teen creator
The 18+ requirement means a parent/guardian-run business or a partner would have to own the Shopify side. Plan merch with them rather than around the rules.

## Related
[[PolicyService_Compliance]] · [[MarketplaceService]] · [[Monetization_Design_Principles]] · [[Content_Maturity_Labels]] · [[Developer_Exchange_DevEx]] · [[Roblox_Wallet_Transition]] · [[Text_Filtering_Compliance]] · [[Age_Checks_and_Chat_Safety]] · [[MOC_Monetization_Analytics_and_Compliance]]

## Sources
- https://create.roblox.com/docs/production/monetization/commerce-products
