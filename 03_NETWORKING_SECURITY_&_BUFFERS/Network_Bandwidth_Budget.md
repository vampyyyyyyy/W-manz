---
aliases: [Bandwidth, Network budget, Data ping, Network ping, KB/s]
tags:
  - roblox-dev
  - networking/performance
type: concept
last_updated: 2026-10-27
status: complete
---
# Network Bandwidth Budget

> **TL;DR:** Bandwidth problems show up as **data ping** climbing above network ping, rubber-banding and delayed remotes. That's replication queues backing up. Budget per feature (bytes × rate × recipients), replicate on change, keep cosmetics on the client, and measure with the Developer Console and MicroProfiler. Don't guess.

## Two pings (official definitions)
- **Network ping:** raw packet round trip, shown in the Performance Stats bar. Mostly geography, outside your control. Simulate it with Studio's network simulation ([[Studio_Testing_Modes]]).
- **Data ping:** round trip through the **replication system**: client queue → network (with retransmits) → server queue → back. It's always ≥ network ping. If it's *much* higher, the server is producing replication data faster than the network or client can drain it. Average data ping is in Developer Console ▸ **Server Stats**, and per-client in **Shift+F3** network stats ([[Developer_Console]]).

## Where bandwidth goes
| Source | Typical mistake | Fix |
| --- | --- | --- |
| Remotes | Per-frame sends, whole inventories on every change | Change-only, deltas, [[Packet_Compression]] |
| Property replication | **Server-side TweenService** (property replicated every frame), server-moved effects | Tween on clients ([[TweenService]]), [[Client_Side_VFX_Replication]] |
| Instance churn | Creating/destroying big trees (maps, rigs with Animation Editor metadata left in) | Chunk loading, clean rigs, [[Object_Pooling]] |
| Physics | Many unanchored client/server-owned assemblies | Anchor, sleep, ownership tuning ([[Physics_Optimization]]) |
| Join burst | Huge `ReplicatedStorage`/`ReplicatedFirst` | [[StreamingEnabled]], lazy-load assets |

## Back-of-envelope math
`bytes/s per client = Σ(feature payload × send rate × entities visible)`. Example: 30 NPCs × 12-byte quantized snapshot × 10 Hz = **3.6 KB/s** per client. Fine. The same data as unquantized CFrames in tables at 60 Hz can be well over 10× that. Keep [[UnreliableRemoteEvent]] packets under **1,000 bytes**, and remember the ~500 msgs/s per-client throttle for client→server.

## Tooling
- **MicroProfiler** scopes: `ProcessPackets` (incoming packets, event invocations, property changes) and `Allocate Bandwidth and Run Senders` (outgoing, servers) ([[MicroProfiler]]).
- `Stats` service and Developer Console ▸ Network for send/receive rates.
- Test with network simulation (latency + loss) before shipping combat or movement ([[Studio_Testing_Modes]]).

## Related
[[Packet_Compression]] · [[Quantization]] · [[Bitpacking]] · [[UnreliableRemoteEvent]] · [[RemoteEvents_and_RemoteFunctions]] · [[Replication_Model]] · [[StreamingEnabled]] · [[MicroProfiler]] · [[Developer_Console]] · [[TweenService]] · [[Client_Side_VFX_Replication]] · [[MOC_Networking_Security_and_Buffers]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://create.roblox.com/docs/performance-optimization/identify#ping
- https://create.roblox.com/docs/performance-optimization/improve#networking-and-replication
