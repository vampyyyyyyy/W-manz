---
aliases: [_G, shared, getfenv, setfenv, global variables, environments]
tags:
  - roblox-dev
  - luau/environment
type: concept
last_updated: 2026-10-27
status: complete
---
# Globals: `_G`, `shared`, `getfenv`/`setfenv`

> **TL;DR:** Avoid them. `_G`/`shared` are untyped, global, mutable bags shared by every script on the same side. Exploiters can read and write the client copy. And `getfenv`/`setfenv` (deprecated) **deoptimize** the whole environment: imports, fastcalls, inlining and native code all get disabled. Use `ModuleScript`s and explicit `require` instead.

## Why `_G` is a smell
```luau
-- legacy style (seen in old scripts and exploit loaders)
_G.AutoClick = true
while _G.AutoClick == true do ... end
```
- **No types, no autocomplete, no ownership.** Any script can flip it at any time. Load-order bugs abound.
- **Client `_G` is attacker-writable.** Never let it gate anything important ([[Exploit_Threat_Model]]).
- Sandboxed scripts need the `ScriptGlobals` capability to see `_G`/`shared` ([[Script_Capabilities]]).
- Replacement: a module that returns a state table, with typed getters and setters, or a store library ([[UI_State_Management]]).

## `getfenv` / `setfenv` (deprecated)
- The compiler's **imports** (`math.max` resolved at load) and **fastcalls** assume a *pure* environment. Calling `getfenv` or `setfenv`, **even just to read**, marks the environment impure and dynamically deoptimizes it ([[Builtin_Fastcalls_and_Imports]]).
- **Inlining is disabled** for modules that use them ([[Luau_Compiler_Optimizations]]). Native code falls back too ([[Native_Code_Generation]]).
- They're unavailable inside sandboxed containers.
- They're a classic **obfuscation tool in backdoors** (`getfenv()["require"]`) ([[Third_Party_Code_and_Backdoors]]).

## `loadstring`
Server-only, and off unless `ServerScriptService.LoadStringEnabled` is true. It also taints the environment. Keep it disabled ([[Luau_Sandboxing]]).

## Related
[[Legacy_Code_Smells]] · [[Deprecated_wait_spawn_delay]] · [[Require_and_Module_Resolution]] · [[Builtin_Fastcalls_and_Imports]] · [[Luau_Compiler_Optimizations]] · [[Native_Code_Generation]] · [[Luau_Sandboxing]] · [[Script_Capabilities]] · [[Third_Party_Code_and_Backdoors]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://luau.org/performance#importing-global-access-chains · https://rfcs.luau.org/deprecate-getfenv-setfenv.html
