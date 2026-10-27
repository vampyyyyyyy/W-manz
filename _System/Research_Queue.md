# Research Queue

Prioritized work for the research agent. **P1** = verify or correct facts the vault already relies on. **P2** = new coverage. **P3** = depth and polish. The agent works top-down after processing `_Inbox/`, checks items off, and moves them to the [[Changelog]] when done. Humans can add items anywhere (plain text is fine).

Format: `- [ ] (P#) Topic: what to find out (where to look)`

## P1: Verify / keep current
- [ ] (P1) Roblox Wallet: official payout details, fees, minimums, eligibility for under-18 creators, DevEx sunset timing (Creator Hub ▸ Finances, DevForum Announcements). Update [[Roblox_Wallet_Transition]] and [[Developer_Exchange_DevEx]], and set `status: complete` once confirmed.
- [ ] (P1) RDC 2026 items: confirm Build, AI Scene Generation, browser and offline play timelines in official posts. Update [[RDC_2026_Recap]].
- [ ] (P1) Server Authority: GA date, any API changes since the beta docs. Update [[Server_Authority_Model]] (still `needs-verification`).
- [ ] (P1) New type solver rollout state (`Workspace.UseNewLuauTypeSolver` default). Update [[New_Type_Solver]].
- [ ] (P1) Weekly: diff Creator Docs release notes (`Roblox/creator-docs`, `content/en-us/releases*`) and update affected notes ([[Release_Notes_and_Change_Tracking]]).
- [ ] (P1) Weekly: `luau-lang/rfcs` changes, especially implementation progress on classes ([[Luau_RFC_Tracker]], [[Luau_Classes_Proposal]]).
- [ ] (P1) Monthly: re-check last-commit dates for [[Community_Modules_Index]].
- [ ] (P1) FFlag override restrictions: find the official announcement and cite it in [[Fast_Flags_and_Beta_Features]].

## P2: New notes to add (create with the templates, link from the right MOC)
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
