---
aliases: [Analytics dashboard, Creator Hub analytics, KPIs, ARPDAU, Conversion rate, Explore page]
tags:
  - roblox-dev
  - analytics/dashboard
type: concept
last_updated: 2026-10-27
status: complete
---
# Analytics Dashboard & Metrics

> **TL;DR:** Creator Hub Analytics covers **Engagement** (sessions, playtime, new-user first-session retention), **Retention** (D1/D7/D30 by first-play cohort), **Monetization** (conversion rate, ARPPU, ARPDAU), **Acquisition**, **Performance**, **Economy/Funnels/Custom** (from `AnalyticsService`) and an **Explore** page for custom charts and formulas. Full KPIs unlock at **>10 DAU and 10 play-hours for 7 consecutive days**. Use **benchmarks** against similar games, and segment by payer and activity status.

## Core metrics cheat-sheet
| Metric | Meaning | First lever |
| --- | --- | --- |
| D1 / D7 / D30 retention | % of a first-play cohort returning | First 10 minutes, daily reasons to return ([[Retention_and_Engagement_Metrics]]) |
| Avg session time | Total time ÷ sessions | Core loop depth, session goals |
| Payer conversion | % of DAU who pay | Shop visibility, a starter offer that's a real deal ([[Monetization_Design_Principles]]) |
| ARPPU | Revenue per paying user | Item ladder, subscriptions ([[Subscriptions]]) |
| ARPDAU | Conversion × ARPPU | Both of the above |

## Segmentation
Breakdowns by *in-experience activity* (Early = first 30 days, Active, Lapsed, Reactivated), *platform activity*, payer status, platform/device, country/language, and new vs returning. These are the same attributes Configs can target ([[Configs_Remote_Configuration]]).

## Workflow
1. Instrument funnels, economy and custom events ([[AnalyticsService_Events]]).
2. Read cohorts, not totals. A traffic spike lowers retention temporarily.
3. Hypothesis → **experiment**, not "ship and hope" ([[Experiments_and_AB_Testing]]).
4. Watch **Performance** (crashes, memory, FPS by device), since a laggy game churns ([[Mobile_and_Low_End_Optimization]]).

## Related
[[AnalyticsService_Events]] · [[Retention_and_Engagement_Metrics]] · [[Experiments_and_AB_Testing]] · [[Configs_Remote_Configuration]] · [[Monetization_Design_Principles]] · [[Subscriptions]] · [[Creator_Rewards]] · [[Mobile_and_Low_End_Optimization]] · [[Performance_Optimization_Workflow]] · [[MOC_Monetization_Analytics_and_Compliance]]

## Sources
- https://create.roblox.com/docs/production/analytics/analytics-dashboard · https://create.roblox.com/docs/production/analytics/monetization · https://create.roblox.com/docs/production/analytics/retention
