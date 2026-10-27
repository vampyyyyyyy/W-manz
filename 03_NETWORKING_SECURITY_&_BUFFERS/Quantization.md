---
aliases: [Quantisation, Fixed point, Float compression, CFrame compression, Angle compression]
tags:
  - roblox-dev
  - networking/serialization
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Quantization

> **TL;DR:** Map a continuous value onto a small integer range at a precision you choose. For example, a position within ±2,048 studs at 1/16-stud precision fits in **16 bits per axis** instead of 32 or 64. Quantization is the biggest single bandwidth win for movement, aim and projectile data.

## Core formula
```
q = round((value - min) / (max - min) * (2^bits - 1))
value ≈ min + q / (2^bits - 1) * (max - min)
max error = (max - min) / (2^bits - 1) / 2
```

## Recipes
```luau
--!strict
local function quantize(v: number, min: number, max: number, bits: number): number
	local steps = 2 ^ bits - 1
	return math.round((math.clamp(v, min, max) - min) / (max - min) * steps)
end
local function dequantize(q: number, min: number, max: number, bits: number): number
	return min + q / (2 ^ bits - 1) * (max - min)
end

-- Unit direction (aim/look): 3 x int16 = 6 bytes; error ~0.00003 per axis
local function writeDir(b: buffer, o: number, d: Vector3)
	buffer.writei16(b, o, math.round(d.X * 32767))
	buffer.writei16(b, o + 2, math.round(d.Y * 32767))
	buffer.writei16(b, o + 4, math.round(d.Z * 32767))
end

-- Yaw only (characters mostly rotate around Y): 1 x u16, ~0.0055 degrees
local function writeYaw(b: buffer, o: number, cf: CFrame)
	local _, yaw, _ = cf:ToOrientation()
	buffer.writeu16(b, o, quantize(yaw, -math.pi, math.pi, 16))
end
```

## Choosing ranges and precision
| Data | Typical encoding | Notes |
| --- | --- | --- |
| Position in arena | 3 × u16 relative to arena min/max | Re-base per map/chunk; never quantize absolute world coords on huge maps |
| Velocity | 3 × i16 scaled by max speed | Clamp, because exploiters send absurd values |
| Health 0–100 | u8 or 7 bits | [[Bitpacking]] |
| Look direction | 3 × i16, or octahedral 2 × u16 | Octahedral encoding gives the best bits/accuracy ratio for unit vectors |
| Full rotation | "smallest three" quaternion: 2 bits index + 3 × ~10–15 bits | Drop the largest component and rebuild it from unit length |

## Pitfalls
- **Clamp before quantizing.** Out-of-range input otherwise wraps when written with fewer bits.
- **Accumulated error:** never quantize a value, feed it back into simulation, then quantize it again. Keep full-precision authoritative state on the server.
- **Determinism:** client prediction compares predicted vs authoritative states. Compare in quantized space or with tolerances ([[Client_Prediction_and_Reconciliation]]).
- `f32` is already a lossy "quantization" with variable precision. It gets worse far from the origin ([[Numbers_and_Floating_Point]]).

## Related
[[Bitpacking]] · [[Buffer_Library]] · [[Packet_Compression]] · [[Custom_Serialization]] · [[UnreliableRemoteEvent]] · [[CFrame_Math]] · [[Numbers_and_Floating_Point]] · [[Network_Bandwidth_Budget]] · [[Client_Prediction_and_Reconciliation]] · [[MOC_Networking_Security_and_Buffers]]

## Sources
- https://create.roblox.com/docs/reference/engine/libraries/buffer
- https://create.roblox.com/docs/reference/engine/datatypes/CFrame#ToOrientation
