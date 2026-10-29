---
aliases: [Luau classes, class keyword, syntax-classes RFC, Native OOP Luau]
tags:
  - roblox-dev
  - community/luau-rfcs
type: concept
last_updated: 2026-10-29
status: complete
---
# Luau Classes Proposal (syntax-classes RFC)

> **TL;DR:** The accepted `syntax-classes` RFC (merged Apr 27, 2026) adds top-level **`class` blocks** with `public` fields, methods, supported metamethods, **nominal types**, a frozen **class object** (call it with a table to construct: `Point { x = 1, y = 2 }`) and **instances as a new VM value type** (`type(inst) == "object"`, no `pairs`/`setmetatable`, reading a missing field **errors**). Goals: polished OOP, accurate autocomplete (setmetatable inference is hard), and speed (direct method dispatch, fixed field offsets). **No inheritance** in this RFC. **As of Oct 29, 2026, implementation is under way but not usable on Roblox.** It sits behind the debug-only flag `DebugLuauUserDefinedClasses` in `luau-lang/luau`, and that prototype already parses `open class` / `extends` inheritance and `__init` constructors, which are still being debated in open RFC PRs.

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

## Implementation status (as of Oct 29, 2026)
| Fact | Confidence |
| --- | --- |
| Engine work since **at least release 721 (May 2026)** across the parser, type checker, compiler and VM, behind `DebugLuauUserDefinedClasses` and `DebugLuauUserDefinedClassesRuntime`, with a dedicated test suite (`TypeInfer.classes.test.cpp`, `ClassRuntimeErrors.test.cpp`) | Confirmed (source) |
| `Debug*` flags are internal test switches, so there's **no Studio beta and no live support** | Confirmed: no beta announcement found. A DevForum thread confirms it "does not seem to work in studio" |
| The prototype supports **inheritance**: `open class Animal … end`, `class Dog extends Animal`, with methods inherited. Only classes marked `open` can be extended | Confirmed (type-checker tests) |
| Constructors as `function __init(self, …)`, called as `Dog()`. `__init`'s first parameter must be named `self` | Confirmed (tests). This differs from the merged RFC's `Point { x = … }` table-call construction |
| Inheritance, `private` fields, hoisting and constructors are being redesigned in open RFC PRs: "Classes mega-RFC" (#242), private fields (#247), hoisting (#259), inheritance alternatives (#267, Oct 27, 2026) | Confirmed these PRs exist. **Outcomes undecided** |

**Takeaway:** the syntax below is likely to change before release, especially construction and inheritance. Don't write code shaped around it yet. Treat the shape as a direction, not an API.

## Key rules in the RFC
- Classes are declared only at the **top scope** (`export class X` allowed). The name is hoisted for types, but instantiation before the statement errors.
- `__`-prefixed names other than the listed metamethods are a **syntax error** (forward compatibility).
- `type()`/`typeof()` return `"class"` for class objects and `"object"` for instances. There's a new `class` library (`isinstance`, `classof`).
- Out of scope: inheritance and `private`. Both are now in active proposal work (see the status table above).

## What to do today
Keep using metatable OOP or plain data + functions ([[OOP_Class_Patterns]], [[Metatables]]), annotate types explicitly, and avoid deep inheritance trees that won't map cleanly onto future classes. Prefer composition (it also suits ECS: [[Entity_Component_System_Pattern]]).

## Related
[[Luau_RFC_Tracker]] · [[Luau_RFC_Process]] · [[OOP_Class_Patterns]] · [[Metatables]] · [[Metamethods]] · [[Luau_Type_System]] · [[Type_Refinements]] · [[Entity_Component_System_Pattern]] · [[Luau_Compiler_Optimizations]] · [[MOC_Resource_Hub_and_Community]]

## Sources
- https://github.com/luau-lang/rfcs/blob/master/docs/syntax-classes.md
- https://github.com/luau-lang/luau (`Ast/src/Parser.cpp`, `tests/TypeInfer.classes.test.cpp`; read at release 744, Oct 2026)
- Open RFC PRs: https://github.com/luau-lang/rfcs/pull/242 · https://github.com/luau-lang/rfcs/pull/247 · https://github.com/luau-lang/rfcs/pull/259 · https://github.com/luau-lang/rfcs/pull/267
- https://devforum.roblox.com/t/classes-added-to-luau/4636979 (community thread: not available in Studio)
