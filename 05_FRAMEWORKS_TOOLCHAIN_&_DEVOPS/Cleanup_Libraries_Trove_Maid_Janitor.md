---
aliases: [Trove, Maid, Janitor, Cleanup library, Lifetime management]
tags:
  - roblox-dev
  - framework/lifecycle
type: framework
last_updated: 2026-10-27
status: complete
---
# Cleanup Libraries (Trove, Maid, Janitor)

> **TL;DR:** A cleanup object collects everything a lifetime creates (connections, instances, threads, callbacks) and destroys it all at once. That's the antidote to leaks ([[Memory_Leaks]]). **Trove** (Sleitnick, in RbxUtil, active) is the modern default. **Janitor** (howmanysmall, thread-safe branch, active) is also popular. **Maid** (Quenty) is the classic origin.

## Trove
```luau
local Trove = require(ReplicatedStorage.Packages.Trove)

local function onCharacter(char: Model)
	local trove = Trove.new()
	trove:Connect(RunService.Heartbeat, function(dt) Stamina.tick(char, dt) end)
	trove:Add(Instance.new("Highlight"))                  -- destroyed with the trove
	trove:Add(task.delay(30, warn, "slow spawn"))         -- threads get cancelled
	trove:Add(function() Registry.remove(char) end)       -- arbitrary cleanup function
	trove:AttachToInstance(char)                          -- auto-clean when char is destroyed
end
```
Core methods: `Add`, `Connect`, `Clone`, `Construct`, `Extend` (child trove), `Remove`, `Clean`, `Destroy`, `AttachToInstance`.

## Janitor
`Janitor.new()`, `:Add(object, methodName?, index?)` (index lets you replace or remove by key), `:Remove(index)`, `:Cleanup()`, `:Destroy()`, `:LinkToInstance(inst)`. The thread-safe branch avoids global state.

## Patterns
- One cleanup object per **lifetime**: session, character, round, UI screen, ability cast ([[Connection_Management]]).
- Objects with a `Destroy()` method (your classes) can be added directly ([[OOP_Class_Patterns]]).
- Child troves for nested lifetimes (`trove:Extend()`): an ability inside a character life.

## Related
[[Connection_Management]] · [[Memory_Leaks]] · [[Signals_and_Connections]] · [[Instance_Lifecycle_and_Destroy]] · [[OOP_Class_Patterns]] · [[Signal_Libraries]] · [[Player_and_Character_Lifecycle]] · [[Wally]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://github.com/Sleitnick/RbxUtil (trove) · https://github.com/howmanysmall/Janitor
