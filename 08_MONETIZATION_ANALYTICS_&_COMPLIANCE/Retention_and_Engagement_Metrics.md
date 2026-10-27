---
aliases: [Retention, D1 retention, D7, D30, Session length, First session, Engagement]
tags:
  - roblox-dev
  - analytics/retention
type: concept
last_updated: 2026-10-27
status: complete
---
# Retention & Engagement Metrics

> **TL;DR:** Retention (**D1/D7/D30**, measured per *first-play cohort*) and **session time** decide discovery, Creator Rewards and revenue. Most players are lost in the **first session**, so the "New User First Session Retention" curve (how many are still playing X minutes in) is your highest-leverage chart. Fix order: get to fun fast → clear short-term goals → reasons to return tomorrow → long-term mastery.

## Diagnose with the right chart
| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Big drop in first 1–3 min | Slow load, confusing spawn, no immediate action | Instant gameplay, minimal UI, tutorial-by-doing ([[Loading_Screens_and_ReplicatedFirst]]) |
| Drop at a specific funnel step | Difficulty spike or unclear objective | Funnel events + experiments ([[AnalyticsService_Events]]) |
| OK D1, poor D7 | Shallow loop, no progression or social hooks | Progression, daily goals, friends ([[Experience_Notifications]]) |
| Retention dips after big traffic days | Normal cohort-quality effect | Read cohorts separately |

## Genre-specific hooks (combat/movement games)
- **Mastery feel:** responsive input and satisfying hits keep players (feel is retention) ([[Hitstop_and_Impact_Feel]], [[Combo_Systems_and_Input_Buffering]]).
- **Movement as reward:** ODM/grapple skill expression gives a reason to come back and improve ([[ODM_Gear_System]]).
- **Session goals:** "Clear 3 waves" or "beat your best time", visible in the HUD ([[Custom_HUD_Design]]).
- **Performance is retention:** low-end lag ends sessions ([[Mobile_and_Low_End_Optimization]]).

## Related
[[Analytics_Dashboard_and_Metrics]] · [[AnalyticsService_Events]] · [[Experiments_and_AB_Testing]] · [[Creator_Rewards]] · [[Experience_Notifications]] · [[Loading_Screens_and_ReplicatedFirst]] · [[Hitstop_and_Impact_Feel]] · [[ODM_Gear_System]] · [[Mobile_and_Low_End_Optimization]] · [[Custom_HUD_Design]] · [[MOC_Monetization_Analytics_and_Compliance]]

## Sources
- https://create.roblox.com/docs/production/analytics/retention · https://create.roblox.com/docs/production/analytics/engagement
