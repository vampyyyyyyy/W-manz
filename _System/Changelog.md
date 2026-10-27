# Changelog

Newest first. Every research run appends an entry: date, what changed, sources checked, open questions. Keep entries short and link the notes you touched.

## 2026-10-27: First scheduled research run (P1 items)
- **[[New_Type_Solver]] → `complete`.** Staff GA post "[General Release] Luau's New Type Solver": the new solver is on for `nocheck`/`nonstrict`, **projects with `--!strict` scripts stay on the old solver under `Default`** until `UseNewLuauTypeSolver = Enabled`, and the beta toggle was removed Jan 7, 2026. The property is `NotScriptable` (API YAML). Found no announcement since then that changes the strict-mode default. Also updated [[Type_Checking_Modes]].
- **[[Roblox_Wallet_Transition]] rewritten from the official DevForum post** "Introducing Roblox Wallet and Card: Get Paid Faster": U.S. 18+ sole proprietors from Dec 2026, automatic USD payouts every business day, 2SV required, U.S. DevEx until mid-2027, Robux buy-back at $0.0038, Card in 2027. Airwallex, state exclusions, UK/EU timing and the 30-day hold stay labeled as unconfirmed. The status stays `needs-verification` because fees, groups and the under-18 path are unpublished. [[RDC_2026_Recap]]'s payout row is now marked official.
- **New fact (official docs): DevEx becomes royalty income on Nov 1, 2026.** Tax info moves to Creator Hub ▸ Taxes, and invalid or missing info means 24% backup withholding. Non-U.S. creators pay 0–30% withholding on U.S.-player sales depending on treaty. **Deadline Oct 31, 2026.** Added to [[Developer_Exchange_DevEx]].
- Release-notes sweep: incomplete (see the queue). The only contradiction found is the already-known stale "beta" line on the network-ownership docs page.
- Sources: `Roblox/creator-docs` @ 2026-10-27 (Workspace.yaml, tax-information.md), `luau-lang/luau` @ release 744 (2026-10-23), and DevForum posts 4084991 and 4865505 via search excerpts (direct fetch blocked).
- Open questions: Wallet fees, groups and minors; strict-mode solver default; how to read weekly release notes from the cloud.

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
