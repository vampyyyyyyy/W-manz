---
aliases: [RDC 2026, Roblox Developers Conference 2026, RDC recap, Roblox Build, AI Scene Generation]
tags:
  - roblox-dev
  - community/events
type: concept
last_updated: 2026-10-29
status: needs-verification
---
# RDC 2026 Recap (Sept 2026, San Jose)

> **TL;DR:** Roblox's 20th-anniversary RDC centered on **AI-assisted creation** ("Build", a mobile AI game-creation tab, and **AI Scene Generation** from a prompt + reference image, refined in Studio), **engine realism**, **monetization** (a creator **Wallet** with daily USD payouts for U.S. 18+ sole proprietors from Dec 2026, a **Roblox Card** in 2027) and **reach** (Chrome browser play by end of 2026, **offline play** that can mix with online modes (mid-2027 per press), standalone "Roblox Everywhere" apps). Discovery now weighs a game's **first 28 days** of performance. Official sources (as of Oct 29, 2026): the Sept 11, 2026 press release, the Wallet DevForum post and the newsroom. The table marks what's still press-only. None of these features has Creator Docs pages yet.

## Announcements by area
| Area | Item | Confidence |
| --- | --- | --- |
| Creation | **Build:** prompt-based game making in the Roblox app. Public alpha started in New Zealand and is **expanding to Serbia and Singapore**, adding an asset library and iterative editing. About 9,000 games published so far, **71% by first-time Studio users** | **Official** (press release) |
| Creation | **Scene Generator:** prompt (+ reference image) → scene, in Build and Studio **"later this year"** (2026), with deeper controls in Studio | **Official** (press release) |
| AI roadmap | Coding, 3D objects, multiplayer NPCs, video/realism (VP Foundation AI) | Press |
| Discovery | Ranking considers a game's **first 28 days**, not just week one | Newsroom |
| Payouts | **Wallet**: daily USD payouts for U.S. 18+ sole proprietors from Dec 2026. U.S. DevEx stays until mid-2027. **Roblox Card** in 2027 ([[Roblox_Wallet_Transition]]) | **Official** (DevForum announcement) |
| Payouts | Higher 18+ U.S. rate (docs: $0.0054 vs $0.0038) ([[Developer_Exchange_DevEx]]) | Docs ✓ |
| Platform | **Browser play:** launch from an Experience Details Page in **Chrome by end of 2026** without installing the app. Other browsers later | **Official** (press release) |
| Platform | **Offline play:** single-player/offline sessions that creators can **combine with online modes in one game**. Mid-2027 timing is press-only | Official (feature) · Press (date) |
| Platform | **Standalone apps:** publish a game as its own app on mobile, PC and consoles, with Roblox providing the tech and services | **Official** (press release) |
| Platform | Reports of letting developers sell games outside Roblox | Single source |

## Shipped in the docs around the same time (verified)
Built-in Studio MCP server + coding-harness guide ([[Roblox_Studio_MCP_Server]]), Assistant planning mode and skills ([[Roblox_Assistant_and_AI_Tools]]), Server Authority full release ([[Server_Authority_Model]]), Character Controller Library beta, UI styling/StyleSheets ([[UI_Styling_StyleSheets]]), Roblox Plus and Robux transfers ([[MarketplaceService]]).

## What it means for a combat/VFX creator
- AI tools speed up blockouts and scaffolding, but **game feel** (hit timing, movement) and **server-authoritative netcode** are still the differentiators ([[Combat_System_Architecture]]).
- The 28-day discovery window rewards strong retention after launch, so plan update cadence ([[Retention_and_Engagement_Metrics]]).

## Related
[[Roblox_Wallet_Transition]] · [[Developer_Exchange_DevEx]] · [[Roblox_Studio_MCP_Server]] · [[Roblox_Assistant_and_AI_Tools]] · [[Server_Authority_Model]] · [[UI_Styling_StyleSheets]] · [[MarketplaceService]] · [[Retention_and_Engagement_Metrics]] · [[Combat_System_Architecture]] · [[Release_Notes_and_Change_Tracking]] · [[MOC_Resource_Hub_and_Community]]

## Sources
- https://about.roblox.com/newsroom/2026/09/rdc-2026-the-world-needs-more-play
- https://www.businesswire.com/news/home/20260911312666/en/Roblox-Unveils-New-Ways-to-Play-Build-and-Grow-at-the-Roblox-Developers-Conference-RDC (official press release, Sept 11, 2026; same text as ir.roblox.com, which is blocked from the research environment)
- https://devforum.roblox.com/t/rdc26-what-we-announced/4865880 (staff summary; not readable from the research environment)
- https://gamesbeat.com/roblox-hits-20-and-opens-rdc-2026-to-invite-the-world-to-play-and-make-games-dave-baszucki-keynote/ · https://gamesbeat.com/roblox-dives-into-the-details-on-its-rdc-engine-updates-roblox-wallet-and-offline-play-press-briefing/
- https://gamesbeat.com/roblox-unveils-creator-wallets-and-physical-cards-rdc-2026/ · https://www.pockettactics.com/roblox/ai-build · https://allthings.how/roblox-rdc-every-major-announcement-for-players-and-creators/
- https://www.progameguides.com/roblox/rdc-2026-roblox-announces-standalone-apps-offline-play-ai-tools-and-more/ · https://northeasttimes.com/2026/09/15/roblox-plans-to-let-developers-sell-games-outside-its-platform/
