---
aliases: [Type solver v2, New solver, UseNewLuauTypeSolver]
tags:
  - roblox-dev
  - luau/types
type: concept
last_updated: 2026-10-27
status: complete
---
# New Type Solver

> **TL;DR:** Luau's type inference was rewritten ("new solver"). It's more accurate, built on semantic subtyping, and it enables features like [[User_Defined_Type_Functions|type functions]], [[Read_Write_Property_Modifiers|read/write properties]], negation in refinements and better `setmetatable` inference. On Roblox, `Workspace.UseNewLuauTypeSolver` controls it. It is on by default for `nocheck`/`nonstrict` scripts, but **projects with `--!strict` scripts stay on the old solver until you set it to `Enabled`** (as of Oct 2026).

## Status (as of Oct 27, 2026)
- **Confirmed (API reference, Creator Docs at Oct 27, 2026):** `Workspace.UseNewLuauTypeSolver` is an `Enum.RolloutState` (`Default` follows the engine-wide rollout, `Disabled` opts out, `Enabled` opts in). It is `NotScriptable`, so you set it in Studio's Properties window, not from code. `Workspace.LuauTypeCheckMode` picks the *mode* and this property picks the *solver* ([[Type_Checking_Modes]]).
- **Confirmed (staff announcement "[General Release] Luau's New Type Solver", DevForum topic 4084991, likely Nov 2025):**
  - The New Type Solver and "Non-Strict by Default" left Studio Beta. The new solver rolled out to **everyone using `nocheck` and `nonstrict` scripts**.
  - **Projects that contain `--!strict` scripts are opted out under `Default`.** They keep the old solver until you set `UseNewLuauTypeSolver = Enabled`. Roblox's stated reason: open issues still block strict projects, and creators have real type errors to fix that the old solver missed.
  - The Studio Beta toggle was removed in the first release of 2026 (**Jan 7, 2026**). Beta testers using strict mode had to switch the property from `Default` to `Enabled` to stay on the new solver.
  - Roblox said it would keep polishing the solver "into 2026", and that creators can move strict projects over at their own pace.
- **Not found (as of Oct 27, 2026):** no later announcement that makes strict projects default to the new solver, and no removal date for the old solver. The engine source (`luau-lang/luau`, release 744, Oct 23, 2026) is still actively fixing the new solver, for example refinement simplification fixes in Oct 2026. Treat "strict projects default to the old solver" as the current state, but re-check before relying on it.
- **What this means for a `--!strict` codebase (the typical production setup):** you are probably still on the **old** solver unless someone set the property. Type functions and read/write modifiers won't behave as the docs describe until you opt in.
- Make CI tooling ([[Luau_LSP]]) use the same solver as Studio. Otherwise CI and the Script Analysis window will disagree.

## What changes for you
- **Fewer false positives** on unions, intersections and table shapes. A few **new errors** where the old solver was unsound.
- **Type functions** (`type function`), builtin type functions (`keyof`, `index`, `rawget`, `getmetatable`/`setmetatable` type functions) and **read/write property modifiers** depend on the new solver.
- Better inference for OOP via `setmetatable` ([[OOP_Class_Patterns]]), though the docs still recommend some explicit annotations.
- Error messages differ. Search the DevForum "New Type Solver" thread when an error looks wrong.

## Migration tips
1. Set `Workspace.UseNewLuauTypeSolver = Enabled` in a branch copy of the place, open your biggest modules, and look at the Script Analysis window.
2. Fix *real* bugs first (nil-safety, wrong table shapes). Use `:: any` only for genuinely dynamic code.
3. Keep `--!strict` files strict. Don't retreat to `--!nocheck` to silence the new solver.

## Related
[[Luau_Type_System]] · [[Type_Checking_Modes]] · [[User_Defined_Type_Functions]] · [[Read_Write_Property_Modifiers]] · [[Type_Refinements]] · [[Generics]] · [[OOP_Class_Patterns]] · [[Luau_LSP]] · [[Luau_RFC_Tracker]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/Workspace#UseNewLuauTypeSolver
- https://devforum.roblox.com/t/general-release-luau%E2%80%99s-new-type-solver/4084991 (staff GA announcement; read via search excerpts because the cloud environment can't reach devforum.roblox.com directly)
- https://devforum.roblox.com/t/new-type-solver-beta/3155804 (earlier beta thread)
- https://github.com/luau-lang/luau (commit log through release 744, Oct 23, 2026)
- https://luau.org/news/2022-10-31-luau-semantic-subtyping
