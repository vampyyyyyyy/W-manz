---
aliases: [string.pack, string.unpack, string.packsize, binary strings]
tags:
  - roblox-dev
  - luau/libraries
type: api
last_updated: 2026-10-27
status: complete
---
# `string.pack` / `string.unpack`

> **TL;DR:** Lua 5.3's binary packing functions, implemented in Luau in 2025. `string.pack(fmt, ...)` returns a binary **string**, `string.unpack(fmt, s, pos?)` reads values back, and `string.packsize(fmt)` gives fixed sizes. They're handy for porting Lua 5.3 code or one-off formats. For game networking and anything you mutate, prefer the [[Buffer_Library|buffer library]] (it's fixed-size, mutable, and the officially recommended structure).

## Format essentials (Lua 5.3 spec)
| Code | Meaning |
| --- | --- |
| `<` `>` `=` | little / big / native endian |
| `b`/`B`, `h`/`H`, `i4`/`I4`, `i8`… | signed/unsigned 1, 2, 4, n-byte ints |
| `f`, `d` | float32, float64 |
| `s4`, `z` | length-prefixed string (n-byte length), zero-terminated string |
| `x` | one padding byte |
```luau
local blob = string.pack("<I2 f s1", 513, 3.5, "ok")
local id, speed, tag, nextPos = string.unpack("<I2 f s1", blob)
print(string.packsize("<I2 f"))  --> 6 (variable-length 's'/'z' not allowed here)
```

## Pack vs buffer
| | `string.pack` | `buffer` |
| --- | --- | --- |
| Result | Immutable string | Mutable fixed-size memory |
| Bit-level fields | ❌ | ✔️ `readbits`/`writebits` ([[Bitpacking]]) |
| Incremental writes | Re-pack the whole string | Write at offsets |
| Big-endian formats | ✔️ `>` | Manual (`bit32.byteswap`) ([[Bitwise_Operations_bit32]]) |
| Fastcall/native lowering | Library call | Builtins ([[Native_Code_Generation]]) |

## Gotchas
- Packed strings contain arbitrary bytes, so they're often **invalid UTF-8**. Don't store them in DataStores as strings. Store a `buffer` instead ([[Custom_Serialization]]).
- `i8`/`I8` (64-bit) round through doubles, so values above 2^53 lose precision ([[Numbers_and_Floating_Point]]).

## Related
[[Buffer_Library]] · [[Bitpacking]] · [[Custom_Serialization]] · [[String_Library_and_Patterns]] · [[Bitwise_Operations_bit32]] · [[Numbers_and_Floating_Point]] · [[Luau_Lua_Compatibility]] · [[Native_Code_Generation]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://create.roblox.com/docs/reference/engine/libraries/string#pack
- https://rfcs.luau.org/function-string-pack-unpack.html · https://www.lua.org/manual/5.3/manual.html#6.4.2
