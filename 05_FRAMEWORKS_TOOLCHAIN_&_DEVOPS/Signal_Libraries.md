---
aliases: [Signal, GoodSignal, LemonSignal, Custom signals, Event library]
tags:
  - roblox-dev
  - framework/events
type: framework
last_updated: 2026-10-27
status: complete
---
# Signal Libraries

> **TL;DR:** Pure-Luau signals (`Signal.new()`, `:Connect`, `:Once`, `:Fire`, `:Wait`, `:DisconnectAll`) replace BindableEvents for in-code events. They're faster, keep **table identity and metatables** (no argument copying), and can be fully typed. Popular options: **LemonSignal** (performance-focused, active), **Sleitnick's Signal** (in RbxUtil), and the classic **GoodSignal** (stravant) design that most others build on.

## Options (Oct 2026)
| Library | Notes |
| --- | --- |
| **LemonSignal** (Data-Oriented-House) | "Faster than most implementations". Docs site. Active (2026) |
| **Signal** (Sleitnick, RbxUtil) | Part of RbxUtil (trove, comm, component, timer…). Active (2026) |
| **GoodSignal** (stravant) | DevForum classic. Thread reuse for fast firing. Many forks |

## Typical API
```luau
local Signal = require(ReplicatedStorage.Packages.Signal)
local Damaged = Signal.new()                      -- typed wrappers: see Generics note
local conn = Damaged:Connect(function(target, amount) print(target, amount) end)
Damaged:Fire(model, 25)
Damaged:Once(function() print("first damage") end)
conn:Disconnect()
Damaged:DisconnectAll()
```

## Semantics to check before adopting
- **Handler thread model:** are handlers run in a new or reused thread (safe to yield) or inline (fast, but a yield blocks `Fire`)?
- **Error isolation:** does one erroring handler stop the others?
- **Deferred vs immediate:** custom signals fire immediately regardless of `SignalBehavior` ([[Deferred_Events_and_SignalBehavior]]).
- **Typing:** a generic `Signal<T...>` type gives typed `Fire` and `Connect` ([[Generics]]).

## Related
[[Signals_and_Connections]] · [[Bindable_Events_and_Functions]] · [[Generics]] · [[Cleanup_Libraries_Trove_Maid_Janitor]] · [[Deferred_Events_and_SignalBehavior]] · [[Promise_Library]] · [[Single_Script_Architecture]] · [[Community_Modules_Index]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://github.com/Data-Oriented-House/LemonSignal · https://github.com/Sleitnick/RbxUtil
