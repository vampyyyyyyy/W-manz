# Changelog

Newest first. Every research run appends an entry: date, what changed, sources checked, open questions. Keep entries short and link the notes you touched.

## 2026-11-02: Scheduled research run (change sweep: security + teleports)
- Inbox: empty.
- **New note: [[Device_Trust_API]]** (`complete`, from the official Creator Docs page and API YAML @ 2026-10-29). Covers `IntegrityService.EvaluatePlayerDeviceTrust` and `Player.DeviceTrustLevel`, with levels, platform coverage (only Android, Chromebook and Quest verified; web = `None`; Windows, iOS, macOS and consoles = `Unknown`), the official genre policies, callback rules (fail-open, ~10 s timeout, one per place), the measures caveat, Studio testing, and a strict-mode ranked-queue gate for a battlegrounds game. Linked from [[MOC_Anti_Exploit]], [[MOC_Networking_Security_and_Buffers]], [[Exploit_Threat_Model]], [[Data_Duplication_and_Trade_Exploits]] and [[Matchmaking_Customization]].
- **[[TeleportService_and_Reserved_Servers]] rewritten:** `TeleportOptions.ReservedServerId` (a server-generated GUID; the first teleport creates the server, reuse routes to it) and `VipServerId` replace the access-code flow. **`ReserveServerAsync`, `ReservedServerAccessCode` and `ShouldReserveServer` are deprecated** (they still work). Added routing rules, reserved-server ID security, and a migration table. The old core example used `ShouldReserveServer`. Also updated [[Paid_Access_and_Private_Servers]] and [[Legacy_Code_Smells]].
- **[[Humanoid_and_Character_Model]]:** the AvatarUnificationMode enum docs now say the property "no longer has an effect; R6 avatars always load as R6 rigs". After Dec 1 the risk is code built *for* the adapter, not classic R6 code.
- **[[If_Local_Bindings]]:** added the `while local` prototype (debug-only flag, release 745).
- **Formatting fix in 13 notes:** 14 places where a text line or code fence followed a table without a blank line, so it rendered as a broken table row. `last_updated` not bumped (formatting only).
- Sources: `Roblox/creator-docs` @ 2026-10-29 (`scripting/security/device-trust.md`, `projects/teleport-private-servers.md`, `projects/teleport.md`, IntegrityService/Player/TeleportOptions/AvatarUnificationMode YAML), `luau-lang/luau` @ release 745, `luau-lang/rfcs` (no changes), and "Weekly Recap: October 26–30, 2026" via search excerpts.
- Open questions: the other recap betas (orthographic camera, Web Play, AnimatedImage) are unverified; Device Trust Windows timing.

## 2026-10-29: Scheduled research run (Luau change sweep, P1 items)
- Inbox: empty.
- **New note: [[If_Local_Bindings]]** (`needs-verification`). It covers `if local` / `if const`, a Roblox Studio beta since Oct 6, 2026. The semantics come from the engine's own tests (`luau-lang/luau` parser, compiler and conformance tests): truthiness test, binding scoped to the `then` block only, single binding, works in `elseif` and if-expressions. Includes a server-validation example and gotchas (`false` is a miss). There's no merged RFC yet. Linked from [[MOC_Luau_Core_and_Compiler]], [[Luau_Syntax_Extensions]], [[Fast_Flags_and_Beta_Features]] and [[Luau_RFC_Tracker]].
- **[[Luau_Classes_Proposal]] corrected:** no longer "not yet implemented". The prototype has been in `luau-lang/luau` since at least May 2026 behind the debug-only `DebugLuauUserDefinedClasses` flag, and it already has `open class` / `extends` inheritance and `__init` constructors that aren't in the merged RFC. Open RFC PRs #242/#247/#259/#267 are redesigning construction, private fields and inheritance. It's not usable on Roblox.
- **[[Luau_RFC_Tracker]]:** added an "in source, not on Roblox" table (classes, `if local`, `export` values, 64-bit `integer`) and recent changes. **Shared self types withdrawn** (Oct 13, 2026), so [[OOP_Class_Patterns]] now says to keep annotating `self` explicitly.
- **[[RDC_2026_Recap]]:** Build, Scene Generator, browser play, offline play and standalone apps are now marked official (Sept 11, 2026 press release). The offline mid-2027 date stays press-only, and the TL;DR's "local-currency payouts" is now USD.
- **[[Fast_Flags_and_Beta_Features]]:** cited the official client FFlag allowlist announcement.
- **[[Humanoid_and_Character_Model]]:** `Workspace.AvatarUnificationMode` (the R6-to-R15 adapter) is a planned deprecation. Test before **Dec 1, 2026** (staff weekly recap). No replacement has been announced. Added an R6 combat checklist.
- Sources: `luau-lang/luau` @ 2026-10-29, `luau-lang/rfcs` @ 2026-10-16, `Roblox/creator-docs` @ 2026-10-29 (Workspace/AssetService API YAML), Business Wire press release, and DevForum posts via search excerpts (direct fetch is blocked; ir.roblox.com is also blocked).
- Open questions: `if local` live availability; the AvatarUnificationMode replacement; the RDC offline-play date.

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
