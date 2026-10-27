---
aliases: [Delta compression, Network compression, Snapshot compression, Delta encoding]
tags:
  - roblox-dev
  - networking/serialization
type: concept
last_updated: 2026-10-27
status: complete
---
# Packet Compression

> **TL;DR:** In order of payoff: **send less often** (rate control, change-only), **send less** (delta against the last acknowledged state, interest management), then **encode tighter** ([[Quantization]] + [[Bitpacking]]). Generic compressors rarely help small game packets. The engine already compresses remote payloads, buffers included.

## Techniques, ranked by usual impact
1. **Event-driven instead of per-frame.** Replicate state when it *changes* ("character state on change, not every frame"). This is Roblox's own top networking recommendation.
2. **Interest management.** Only send what a client can perceive: nearby entities, same team, in view. [[StreamingEnabled]] does this for instances, and you do it for custom remotes.
3. **Rate tiers.** Near targets at 20–30 Hz, far ones at 2–5 Hz. Cosmetic data over [[UnreliableRemoteEvent]].
4. **Delta encoding.** Send only the fields that changed since the last state the receiver has acknowledged, using a bitmask header: `u8 mask` → which of 8 fields follow. Reliable channels can delta against "last sent". Unreliable ones need acks or periodic full snapshots.
5. **Quantize + bitpack** the remaining fields ([[Quantization]], [[Bitpacking]]).
6. **Batch per frame** to amortize per-message overhead ([[Remote_Architecture_Patterns]]). IDL tools do this for you ([[Blink_IDL]], [[Zap_IDL]]).

```luau
--!strict
-- Field-mask delta: only changed fields are written after the mask byte
local FIELDS = { "Health", "Ammo", "State", "Weapon" }
local function encodeDelta(prev: { [string]: number }, cur: { [string]: number }): buffer
	local mask, payload = 0, {}
	for i, f in FIELDS do
		if prev[f] ~= cur[f] then
			mask = bit32.bor(mask, bit32.lshift(1, i - 1))
			table.insert(payload, cur[f])
		end
	end
	local b = buffer.create(1 + #payload)
	buffer.writeu8(b, 0, mask)
	for i, v in payload do buffer.writeu8(b, i, math.clamp(v, 0, 255)) end
	return b
end
```

## Generic compression?
LZ-style or Huffman compression in Luau costs CPU and helps mainly on **large, repetitive** blobs: saves, map data, replays. For DataStore blobs, measure the *stored* (serialized) size, which `HttpService:JSONEncode` previews. Buffers are a supported DataStore value type ([[Custom_Serialization]]).

## Measure first
Use the Developer Console network stats, `Shift+F3` network debug stats, and the MicroProfiler `ProcessPackets` and "Allocate Bandwidth and Run Senders" scopes before and after each change ([[Network_Bandwidth_Budget]], [[MicroProfiler]]).

## Related
[[Quantization]] · [[Bitpacking]] · [[Custom_Serialization]] · [[Network_Bandwidth_Budget]] · [[UnreliableRemoteEvent]] · [[StreamingEnabled]] · [[Remote_Architecture_Patterns]] · [[Networking_Libraries_Comparison]] · [[MicroProfiler]] · [[MOC_Networking_Security_and_Buffers]]

## Sources
- https://create.roblox.com/docs/performance-optimization/improve#networking-and-replication
