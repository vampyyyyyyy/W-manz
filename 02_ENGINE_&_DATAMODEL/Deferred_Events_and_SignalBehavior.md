---
aliases: [Deferred events, SignalBehavior, Immediate events, Resumption points]
tags:
  - roblox-dev
  - engine/scheduler
type: concept
last_updated: 2026-10-27
status: complete
---
# Deferred Events (`Workspace.SignalBehavior`)

> **TL;DR:** With `SignalBehavior = Deferred` (recommended, the default for template places, and **required** for [[Server_Authority_Model|server authority]]), event handlers don't run *inside* the action that triggered them. They're queued and run at the next **resumption point**. That's faster and avoids re-entrancy bugs, but code that expected an instant callback breaks. `Default` currently equals `Immediate` and will eventually switch to `Deferred`.

## What changes
- Changing 1,000 properties no longer runs 1,000 handler snippets interleaved with engine work.
- No more "Removing fired before Added" weirdness.
- Re-entrancy depth limit is **10** (events triggering events).

## Patterns that break under Deferred
```luau
-- 1) Expecting the handler to have run already
local fired = false
event:Connect(function() fired = true end)
triggerEvent()
print(fired)            --> false under Deferred (handler runs at the next resumption point)

-- 2) "First occurrence" with manual disconnect: several invocations may already be queued
local c; c = event:Connect(function() c:Disconnect() doOnce() end)  -- may still run more than once
event:Once(doOnce)                                                    -- ✅ use Once

-- 3) Reading state "during" an ancestry/property change: handlers see the state AFTER the change
part.Destroying:Connect(function() print(#part:GetChildren()) end)    -- runs after the destroy happened
```
`:Disconnect()` drops pending invocations. `:Destroy()` disconnects immediately but **still runs** handlers that were already pending.

## Resumption points (in frame order)
Input processing → `PreRender` → legacy `wait`/`spawn`/`delay` → `PreAnimation` → `PreSimulation` → `PostSimulation` → `task.*` resumptions → `Heartbeat` → `BindToClose` ([[Task_Scheduler]]).

## Migration checklist
1. Set `Workspace.SignalBehavior = Deferred` in a test place.
2. Search for connect-then-read patterns and replace them with `Once`, explicit callbacks or `:Wait()`.
3. Check remote handlers that rely on instance state set "just before" firing. Remotes and property replication aren't ordered relative to each other anyway ([[RemoteEvents_and_RemoteFunctions]]).
4. Run the full game flow in [[Studio_Testing_Modes]].

## Related
[[Task_Scheduler]] · [[Signals_and_Connections]] · [[Instance_Lifecycle_and_Destroy]] · [[Server_Authority_Model]] · [[RunService_Frame_Events]] · [[RemoteEvents_and_RemoteFunctions]] · [[Bindable_Events_and_Functions]] · [[task_Library]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/scripting/events/deferred
