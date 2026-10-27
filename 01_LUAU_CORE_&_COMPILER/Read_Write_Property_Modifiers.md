---
aliases: [read-only properties, write-only properties, read modifier, write modifier]
tags:
  - roblox-dev
  - luau/types
type: concept
last_updated: 2026-10-27
status: complete
---
# Read/Write Property Modifiers

> **TL;DR:** Table type properties and indexers can be marked **`read`** (read-only through this type) or **`write`** (write-only). It's a type-level guarantee, great for public module APIs and config. For runtime immutability, combine with `table.freeze` ([[Table_Library]]) and [[Const_Bindings]].

## Syntax (implemented)
```luau
--!strict
type PlayerView = { read UserId: number, read Name: string, Score: number }
type ReadOnlyMap<K, V> = { read [K]: V }
type ReadArray<T> = { read T }

-- Different read/write types (legal, but rarely a good idea)
type Slot = { read item: Item, write item: Weapon }
```
- `read` and `write` are **contextual** keywords, so they still work as property names: `{ read: () -> number }`.
- Each property can have at most one read type and one write type. `{ x: string, read x: "a" }` is an error.

## Why it matters
- **API safety:** expose `read` fields so consumers can't accidentally mutate internal state (`stats.MaxHp = 9e9`).
- **Variance:** read-only properties are *covariant*. A `{ read pet: Dog }` can be passed where `{ read pet: Animal }` is expected, which isn't sound for mutable properties.
- Pairs naturally with frozen config tables:
```luau
const WEAPONS = table.freeze({
	Katana = table.freeze({ damage = 18, range = 7 }),
}) :: { read [string]: { read damage: number, read range: number } }
```

## Related
[[Table_Types]] · [[Luau_Type_System]] · [[New_Type_Solver]] · [[Const_Bindings]] · [[Table_Library]] · [[Generics]] · [[User_Defined_Type_Functions]] · [[OOP_Class_Patterns]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://rfcs.luau.org/syntax-property-access-modifiers.html
- https://rfcs.luau.org/property-readonly.html · https://rfcs.luau.org/property-writeonly.html
