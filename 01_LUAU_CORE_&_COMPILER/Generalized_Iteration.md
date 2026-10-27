---
aliases: [for in loop, __iter, pairs vs ipairs, generalized for]
tags:
  - roblox-dev
  - luau/syntax
type: concept
last_updated: 2026-10-27
status: complete
---
# Generalized Iteration

> **TL;DR:** In Luau you can write `for k, v in t do` with no `pairs`/`ipairs`. It's the recommended default: as fast as `pairs`/`ipairs` (the VM has specialized iteration bytecode), shorter, and it supports custom containers via the `__iter` metamethod.

## Semantics
```luau
for i, v in { "a", "b", "c" } do print(i, v) end     -- array part in order, then hash part
for key, value in inventory do print(key, value) end
for _, child in workspace:GetChildren() do end        -- GetChildren returns an array
```
- Iterates the **array part in order (1..n)**, then the hash part in unspecified order, like `pairs`.
- `ipairs(t)` is different: it **stops at the first `nil`**. Use it only when you need that behavior.
- Modifying a table while iterating: **assigning existing keys (including to nil) is fine. Adding new keys is undefined.** Collect changes and apply them after the loop.

## Custom iteration with `__iter`
```luau
--!strict
local Ring = {}
Ring.__index = Ring
Ring.__iter = function(self)
	local i = 0
	return function()
		i += 1
		if i > self.count then return nil end
		return i, self.items[((self.head + i - 2) % self.capacity) + 1]
	end
end
-- for i, sample in myRingBuffer do ... end  -- iterates oldest to newest
```

## Performance notes (Luau team)
- `for … in t`, `pairs` and `ipairs` are all **specialized** with no function call per step, and roughly equal in speed. Generalized iteration also skips the `pairs()` call at loop start.
- `for i = 1, #t do local v = t[i]` is *slightly* slower for array reads, but use it when you need index arithmetic.
- Iterating Roblox APIs (`GetChildren`, `GetDescendants`) allocates a fresh array each call. Cache it if you iterate every frame ([[Luau_Micro_Optimizations]]).

## Related
[[Luau_Syntax_Extensions]] · [[Metamethods]] · [[Table_Library]] · [[Luau_Compiler_Optimizations]] · [[Luau_Micro_Optimizations]] · [[Coroutines]] · [[Luau_Lua_Compatibility]] · [[Table_Types]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://rfcs.luau.org/generalized-iteration.html · https://luau.org/performance#optimized-table-iteration
