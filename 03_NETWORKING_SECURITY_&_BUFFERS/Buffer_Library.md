---
aliases: [buffer, buffers, buffer library, Luau buffer]
tags:
  - roblox-dev
  - luau/buffers
type: api
last_updated: 2026-10-27
status: complete
---
# Buffer Library

> **TL;DR:** `buffer` is Luau's fixed-size, mutable block of raw bytes, up to **1 GiB**. Read and write typed integers and floats (little-endian), strings and, since 2025, **arbitrary bit widths** (`readbits`/`writebits`). It's the foundation of compact networking ([[Bitpacking]], [[Custom_Serialization]]) and fast binary data processing.

## API (Roblox, Oct 2026: 26 functions)
| Group | Functions |
| --- | --- |
| Create/convert | `buffer.create(size)` (zero-filled), `buffer.fromstring(s)`, `buffer.tostring(b)`, `buffer.len(b)` |
| Integers | `readi8/readu8`, `readi16/readu16`, `readi32/readu32` + matching `write*` |
| Floats | `readf32/writef32`, `readf64/writef64` |
| Bits | `buffer.readbits(b, bitOffset, bitCount)` → unsigned, `buffer.writebits(b, bitOffset, bitCount, value)`, with `bitCount` 0–32 |
| Bytes | `readstring(b, offset, count)`, `writestring(b, offset, s, count?)`, `copy(target, tOff, source, sOff?, count?)`, `fill(b, offset, value, count?)` |

## Semantics that matter
- **Offsets are bytes** (except the `*bits` functions, which take a *bit* offset). Out-of-range access **errors**. There's no silent overflow.
- **Little-endian** everywhere. `readbits` and `writebits` go LSB-first: `writebits(b, 0, 1, 1)` then `writebits(b, 1, 1, 1)` makes byte 0 equal 3.
- `writeu8(b, 0, 300)` stores `300 % 256` (truncation). Validate ranges yourself.
- `buffer.copy` handles overlapping regions correctly (memmove semantics).
- Passing a buffer through Roblox APIs (remotes, attributes, Bindables) **copies** it, so identity isn't preserved. One buffer can't be shared between [[Actors_and_Messaging|Actors]].
- Buffers are their own type: `typeof(b) == "buffer"` and `type(b) == "buffer"`.

## Example: writer/reader cursor
```luau
--!strict
local Writer = {}
Writer.__index = Writer
export type Writer = typeof(setmetatable({} :: { buf: buffer, pos: number }, Writer))

function Writer.new(capacity: number?): Writer
	return setmetatable({ buf = buffer.create(capacity or 64), pos = 0 }, Writer)
end

function Writer.ensure(self: Writer, n: number)
	local need = self.pos + n
	local len = buffer.len(self.buf)
	if need <= len then return end
	local grown = buffer.create(math.max(need, len * 2)) -- amortized growth
	buffer.copy(grown, 0, self.buf, 0, self.pos)
	self.buf = grown
end

function Writer.u16(self: Writer, v: number) self:ensure(2) buffer.writeu16(self.buf, self.pos, v) self.pos += 2 end
function Writer.f32(self: Writer, v: number) self:ensure(4) buffer.writef32(self.buf, self.pos, v) self.pos += 4 end
function Writer.str(self: Writer, s: string)
	self:u16(#s)
	self:ensure(#s)
	buffer.writestring(self.buf, self.pos, s)
	self.pos += #s
end

function Writer.finish(self: Writer): buffer -- trim to exact size before sending
	local out = buffer.create(self.pos)
	buffer.copy(out, 0, self.buf, 0, self.pos)
	return out
end
return Writer
```

## Performance notes
- Buffer reads and writes are builtin **fastcalls**, and [[Native_Code_Generation]] lowers them to direct memory ops (the 2025 codegen work added load-store propagation for buffers) ([[Builtin_Fastcalls_and_Imports]]).
- Integer math on values read from buffers can stay in CPU integer registers under native codegen.
- For networking, the engine also compresses buffers. Measure real packet sizes before hand-optimizing every bit ([[Network_Bandwidth_Budget]]).

## Gotchas
- `f32` loses precision (about 7 significant digits). World positions far from the origin lose centimetres, so quantize relative to a reference point ([[Quantization]], [[Numbers_and_Floating_Point]]).
- `readstring` returns raw bytes. Validate UTF-8 (`utf8.len`) before saving to DataStores ([[Server_Side_Validation]]).
- `string.pack`/`string.unpack` also exist now, but buffers are the recommended structure for binary work ([[String_Pack_and_Unpack]]).

## Related
[[Bitpacking]] · [[Bitwise_Operations_bit32]] · [[Custom_Serialization]] · [[Quantization]] · [[Packet_Compression]] · [[UnreliableRemoteEvent]] · [[Networking_Libraries_Comparison]] · [[String_Pack_and_Unpack]] · [[Native_Code_Generation]] · [[Numbers_and_Floating_Point]] · [[MOC_Networking_Security_and_Buffers]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://create.roblox.com/docs/reference/engine/libraries/buffer
- https://rfcs.luau.org/type-byte-buffer.html · https://rfcs.luau.org/function-buffer-bits.html
- https://luau.org/news/2025-12-19-luau-recap-runtime-2025
