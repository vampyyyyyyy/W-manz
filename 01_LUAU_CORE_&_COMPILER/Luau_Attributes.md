---
aliases: ["@native", "@deprecated", function attributes]
tags:
  - roblox-dev
  - luau/syntax
type: api
last_updated: 2026-10-27
status: complete
---
# Luau Attributes (`@native`, `@deprecated`)

> **TL;DR:** Attributes are built-in `@name` annotations placed before a function declaration. They change compiler or analyzer behavior. Today there are two user-facing ones: **`@native`** (compile this function to machine code) and **`@deprecated`** (lint warning, with optional `use`/`reason` parameters). Users can't define their own.

## `@native`
```luau
@native
local function integrate(positions: buffer, velocities: buffer, count: number, dt: number)
	for i = 0, count - 1 do
		local o = i * 12
		buffer.writef32(positions, o, buffer.readf32(positions, o) + buffer.readf32(velocities, o) * dt)
		-- ...y, z
	end
end
```
- Function-level equivalent of `--!native`. It's **not recursive**: inner functions need their own `@native`.
- Prefer targeted `@native` over file-wide `--!native`, because native code has a **per-game size budget** ([[Native_Code_Generation]]).

## `@deprecated`
```luau
@deprecated
local function oldApi() end
-- warning: Function 'oldApi' is deprecated.

@[deprecated { use = "Combat.applyDamage()", reason = "Handles armor and i-frames." }]
function Combat.dealDamage(target: Model, amount: number) end
-- warning: Member 'Combat.dealDamage' is deprecated, use 'Combat.applyDamage()' instead. Handles armor and i-frames.
```
Great for evolving internal APIs in a team or a library ([[Luau_LSP]] shows deprecated members with a distinct style).

## Syntax forms
- `@attr`, `@[attr]` and `@[attr()]` are equivalent. Combine with `@native @deprecated` or `@[deprecated {...}, native]`.
- Works on `local function`, `function t.f`, `function t:m`, and function *expressions*: `local f = @native function(x) return x * 2 end`.
- Parameters must be literals (nil, booleans, numbers, strings, table constructors).

## Related
[[Native_Code_Generation]] · [[Luau_Syntax_Extensions]] · [[Luau_Compiler_Optimizations]] · [[Luau_LSP]] · [[Selene]] · [[Buffer_Library]] · [[Luau_Micro_Optimizations]] · [[Luau_RFC_Tracker]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://luau.org/attributes · https://rfcs.luau.org/syntax-attribute-functions-native.html · https://rfcs.luau.org/syntax-attribute-functions-deprecated.html
