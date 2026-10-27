---
aliases: [Bit packing, Bitfields, Packing booleans, Bit buffer]
tags:
  - roblox-dev
  - networking/serialization
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Bitpacking

> **TL;DR:** Store values in exactly as many **bits** as their range needs: 1 bit per boolean, 7 bits for 0–100 health, 10 bits for an angle at about 0.35° precision. Then pack them back-to-back. With `buffer.writebits`/`readbits` (2025) this no longer needs manual shifting across byte boundaries.

## Problem
A naive state packet `{alive=true, crouching=false, ammo=27, health=83, weaponId=5}` sent through a remote costs tens of bytes after engine encoding. The real information is **1 + 1 + 6 + 7 + 5 = 20 bits ≈ 3 bytes**.

## Solution A: `buffer.writebits` (simplest)
```luau
--!strict
-- layout: [alive:1][crouch:1][ammo:6 (0-63)][health:7 (0-100)][weapon:5 (0-31)] = 20 bits -> 3 bytes
local function packState(alive: boolean, crouch: boolean, ammo: number, health: number, weapon: number): buffer
	local b = buffer.create(3)
	buffer.writebits(b, 0, 1, if alive then 1 else 0)
	buffer.writebits(b, 1, 1, if crouch then 1 else 0)
	buffer.writebits(b, 2, 6, math.clamp(ammo, 0, 63))
	buffer.writebits(b, 8, 7, math.clamp(math.round(health), 0, 100))
	buffer.writebits(b, 15, 5, math.clamp(weapon, 0, 31))
	return b
end

local function unpackState(b: buffer)
	return buffer.readbits(b, 0, 1) == 1,
		buffer.readbits(b, 1, 1) == 1,
		buffer.readbits(b, 2, 6),
		buffer.readbits(b, 8, 7),
		buffer.readbits(b, 15, 5)
end
```

## Solution B: `bit32` into one integer (fastest for ≤ 32 bits)
```luau
local packed = bit32.bor(
	if alive then 1 else 0,
	bit32.lshift(if crouch then 1 else 0, 1),
	bit32.lshift(ammo, 2),
	bit32.lshift(health, 8),
	bit32.lshift(weapon, 15)
)
-- decode: bit32.extract(packed, 8, 7) -> health
```
`bit32.extract(n, field, width)` and `bit32.replace(n, v, field, width)` are made for this. See [[Bitwise_Operations_bit32]].

## Why it works
Information content is set by the **number of distinct values**, not by the Luau type. Every value in Luau is a double (8 bytes) or a heavier object. Fixed layouts also make the decoder trivially validating: a 7-bit field can't hold 5,000 health.

## Variations & pitfalls
- **Signed values**: store with a bias (`value + 512` in 10 bits) or zig-zag encoding. `readbits` is unsigned-only by design.
- **Floats**: convert to fixed point first ([[Quantization]]), then pack the integer.
- **Clamp before packing.** `writebits` keeps only the low `bitCount` bits, so an out-of-range value silently *wraps*, which is a correctness bug and an exploit surface.
- `readbits`/`writebits` loop internally with bounds checks, so they're slightly slower than aligned `readu32` + `bit32.extract`. Pick by hotness ([[Benchmarking_Methodology]]).
- Version your layouts. Add a header byte with a schema version if packets persist (saves, replays) ([[Data_Versioning_and_Schema_Migration]]).

## Related
[[Buffer_Library]] · [[Bitwise_Operations_bit32]] · [[Quantization]] · [[Custom_Serialization]] · [[Packet_Compression]] · [[UnreliableRemoteEvent]] · [[Network_Bandwidth_Budget]] · [[Blink_IDL]] · [[Zap_IDL]] · [[MOC_Networking_Security_and_Buffers]]

## Sources
- https://rfcs.luau.org/function-buffer-bits.html
- https://create.roblox.com/docs/reference/engine/libraries/bit32
