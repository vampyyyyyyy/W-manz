---
aliases: [BindableEvent, BindableFunction, Same-side events]
tags:
  - roblox-dev
  - engine/events
type: api
last_updated: 2026-10-27
status: complete
---
# BindableEvents & BindableFunctions

> **TL;DR:** Bindables are same-side (server↔server or client↔client) events and callbacks implemented as Instances. They're useful as **capability bridges** for sandboxed code and for decoupling scripts. They **copy arguments with remote-like rules** (tables copied, metatables stripped, mixed tables mangled), so many projects prefer pure-Luau [[Signal_Libraries]] for in-module events.

## API
| Object | Fire | Listen |
| --- | --- | --- |
| `BindableEvent` | `:Fire(...)` | `.Event:Connect(fn)` |
| `BindableFunction` | `:Invoke(...)` (yields, returns values) | `.OnInvoke = fn` (callback, single handler) |

## When Bindables are the right tool
- **Sandboxed containers:** a callback registered by trusted code runs with *its* capabilities when untrusted code fires it, so you can expose a narrow, safe API to UGC or third-party models ([[Script_Capabilities]]).
- Cross-script communication between separately authored scripts (legacy or plugin systems) without shared requires.
- Exposing hooks to `StarterGui:SetCore` style APIs, which require BindableFunctions.

## When not
- Inside one codebase, a ModuleScript signal is faster, keeps table identity and metatables, and is type-safe ([[Signal_Libraries]], [[Generics]]).
- **Never** to cross client↔server. That's what remotes are for ([[RemoteEvents_and_RemoteFunctions]]).

## Gotchas
- `BindableFunction:Invoke` yields if the callback yields, and errors propagate to the invoker.
- Arguments follow the same rules as remotes (per the official docs): tables are **copied** (identity lost), metatables are stripped, non-string keys become strings, and mixed or `nil`-holed tables lose elements.
- Deferred signal behavior applies to `.Event` handlers ([[Deferred_Events_and_SignalBehavior]]).

## Related
[[Signals_and_Connections]] · [[Signal_Libraries]] · [[RemoteEvents_and_RemoteFunctions]] · [[Script_Capabilities]] · [[Deferred_Events_and_SignalBehavior]] · [[Generics]] · [[Single_Script_Architecture]] · [[Metatables]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/scripting/events/bindable · https://create.roblox.com/docs/scripting/capabilities#bindable-functions-and-events
