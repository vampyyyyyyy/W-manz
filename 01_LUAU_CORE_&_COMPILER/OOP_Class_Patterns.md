---
aliases: [OOP, Classes in Luau, Class pattern, Inheritance, Composition]
tags:
  - roblox-dev
  - luau/oop
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# OOP Class Patterns

> **TL;DR:** Luau classes are tables plus a metatable whose `__index` is the class table. Store per-instance data **in the object**, methods **on the class**, and type it with the `typeof(setmetatable(...))` pattern. Prefer **composition** over deep inheritance: it's faster (inline caching) and easier to reason about in game systems. A native `class` syntax is only a proposal so far ([[Luau_Classes_Proposal]]).

## The canonical typed class (strict mode)
```luau
--!strict
local Hitbox = {}
Hitbox.__index = Hitbox

type HitboxData = {
	size: Vector3,
	offset: CFrame,
	hitList: { [Model]: boolean },
	active: boolean,
}
export type Hitbox = typeof(setmetatable({} :: HitboxData, Hitbox))

function Hitbox.new(size: Vector3, offset: CFrame?): Hitbox
	local self: HitboxData = {
		size = size,
		offset = offset or CFrame.identity,
		hitList = {},
		active = false,
	}
	return setmetatable(self, Hitbox)
end

function Hitbox.Start(self: Hitbox)
	self.active = true
	table.clear(self.hitList)
end

function Hitbox.Query(self: Hitbox, origin: CFrame, params: OverlapParams): { BasePart }
	if not self.active then return {} end
	return workspace:GetPartBoundsInBox(origin * self.offset, self.size, params)
end

function Hitbox.Destroy(self: Hitbox)
	self.active = false
	table.clear(self.hitList)
end

return Hitbox
```
- Declaring methods as `function Hitbox.Start(self: Hitbox)` rather than `Hitbox:Start()` gives the analyzer an explicit `self` type, which the Luau docs recommend for strict OOP.
- All fields are created in **one literal** in the constructor, which uses table templates for fast allocation ([[Luau_Compiler_Optimizations]]).

## Inheritance (use sparingly)
```luau
local Base = {} Base.__index = Base
local Derived = setmetatable({}, { __index = Base }) Derived.__index = Derived
-- lookups: obj -> Derived -> Base. Each level is one more miss
```
Two levels is fine. Deep chains slow every method call and complicate types.

## Composition (preferred for gameplay)
A `Fighter` *has* a `Hitbox`, a `Stamina`, a `StateMachine` ([[Combat_State_Machine]]), and a `Trove` for cleanup ([[Cleanup_Libraries_Trove_Maid_Janitor]]). Many large games use [[Entity_Component_System_Pattern|ECS]] instead of classes for thousands of entities.

## Gotchas
- **Always provide `Destroy`** and disconnect connections. Leaked objects with live connections are the #1 memory leak ([[Memory_Leaks]], [[Connection_Management]]).
- Objects lose their metatable through remotes and DataStores. Send plain data and rebuild ([[RemoteEvents_and_RemoteFunctions]]).
- Avoid `__index` *functions* for method lookup, because they disable the fast path ([[Metatables]]).

## Related
[[Metatables]] · [[Metamethods]] · [[Luau_Type_System]] · [[New_Type_Solver]] · [[Luau_Classes_Proposal]] · [[Entity_Component_System_Pattern]] · [[Cleanup_Libraries_Trove_Maid_Janitor]] · [[Memory_Leaks]] · [[Hitbox_Detection_Methods]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://luau.org/types/object-oriented-programs · https://luau.org/performance#fast-method-calls
