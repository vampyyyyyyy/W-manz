---
aliases: [Closures, Upvalues, Lexical scope, Captured variables]
tags:
  - roblox-dev
  - luau/functions
type: concept
last_updated: 2026-10-27
status: complete
---
# Closures & Upvalues

> **TL;DR:** A closure is a function plus the outer locals it captures (its **upvalues**). Luau optimizes the common case: **upvalues that are never reassigned are captured by value** with no extra allocation. Identical closures may even be **cached** and reused. Mutable upvalues cost an extra object. Closures are also the #1 way to accidentally keep objects alive ([[Memory_Leaks]]).

## Basics
```luau
local function makeCounter()
	local n = 0                 -- mutable upvalue (reassigned below)
	return function()
		n += 1
		return n
	end
end
local c = makeCounter()
print(c(), c()) --> 1 2
```

## Luau-specific optimizations
- **Immutable upvalue capture:** about 90% of upvalues are never reassigned. Luau captures them without allocating an upvalue box, so closures are cheaper to create and call. "Immutable" refers to the *variable*: a never-reassigned table whose contents change still counts ([[Const_Bindings]] makes this explicit).
- **Closure caching:** if a `function() … end` expression would create a semantically identical closure each time (same captured values), the compiler may return the **same function object**. Code that uses functions as table keys can observe this ([[Luau_Lua_Compatibility]]).
- **Inlining** (O2) can remove small local function calls entirely ([[Luau_Compiler_Optimizations]]).

## Patterns
- **Factory functions** for per-object behavior without metatables (simple, but each instance allocates its own closures, while metatables share methods).
- **Callbacks** for signals: the connection holds the closure, the closure holds the upvalues, and the upvalues hold your objects. That's why every connection needs a cleanup path ([[Connection_Management]]).

## Gotchas
- Creating closures **inside hot loops** (`for … do table.sort(t, function(a, b) … end) end`) allocates per iteration unless caching applies. Hoist the comparator out ([[Luau_Micro_Optimizations]]).
- Loop variables are fresh per iteration in `for` loops, so capturing `i` inside the loop body captures that iteration's value (unlike JavaScript `var`).
- Recursive local functions: use `local function f()` (not `local f = function()`) so `f` is in scope inside itself.

## Related
[[Coroutines]] · [[Garbage_Collection]] · [[Memory_Leaks]] · [[Connection_Management]] · [[Luau_Compiler_Optimizations]] · [[Const_Bindings]] · [[OOP_Class_Patterns]] · [[Luau_Micro_Optimizations]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://luau.org/performance#optimized-upvalue-storage · https://luau.org/performance#closure-caching
