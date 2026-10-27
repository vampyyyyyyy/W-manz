---
aliases: [Type solver v2, New solver, UseNewLuauTypeSolver]
tags:
  - roblox-dev
  - luau/types
type: concept
last_updated: 2026-10-27
status: needs-verification
---
# New Type Solver

> **TL;DR:** Luau's type inference was rewritten ("new solver"). It's more accurate, built on semantic subtyping, and it enables features like [[User_Defined_Type_Functions|type functions]], [[Read_Write_Property_Modifiers|read/write properties]], negation in refinements and better `setmetatable` inference. On Roblox it's controlled by `Workspace.UseNewLuauTypeSolver`, a `RolloutState` that follows the engine-wide rollout by default.

## Status (as of Oct 2026)
- **Confirmed (official docs):** `Workspace.UseNewLuauTypeSolver` exists with `Default` (engine rollout), `Disabled` (opt out) and `Enabled` (opt in). The Luau docs mention behavior "in the new type solver" throughout.
- **Reported (secondary sources, verify on the DevForum):** around Nov 2025 Roblox took the solver out of Studio Beta and enabled it by default for `nocheck`/`nonstrict` scripts, with strict-mode users able to opt in and the beta toggle removed in early Jan 2026. The legacy solver reportedly stays available through 2026 and is slated for removal.
- Action: set `UseNewLuauTypeSolver = Enabled` in projects you want on the new solver now, and make sure CI tooling ([[Luau_LSP]]) uses the same solver as Studio.

## What changes for you
- **Fewer false positives** on unions, intersections and table shapes. A few **new errors** where the old solver was unsound.
- **Type functions** (`type function`), builtin type functions (`keyof`, `index`, `rawget`, `getmetatable`/`setmetatable` type functions) and **read/write property modifiers** depend on the new solver.
- Better inference for OOP via `setmetatable` ([[OOP_Class_Patterns]]), though the docs still recommend some explicit annotations.
- Error messages differ. Search the DevForum "New Type Solver" thread when an error looks wrong.

## Migration tips
1. Flip the property on in a branch place, open your biggest modules, and look at the Script Analysis window.
2. Fix *real* bugs first (nil-safety, wrong table shapes). Use `:: any` only for genuinely dynamic code.
3. Keep `--!strict` files strict. Don't retreat to `--!nocheck` to silence the new solver.

## Related
[[Luau_Type_System]] · [[Type_Checking_Modes]] · [[User_Defined_Type_Functions]] · [[Read_Write_Property_Modifiers]] · [[Type_Refinements]] · [[Generics]] · [[OOP_Class_Patterns]] · [[Luau_LSP]] · [[Luau_RFC_Tracker]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/Workspace#UseNewLuauTypeSolver
- https://devforum.roblox.com/t/new-type-solver-beta/3155804 (beta thread; check for the GA announcement)
- https://luau.org/news/2022-10-31-luau-semantic-subtyping
