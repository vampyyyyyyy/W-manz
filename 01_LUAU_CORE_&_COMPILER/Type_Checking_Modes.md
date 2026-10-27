---
aliases: [--!strict, --!nonstrict, --!nocheck, strict mode, LuauTypeCheckMode]
tags:
  - roblox-dev
  - luau/types
type: concept
last_updated: 2026-10-27
status: complete
---
# Type Checking Modes

> **TL;DR:** A comment directive on the first line picks how hard the analyzer checks the file. **`--!strict`** infers and reports everything. **`--!nonstrict`** (default) gives unannotated values `any`. **`--!nocheck`** turns checking off. New Roblox code should be strict, especially shared modules and anything handling remote input.

## The directives
```luau
--!strict     -- full inference + errors; required to get real value from types
--!nonstrict  -- default when no directive: unannotated params/locals are 'any'
--!nocheck    -- no type errors reported (legacy or generated code)
```
Other directives live in the same comment slot: `--!native` ([[Native_Code_Generation]]), `--!optimize 0|1|2` ([[Luau_Compiler_Optimizations]]), `--!nolint`.

## Experience-wide default (Roblox)
`Workspace.LuauTypeCheckMode` sets the mode for scripts without a directive. `Workspace.UseNewLuauTypeSolver` (`Enum.RolloutState`: `Default`/`Disabled`/`Enabled`) chooses the solver implementation ([[New_Type_Solver]]). File directives still win per script.

## Strict vs nonstrict in practice
```luau
--!nonstrict
local function add(a, b) return a + b end  -- a, b: any. add("x", {}) is NOT an error

--!strict
local function add(a, b) return a + b end  -- a, b inferred from usage (generic or number);
add("x", {})                               -- error: cannot add string and table
```

## Adoption strategy for existing projects
1. Turn on `--!strict` for **leaf modules** first (utilities, config, math). They have few dependencies.
2. Give module APIs explicit types (`export type`), then upgrade their consumers.
3. Use `unknown` at trust boundaries (remotes, DataStore loads) and refine ([[Type_Refinements]]).
4. Keep a temporary `:: any` cast on genuinely dynamic code and leave a `TODO`. Don't drop the whole file to nocheck.
5. Run `luau-lsp analyze` in CI so types can't regress ([[GitHub_Actions_CI_CD]], [[Luau_LSP]]).

## Related
[[Luau_Type_System]] · [[New_Type_Solver]] · [[Type_Annotations_and_Casts]] · [[Type_Refinements]] · [[Native_Code_Generation]] · [[Luau_Compiler_Optimizations]] · [[Luau_LSP]] · [[Selene]] · [[GitHub_Actions_CI_CD]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://create.roblox.com/docs/luau/comments#comment-directives
- https://create.roblox.com/docs/reference/engine/classes/Workspace#LuauTypeCheckMode
- https://create.roblox.com/docs/reference/engine/classes/Workspace#UseNewLuauTypeSolver
