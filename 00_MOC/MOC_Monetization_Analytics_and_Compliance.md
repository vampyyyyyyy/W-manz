---
aliases: [Monetization MOC, Business hub, Compliance hub]
tags:
  - roblox-dev
  - moc/monetization
type: moc
last_updated: 2026-10-27
status: complete
---
# MOC: Monetization, Analytics & Compliance

> **TL;DR:** Turning a good game into a **sustainable, compliant business**: purchase APIs and idempotent receipts, passes, subscriptions, access models, payouts (Creator Rewards, DevEx, the coming Wallet), ads, Managed Pricing, analytics/configs/experiments, and the policy layer (PolicyService, paid random items, privacy/RTBF, maturity tiers, chat and text safety, notifications).

*27 notes in this domain.*

## Start here
1. [[Monetization_Design_Principles]]: sell value, keep PvP fair, no dark patterns
2. [[MarketplaceService]]: the purchase API map
3. [[ProcessReceipt_Idempotency]]: the receipt pattern that never double-grants
4. [[Analytics_Dashboard_and_Metrics]]: the metrics that actually matter
5. [[PolicyService_Compliance]]: per-player legal and regional gates
6. [[Content_Maturity_Labels]]: who can play your game (Kids/Select/16+/18+)

## Selling
- **APIs & products:** [[MarketplaceService]] · [[Developer_Products]] · [[ProcessReceipt_Idempotency]] · [[Game_Passes]] · [[Subscriptions]] · [[Paid_Access_and_Private_Servers]] · [[Commerce_Products]]
- **Pricing & design:** [[Price_Optimization_and_Regional_Pricing]] · [[Monetization_Design_Principles]]

## Earning
- **Payouts:** [[Creator_Rewards]] · [[Developer_Exchange_DevEx]] · [[Roblox_Wallet_Transition]]
- **Ads:** [[Immersive_Ads]] · [[Rewarded_Video_Ads]]
- **Engagement:** [[Badges]] · [[Experience_Notifications]]

## Measuring
- **Analytics:** [[Analytics_Dashboard_and_Metrics]] · [[AnalyticsService_Events]] · [[Retention_and_Engagement_Metrics]]
- **Live ops:** [[Configs_Remote_Configuration]] · [[Experiments_and_AB_Testing]]

## Compliance & safety
- **Policy:** [[PolicyService_Compliance]] · [[Paid_Random_Items_Policy]] · [[Content_Maturity_Labels]]
- **Privacy & safety:** [[Right_to_Erasure_GDPR]] · [[Age_Checks_and_Chat_Safety]] · [[Text_Filtering_Compliance]]

## Cross-domain
[[Home]] · [[Learning_Path]] · [[MOC_Game_Systems_and_Algorithms]] · [[MOC_Anti_Exploit]] · [[RDC_2026_Recap]] · [[Session_Locking]]

## Sources
- Each linked note cites its own primary sources. See [[Trusted_Sources]] for the ranking policy.
