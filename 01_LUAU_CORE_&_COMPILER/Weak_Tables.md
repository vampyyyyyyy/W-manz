---
aliases: [__mode, Weak keys, Weak values, Ephemeral cache]
tags:
  - roblox-dev
  - luau/memory
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Weak Tables

> **TL;DR:** A table with metatable `__mode = "k"` (weak keys), `"v"` (weak values) or `"kv"` doesn't keep its entries alive. The GC can remove them once nothing else references them. Luau adds `"s"` (**shrinkable**: the table resizes after entries are collected). Great for caches keyed by objects. **Not** a substitute for explicit cleanup of Instances.

## Patterns
```luau
--!strict
-- Per-object metadata without leaking the object
local meta = setmetatable({} :: { [any]: { lastHit: number } }, { __mode = "ks" })

-- Memoize expensive results by key object; entries vanish when the key dies
local function getBounds(model: Model)
	local cached = meta[model]
	if cached then return cached end
	local entry = { lastHit = 0 }
	meta[model] = entry
	return entry
end
```

## Roblox caveats (important)
- **Instances are kept alive by the engine while parented in the DataModel**, and Lua references to Instances are userdata wrappers. A weak-keyed table entry for an Instance may **not** disappear when you expect, or may persist while the engine still holds it. For Instance lifetimes, use **explicit removal** on `Destroying`/`PlayerRemoving` instead ([[Instance_Lifecycle_and_Destroy]], [[Memory_Leaks]]).
- Strings, numbers and booleans are values, not collectable references. Weak *values* that are strings never get collected from the table.
- No ephemerons: in a weak-key table, a value that references its own key keeps the entry alive ([[Luau_Lua_Compatibility]]).
- Collection timing is non-deterministic, so never rely on entries disappearing "soon".

## When to use what
| Need | Use |
| --- | --- |
| Cache keyed by plain Lua tables/objects | Weak keys (`"ks"`) |
| Lookup of interned objects by id | Weak values (`"v"`) |
| Per-player or per-Instance state | Normal table + explicit cleanup |
| Bounded memory cache | LRU with a size cap |

## Related
[[Garbage_Collection]] · [[Metatables]] · [[Metamethods]] · [[Memory_Leaks]] · [[Instance_Lifecycle_and_Destroy]] · [[Luau_Lua_Compatibility]] · [[Connection_Management]] · [[Luau_Heap_Analysis]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://luau.org/performance#reduced-garbage-collector-pauses (shrinkable weak tables)
- https://create.roblox.com/docs/luau/metatables
