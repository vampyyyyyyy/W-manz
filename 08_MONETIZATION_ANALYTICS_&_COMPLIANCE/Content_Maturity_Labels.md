---
aliases: [Content maturity, Maturity questionnaire, Roblox Kids, Roblox Select, Content May Vary, Restricted 18+]
tags:
  - roblox-dev
  - compliance/maturity
type: concept
last_updated: 2026-10-27
status: complete
---
# Content Maturity Labels & Audience Tiers

> **TL;DR:** The **Maturity & Compliance Questionnaire** produces your label, which decides who can play. **Minimal/Mild** → Roblox **Kids (5–8)** + **Select (9–15)**. **Moderate** → Select + standard Roblox (**16+**). **Content May Vary** → age-checked **16+** only. **Restricted** → age-verified **18+** only. Games without maturity info are restricted for everyone. Reaching **under-16 audiences** also requires a verified, 2FA-protected creator account, a publishing fee or 2-month Plus/Premium subscription, and an **evaluation** (250 unique plays from highly engaged age-checked 16+ players within 60 days, plus a safety review).

## Account tiers (2026)
| Tier | Who | Content | Chat |
| --- | --- | --- | --- |
| Roblox Kids | 5–8 | Minimal/Mild | Off by default (parent can enable after age check) |
| Roblox Select | 9–15 (or unverified 9+) | Minimal, Mild, Moderate (9+) | Gradual, with safeguards after age check |
| Roblox | Age-checked 16+ | All rated except Restricted | On by default where available |

## Practical guidance
- Answer for the **most extreme** content a player can encounter, and **resubmit whenever an update changes answers**. Resubmitting temporarily pauses ads eligibility ([[Immersive_Ads]]).
- Anime combat with blood or gore effects pushes the rating up. Tune VFX (no realistic blood, stylized impacts) if you want Select audiences ([[VFX_Composition_and_Timing]], [[Hitstop_and_Impact_Feel]]).
- Creators **under 18** verify via **facial age estimation**. 18+ creators use government ID.
- Expedited Kids/Select review: a refundable **50,000 Robux** fee per game (for timed launches).
- Asset moderation is separate. Realistic or excessive violence can be moderated regardless of label.

## Related
[[Age_Checks_and_Chat_Safety]] · [[PolicyService_Compliance]] · [[Immersive_Ads]] · [[Rewarded_Video_Ads]] · [[VFX_Composition_and_Timing]] · [[Hitstop_and_Impact_Feel]] · [[Developer_Exchange_DevEx]] · [[Text_Filtering_Compliance]] · [[Monetization_Design_Principles]] · [[MOC_Monetization_Analytics_and_Compliance]]

## Sources
- https://create.roblox.com/docs/production/promotion/content-maturity · https://create.roblox.com/docs/production/publishing/kids-and-select
