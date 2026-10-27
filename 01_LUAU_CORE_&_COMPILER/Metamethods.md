---
aliases: [__index, __newindex, __call, __iter, __eq, __tostring, __len, __mode]
tags:
  - roblox-dev
  - luau/metatables
type: api
last_updated: 2026-10-27
status: complete
---
# Metamethods

> **TL;DR:** Metamethods are the keys a [[Metatables|metatable]] can define to customize behavior. Luau supports the Lua 5.1 set plus `__iter` (custom iteration), `__len` on tables, `__idiv` (`//`) and `__mode` with `s` (shrinkable weak tables). It does **not** support `__gc`, `__close`, `__pairs` or `__ipairs`.

## Reference
| Key | Triggered by | Notes |
| --- | --- | --- |
| `__index` | reading a missing key | Table (fast, cached) or `function(t, k)` |
| `__newindex` | writing a **missing** key | Existing keys are written directly. Use a proxy table to intercept all writes |
| `__call` | `obj(...)` | Callable objects, constructors |
| `__iter` | `for k, v in obj do` | Return iterator function(s) ([[Generalized_Iteration]]) |
| `__len` | `#obj` | Honored on tables (5.2 behavior) |
| `__eq` | `==`, `~=` | Luau calls it **even when objects are rawequal**. Not called for different types |
| `__lt`, `__le` | `<`, `<=`, `>`, `>=` | Like Lua 5.1, a missing `__le` falls back to `not (b < a)` via `__lt` (Luau did **not** adopt 5.4's removal). Define both for clarity |
| `__add` `__sub` `__mul` `__div` `__idiv` `__mod` `__pow` `__unm` | arithmetic | `__idiv` = floor division `//` |
| `__concat` | `..` | |
| `__tostring` | `tostring(obj)`, `print(obj)` | |
| `__mode` | GC | `"k"`, `"v"`, `"kv"`, plus `"s"` for shrinkable ([[Weak_Tables]]) |
| `__metatable` | `getmetatable`/`setmetatable` | Locks the metatable |
| `__namecall` | `obj:Method()` on userdata | Engine-side fast path for Roblox objects ("namecall"). Exploit tools hook the client's copy to spy on remote calls, so client code can't be trusted ([[Exploit_Threat_Model]]) |

## Example: a value type with operators
```luau
--!strict
local Money = {}
Money.__index = Money
type Money = typeof(setmetatable({} :: { cents: number }, Money))

function Money.new(cents: number): Money
	return setmetatable({ cents = math.floor(cents) }, Money)
end
Money.__add = function(a: Money, b: Money) return Money.new(a.cents + b.cents) end
Money.__eq = function(a: Money, b: Money) return a.cents == b.cents end
Money.__lt = function(a: Money, b: Money) return a.cents < b.cents end
Money.__le = function(a: Money, b: Money) return a.cents <= b.cents end
Money.__tostring = function(m: Money) return string.format("$%d.%02d", m.cents // 100, m.cents % 100) end

print(Money.new(150) + Money.new(275)) --> $4.25
```

## Gotchas
- **Metamethods can't yield** in Luau, so no `task.wait` inside `__index` ([[Luau_Lua_Compatibility]]).
- Operator metamethods make `a + b` unpredictable for the compiler and native codegen. Hot numeric code should stay on plain numbers or vectors ([[Native_Code_Generation]]).
- `__index` functions run on **every miss**. Cache results with `rawset` if they're expensive.

## Related
[[Metatables]] · [[OOP_Class_Patterns]] · [[Generalized_Iteration]] · [[Weak_Tables]] · [[Luau_Lua_Compatibility]] · [[Luau_Syntax_Extensions]] · [[Native_Code_Generation]] · [[String_Library_and_Patterns]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://create.roblox.com/docs/luau/metatables · https://luau.org/compatibility
- https://rfcs.luau.org/generalized-iteration.html · https://rfcs.luau.org/len-metamethod-rawlen.html
