---
aliases: [Badges, BadgeService, AwardBadgeAsync, Achievements]
tags:
  - roblox-dev
  - monetization/engagement
type: api
last_updated: 2026-10-27
status: complete
---
# Badges

> **TL;DR:** Badges are platform-visible achievements. Award them server-side with `BadgeService:AwardBadgeAsync(userId, badgeId)` (the sync `AwardBadge` is legacy), check with `UserHasBadgeAsync` / `CheckUserBadgesAsync`, and read metadata with `GetBadgeInfoAsync` (check `IsEnabled`). You get **5 free badges per game per 24 h (GMT)**, then **100 Robux** each. Use them as onboarding milestones and long-term goals, and track them as funnel steps.

## Award safely
```luau
local function award(player: Player, badgeId: number)
	local okInfo, info = pcall(BadgeService.GetBadgeInfoAsync, BadgeService, badgeId)
	if not (okInfo and info.IsEnabled) then return end
	local okHas, has = pcall(BadgeService.UserHasBadgeAsync, BadgeService, player.UserId, badgeId)
	if okHas and has then return end
	local ok, err = pcall(BadgeService.AwardBadgeAsync, BadgeService, player.UserId, badgeId)
	if not ok then warn("badge award failed", badgeId, err) end   -- retry later; never block gameplay on it
end
```
Award **only** from server-verified events (boss killed on the server, quest validated), never from a client remote saying "I did it" ([[Server_Side_Validation]], [[Exploit_Threat_Model]]).

## Design
- **Onboarding ladder:** "First Blood", "Learn to grapple", "Survive Wave 5". Each maps to an onboarding funnel step ([[AnalyticsService_Events]]).
- **Mastery badges** for long-tail retention (rare boss no-hit, 100 ODM kills) ([[Retention_and_Engagement_Metrics]]).
- Avoid spammy badges for joining. They dilute value and clutter profiles.
- Cache ownership per session to avoid repeated web calls.

## Related
[[AnalyticsService_Events]] · [[Retention_and_Engagement_Metrics]] · [[Server_Side_Validation]] · [[Exploit_Threat_Model]] · [[Error_Handling_pcall_xpcall]] · [[Monetization_Design_Principles]] · [[Combat_System_Architecture]] · [[Analytics_Dashboard_and_Metrics]] · [[MOC_Monetization_Analytics_and_Compliance]]

## Sources
- https://create.roblox.com/docs/production/publishing/badges · https://create.roblox.com/docs/reference/engine/classes/BadgeService
