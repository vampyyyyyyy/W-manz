---
aliases: [Table types, Sealed tables, Unsealed tables, Array types, Dictionary types]
tags:
  - roblox-dev
  - luau/types
type: concept
last_updated: 2026-10-27
status: complete
---
# Table Types

> **TL;DR:** Luau table types are **structural**: `{ x: number }` matches any table with a numeric `x`. Arrays are `{ T }`, maps `{ [K]: V }`, records list their fields. Tables built from literals are **unsealed** while you're building them in the same scope (you can add fields). Annotated or returned tables are **sealed** (adding unknown fields is an error).

## Shapes
```luau
--!strict
type Vec = { x: number, y: number }                 -- record
type Inventory = { [string]: number }               -- map: itemId -> count
type Hand = { string }                              -- array of string
type Weapon = { name: string, mods: { string }, stats: { [string]: number }? }

local w: Weapon = { name = "Katana", mods = {} }    -- stats omitted: OK (optional)
-- w.durability = 10                               -- error: sealed table, unknown field
```

## Sealed vs unsealed
```luau
local t = {}       -- unsealed: the analyzer tracks fields as you add them
t.hp = 100
t.name = "Boss"    -- t: { hp: number, name: string }
local function make(): { hp: number } return { hp = 1 } end
local u = make()
-- u.extra = true  -- error: u is sealed
```
Width subtyping: a sealed `{ hp: number, name: string }` can be passed where `{ hp: number }` is expected.

## Mixed tables
Luau types don't model "array + dictionary" tables well, and Roblox remotes mangle them anyway ([[RemoteEvents_and_RemoteFunctions]]). Keep arrays and records separate: `{ items: { Item }, meta: Meta }`.

## Performance link
The VM uses **inline caching** for field access by constant name, so consistent shapes are fast. Constructing records with all fields in **one literal** uses table templates ([[Luau_Compiler_Optimizations]], [[Luau_Micro_Optimizations]]).

## Related
[[Luau_Type_System]] · [[Read_Write_Property_Modifiers]] · [[Generics]] · [[Type_Refinements]] · [[Table_Library]] · [[Metatables]] · [[OOP_Class_Patterns]] · [[Luau_Compiler_Optimizations]] · [[RemoteEvents_and_RemoteFunctions]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://luau.org/types/tables · https://rfcs.luau.org/sealed-table-subtyping.html · https://rfcs.luau.org/unsealed-table-literals.html
