---
aliases: [if local, if const, if-let, Conditional bindings, LuauExperimentalIfLocalSyntax]
tags:
  - roblox-dev
  - luau/syntax
type: concept
last_updated: 2026-10-29
status: needs-verification
---
# If Local Bindings (`if local` / `if const`)

> **TL;DR:** `if local x = expr then … end` declares `x`, runs the block only if `x` is **truthy** (not `nil`, not `false`), and scopes `x` to **that `then` block only**. It isn't visible in `elseif`/`else` or after `end`. `if const` makes the binding immutable ([[Const_Bindings]]). It also works in `elseif` and in if-expressions. **Status (Oct 29, 2026):** Roblox **Studio beta** (DevForum, Oct 6, 2026), with the parser behind `LuauExperimentalIfLocalSyntax` in `luau-lang/luau`. There's no merged RFC yet. Don't ship it in live code until it graduates.

## Status (as of Oct 29, 2026)
| Fact | Confidence |
| --- | --- |
| Announced as a **beta** by Roblox staff on Oct 6, 2026 ("[Beta] if local Statements and Expressions") | Confirmed (announcement, read via search excerpts) |
| Implemented in `luau-lang/luau` behind `LuauExperimentalIfLocalSyntax` (parser, compiler, conformance tests), first synced around release 740 (Sept 25, 2026). Type-checker support sits behind a second flag, `LuauExperimentalIfLocalAnalysis` | Confirmed (source and tests) |
| A merged RFC in `luau-lang/rfcs/docs` | **None** yet. The syntax could still change |
| Works in **live servers and clients**, not just Studio | **Unknown.** Assume Studio-only while it's a beta ([[Fast_Flags_and_Beta_Features]]) |

## Semantics (verified against the engine's own tests)
```luau
if local character = player.Character then
	-- character: Model (narrowed from Model?)
	print(character.Name)
end
-- `character` does not exist here
```
- **The test is truthiness of the bound value.** `nil` and `false` skip the block. `0`, `""` and `{}` enter it (normal Luau truthiness). The compiler emits a plain `JUMPIFNOT` on the local, so it costs the same as `local x = …; if x then`.
- **Scope = the `then` block only.** The binding is gone in `else` and in later `elseif` conditions. An outer variable with the same name is shadowed only inside `then`:
  ```luau
  local x = "outer"
  if local x = nil then
  	-- not reached
  else
  	print(x) --> "outer" (the if-local binding isn't visible here)
  end
  ```
- **Exactly one binding.** `if local a, b = f() then` is a parse error ("only a single binding is allowed"). With a multi-return call, only the first value is bound.
- **Annotations work**, and the type still narrows: `if local x: number? = v then` gives `x: number` inside the block ([[Type_Refinements]]).
- **`elseif local`** gives each branch its own independent binding.
- **Expressions:** `local name = if local p = Players:GetPlayerFromCharacter(model) then p.Name else "Unknown"`. In the `else` arm, the name refers to whatever was in scope outside, not the binding.
- `if const x = …` behaves the same but `x` can't be reassigned.

## Where it helps: server-side request validation
Validation chains in remote handlers are mostly "look this up, bail if nil". Today that's a ladder of `local` + `if not x then return end`. Here's the same check with `if local`, as **beta syntax** you can try in Studio only:
```luau
--!strict
-- Server: validate a melee hit request (see Server_Side_Validation)
HitRemote.OnServerEvent:Connect(function(player: Player, targetModel: unknown)
	if typeof(targetModel) ~= "Instance" or not targetModel:IsA("Model") then return end

	if local character = player.Character then
		if local humanoid = character:FindFirstChildOfClass("Humanoid") then
			if local targetHumanoid = targetModel:FindFirstChildOfClass("Humanoid") then
				if humanoid.Health > 0 and targetHumanoid.Health > 0 then
					DamagePipeline.TryApply(player, targetModel, targetHumanoid) -- your own module
				end
			end
		end
	end
end)
```
For **production today**, early-return guards stay the clearer pattern and run everywhere:
```luau
local character = player.Character
if not character then return end
local humanoid = character:FindFirstChildOfClass("Humanoid")
if not humanoid or humanoid.Health <= 0 then return end
```
`if local` wins when you need the binding *only* inside one branch (it keeps the outer scope clean), or inside an if-expression. Early returns still win for long validation chains, because nesting gets deep fast.

## Gotchas
- **`false` is a miss.** `if local enabled = part:GetAttribute("Enabled") then` skips the block for an attribute that exists and is `false`. Use a plain `local` and compare with `~= nil` when `false` is meaningful.
- **Not a pcall.** A throwing expression still throws ([[Error_Handling_pcall_xpcall]]). Bind the result of `pcall` instead: `if local ok = pcall(fn) then` loses the error message, so prefer `local ok, err = pcall(fn)`.
- **Tooling lag:** check that [[Luau_LSP]], [[StyLua]] and [[Selene]] parse the syntax before you adopt it, or CI will fail on files that Studio accepts.

## Related
[[Luau_Syntax_Extensions]] · [[Const_Bindings]] · [[Type_Refinements]] · [[Type_Checking_Modes]] · [[Error_Handling_pcall_xpcall]] · [[Server_Side_Validation]] · [[Damage_Pipeline]] · [[Fast_Flags_and_Beta_Features]] · [[Luau_RFC_Tracker]] · [[Luau_LSP]] · [[StyLua]] · [[Selene]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://devforum.roblox.com/t/beta-if-local-statements-and-expressions/4918297 (staff beta announcement, Oct 6, 2026; read via search excerpts because devforum.roblox.com is blocked from the research environment)
- https://github.com/luau-lang/luau (`Ast/src/Parser.cpp` `parseIfLocalCondition`, `tests/conformance/iflocal.luau`, `tests/Compiler.test.cpp` `IfLocal*`, `tests/TypeInfer.refinements.test.cpp`; read at release 744, Oct 2026)
- https://github.com/luau-lang/rfcs/tree/master/docs (no `if local` RFC merged as of Oct 29, 2026)
