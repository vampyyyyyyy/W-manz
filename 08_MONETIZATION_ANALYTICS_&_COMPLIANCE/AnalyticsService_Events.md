---
aliases: [AnalyticsService, Custom events, Economy events, Funnel events, LogCustomEvent, LogEconomyEvent]
tags:
  - roblox-dev
  - analytics/events
type: api
last_updated: 2026-10-27
status: complete
---
# AnalyticsService Events

> **TL;DR:** Server-side `AnalyticsService` calls feed the dashboard. **Funnels:** `LogOnboardingFunnelStepEvent` (one-time onboarding) and `LogFunnelStepEvent` (recurring, e.g., shop flow, with a `funnelSessionId`). **Economy:** `LogEconomyEvent` with flow type Source/Sink and transaction types (IAP, TimedReward, Onboarding, Shop, Gameplay, ContextualPurchase…). **Custom:** `LogCustomEvent` (up to **100** event names). Add up to **3 custom fields** (string values) for breakdowns, and prefer fields over many event names (cardinality).

## Examples
```luau
local AnalyticsService = game:GetService("AnalyticsService")

-- Onboarding step (once per user)
AnalyticsService:LogOnboardingFunnelStepEvent(player, 3, "First grapple")

-- Economy: earned 50 coins from a quest
AnalyticsService:LogEconomyEvent(player, Enum.AnalyticsEconomyFlowType.Source, "Coins", 50, newBalance,
	Enum.AnalyticsEconomyTransactionType.Gameplay.Name, "Quest_Rescue",
	{ [Enum.AnalyticsCustomFieldKeys.CustomField01.Name] = "Zone - Wall Maria" })

-- Custom: boss kill time
AnalyticsService:LogCustomEvent(player, "BossKilled", killSeconds,
	{ [Enum.AnalyticsCustomFieldKeys.CustomField01.Name] = "Boss - Colossal" })
```

## Rules of thumb
- **Server-side logging**, triggered by server-validated outcomes (the client can't be trusted for metrics either) ([[Server_Side_Validation]]).
- One event name per *concept* (e.g., `PlantSeed`) with custom fields for variants (Cabbage/Turnip).
- Log sinks *and* sources, or wallet balance charts lie ([[Inventory_Systems]]).
- Funnel step numbers must be stable across versions. Add steps at the end or start a new funnel.
- Combine with experiments to measure changes ([[Experiments_and_AB_Testing]]).

## Related
[[Analytics_Dashboard_and_Metrics]] · [[Retention_and_Engagement_Metrics]] · [[Experiments_and_AB_Testing]] · [[Configs_Remote_Configuration]] · [[Server_Side_Validation]] · [[Inventory_Systems]] · [[Badges]] · [[ProcessReceipt_Idempotency]] · [[Monetization_Design_Principles]] · [[MOC_Monetization_Analytics_and_Compliance]]

## Sources
- https://create.roblox.com/docs/production/analytics/custom-events · https://create.roblox.com/docs/production/analytics/economy-events · https://create.roblox.com/docs/production/analytics/funnel-events · https://create.roblox.com/docs/production/analytics/custom-fields
