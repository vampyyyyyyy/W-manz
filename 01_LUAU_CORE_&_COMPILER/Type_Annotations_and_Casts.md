---
aliases: [Type annotations, Type casts, "::", Type assertion]
tags:
  - roblox-dev
  - luau/types
type: concept
last_updated: 2026-10-27
status: complete
---
# Type Annotations & Casts

> **TL;DR:** Annotate **function signatures and module boundaries**. Let inference handle locals. `expr :: T` is a *cast*: an analyzer-only assertion with **no runtime check**. Use it to correct inference, never to "validate" untrusted data.

## Annotation syntax
```luau
--!strict
local speed: number = 16
local function lerpTo(a: Vector3, b: Vector3, t: number): Vector3
	return a:Lerp(b, t)
end
local onHit: (target: Model, damage: number) -> () = function(target, damage) end
type Callback = (...any) -> ()                 -- variadic function type
local cache: { [Player]: { score: number } } = {}
export type Config = { maxHp: number, regen: number? }
```
- `export type` makes a type available to `require`rs as `Module.Config`.
- Optional fields use `?`: `regen: number?` means the key may be missing.
- Generic functions: `local function first<T>(list: { T }): T? return list[1] end` ([[Generics]]).

## Casts (`::`)
```luau
local hrp = character:FindFirstChild("HumanoidRootPart") :: BasePart  -- you assert it exists and is a BasePart
local data = HttpService:JSONDecode(body) :: { version: number }     -- you assert the shape
```
- The analyzer only allows casts between *related* types (e.g. `any` to anything, a supertype to a subtype). To force anything, go through `any`: `(x :: any) :: T`.
- **No runtime effect.** If the instance doesn't exist, you get a runtime error later, not at the cast. For remote arguments, always check at runtime with `typeof` ([[Server_Side_Validation]]).
- Prefer `FindFirstChildOfClass("Humanoid")` or `:WaitForChild("X") :: T` patterns that are actually safe.

## Explicit type instantiation (2025)
```luau
local binding = createBinding<<number?>>(nil)   -- bind generic T explicitly; zero runtime effect
```
This avoids unsound casts like `nil :: number?` when inference picks a type that's too narrow.

## Related
[[Luau_Type_System]] · [[Type_Checking_Modes]] · [[Generics]] · [[Type_Refinements]] · [[Table_Types]] · [[Typeof_vs_type]] · [[Server_Side_Validation]] · [[Require_and_Module_Resolution]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://luau.org/types · https://rfcs.luau.org/explicit-type-parameter-instantiation.html
- https://rfcs.luau.org/syntax-type-ascription.html
