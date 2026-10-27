---
aliases: [CollectionService, Tags, AddTag, GetTagged, GetInstanceAddedSignal]
tags:
  - roblox-dev
  - engine/datamodel
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# CollectionService & Tags

> **TL;DR:** Tags label Instances with strings (`"Lava"`, `"Interactable"`, `"Destructible"`). One system script then handles **every** tagged instance, including ones added later or streamed in, using `GetTagged` + `GetInstanceAddedSignal` + `GetInstanceRemovedSignal`. It replaces copy-pasted scripts inside every model, and pairs naturally with [[Attributes]] for per-instance config.

## The binder pattern (streaming-safe)
```luau
--!strict
local CollectionService = game:GetService("CollectionService")

local function bindTag(tag: string, onAdded: (Instance) -> (() -> ())?)
	local cleanups: { [Instance]: () -> () } = {}
	local function add(inst: Instance)
		local cleanup = onAdded(inst)
		if cleanup then cleanups[inst] = cleanup end
	end
	CollectionService:GetInstanceAddedSignal(tag):Connect(add)
	CollectionService:GetInstanceRemovedSignal(tag):Connect(function(inst)
		local c = cleanups[inst]
		if c then c() cleanups[inst] = nil end
	end)
	for _, inst in CollectionService:GetTagged(tag) do task.spawn(add, inst) end
end

bindTag("Lava", function(part)
	local conn = (part :: BasePart).Touched:Connect(function(hit) --[[ damage with validation ]] end)
	return function() conn:Disconnect() end
end)
```
With [[StreamingEnabled]], instances stream in and out on clients. The added and removed signals fire accordingly, which makes this the **correct** way to attach client behavior to world objects.

## API
`inst:AddTag(tag)`, `inst:RemoveTag(tag)`, `inst:HasTag(tag)`, `inst:GetTags()`, and on `CollectionService`: `GetTagged`, `GetAllTags`, `GetInstanceAddedSignal`, `GetInstanceRemovedSignal`. Tags set in Studio (Tag Editor in the Properties window) save with the place, and server-added tags replicate.

## Design tips
- Tags = **what it is / which systems apply**. Attributes = **parameters** (damage per second, respawn time).
- Keep the tag name list in a shared constants module to avoid typos ([[Const_Bindings]]).
- ECS-style designs often map tags to components ([[Entity_Component_System_Pattern]]).

## Related
[[Attributes]] · [[StreamingEnabled]] · [[Entity_Component_System_Pattern]] · [[Signals_and_Connections]] · [[Connection_Management]] · [[Client_Triggered_Instance_Security]] · [[Single_Script_Architecture]] · [[DataModel_and_Instance_Hierarchy]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/CollectionService
