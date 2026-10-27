---
aliases: [Refinements, Type narrowing, Type guards]
tags:
  - roblox-dev
  - luau/types
type: concept
last_updated: 2026-10-27
status: complete
---
# Type Refinements

> **TL;DR:** Inside an `if`, Luau **narrows** a value's type based on the condition. Truthiness removes `nil` and `false`. `type(x) == "string"` / `typeof(x) == "Instance"` pick a union member. `x:IsA("BasePart")` narrows Roblox classes. Equality against a singleton picks a tagged-union branch. Refinements are how `unknown` input becomes usable safely.

## Forms that refine
```luau
--!strict
local function handle(input: unknown)
	if typeof(input) == "Vector3" then
		print(input.Magnitude)            -- input: Vector3
	elseif type(input) == "string" then
		print(#input)                     -- input: string
	end
end

local function rootOf(char: Model?): BasePart?
	if not char then return nil end     -- char: Model below this line
	local root = char:FindFirstChild("HumanoidRootPart")
	if root and root:IsA("BasePart") then
		return root                       -- root: BasePart
	end
	return nil
end

type Event = { kind: "hit", target: Model, damage: number } | { kind: "heal", amount: number }
local function apply(e: Event)
	if e.kind == "hit" then
		print(e.target, e.damage)         -- tagged union narrowed by the 'kind' singleton
	else
		print(e.amount)
	end
end
```

## What refines
- Truthiness: `if x`, `if not x then return end`, `x and x.y`
- `type(x) == "..."` and `typeof(x) == "..."` (either order)
- `x == nil`, `x ~= nil`, equality with singletons (`state == "Idle"`)
- `:IsA("ClassName")` on Instances
- `assert(x)` narrows afterwards
- Combinations with `and`, `or`, `not`. The new solver handles negation better ([[New_Type_Solver]])

## Gotchas
- Refinement applies to **locals**, not to arbitrary expressions. `if t.a.b then use(t.a.b) end` re-reads and may not narrow. Copy to a local first.
- A yield between check and use (e.g. `task.wait`) doesn't invalidate the static refinement, **but the instance may be destroyed at runtime**. Re-check after yields ([[Instance_Lifecycle_and_Destroy]]).
- `type()` sees every Roblox value as `"userdata"`, so use `typeof()` for Roblox types ([[Typeof_vs_type]]).

## Related
[[Luau_Type_System]] · [[Typeof_vs_type]] · [[Type_Annotations_and_Casts]] · [[Table_Types]] · [[New_Type_Solver]] · [[Server_Side_Validation]] · [[Finite_State_Machines]] · [[Instance_Lifecycle_and_Destroy]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://luau.org/types/refinements
