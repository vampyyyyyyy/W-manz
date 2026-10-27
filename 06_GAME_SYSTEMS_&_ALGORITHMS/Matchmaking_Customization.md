---
aliases: [Matchmaking, Custom matchmaking, Matchmaking signals, Server scoring]
tags:
  - roblox-dev
  - systems/cross-server
type: concept
last_updated: 2026-10-27
status: complete
---
# Matchmaking (Roblox Custom Matchmaking)

> **TL;DR:** When players join, Roblox filters eligible public servers (not full, private, reserved or shutting down), **scores** them as a **weighted sum of signals**, and picks the best one. In Creator Dashboard ▸ Configurations ▸ **Custom matchmaking** you can re-weight Roblox's signals (latency, age group, language, friends…) and add up to **2 custom signals** built on **custom attributes** (e.g. skill rating stored in DataStores), with simulation on mock servers and analytics.

## Concepts
- **Attributes:** numerical (skill, level) or categorical (language, mode preference).
  - Numerical signals reward small differences between the joining player and the server's aggregate.
  - Categorical signals reward how common the player's value is in the server.
- **Signals:** Roblox-provided (location/latency, age group, language, friends, occupancy…) or custom (player or server, numerical or categorical).
- **Weights:** the per-signal importance in the weighted sum. Preview the impact on mock servers before applying.
- **Analytics:** track configuration success (dashboard).

## When to use which matchmaking
| Need | Tool |
| --- | --- |
| "Put players in a good public server" (skill-ish, language, latency) | **Custom matchmaking config** (no code) |
| Exact team sizes, ranked queues, parties, draft modes | **Your own queue** in MemoryStore + `TeleportAsync` to reserved servers ([[MemoryStore_Data_Structures]], [[TeleportService_and_Reserved_Servers]]) |
| Lobby → match → lobby loops | Lobby place + reserved match servers + MessagingService notifications ([[MessagingService_Cross_Server]]) |

## Custom ranked queue sketch
1. Player presses "Ranked": the server adds a ticket `{userId, mmr, region, t}` to `Queue_<region>_<shard>`.
2. A matchmaker loop (one designated server per shard, or all servers with a lock) reads batches, buckets by MMR ± a window that **widens with wait time**, and forms matches.
3. It reserves a server, teleports the group, and removes the tickets (`RemoveAsync`). It re-queues on teleport failure.

## Related
[[MemoryStore_Data_Structures]] · [[TeleportService_and_Reserved_Servers]] · [[MessagingService_Cross_Server]] · [[MemoryStoreService]] · [[Analytics_Dashboard_and_Metrics]] · [[Experiments_and_AB_Testing]] · [[DataStoreService]] · [[Retention_and_Engagement_Metrics]] · [[MOC_Game_Systems_and_Algorithms]]

## Sources
- https://create.roblox.com/docs/matchmaking · https://create.roblox.com/docs/matchmaking/customize-matchmaking
