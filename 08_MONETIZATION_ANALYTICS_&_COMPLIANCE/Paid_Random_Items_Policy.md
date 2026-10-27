---
aliases: [Loot boxes, Paid random items, Gacha, Odds disclosure, Crates]
tags:
  - roblox-dev
  - compliance/monetization
type: concept
last_updated: 2026-10-27
status: complete
---
# Paid Random Items Policy

> **TL;DR:** Anything random bought **directly or indirectly with Robux** (crates, spins, rerolls, or keys/tickets/gems bought with Robux) requires **odds disclosure before purchase**: percentages that **sum to exactly 100%**, updated when outcomes are removed for that user, with numeric explanations for any odds-boosting items (lucky potions). For players where **`ArePaidRandomItemsRestricted`** is true, you must offer the outcomes for **direct purchase** (priced around expected value) or **block** the purchase. Free random rewards don't need disclosure.

## Implementation checklist
- Single source of truth: odds tables live in a server module and are **displayed from the same data**, so disclosure can't drift from reality.
- Roll on the **server** with a robust RNG (`Random.new()` per server, not client-supplied seeds) ([[Server_Side_Validation]]).
- Indirect currency counts: if gems can be bought with Robux, gem crates are paid random items.
- Pity/guarantee systems are good practice. Explain them numerically too.
- Rewarded-video rewards can **never** be random ([[Rewarded_Video_Ads]]).
- Log rolls (economy sinks/sources) for audits and balancing ([[AnalyticsService_Events]]).

## Restricted-user treatment
```luau
if policy(player).ArePaidRandomItemsRestricted then
	-- show "Buy Dragon Blade directly: 200 R$" (5% crate at 10 R$ → EV-priced direct offer), or block with a clear message
end
```
([[PolicyService_Compliance]])

## Related
[[PolicyService_Compliance]] · [[Developer_Products]] · [[Game_Passes]] · [[Rewarded_Video_Ads]] · [[Monetization_Design_Principles]] · [[AnalyticsService_Events]] · [[Server_Side_Validation]] · [[Inventory_Systems]] · [[Math_Library]] · [[MOC_Monetization_Analytics_and_Compliance]]

## Sources
- https://create.roblox.com/docs/production/monetization/paid-random-items
