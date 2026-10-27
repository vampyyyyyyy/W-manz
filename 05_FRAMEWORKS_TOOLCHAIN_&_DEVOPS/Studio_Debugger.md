---
aliases: [Breakpoints, Logpoints, Watch window, Call stack, Roblox debugger]
tags:
  - roblox-dev
  - toolchain/debugging
type: api
last_updated: 2026-10-27
status: complete
---
# Studio Debugger

> **TL;DR:** Studio has a real debugger: **standard, conditional, logpoint and temporary breakpoints**, per-context triggering (**Client / Server / Edit**), **Watch** (Variables + My Watches), **Call Stack**, hover inspection, and stepping (**F11** into, **F10** over, **Shift+F11** out). Logpoints replace throwaway `print`s without editing code. File-synced code ([[Script_Sync]]) can't be debugged from your external editor, so set breakpoints in Studio.

## Breakpoint types
| Type | Use |
| --- | --- |
| Standard | Pause on a line |
| Conditional (`hitCount > 3 and target.Name == "Dummy"`) | Break only on the interesting iteration or entity |
| Logpoint (`"dmg", dmg, "hp", hum.Health`) | Prints like `print(...)` **without pausing**. Great for timing-sensitive combat code |
| Temporary | Removes itself after the session |

**Trigger At** sets where it fires: Client, Server, or Edit (plugin debugging). In the Breakpoints window you can disable a breakpoint per context, e.g. keep the server one and disable the client one for shared modules.

## Debugging workflow (systematic)
1. **Reproduce** in the right mode: Test for client+server, Server & Clients for replication bugs ([[Studio_Testing_Modes]]).
2. **Inspect:** a logpoint at the remote handler entry shows what the client actually sent ([[RemoteEvents_and_RemoteFunctions]]).
3. **Isolate:** a conditional breakpoint on the failing branch. Read the Call Stack to see who called it.
4. **Fix, then verify** with the same reproduction, plus a regression test where possible ([[Testing_Frameworks]]).

## Other tools
- **Command Bar** runs Luau at edit/runtime. The [[Developer_Console]] (F9 or `/console`) shows client/server logs, memory and network.
- **Log files:** Windows `%LOCALAPPDATA%\Roblox\logs`, macOS `~/Library/Logs/Roblox`. Android uses Logcat, iOS uses Console.app or sysdiagnose.
- Error context: `xpcall(fn, debug.traceback)` for stack traces in production logs ([[Error_Handling_pcall_xpcall]]).
- Performance problems aren't debugger problems. Use [[MicroProfiler]] and [[Script_Profiler]].

## Gotchas
- Pausing at a breakpoint freezes the simulation, so network timeouts and physics hand-offs can behave differently after resuming. Prefer logpoints for netcode ([[Network_Ownership]]).
- Deferred events change *when* handlers run, so a breakpoint shows the deferred order ([[Deferred_Events_and_SignalBehavior]]).
- The `rbx-debug` Assistant skill can drive breakpoints programmatically ([[Roblox_Assistant_and_AI_Tools]]).

## Related
[[Studio_Testing_Modes]] · [[Developer_Console]] · [[Error_Handling_pcall_xpcall]] · [[MicroProfiler]] · [[Script_Profiler]] · [[Testing_Frameworks]] · [[RemoteEvents_and_RemoteFunctions]] · [[Deferred_Events_and_SignalBehavior]] · [[Network_Ownership]] · [[Script_Sync]] · [[Roblox_Assistant_and_AI_Tools]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://create.roblox.com/docs/studio/debugging
