---
aliases: [Unreliable Remote, UnreliableRemoteEvents, unreliable events]
tags:
  - roblox-dev
  - networking/remotes
type: api
last_updated: 2026-10-27
status: complete
---
# UnreliableRemoteEvent

> **TL;DR:** A [[RemoteEvents_and_RemoteFunctions|RemoteEvent]] variant with no delivery and no ordering guarantees. In return it's cheaper and lower-latency. Use it for continuously changing or cosmetic data where a newer packet makes the old one worthless: aim direction, look vectors, cosmetic VFX triggers, snapshot positions.

## Hard rules (official)
- **Payload over 1,000 bytes is dropped.** Studio's Output tells you how far over you went. The engine encodes and compresses some types ([[Buffer_Library|buffers]] included), so you can't always know the exact size in advance. Leave headroom (see [[Network_Bandwidth_Budget]]).
- Shares the **~500 requests/second per client** limit with the other unreliable remotes. Excess gets **dropped**, not queued.
- **No queue:** if nothing is connected to `OnServerEvent` or `OnClientEvent` when a packet arrives, it's discarded immediately.
- **No ordering**, including relative to reliable RemoteEvents and RemoteFunctions. A packet can arrive *after* a newer one.
- Scripts that fire it never yield.

## When to use / when not to
| Good fit | Bad fit (use a reliable RemoteEvent) |
| --- | --- |
| Head/aim direction at 10–30 Hz | "Ability used", "item bought", state transitions |
| Cosmetic hit sparks, footstep cues | Anything that grants currency, XP or damage |
| Snapshot interpolation of NPCs | Anything the receiver must see exactly once |
| Voice/emote-like ephemeral cues | Initial state sync for a joining player |

## Pattern: sequence numbers + fixed send rate
```luau
--!strict
-- Client: send aim at 20 Hz, not every frame
local RunService = game:GetService("RunService")
local AimRemote = game.ReplicatedStorage.Remotes.Aim :: UnreliableRemoteEvent
local SEND_INTERVAL = 1 / 20
local seq, acc = 0, 0

RunService.Heartbeat:Connect(function(dt)
	acc += dt
	if acc < SEND_INTERVAL then return end
	acc = 0
	seq = (seq + 1) % 65536
	local look = workspace.CurrentCamera.CFrame.LookVector
	local b = buffer.create(2 + 6)
	buffer.writeu16(b, 0, seq)
	-- quantize each axis of a unit vector to int16 (see Quantization)
	buffer.writei16(b, 2, math.round(look.X * 32767))
	buffer.writei16(b, 4, math.round(look.Y * 32767))
	buffer.writei16(b, 6, math.round(look.Z * 32767))
	AimRemote:FireServer(b)
end)
```
```luau
--!strict
-- Server: drop stale/out-of-order packets (with u16 wraparound)
local lastSeq: { [Player]: number } = {}
AimRemote.OnServerEvent:Connect(function(player: Player, b: unknown)
	if typeof(b) ~= "buffer" or buffer.len(b) ~= 8 then return end
	local s = buffer.readu16(b, 0)
	local prev = lastSeq[player]
	if prev and ((s - prev) % 65536) >= 32768 then return end -- older than what we have
	lastSeq[player] = s
	-- decode + clamp, then store for hit validation / replication
end)
```

## Gotchas
- Still attacker input: validate exactly like reliable remotes ([[Server_Side_Validation]]).
- Dropped packets are normal (packet loss, throttling), so receivers must **interpolate** or hold the last value ([[Client_Prediction_and_Reconciliation]]).
- Don't send "start" and "stop" over unreliable. If "stop" is lost, the effect never ends. Send a *state* (e.g. `isCharging = true` repeated each tick) or use reliable events for edges.
- In [[Blink_IDL]] and [[Zap_IDL]], `Type: Unreliable` maps to this class with the same 1,000-byte cap.

## Related
[[RemoteEvents_and_RemoteFunctions]] · [[Remote_Architecture_Patterns]] · [[Quantization]] · [[Bitpacking]] · [[Packet_Compression]] · [[Buffer_Library]] · [[Network_Bandwidth_Budget]] · [[Client_Side_VFX_Replication]] · [[Lag_Compensation]] · [[Networking_Libraries_Comparison]] · [[MOC_Networking_Security_and_Buffers]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/UnreliableRemoteEvent
- https://create.roblox.com/docs/scripting/events/remote#unreliableremoteevents
