---
aliases: [Immersive ads, Ad units, Image ads, Portal ads, Video ads, AdService]
tags:
  - roblox-dev
  - monetization/ads
type: concept
last_updated: 2026-10-27
status: complete
---
# Immersive Ads

> **TL;DR:** Ad units placed in your 3D world serve **image ads** (paid per impression: viewed 1+ s at a minimum screen share), **portal ads** (paid per successful teleport to the advertiser's game; they must offer a return button) and **click-to-play video ads** (paid per 15-second view). Eligibility: **public game**, creator **13+** with **ID verification + 2FA**, an approved **Maturity & Compliance Questionnaire**, and **2,000+ unique visitors/month**. Ineligible viewers see your fallback content. Fraud gets payouts revoked.

## Placement principles
- Put units where players naturally look, but **not** in combat sightlines or over gameplay-critical info. Lobbies, hubs and queue areas work best.
- Match the world's art (frame the billboard like an in-world sign) ([[Game_UI_Art_Direction]]).
- Never incentivize looking at ads in prohibited ways (fake rewards, forced camera). That's ad fraud under the Advertising Standards.
- `PolicyService.AreAdsAllowed` per player: hide or replace units for ineligible players ([[PolicyService_Compliance]]).

## Performance
Ad units render like other world surfaces. Keep the count small and stream them with the hub area ([[StreamingEnabled]], [[Rendering_Optimization]]).

## Related
[[Rewarded_Video_Ads]] · [[PolicyService_Compliance]] · [[Content_Maturity_Labels]] · [[Monetization_Design_Principles]] · [[Game_UI_Art_Direction]] · [[StreamingEnabled]] · [[Rendering_Optimization]] · [[Analytics_Dashboard_and_Metrics]] · [[MOC_Monetization_Analytics_and_Compliance]]

## Sources
- https://create.roblox.com/docs/production/monetization/immersive-ads · https://en.help.roblox.com/hc/en-us/articles/13722260778260-Advertising-Standards
