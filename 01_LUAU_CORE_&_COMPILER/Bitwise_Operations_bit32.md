---
aliases: [bit32, Bitwise_Operators, Bitwise operators, bit flags, bitmask]
tags:
  - roblox-dev
  - luau/libraries
type: api
last_updated: 2026-10-27
status: complete
---
# Bitwise Operations (`bit32`)

> **TL;DR:** Luau has **no bitwise operators** (`&`, `|`, `<<`). Use the `bit32` library instead. It treats numbers as **unsigned 32-bit integers**. All `bit32` functions are fastcall builtins, and under native codegen they map to integer CPU instructions, so they're the right tool for flags, packing and hashing ([[Bitpacking]]).

## API (15 functions)
| Function | Meaning |
| --- | --- |
| `band(...)`, `bor(...)`, `bxor(...)`, `bnot(x)` | AND / OR / XOR / NOT (variadic for and/or/xor) |
| `btest(...)` | `band(...) ~= 0`, as a boolean (branch-free under codegen) |
| `lshift(x, n)`, `rshift(x, n)`, `arshift(x, n)` | Logical shifts and arithmetic (sign-filling) right shift |
| `lrotate(x, n)`, `rrotate(x, n)` | Rotations |
| `extract(n, field, width = 1)` | Bits `field..field+width-1` as unsigned (fastest with constant field/width) |
| `replace(n, v, field, width = 1)` | Write `v` into that bit range |
| `byteswap(x)` | Reverse byte order (endianness conversion) |
| `countlz(x)`, `countrz(x)` | Leading or trailing zero count (32 if `x == 0`) |

## Patterns
```luau
--!strict
-- Flags (status effects as a bitmask)
const STUNNED, ROOTED, SILENCED = 0x1, 0x2, 0x4
local status = 0
status = bit32.bor(status, STUNNED, SILENCED)
local canCast = not bit32.btest(status, SILENCED)
status = bit32.band(status, bit32.bnot(STUNNED))   -- clear a flag

-- Bit fields
local packed = bit32.replace(0, 83, 8, 7)          -- health 83 in bits 8..14
print(bit32.extract(packed, 8, 7))                 --> 83

-- Lowest set bit index (e.g. first free slot in a 32-slot bitmap)
local function firstSet(mask: number): number? return if mask == 0 then nil else bit32.countrz(mask) end
```

## Gotchas
- Inputs are converted to **uint32**: negative numbers wrap (`bit32.band(-1)` is `4294967295`), and values ≥ 2^32 lose high bits. If you need 64-bit masks, use two numbers or a [[Buffer_Library|buffer]].
- Results are unsigned. Convert back to signed with `if x >= 2^31 then x - 2^32 else x`.
- `extract`/`replace` error when `field + width > 32`.
- A 64-bit integer type is only a **proposal** (RFC "long integer", not implemented as of Oct 2026) ([[Luau_RFC_Tracker]]).

## Related
[[Bitpacking]] · [[Buffer_Library]] · [[Numbers_and_Floating_Point]] · [[Status_Effects]] · [[Builtin_Fastcalls_and_Imports]] · [[Native_Code_Generation]] · [[Custom_Serialization]] · [[Luau_Lua_Compatibility]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://create.roblox.com/docs/reference/engine/libraries/bit32
- https://rfcs.luau.org/function-bit32-byteswap.html · https://rfcs.luau.org/function-bit32-countlz-countrz.html
