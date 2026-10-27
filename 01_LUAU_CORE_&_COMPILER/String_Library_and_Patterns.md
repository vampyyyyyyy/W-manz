---
aliases: [string library, string patterns, string.split, string.format, gsub, utf8]
tags:
  - roblox-dev
  - luau/libraries
type: api
last_updated: 2026-10-27
status: complete
---
# String Library & Patterns

> **TL;DR:** Strings are immutable byte sequences (not Unicode-aware unless you use `utf8`). Use `string.split` (Luau addition) for simple splitting, Lua **patterns** (not regex) for matching, `string.format` or [[String_Interpolation]] for building, and `table.concat` for joining many pieces. Validate untrusted strings with `utf8.len` and a length cap.

## Most used (17 functions on Roblox)
| Function | Notes |
| --- | --- |
| `split(s, sep = ",")` | Plain separator (not a pattern). Empty slices kept: `"a||b"` → `{"a", "", "b"}` |
| `format(fmt, ...)` | `%d %s %q %x %.2f` and `%*` (any value via tostring) |
| `find(s, pattern, init?, plain?)` | Pass `plain = true` to search literal text |
| `match`, `gmatch`, `gsub` | Pattern matching, iteration, replacement (with captures) |
| `sub`, `byte`, `char`, `rep`, `reverse`, `lower`, `upper`, `len` | Byte-based |
| `pack`, `unpack`, `packsize` | Binary formats (2025) ([[String_Pack_and_Unpack]]) |

## Patterns cheat sheet
`.` any · `%a` letters · `%d` digits · `%s` space · `%w` alnum · `%p` punct · `%x` hex · `[%w_]` sets · `^`/`$` anchors · `*` `+` `-` (lazy) `?` · `%b()` balanced · `%f[%w]` frontier · `()` capture. Escape magic chars with `%`.
```luau
local cmd, arg = string.match("/give sword", "^/(%w+)%s+(.+)$")   --> "give", "sword"
local clean = string.gsub(name, "[^%w_]", "")                     -- strip non-identifier chars
for word in string.gmatch(text, "%S+") do end                     -- iterate words
```

## UTF-8
`utf8.len(s)` (nil + position if invalid), `utf8.codes(s)`, `utf8.char(...)`, `utf8.codepoint(s, i, j)`, `utf8.offset(s, n)`, `utf8.charpattern`. Display text, names and chat are UTF-8: `#s` counts **bytes**, not characters.

## Performance
- Repeated `s = s .. piece` in a loop is O(n²). Collect pieces in a table and `table.concat` once ([[Luau_Micro_Optimizations]]).
- `string.byte(s, i)` (function form) is a fastcall, while `s:byte(i)` (method form) isn't ([[Builtin_Fastcalls_and_Imports]]).
- The compiler constant-folds `string.char`, `string.sub` and concatenations of constants (2025).

## Security
Cap lengths **before** pattern matching untrusted input (pathological patterns on huge strings burn CPU), validate UTF-8 before saving ([[Server_Side_Validation]]), and filter any player text shown to others ([[Text_Filtering_Compliance]]).

## Related
[[String_Interpolation]] · [[String_Pack_and_Unpack]] · [[Server_Side_Validation]] · [[Text_Filtering_Compliance]] · [[Builtin_Fastcalls_and_Imports]] · [[Luau_Micro_Optimizations]] · [[Rich_Text]] · [[Metamethods]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://create.roblox.com/docs/reference/engine/libraries/string · https://create.roblox.com/docs/reference/engine/libraries/utf8
