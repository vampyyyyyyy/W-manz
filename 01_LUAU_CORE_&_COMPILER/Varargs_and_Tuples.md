---
aliases: ["...", varargs, select, table.pack, table.unpack, multiple returns, tuples]
tags:
  - roblox-dev
  - luau/functions
type: concept
last_updated: 2026-10-27
status: complete
---
# Varargs & Tuples

> **TL;DR:** Functions can take and return any number of values (`...`). Use `select("#", ...)` for the true count (nils included), `table.pack(...)` to capture args with `.n`, and `table.unpack(t, 1, t.n)` to spread them back without losing trailing nils. Tuples are how Luau returns multiple values. They're not tables.

## Essentials
```luau
local function count(...) return select("#", ...) end
print(count(1, nil, nil)) --> 3   (#{...} could say 1)

local function forward(fn, ...)
	local args = table.pack(...)          -- { n = 3, ... }
	return fn(table.unpack(args, 1, args.n))
end

local function minmax(list: { number }): (number, number)
	return math.min(table.unpack(list)), math.max(table.unpack(list))
end
local lo, hi = minmax({ 3, 9, 1 })
```

## Rules that trip people up
- **Only the last expression expands.** `f(g())` passes all of g's returns, `f(g(), 1)` passes only g's **first** return, then `1`. `{ g() }` captures all, `{ g(), x }` captures one.
- Wrapping in parentheses truncates to one value: `(g())`.
- `table.unpack` has a stack limit (thousands of values). Don't unpack huge arrays into `math.max`. Loop instead.
- `select(i, ...)` with `...` is optimized to **O(1)** by the builtin fastcall ([[Builtin_Fastcalls_and_Imports]]).

## Types
```luau
local function log(fmt: string, ...: any): ()
	print(string.format(fmt, ...))
end
type Handler<Args...> = (Args...) -> ()     -- generic type packs ([[Generics]])
local function pair(): (string, number) return "hp", 100 end
```

## Roblox notes
- `RemoteEvent:FireServer(...)` arguments arrive as a tuple after `player`. Trailing `nil`s may be dropped, so prefer one table argument with explicit fields ([[RemoteEvents_and_RemoteFunctions]]).
- `pcall(fn, ...)` returns `ok, ...results` ([[Error_Handling_pcall_xpcall]]).

## Related
[[Generics]] · [[Table_Library]] · [[Builtin_Fastcalls_and_Imports]] · [[Error_Handling_pcall_xpcall]] · [[RemoteEvents_and_RemoteFunctions]] · [[Closures_and_Upvalues]] · [[Type_Annotations_and_Casts]] · [[Luau_Overview]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://create.roblox.com/docs/luau/tuples · https://rfcs.luau.org/syntax-typed-variadics.html
