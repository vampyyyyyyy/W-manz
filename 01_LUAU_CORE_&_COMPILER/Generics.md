---
aliases: [Generic functions, Generic types, Type parameters, Type packs]
tags:
  - roblox-dev
  - luau/types
type: concept
last_updated: 2026-10-27
status: complete
---
# Generics

> **TL;DR:** Generics let one function or type work over many types while keeping them connected. A `Signal<Player, number>` only accepts `(Player, number)` listeners, and `map<T, U>` returns `{ U }`. Luau supports generic **types**, generic **functions**, **type packs** (`T...`), defaults, and explicit instantiation (`f<<T>>()`).

## Generic functions
```luau
--!strict
local function map<T, U>(list: { T }, fn: (T) -> U): { U }
	local out = table.create(#list)
	for i, v in list do out[i] = fn(v) end
	return out
end
local names = map(game:GetService("Players"):GetPlayers(), function(p) return p.Name end) -- { string }
```

## Generic types + type packs (typed signals)
```luau
--!strict
export type Signal<Args...> = {
	Connect: (self: Signal<Args...>, fn: (Args...) -> ()) -> () -> (),
	Fire: (self: Signal<Args...>, Args...) -> (),
}

local function createSignal<Args...>(): Signal<Args...>
	local listeners: { (Args...) -> () } = {}
	local self = {} :: Signal<Args...>
	function self.Connect(_, fn)
		table.insert(listeners, fn)
		return function() local i = table.find(listeners, fn) if i then table.remove(listeners, i) end end
	end
	function self.Fire(_, ...)
		for _, fn in listeners do task.spawn(fn, ...) end
	end
	return self
end

local damaged = createSignal<<Player, number>>()   -- explicit instantiation (2025)
damaged:Connect(function(player, amount) print(player.Name, amount) end)
```
See [[Signal_Libraries]] for production signal implementations.

## Defaults and constraints
- Type alias defaults: `type Result<T, E = string> = { ok: true, value: T } | { ok: false, err: E }`.
- Luau has **no** `T extends X` bounds syntax. Constrain through usage, or with [[User_Defined_Type_Functions|type functions]].

## Gotchas
- Generic **inference failures** sometimes widen to `unknown` or `any`. Annotate the call-site variable or use `f<<T>>()`.
- Recursive generic types have restrictions (relaxed over time; see [[Luau_RFC_Tracker]]).
- Generics are erased at runtime, so there's no reflection on `T`.

## Related
[[Luau_Type_System]] · [[Type_Annotations_and_Casts]] · [[Table_Types]] · [[User_Defined_Type_Functions]] · [[Signal_Libraries]] · [[Custom_Serialization]] · [[New_Type_Solver]] · [[Varargs_and_Tuples]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://luau.org/types/generics · https://rfcs.luau.org/generic-functions.html
- https://rfcs.luau.org/syntax-type-alias-type-packs.html · https://rfcs.luau.org/explicit-type-parameter-instantiation.html
