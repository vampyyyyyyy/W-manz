---
aliases: [Serialization, Binary serialization, Schema serialization, Save compression]
tags:
  - roblox-dev
  - networking/serialization
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Custom Serialization

> **TL;DR:** Serialization turns Luau values into bytes and back. Schema-driven binary serialization (both sides know the layout) is far smaller and faster than generic encoding. Use it for hot network paths, replays, large save blobs and cross-server messages. **Don't** hand-roll it for a few cold remotes, where IDL tools ([[Blink_IDL]], [[Zap_IDL]]) or plain remotes are fine.

## When it pays off
| Use case | Why |
| --- | --- |
| High-frequency replication (projectiles, NPC snapshots) | Bytes × rate × players adds up ([[Network_Bandwidth_Budget]]) |
| Replays / kill-cams | Thousands of frames; JSON is enormous |
| Big player saves (building games, plots) | DataStore value size limit (4 MB) ([[DataStore_Limits_and_Error_Codes]]) |
| [[MessagingService_Cross_Server]] / [[MemoryStoreService]] payloads | Strict per-message size limits |

## Pattern: schema + codec table
```luau
--!strict
type Codec<T> = { size: (T) -> number, write: (buffer, number, T) -> number, read: (buffer, number) -> (T, number) }

local u8: Codec<number> = {
	size = function() return 1 end,
	write = function(b, o, v) buffer.writeu8(b, o, v) return o + 1 end,
	read = function(b, o) return buffer.readu8(b, o), o + 1 end,
}
local f32: Codec<number> = {
	size = function() return 4 end,
	write = function(b, o, v) buffer.writef32(b, o, v) return o + 4 end,
	read = function(b, o) return buffer.readf32(b, o), o + 4 end,
}
local vec3: Codec<Vector3> = {
	size = function() return 12 end,
	write = function(b, o, v) o = f32.write(b, o, v.X) o = f32.write(b, o, v.Y) return f32.write(b, o, v.Z) end,
	read = function(b, o)
		local x, y, z
		x, o = f32.read(b, o) y, o = f32.read(b, o) z, o = f32.read(b, o)
		return Vector3.new(x, y, z), o
	end,
}
local function array<T>(item: Codec<T>): Codec<{ T }>
	return {
		size = function(list) local n = 2 for _, v in list do n += item.size(v) end return n end,
		write = function(b, o, list)
			buffer.writeu16(b, o, #list) o += 2
			for _, v in list do o = item.write(b, o, v) end
			return o
		end,
		read = function(b, o)
			local n = buffer.readu16(b, o) o += 2
			local out = table.create(n)
			for i = 1, n do out[i], o = item.read(b, o) end
			return out, o
		end,
	}
end

local function encode<T>(codec: Codec<T>, value: T): buffer
	local b = buffer.create(codec.size(value))
	codec.write(b, 0, value)
	return b
end
```
Compose codecs into records, add [[Quantization]] codecs (e.g. `vec3_q16` relative to the map center), and you have a tiny serializer.

## Rules
- **Version byte first** for anything persisted. Migrations then become a `switch` on the version ([[Data_Versioning_and_Schema_Migration]]).
- **Decoders must be defensive** on the server. Check `buffer.len` before reading, cap array lengths, and treat decode errors as malformed input ([[Server_Side_Validation]]). A crafted `u16` length of 65535 shouldn't allocate a huge table, so bound it.
- **DataStores serialize values to JSON and support `buffer` values natively** (buffers are on the official list of supported types). Save the buffer itself. Don't `buffer.tostring` raw bytes into a string field, because DataStores reject invalid UTF-8. Preview the stored form with `HttpService:JSONEncode`, and never store `inf` or `NaN` (not valid JSON) ([[DataStoreService]]).
- Keep floats as `f32` only when the precision is enough ([[Numbers_and_Floating_Point]]).

## Related
[[Buffer_Library]] · [[Bitpacking]] · [[Quantization]] · [[Packet_Compression]] · [[Networking_Libraries_Comparison]] · [[Blink_IDL]] · [[Zap_IDL]] · [[DataStore_Limits_and_Error_Codes]] · [[Data_Versioning_and_Schema_Migration]] · [[Generics]] · [[MOC_Networking_Security_and_Buffers]]

## Sources
- https://create.roblox.com/docs/reference/engine/libraries/buffer
- https://create.roblox.com/docs/cloud-services/data-stores/error-codes-and-limits
