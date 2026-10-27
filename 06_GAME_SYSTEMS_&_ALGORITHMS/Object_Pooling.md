---
aliases: [Object pool, Instance pooling, Part pooling, VFX pooling, Reuse instances]
tags:
  - roblox-dev
  - systems/performance
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Object Pooling

> **TL;DR:** Creating and destroying instances every shot or hit costs CPU, memory churn and (on the server) replication. **Pool** them: keep released objects parented to a hidden container (or `nil`), reset their state, and reuse them. Pool **client-side cosmetic** objects (bullets, sparks, damage numbers, decals) aggressively. Server-side pooling helps for NPCs and projectiles.

## Pool module
```luau
--!strict
local Pool = {}
local free: { [Instance]: { Instance } } = {}         -- template → available clones
local origin: { [Instance]: Instance } = {}           -- clone → template
local HIDDEN = CFrame.new(0, -10000, 0)

function Pool.get(template: Instance): Instance
	local list = free[template]
	local inst = list and table.remove(list)
	if not inst then
		inst = template:Clone()
		origin[inst] = template
	end
	return inst
end

function Pool.release(inst: Instance)
	local template = origin[inst]
	if not template then inst:Destroy() return end
	-- reset state: stop emitters, hide, park
	for _, d in inst:GetDescendants() do
		if d:IsA("ParticleEmitter") then d.Enabled = false d:Clear()
		elseif d:IsA("Trail") or d:IsA("Beam") then d.Enabled = false end
	end
	if inst:IsA("BasePart") then inst.CFrame = HIDDEN
	elseif inst:IsA("Attachment") then inst.WorldCFrame = HIDDEN end
	local list = free[template]
	if not list then list = {}; free[template] = list end
	table.insert(list, inst)
end

function Pool.prewarm(template: Instance, n: number, parent: Instance)
	for _ = 1, n do
		local i = template:Clone()
		origin[i] = template
		i.Parent = parent
		Pool.release(i)
	end
end
return Pool
```

## Notes
- **Parking vs unparenting:** moving parked parts far away keeps them parented (no re-parent cost on reuse), while `Parent = nil` saves rendering and physics but costs reparenting. Choose per object type. **Never `Destroy()`** pooled objects, because Destroy locks Parent ([[Instance_Lifecycle_and_Destroy]]).
- Reset **everything** a user can see (transparency, size, color, attributes) or you'll get ghosts from the previous use.
- Cap pool sizes, and log when a pool grows past its expected maximum (that usually means a leak) ([[Memory_Leaks]]).
- For hundreds of moving pooled parts, update them with `workspace:BulkMoveTo` ([[Steering_and_Flocking]]).
- `table.clear` on reusable tables is the Lua-side equivalent of pooling ([[Table_Library]]).

## Related
[[Client_Side_VFX_Replication]] · [[Particle_Emitters]] · [[Projectile_Systems]] · [[Damage_Numbers_and_Hit_Markers]] · [[Instance_Lifecycle_and_Destroy]] · [[Memory_Leaks]] · [[Garbage_Collection]] · [[Table_Library]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://create.roblox.com/docs/performance-optimization/improve (pool NPCs and reuse instances)
