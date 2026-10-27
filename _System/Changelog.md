# Changelog

Newest first. Every research run appends an entry: date, what changed, sources checked, open questions. Keep entries short and link the notes you touched.

## 2026-10-27: Correction after first test run
- **Server Authority is in full release** (DevForum "[Full Release] Ship Fair And Competitive Games with Server Authority"). Removed "beta" wording across [[Server_Authority_Model]] (now `complete`), [[Movement_Validation]], [[Exploit_Threat_Model]], [[Replication_Model]], [[Client_Prediction_and_Reconciliation]], [[ODM_Gear_System]], [[Fast_Flags_and_Beta_Features]], [[RDC_2026_Recap]], [[Glossary]] and the Engine MOC. Found by the first automated research run, then verified.
- Note: Creator Docs page `scripting/security/network-ownership` still says "currently in beta". It's stale; prefer the announcement.

## 2026-10-27: Vault created
- Built the full taxonomy (00_MOC to 09_RESOURCE_HUB_&_COMMUNITY): **300 atomic notes**, every one with valid frontmatter, at least 8 links (average about 13) and at least one backlink. The linter passes with 0 errors.
- Primary sources: `Roblox/creator-docs` (Oct 2026), `luau-lang/rfcs`, `luau-lang/luau`, luau.org, and 35+ community repos (cloned and dated). Secondary: RDC 2026 press coverage (marked `needs-verification`).
- Highlights of 2025–26 changes captured: Server Authority (full release), Character Controller Library, built-in Studio MCP server and coding-harness workflow, Script Sync, engine StyleSheets, `BindReceiptHandler`, Roblox Plus and Robux transfers, Creator Rewards, the DevEx 0.0038/0.0054 rates, Managed Pricing, Configs and Experiments, Kids/Select audience tiers, RTBF deletion templates, Luau `const` and read/write properties, and lifting of the parser-backtracking restriction (Oct 15, 2026).
- Notes marked `needs-verification`: [[Server_Authority_Model]], [[New_Type_Solver]], [[Roblox_Wallet_Transition]], [[RDC_2026_Recap]].
- Not reachable from the build environment: Google Drive (network policy) and Discord (requires a logged-in account, scraping not allowed). Use `_Inbox/` instead ([[Inbox_Guide]]).
- See also: [[Home]] · [[Research_Queue]]
