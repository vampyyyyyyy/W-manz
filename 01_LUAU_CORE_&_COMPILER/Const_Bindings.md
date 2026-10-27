---
aliases: [const, const keyword, const local, Immutable binding]
tags:
  - roblox-dev
  - luau/syntax
type: concept
last_updated: 2026-10-27
status: complete
---
# `const` Bindings

> **TL;DR:** `const NAME = value` declares a local that **can't be reassigned**, and that includes `+=`. The **binding** is immutable, not the value: a `const` table can still be mutated unless you also `table.freeze` it. It's documented on Roblox's Creator Hub and implemented in Luau (RFC "Const Keyword").

## Syntax
```luau
const MAX_HEALTH = 100
const GRAVITY: number = workspace.Gravity
const a, b = 1, 2
const function clampHealth(h: number): number
	return math.clamp(h, 0, MAX_HEALTH)
end

MAX_HEALTH = 50      -- error: cannot reassign a const variable
MAX_HEALTH += 1      -- error
clampHealth = nil    -- error
```
- **Must be initialized** at declaration: `const x` alone is an error.
- Lexically scoped, and shadowing is allowed (`const x = 1; do const x = 2 end`).
- Captured by closures, it still can't be reassigned inside them.
- **Contextual keyword**: `local const = 1` still works, so old code doesn't break.

## Binding vs value immutability
```luau
const SETTINGS = { volume = 0 }
SETTINGS.volume = 1       -- OK: mutating the table
SETTINGS = {}             -- error: rebinding

const FROZEN = table.freeze({ volume = 0 })
FROZEN.volume = 1         -- runtime error: table is frozen
```
For config modules, use `const` + `table.freeze` + `read` types ([[Read_Write_Property_Modifiers]], [[Table_Library]]).

## Why use it
- Intent: readers know the name always refers to the same value.
- Safety: catches accidental reassignment in long scopes and closures.
- Future: the proposed `export` keyword builds on const semantics ([[Luau_RFC_Tracker]]).
- The compiler already constant-folds locals that are never reassigned, so `const` is about **correctness**, not speed ([[Luau_Compiler_Optimizations]]).

## Related
[[Luau_Syntax_Extensions]] · [[Read_Write_Property_Modifiers]] · [[Table_Library]] · [[Closures_and_Upvalues]] · [[Luau_Compiler_Optimizations]] · [[Luau_RFC_Tracker]] · [[Luau_Overview]] · [[Luau_Lua_Compatibility]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://create.roblox.com/docs/luau/variables (const section)
- https://rfcs.luau.org/const-keyword.html · https://luau.org/syntax#const-bindings
