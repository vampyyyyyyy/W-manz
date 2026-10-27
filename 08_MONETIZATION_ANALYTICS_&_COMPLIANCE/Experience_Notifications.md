---
aliases: [Experience notifications, Push notifications Roblox, ExperienceNotificationService, PromptOptIn, CreateUserNotification]
tags:
  - roblox-dev
  - compliance/notifications
type: api
last_updated: 2026-10-27
status: complete
---
# Experience Notifications

> **TL;DR:** Opted-in players can get **personalized, actionable** notifications from your game. Ask with `ExperienceNotificationService:CanPromptOptInAsync()` → `PromptOptIn()`, then send from the **server** via the Creator Store **Open Cloud** package (`createUserNotification` with a moderated **notification string** asset) or the Open Cloud API. Limits: **1 notification per user per day per game**, delivery isn't guaranteed (spam prevention), and the game needs **100+ visits** and must not be under moderation. **Launch data** routes the player when they join (`Player:GetJoinData()`).

## Good vs bad
| ✅ Personalized & actionable | ❌ Generic or manipulative |
| --- | --- |
| "Your Colossal Titan raid is ready, squad is waiting" | "New update! Play now!" |
| "@Friend just beat your ODM course record" | "Buy in the next 10 minutes or lose progress!" (false urgency) |
| "Your crops finished growing" | "Click for important account info" (disguised ad) |

Dark patterns (disguised ads, false time pressure, bait-and-switch freebies) are prohibited, and all text is filtered and moderated ([[Text_Filtering_Compliance]]).

## Implementation notes
- Prompt for opt-in at a **moment of value** (after finishing a first raid), not on join.
- Notify from server-confirmed state (timer completed server-side) ([[Server_Side_Validation]]).
- Use launch data to drop the player directly into the relevant place ([[TeleportService_and_Reserved_Servers]]).
- Measure the impact on D7 retention with experiments ([[Experiments_and_AB_Testing]], [[Retention_and_Engagement_Metrics]]).

## Related
[[Retention_and_Engagement_Metrics]] · [[Experiments_and_AB_Testing]] · [[Text_Filtering_Compliance]] · [[Open_Cloud_APIs]] · [[Server_Side_Validation]] · [[TeleportService_and_Reserved_Servers]] · [[Creator_Rewards]] · [[Monetization_Design_Principles]] · [[MOC_Monetization_Analytics_and_Compliance]]

## Sources
- https://create.roblox.com/docs/production/promotion/experience-notifications · https://create.roblox.com/docs/reference/engine/classes/ExperienceNotificationService
