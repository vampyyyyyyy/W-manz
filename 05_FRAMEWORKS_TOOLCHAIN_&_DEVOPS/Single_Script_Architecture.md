---
aliases: [Single script architecture, SSA, Module loader, Bootstrap script, Init/Start pattern]
tags:
  - roblox-dev
  - framework/architecture
type: architecture
last_updated: 2026-10-27
status: complete
---
# Single-Script Architecture (Module Loader)

> **TL;DR:** One server bootstrap `Script` and one client bootstrap `LocalScript` each **require every feature module**, call `init()` on all of them (wire dependencies, no yielding), then `start()` (begin behavior). Everything else is a ModuleScript. You get deterministic load order, no scattered scripts in models, easy testing, and clear ownership. This is the framework-free successor to [[Knit]]-style setups.

## Layout (Rojo / Script Sync friendly)
```text
src/
  server/            → ServerScriptService.Server
    init.server.luau        (bootstrap)
    Combat/init.luau        (feature module)
    Data/init.luau
  client/            → StarterPlayerScripts.Client
    init.client.luau        (bootstrap)
    CameraController.luau
    HUD/init.luau
  shared/            → ReplicatedStorage.Shared
    Attacks.luau  Net.luau  Validate.luau
```

## Bootstrap
```luau
--!strict
-- src/server/init.server.luau
type Feature = { name: string, init: ((any) -> ())?, start: (() -> ())?, order: number? }

local features: { Feature } = {}
for _, child in script:GetChildren() do
	if child:IsA("ModuleScript") then
		local mod = require(child) :: any
		mod.name = child.Name
		table.insert(features, mod)
	end
end
table.sort(features, function(a, b) return (a.order or 100) < (b.order or 100) end)

local registry = {}
for _, f in features do registry[f.name] = f end
for _, f in features do if f.init then f.init(registry) end end        -- wire deps, no yields
for _, f in features do if f.start then task.spawn(f.start) end end    -- start behavior
```

## Rules
- `init` must not yield. `start` may (it's spawned).
- Features talk through **explicit APIs or signals**, not `_G` ([[Globals_G_shared_and_getfenv]], [[Signal_Libraries]]).
- Each feature owns its cleanup ([[Memory_Leaks]]).
- World objects get behavior through tag binders, not scripts inside models ([[CollectionService_Tags]]).

## Related
[[Knit]] · [[Require_and_Module_Resolution]] · [[Script_Types_and_RunContext]] · [[Rojo]] · [[Script_Sync]] · [[Remote_Architecture_Patterns]] · [[CollectionService_Tags]] · [[Signal_Libraries]] · [[Entity_Component_System_Pattern]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- Community-standard pattern; script locations per https://create.roblox.com/docs/scripting/locations
