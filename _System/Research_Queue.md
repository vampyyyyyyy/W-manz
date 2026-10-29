# Research Queue

Prioritized work for the research agent. **P1** = verify or correct facts the vault already relies on. **P2** = new coverage. **P3** = depth and polish. The agent works top-down after processing `_Inbox/`, checks items off, and moves them to the [[Changelog]] when done. Humans can add items anywhere (plain text is fine).

Format: `- [ ] (P#) Topic: what to find out (where to look)`

## P1: Verify / keep current
- [x] (P1) Roblox Wallet: official DevForum announcement found (U.S. 18+ sole proprietors from Dec 2026, daily USD payouts, 2SV required, U.S. DevEx until mid-2027). Updated [[Roblox_Wallet_Transition]] and [[Developer_Exchange_DevEx]] (also added the official Nov 1, 2026 DevEx royalty tax change) on 2026-10-27.
- [ ] (P1) Roblox Wallet follow-up: fees, minimums, group-owned earnings, under-18 path, the 30-day holding claim, Airwallex partnership, excluded U.S. states. Read the full DevForum post (4865505) from a machine that can reach devforum.roblox.com, or wait for a Creator Docs page. Then set [[Roblox_Wallet_Transition]] to `complete`.
- [x] (P1) RDC 2026 items: confirmed in the official Sept 11, 2026 press release (Build alpha expansion, Scene Generator "later this year", Chrome browser play by end of 2026, offline play mixable with online modes, standalone apps). Updated [[RDC_2026_Recap]] on 2026-10-29.
- [ ] (P2) RDC follow-up: the offline-play mid-2027 date, the AI roadmap items, and the "sell games outside Roblox" report are still press-only. Check the "RDC26: What We Announced" DevForum post (4865880) when it's readable.
- [x] (P1) Server Authority: confirmed full release (DevForum "[Full Release]" post). Exact date still unverified (a secondary source says July 9, 2026), and one docs page (scripting/security/network-ownership) still says "beta". Updated [[Server_Authority_Model]].
- [x] (P1) New type solver rollout state: GA announcement confirmed (on for nocheck/nonstrict; strict projects opted out under `Default`; beta toggle removed Jan 7, 2026). [[New_Type_Solver]] is now `complete` (2026-10-27).
- [ ] (P1) Watch for the new type solver becoming default for strict projects, or a removal date for the old solver (DevForum topic 4084991, Luau release notes). Also pin the exact GA post date.
- [ ] (P1) Weekly: diff Creator Docs release notes. *2026-10-27: per-version release data isn't in the repo's Markdown/YAML, and create.roblox.com and devforum.roblox.com don't resolve from the cloud environment. Found Release Notes 744 (Oct 2026) via search but couldn't read it. 2026-10-29: confirmed the repo has no per-version release data (only `releases.md`). DevForum "Weekly Recap" posts reached via WebSearch work as a fallback (that's how the AvatarUnificationMode deprecation was found).* Diff (`Roblox/creator-docs`, `content/en-us/releases*`) and update affected notes ([[Release_Notes_and_Change_Tracking]]).
- [ ] (P1) Weekly: `luau-lang/rfcs` changes, especially implementation progress on classes ([[Luau_RFC_Tracker]], [[Luau_Classes_Proposal]]). *Last done 2026-10-29: shared self types withdrawn; classes prototype (with inheritance) behind a Debug flag; open RFC PRs #242/#247/#259/#267. Also grep `luau-lang/luau` `Ast/src/Parser.cpp` for new `LUAU_FASTFLAGVARIABLE` syntax flags.*
- [ ] (P1) Watch `if local` / `if const` beta: does it reach live servers, does an RFC merge, and do Luau LSP, StyLua and Selene support it? Update [[If_Local_Bindings]] and set `complete` once it graduates.
- [ ] (P1) `AvatarUnificationMode` removal on Dec 1, 2026: what replaces it and what R6 games get by default afterward. Update [[Humanoid_and_Character_Model]].
- [ ] (P1) Monthly: re-check last-commit dates for [[Community_Modules_Index]].
- [x] (P1) FFlag override restrictions: official allowlist announcement (DevForum 3966569) cited in [[Fast_Flags_and_Beta_Features]] on 2026-10-29. The exact rollout date is still secondary (about Sept 29, 2025).

## P2: New notes to add (create with the templates, link from the right MOC)
- [ ] (P3) Creator Docs page `scripting/security/network-ownership` still says server authority is "currently in beta" (re-checked 2026-10-27). Consider filing a docs issue on `Roblox/creator-docs`, but ask the owner first.
- [ ] (P2) AssetService in-experience creation: `PromptCreatePlatformContentAsync` replaces the older prompt call (Weekly Recap Oct 19–23, 2026), and `CreateAssetAsync` can now be used in Studio. Covers UGC and avatar-creation flows, safety and moderation.
- [ ] (P2) Audio API objects (AudioPlayer, AudioEmitter, AudioListener, effects) as a dedicated deep dive for combat SFX and spatial weather audio.
- [ ] (P2) ProximityPrompt and DragDetector design patterns (security notes already in [[Client_Triggered_Instance_Security]]).
- [ ] (P2) Avatar and character customization: R15 rigs, layered clothing, HumanoidDescription.
- [ ] (P2) Localization pipeline (LocalizationService, translations, rich-text caveats).
- [ ] (P2) Voice chat APIs and safety rules.
- [ ] (P2) Vehicles and suspension with constraints (racing, mounts).
- [ ] (P2) Destruction: CSG/solid modeling at runtime, fracture, debris pooling.
- [ ] (P2) Water: terrain water, buoyancy, rain-to-puddle-to-river ideas (extends [[Weather_System_Architecture]]).
- [ ] (P2) Path2D and UI drag detectors for advanced UI.
- [ ] (P2) Creator Store and selling plugins and models.

## P3: Depth & polish
- [ ] (P3) ODM: add a full working prototype (anchor selection, reel force tuning table, gas economy curve) to [[ODM_Gear_System]].
- [ ] (P3) Combat: benchmark raycast vs shapecast vs overlap hitboxes at 30 players and record the numbers in [[Hitbox_Detection_Methods]] ([[Benchmarking_Methodology]]).
- [ ] (P3) Weather: measured costs (MicroProfiler captures) for rain at 3 densities on mobile ([[Rain_and_Precipitation]]).
- [ ] (P3) Add `forum-archive` notes from inbox showcases as they arrive.
