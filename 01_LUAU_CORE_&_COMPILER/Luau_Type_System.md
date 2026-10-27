---
aliases: [Luau types, Type checking, Gradual typing, Typed Luau]
tags:
  - roblox-dev
  - luau/types
type: concept
last_updated: 2026-10-27
status: complete
---
# Luau Type System

> **TL;DR:** Luau has a **gradual, structural** type system. It's checked statically (in Studio, [[Luau_LSP]] and `luau-analyze`) and **erased at runtime**: types never change behavior, but they power autocomplete, catch bugs, and help [[Native_Code_Generation]] specialize code. Use `--!strict` in new code ([[Type_Checking_Modes]]).

## Building blocks
| Concept | Example | Note |
| --- | --- | --- |
| Primitives | `number`, `string`, `boolean`, `nil`, `thread`, `buffer`, `vector` | Plus Roblox types: `Instance`, `Vector3`, `CFrame`… |
| Top/bottom | `unknown` (must refine before use), `never`, `any` (opts out) | Prefer `unknown` for untrusted input ([[Server_Side_Validation]]) |
| Tables | `{ x: number }`, arrays `{ T }`, maps `{ [K]: V }` | Structural: shape matters, not name ([[Table_Types]]) |
| Read/write modifiers | `{ read id: number }` | [[Read_Write_Property_Modifiers]] |
| Functions | `(number, string) -> boolean`, variadics `(...number) -> ()` | Named args: `(target: Model, dmg: number) -> ()` |
| Unions / optionals | `string | number`, `Player?` (= `Player | nil`) | Narrowed by [[Type_Refinements]] |
| Intersections | `A & B` | Overloaded functions, mixins |
| Singletons | `"Idle" | "Attack" | "Stunned"` | Perfect for state machines ([[Finite_State_Machines]]) |
| Generics | `<T>(T) -> { T }`, packs `<A...>` | [[Generics]] |
| Type functions | `type function Partial(t) … end` | Compute types at analysis time ([[User_Defined_Type_Functions]]) |
| `typeof(expr)` in types | `type Module = typeof(require(...))` | Derive a type from a value |

## Example
```luau
--!strict
export type State = "Idle" | "Windup" | "Active" | "Recovery" | "Stunned"
export type Attack = {
	read name: string,
	damage: number,
	windup: number,
	onHit: ((target: Model) -> ())?,
}

local function canAct(state: State): boolean
	return state == "Idle" or state == "Recovery"
end

local swing: Attack = { name = "Light1", damage = 12, windup = 0.18 }
-- swing.name = "x"  -- type error: 'name' is read-only
```

## How it plays with the runtime
- Annotations cost nothing at runtime, **except** that native codegen trusts annotated argument types and inserts checks. Mismatches cause a fallback, not a crash ([[Native_Code_Generation]]).
- `::` casts are **unchecked** assertions to the analyzer ([[Type_Annotations_and_Casts]]).
- Metatables and OOP are the hardest area for inference. Use the documented patterns ([[OOP_Class_Patterns]]).

## Related
[[Type_Checking_Modes]] · [[New_Type_Solver]] · [[Type_Annotations_and_Casts]] · [[Generics]] · [[Type_Refinements]] · [[Table_Types]] · [[Read_Write_Property_Modifiers]] · [[User_Defined_Type_Functions]] · [[OOP_Class_Patterns]] · [[Luau_LSP]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://luau.org/types · https://create.roblox.com/docs/luau/type-checking
