---
aliases: [RBXScriptSignal, RBXScriptConnection, Connect, Once, Wait, Changed, GetPropertyChangedSignal]
tags:
  - roblox-dev
  - engine/events
type: api
last_updated: 2026-10-27
status: complete
---
# Signals & Connections

> **TL;DR:** Engine events are `RBXScriptSignal`s: `:Connect(fn)` returns an `RBXScriptConnection` you must eventually `:Disconnect()`, `:Once(fn)` auto-disconnects after one fire, and `:Wait()` yields until the next fire. Prefer specific signals (`GetPropertyChangedSignal("Health")`, `GetAttributeChangedSignal`) over broad ones (`Changed`, `DescendantAdded` on big trees).

## API
```luau
local conn = humanoid.HealthChanged:Connect(function(hp) updateBar(hp) end)
conn:Disconnect()                                  -- stop listening; conn.Connected == false

humanoid.Died:Once(function() showDeathScreen() end)   -- one-shot
local char = player.CharacterAdded:Wait()             -- yield for next fire

part:GetPropertyChangedSignal("Transparency"):Connect(onFade)
model:GetAttributeChangedSignal("State"):Connect(onState)
```
- `Changed` on Instances fires for **every** property change (and, on `ValueBase` objects, with the new value). It's often noisy.
- Connections on an Instance are **auto-disconnected when it's `:Destroy()`ed**, but not when it's just unparented ([[Instance_Lifecycle_and_Destroy]]).
- Connections on **services or long-lived objects** (`Players.PlayerAdded`, `RunService.Heartbeat`) live forever unless you disconnect them. That's the biggest leak source ([[Memory_Leaks]]).

## Custom signals
Pure-Luau signal objects (`GoodSignal`-style) avoid Bindable overhead and keep Lua values intact (tables keep identity and metatables) ([[Signal_Libraries]]). Typed generic signals are shown in [[Generics]].

## Deferred behavior
Under `SignalBehavior = Deferred`, handlers run at the next resumption point, not immediately ([[Deferred_Events_and_SignalBehavior]]).

## Cleanup pattern
```luau
local trove = Trove.new()
trove:Connect(RunService.Heartbeat, step)
trove:Connect(humanoid.Died, onDied)
-- later (character removed / UI closed)
trove:Destroy()                     -- disconnects all
```
See [[Cleanup_Libraries_Trove_Maid_Janitor]] and [[Connection_Management]].

## Related
[[Connection_Management]] · [[Memory_Leaks]] · [[Deferred_Events_and_SignalBehavior]] · [[Bindable_Events_and_Functions]] · [[Signal_Libraries]] · [[Cleanup_Libraries_Trove_Maid_Janitor]] · [[Attributes]] · [[Instance_Lifecycle_and_Destroy]] · [[Generics]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/reference/engine/datatypes/RBXScriptSignal
- https://create.roblox.com/docs/scripting/events
