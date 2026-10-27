---
aliases: [Luau classes, class keyword, syntax-classes RFC, Native OOP Luau]
tags:
  - roblox-dev
  - community/luau-rfcs
type: concept
last_updated: 2026-10-27
status: complete
---
# Luau Classes Proposal (syntax-classes RFC)

> **TL;DR:** The accepted (merged, **not yet implemented** as of Oct 2026) `syntax-classes` RFC adds top-level **`class` blocks** with `public` fields, methods, supported metamethods, **nominal types**, a frozen **class object** (call it with a table to construct: `Point { x = 1, y = 2 }`) and **instances as a new VM value type** (`type(inst) == "object"`, no `pairs`/`setmetatable`, reading a missing field **errors**). Goals: polished OOP, accurate autocomplete (setmetatable inference is hard), and speed (direct method dispatch, fixed field offsets). **No inheritance** in this RFC.

## Shape
```luau
class Point
	public x: number
	public y: number

	function length(self) return math.sqrt(self.x * self.x + self.y * self.y) end
	function __add(self, other: Point) return Point { x = self.x + other.x, y = self.y + other.y } end
	function new(x: number, y: number) return Point { x = x, y = y } end   -- static factory
end

local p = Point.new(3, 4)
print(p:length())                    -- 5
print(class.isinstance(p, Point))    -- true (refines types too)
```
(Proposed syntax. It **does not run in Studio today**.)

## Key rules in the RFC
- Classes are declared only at the **top scope** (`export class X` allowed). The name is hoisted for types, but instantiation before the statement errors.
- `__`-prefixed names other than the listed metamethods are a **syntax error** (forward compatibility).
- `type()`/`typeof()` return `"class"` for class objects and `"object"` for instances. There's a new `class` library (`isinstance`, `classof`).
- Out of scope: inheritance (still being evaluated), and `private` (a future RFC).

## What to do today
Keep using metatable OOP or plain data + functions ([[OOP_Class_Patterns]], [[Metatables]]), annotate types explicitly, and avoid deep inheritance trees that won't map cleanly onto future classes. Prefer composition (it also suits ECS: [[Entity_Component_System_Pattern]]).

## Related
[[Luau_RFC_Tracker]] · [[Luau_RFC_Process]] · [[OOP_Class_Patterns]] · [[Metatables]] · [[Metamethods]] · [[Luau_Type_System]] · [[Type_Refinements]] · [[Entity_Component_System_Pattern]] · [[Luau_Compiler_Optimizations]] · [[MOC_Resource_Hub_and_Community]]

## Sources
- https://github.com/luau-lang/rfcs/blob/master/docs/syntax-classes.md
