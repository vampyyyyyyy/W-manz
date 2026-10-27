---
aliases: [Lua compatibility, Luau vs Lua, Lua 5.1 differences]
tags:
  - roblox-dev
  - luau/language
type: concept
last_updated: 2026-10-27
status: complete
---
# Luau vs Lua Compatibility

> **TL;DR:** Luau = Lua 5.1 minus the unsafe bits, plus a curated set of features from 5.2–5.5. If a Lua tutorial uses `goto`, integers, bitwise operators, `__gc`, `<close>` or `io`, it **won't** work in Luau. Luau also has limits (200 locals and 200 upvalues per function, 20,000-deep Lua call stack) you can hit in generated or huge code.

## Removed from Lua 5.1 (sandboxing)
`io`, `package`, most of `os` and `debug` (`os.time`, `os.clock`, `os.date`, `os.difftime` and `debug.traceback`/`info`/profile functions remain), `loadfile`, `dofile`, `string.dump`, bytecode in `loadstring`. `newproxy` is limited to nil or boolean ([[Luau_Sandboxing]]).

## Adopted from later Lua
| Feature | From | In Luau |
| --- | --- | --- |
| Yieldable `pcall`/`xpcall` | 5.2 | ✔️ ([[Error_Handling_pcall_xpcall]]) |
| `__len` on tables, frontier patterns, `%g`, hex/`\z` escapes | 5.2 | ✔️ |
| `bit32` library | 5.2 | ✔️, extended with `byteswap`, `countlz`, `countrz` ([[Bitwise_Operations_bit32]]) |
| `utf8` library, `\u{}` escapes | 5.3 | ✔️ ([[String_Library_and_Patterns]]) |
| `string.pack`/`unpack`/`packsize` | 5.3 | ✔️ (implemented 2025) ([[String_Pack_and_Unpack]]) |
| Floor division `//` | 5.3 | ✔️ ([[Luau_Syntax_Extensions]]) |
| `table.move`, `coroutine.isyieldable` | 5.3 | ✔️ |
| `coroutine.close` | 5.4 | ✔️ ([[Coroutines]]) |
| Const variables | 5.4 | ✔️ via `const x = …` (Luau syntax, not `<const>`) ([[Const_Bindings]]) |
| PCG-based `math.random` | — | ✔️ ([[Math_Library]]) |

## Deliberately NOT in Luau
`goto` · 64-bit integers and bitwise operators (`&`, `|`, `<<`): use `bit32` · `__gc` finalizers · `<close>` to-be-closed variables · ephemeron tables · `__pairs`/`__ipairs` (replaced by `__iter`, [[Generalized_Iteration]]) · yieldable metamethods · `_ENV`.

## Behavioral differences worth knowing
- **No tail calls.** Deep recursion keeps its stack frames (20,000 Lua call limit), and `pcall`/`resume` nesting is capped at 200 C calls.
- Table literal assignment order follows **program order** in mixed tables.
- `__eq` is called **even when objects are rawequal**.
- Function expressions may **reuse a cached closure** when captured upvalues are identical, so function identity can differ from Lua 5.1 ([[Closures_and_Upvalues]]).
- `os.time(t)` interprets the table as **UTC**.

## Implementation limits
200 locals per function · 200 upvalues · 255 registers · 2^23 constants and instructions · 2^15 nested functions · 20,000 Lua calls deep.

## Related
[[Luau_Overview]] · [[Luau_Sandboxing]] · [[Luau_Syntax_Extensions]] · [[Bitwise_Operations_bit32]] · [[Metamethods]] · [[Generalized_Iteration]] · [[String_Pack_and_Unpack]] · [[Garbage_Collection]] · [[Numbers_and_Floating_Point]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://luau.org/compatibility (luau-lang/site getting-started/compatibility.md, Oct 2026)
