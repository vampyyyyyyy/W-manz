---
aliases: [Experiments, A/B testing, Matchmaking experiments, Variants, Minimum detectable effect]
tags:
  - roblox-dev
  - analytics/experiments
type: concept
last_updated: 2026-10-27
status: complete
---
# Experiments & A/B Testing

> **TL;DR:** Creator Hub **Experiments** run causal A/B tests on **config values** (in-game experiments) or **matchmaking configurations** (one matchmaking experiment at a time). Each test has a goal metric, a **14–60 day** duration, a **rollout %**, up to **two variants + control**, optional targeting, and a fixed config once scheduled. Read results against the **minimum detectable effect**, not gut feel.

## Setup
1. Put the tunable behind a config key, e.g. `onboarding_variant` or `bossHealth` ([[Configs_Remote_Configuration]]).
2. Read it **per player**: `ConfigService:GetConfigForPlayerAsync(player)`, since experiments and targeting only apply there.
3. Create the experiment: goal metric (e.g., D7 retention), duration, rollout (e.g., 40%), and variants/split (e.g., 50/50).
4. Don't change the build in ways that interact with the test mid-run.

```luau
local snapshot = ConfigService:GetConfigForPlayerAsync(player)
local tutorial = snapshot:GetValue("onboarding_variant") or "classic"   -- "classic" | "action_first"
```

## Good experiment hygiene
- **One primary question per test.** Simple 50/50 tests on large rollouts are easiest to read.
- Big enough samples: a small game can't detect small effects, so test bold changes.
- Guardrail metrics: watch revenue *and* retention *and* session time. All metrics are tracked automatically.
- Ads and pricing: roll new ad placements out via experiments ([[Rewarded_Video_Ads]]). Price tests run through Managed Pricing ([[Price_Optimization_and_Regional_Pricing]]).
- Matchmaking experiments test custom signals and weights ([[Matchmaking_Customization]]).

## Related
[[Configs_Remote_Configuration]] · [[Analytics_Dashboard_and_Metrics]] · [[AnalyticsService_Events]] · [[Retention_and_Engagement_Metrics]] · [[Rewarded_Video_Ads]] · [[Price_Optimization_and_Regional_Pricing]] · [[Matchmaking_Customization]] · [[Benchmarking_Methodology]] · [[MOC_Monetization_Analytics_and_Compliance]]

## Sources
- https://create.roblox.com/docs/production/experiments
