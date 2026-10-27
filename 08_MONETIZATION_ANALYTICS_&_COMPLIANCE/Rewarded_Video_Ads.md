---
aliases: [Rewarded video, Rewarded ads, ShowRewardedVideoAdAsync, Watch ad for reward]
tags:
  - roblox-dev
  - monetization/ads
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Rewarded Video Ads

> **TL;DR:** Opt-in, full-screen **6–30 s** videos that grant a **developer product** as the reward (never Robux, never random items). Client: `AdService:GetAdAvailabilityNowAsync(Enum.AdFormat.RewardedVideo)` right before showing the button. Server: `AdService:CreateAdRewardFromDevProductId(id)` → `AdService:ShowRewardedVideoAdAsync(player, reward)`. The reward arrives through your **receipt handler** with `ProductPurchaseChannel.AdReward`. Earnings = EPM × impressions. The recommended reward value is about **3–10 Robux**.

## Flow
```text
Client: open shop → GetAdAvailabilityNowAsync → show "Watch ad: 2× coins (30 min)" button
Client → server (intent remote, rate-limited) → server validates cooldown
Server: ShowRewardedVideoAdAsync(player, CreateAdRewardFromDevProductId(BOOST_ID))
Roblox: player completes video → receipt (channel AdReward) → your idempotent handler grants the boost
```
See [[ProcessReceipt_Idempotency]]. The reward path is the same as a purchase, so you get no separate grant logic and no dupes.

## Rules & tips
- **Clearly disclosed** and opt-in. Pause damage or only offer it in safe zones, since an ad must not get the player killed ([[Combat_System_Architecture]]).
- Rewards must be products you'd normally sell, mustn't inflate the economy, and can't be randomized ([[Paid_Random_Items_Policy]]).
- Call availability as late as possible. After an ad, only re-check if you'll offer another.
- Eligible games: public, unrestricted, **no free-form user creation**, approved questionnaire. Creator 13+, ID-verified, 2FA, 2k+ monthly visitors.
- Roll new placements out with **experiments** and watch opt-in rate, frequency and DUV/eDAU ([[Experiments_and_AB_Testing]]).

## Related
[[Immersive_Ads]] · [[Developer_Products]] · [[ProcessReceipt_Idempotency]] · [[Paid_Random_Items_Policy]] · [[Experiments_and_AB_Testing]] · [[Remote_Rate_Limiting]] · [[Combat_System_Architecture]] · [[Analytics_Dashboard_and_Metrics]] · [[Monetization_Design_Principles]] · [[MOC_Monetization_Analytics_and_Compliance]]

## Sources
- https://create.roblox.com/docs/production/promotion/rewarded-video-ads · https://create.roblox.com/docs/reference/engine/classes/AdService
