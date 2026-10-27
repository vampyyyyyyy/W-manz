---
aliases: [DevEx, Developer Exchange, Cash out Robux, Earned Robux, DevEx rate]
tags:
  - roblox-dev
  - monetization/payouts
type: concept
last_updated: 2026-10-27
status: complete
---
# Developer Exchange (DevEx)

> **TL;DR:** DevEx converts **Earned Robux** to real money. Standard rate **$0.0038/Robux** (since Sep 5, 2025; **$114 per 30,000**). Older balances cash out first at the old $0.0035. The **U.S. 18+ rate is $0.0054** (about 42% higher) for dev products, passes, subscriptions and private servers bought by **age-verified U.S. adults** in **eligible games** (R15/human-form character and quality criteria). Requirements: **13+**, **30,000 Earned Robux minimum**, verified email, DevEx portal account, a W-9/W-8 on file, and full ToS compliance.

## Tax change on Nov 1, 2026 (official, Creator Docs)
- From **Nov 1, 2026**, DevEx payments are classified as **royalties** under the updated Terms of Use. Withholding is based on the **payout date**, not the request date, so a request you submit in October but that pays out on Nov 1 or later is covered.
- Tax info moves from Tipalti to Creator Hub ▸ **Taxes**, which becomes the system of record for W-9/W-8 forms. Tipalti still processes payouts (same account) and receives the **net** amount after withholding.
- **U.S. creators:** a valid W-9 (TIN validated with the IRS) means no withholding. Valid Tipalti W-9s migrate automatically and show as "Validated". Missing or invalid info, or an IRS B-Notice, means **24% backup withholding**. Year-end forms: 1099-NEC for payments before Nov 1, 1099-MISC (royalties) after, so 2026 can have both.
- **Non-U.S. creators:** W-8BEN (individual) or W-8BEN-E (entity) through the Taxes page. With valid info by **Oct 31, 2026**, **0–30%** withholding applies to payouts tied to sales to U.S. players, depending on country and treaty claim. Without it, 24% backup withholding may hit the full payout.
- Under 18: a parent or guardian should handle this with you. It's a tax filing, not a game setting.

## Earned vs not earned
| Earned (cashable) | Not earned |
| --- | --- |
| Products, passes, subscriptions, private servers, paid access in Robux | Robux bought directly, monthly subscription grants |
| Creator Store sales, Marketplace items, Creator Rewards, ads, Plus incentives | Robux **received** via transfers, gift cards |
| Your 10% creator fee on in-game Robux transfers | Trading/resale, template-game pass farming, moderated content |

## Practical notes for young creators
- At 13–17 you can participate, but tax forms and payout accounts typically need a **parent/guardian**. Involve them early.
- Group games: payouts go to the group, so set up revenue splits deliberately.
- The 18+ rate pushes games toward R15, polished character articulation and adult-appeal content. Weigh that against your audience ([[Content_Maturity_Labels]]).
- **Payout rails are changing:** Roblox Wallet (daily USD payouts) starts rolling out in Dec 2026 to U.S. 18+ sole proprietors, and U.S. DevEx stays until mid-2027. See [[Roblox_Wallet_Transition]].

## Related
[[Roblox_Wallet_Transition]] · [[Creator_Rewards]] · [[Developer_Products]] · [[Game_Passes]] · [[Subscriptions]] · [[Paid_Access_and_Private_Servers]] · [[Content_Maturity_Labels]] · [[Monetization_Design_Principles]] · [[RDC_2026_Recap]] · [[MOC_Monetization_Analytics_and_Compliance]]

## Sources
- https://create.roblox.com/docs/production/monetization/developer-exchange · https://create.roblox.com/docs/production/monetization/18-plus-devex-rate · https://create.roblox.com/docs/production/monetization/tax-information
