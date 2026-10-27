---
aliases: [Type functions, type function, UDTF, keyof, index type]
tags:
  - roblox-dev
  - luau/types
type: concept
last_updated: 2026-10-27
status: complete
---
# User-Defined Type Functions

> **TL;DR:** `type function` declares Luau code that runs **at analysis time** on *types*, not values. It uses the `types` library to inspect and build types. Use it to derive `Partial<T>`, `ReadOnly<T>`, key unions, network schemas or component types without hand-duplicating definitions. Builtins like `keyof<T>` and `index<T, K>` cover common cases. Requires the [[New_Type_Solver]].

## Example: `Partial<T>` (all props optional)
```luau
--!strict
type function Partial(t)
	if not t:is("table") then
		error("Partial expects a table type")
	end
	local out = types.newtable()
	for key, prop in t:properties() do
		-- properties() maps key -> { read: type?, write: type? }
		if prop.read then
			out:setproperty(key, types.optional(prop.read))
		end
	end
	return out
end

type Stats = { hp: number, stamina: number, speed: number }
type StatPatch = Partial<Stats>  -- { hp: number?, stamina: number?, speed: number? }
```

## Builtin type functions
| Function | Result |
| --- | --- |
| `keyof<T>` / `rawkeyof<T>` | Union of a table's string keys (`rawkeyof` ignores `__index`) |
| `index<T, K>` / `rawget<T, K>` | The type of `T[K]` |
| `getmetatable<T>` / `setmetatable<T, MT>` | Metatable types, used by OOP inference |
| `typeof(expr)` | (classic) type of a value expression |

## Environment and API
- Inside type functions you get `types`, plus `assert`, `error`, `print`, `pairs`/`ipairs`/`next`, `select`, `unpack`, `getmetatable`/`setmetatable`, `raw*`, `tonumber`/`tostring`, `type`/`typeof`, and the `math`, `table`, `string`, `bit32`, `utf8` and `buffer` libraries.
- `types` constructors: `types.singleton(v)`, `types.unionof(...)`, `types.intersectionof(...)`, `types.optional(t)`, `types.negationof(t)`, `types.newtable(props?, indexer?, metatable?)`, `types.newfunction(...)`, and more. Instances expose `:is("table" | "union" | ...)`, `:properties()` (key → `{ read: type?, write: type? }`), `:setproperty`, `:setreadproperty`/`:setwriteproperty`, `:readproperty`, `types.copy`, `types.generic(name, ispack)`, etc.
- Roblox engine classes appear as **extern** types inside type functions (renamed from "class" types in 2025).

## When to use it
- ✅ Library authors: reflect schemas (networking, ECS components, data templates) into types.
- ❌ App code that a simple `type` alias could express. Type functions add analysis cost and complexity.

## Related
[[Luau_Type_System]] · [[New_Type_Solver]] · [[Generics]] · [[Table_Types]] · [[Read_Write_Property_Modifiers]] · [[Metatables]] · [[ECS_Libraries_Jecs_and_Matter]] · [[Luau_RFC_Tracker]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://luau.org/types/type-functions · https://luau.org/types-library
- https://rfcs.luau.org/user-defined-type-functions.html · https://rfcs.luau.org/udtf-is-extern.html
