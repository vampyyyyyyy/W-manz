---
aliases: [Sandbox, Luau sandbox, loadstring, LoadStringEnabled, readonly globals]
tags:
  - roblox-dev
  - luau/security
type: concept
last_updated: 2026-10-27
status: complete
---
# Luau Sandboxing

> **TL;DR:** Luau is designed to run **actively malicious** code safely. Unsafe libraries are removed, bytecode loading is gone, built-in libraries and the global table are **read-only**, there's no `__gc`, and hosts can interrupt runaway scripts. Within Roblox, **isolation between scripts** is the developer's job: use [[Script_Capabilities]] and avoid `_G`, `loadstring` and asset requires.

## What's removed or limited (and why)
| Item | Status | Reason |
| --- | --- | --- |
| `io`, `package`, `dofile`, `loadfile`, `module` | Removed | File/process access, global overrides |
| `os` | Only `clock`, `date`, `difftime`, `time` | Environment and process access |
| `debug` | Only `traceback`, `info` (+ Roblox profiling/memory helpers) | Memory-unsafe or isolation-breaking |
| `loadstring` with bytecode, `string.dump`, `load` | Removed | Untrusted bytecode can't be validated |
| `collectgarbage` | Only `"count"` | Other code relies on GC state |
| `newproxy` | Only `true`/`false`/`nil` | |
| `__gc` | Unsupported | Perf, memory safety, thread identity ([[Garbage_Collection]]) |

## Readonly globals
Library tables (`string`, `math`…), the string metatable and the global table are **frozen at VM level**. Even `rawset` and `setmetatable` fail. Roblox gives each script its own global table with `__index` to the builtins, so scripts can write "globals" without monkey-patching shared libraries. Only `setfenv` can substitute globals, which is one more reason it's deprecated ([[Globals_G_shared_and_getfenv]]).

## Interrupts and limits
Hosts install an interrupt handler the VM is guaranteed to call periodically. That's how Roblox kills scripts that exhaust their execution budget ("Script timeout: exhausted allowed execution time").

## For Roblox developers
- Keep `ServerScriptService.LoadStringEnabled = false` unless you run your own sandboxed interpreter.
- Untrusted user code (admin consoles, scripting games) → [[Script_Capabilities]], plus a separate restricted environment or VM design.
- Third-party models → sandbox them ([[Third_Party_Code_and_Backdoors]]).

## Related
[[Script_Capabilities]] · [[Third_Party_Code_and_Backdoors]] · [[Globals_G_shared_and_getfenv]] · [[Luau_Lua_Compatibility]] · [[Luau_C_API_and_Embedding]] · [[Garbage_Collection]] · [[Exploit_Threat_Model]] · [[Luau_Overview]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://luau.org/sandbox (luau-lang/site guides/sandbox.md)
