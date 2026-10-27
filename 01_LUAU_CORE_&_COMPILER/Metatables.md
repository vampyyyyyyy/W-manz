---
aliases: [setmetatable, getmetatable, metatable, __metatable]
tags:
  - roblox-dev
  - luau/metatables
type: concept
last_updated: 2026-10-27
status: complete
---
# Metatables

> **TL;DR:** A metatable is a table attached to another table (with `setmetatable`) that defines what happens on missing keys, operators, calls, iteration and so on, through [[Metamethods]]. It's the mechanism behind OOP classes ([[OOP_Class_Patterns]]), proxies, read-only views and default values. Keep `__index` pointing **directly at a table** for speed.

## Core API
```luau
local mt = { __index = { hp = 100 } }
local obj = setmetatable({}, mt)    -- returns obj
print(obj.hp)                       --> 100 (falls back to mt.__index)
print(getmetatable(obj) == mt)      --> true
print(rawget(obj, "hp"))            --> nil (bypasses metamethods)
```
- `setmetatable(t, mt)` works on **tables only** from Luau. Strings share a library metatable. Userdata metatables are engine-controlled.
- `__metatable = "locked"` makes `getmetatable` return that value and `setmetatable` error. It's useful for sealed library objects.
- `rawget`, `rawset`, `rawequal` and `rawlen` bypass metamethods (also faster when you know there's no metatable).

## Performance (from the Luau team)
- Method calls via `obj:Method()` are specialized. The VM inline-caches lookups **when `__index` is a table**. `__index` *functions* and deep inheritance chains defeat the cache ([[Luau_Compiler_Optimizations]]).
- Ideal object = table with fields stored **directly in itself** + metatable whose `__index` points to the class table.
- Access "static" fields through the class (`Class.MAX`), not through instances.

## Common uses
| Use | Sketch |
| --- | --- |
| Classes | `Class.__index = Class; setmetatable(obj, Class)` |
| Defaults | `setmetatable(settings, { __index = DEFAULTS })` |
| Read-only proxy | `__index = real, __newindex = function() error("read-only") end` (or just `table.freeze`) |
| Lazy loading | `__index = function(t, k) local v = load(k) rawset(t, k, v) return v end` |
| Weak caches | `setmetatable({}, { __mode = "k" })` ([[Weak_Tables]]) |

## Gotchas
- Metatables are **stripped when sent through remotes** and when saved to DataStores ([[RemoteEvents_and_RemoteFunctions]]). Serialize data, then reconstruct objects.
- Typing `setmetatable` patterns is the trickiest part of the type system. Use the documented OOP typing patterns ([[OOP_Class_Patterns]], [[New_Type_Solver]]).
- No `__gc`: there are no finalizers in Luau ([[Garbage_Collection]]).

## Related
[[Metamethods]] · [[OOP_Class_Patterns]] · [[Weak_Tables]] · [[Table_Types]] · [[Table_Library]] · [[Luau_Compiler_Optimizations]] · [[Garbage_Collection]] · [[Generalized_Iteration]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://create.roblox.com/docs/luau/metatables · https://luau.org/performance#fast-method-calls
