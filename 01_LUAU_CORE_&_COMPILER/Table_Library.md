---
aliases: [table library, table.create, table.find, table.freeze, table.clone, table.clear, table.move]
tags:
  - roblox-dev
  - luau/libraries
type: api
last_updated: 2026-10-27
status: complete
---
# Table Library

> **TL;DR:** Luau's `table` library adds **`create`, `find`, `clear`, `clone`, `freeze`/`isfrozen`** and a fast `move` to Lua's set. `table.insert`/`remove`/`move` are tuned for arrays (3x+ faster than stock Lua), and `sort` uses introsort (guaranteed O(n log n)).

## Luau additions
| Function | Use |
| --- | --- |
| `table.create(n, value?)` | Preallocate the array part (optionally filled). Fastest way to build known-size arrays |
| `table.find(t, value, init?)` | Linear search in the array part. Returns index or nil |
| `table.clear(t)` | Removes all keys **but keeps capacity**. Ideal for reusable scratch tables ([[Object_Pooling]]) |
| `table.clone(t)` | **Shallow**, unfrozen copy (keeps the metatable) |
| `table.freeze(t)` / `table.isfrozen(t)` | Shallow read-only. Writes error. Freeze nested tables yourself for deep immutability |
| `table.move(src, a, b, t, dst?)` | Bulk copy; ranges may overlap |
| `table.pack(...)` / `table.unpack(t, i?, j?)` | Varargs ↔ table with `.n` ([[Varargs_and_Tuples]]) |

## Performance tips (Luau team)
```luau
-- fastest array build when size is known
local squares = table.create(N)
for i = 1, N do squares[i] = i * i end

-- object-like tables: give all fields in one literal (table templates)
local hit = { target = model, damage = 25, time = os.clock() }

-- appending without known index: table.insert(t, v) is the fastest generic append
```
- `#t` is almost always O(1) in Luau (cached length, guaranteed array part).
- `table.remove(t, 1)` is O(n), because it shifts everything. For queues use head/tail indices or a ring buffer ([[Lag_Compensation]]).
- Swap-remove for unordered arrays: `t[i] = t[#t]; t[#t] = nil` is O(1).

## Gotchas
- `table.sort` errors with `invalid order function for sorting` if the comparator is inconsistent (e.g. uses `<=`). Always use a strict `<`.
- `table.freeze` is **shallow**, and the table must not already have a protected metatable.
- `table.getn`, `foreach` and `foreachi` are deprecated. Use `#` and generalized iteration ([[Generalized_Iteration]]).

## Related
[[Table_Types]] · [[Generalized_Iteration]] · [[Varargs_and_Tuples]] · [[Const_Bindings]] · [[Read_Write_Property_Modifiers]] · [[Object_Pooling]] · [[Luau_Micro_Optimizations]] · [[Luau_Compiler_Optimizations]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://create.roblox.com/docs/reference/engine/libraries/table · https://luau.org/performance#creating-and-modifying-tables
- https://rfcs.luau.org/function-table-freeze.html · https://rfcs.luau.org/function-table-clone.html
