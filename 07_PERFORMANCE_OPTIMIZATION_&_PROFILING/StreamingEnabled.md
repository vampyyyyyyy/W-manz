---
aliases: [Instance streaming, StreamingEnabled, StreamingTargetRadius, StreamingMinRadius, StreamOutBehavior, RequestStreamAroundAsync]
tags:
  - roblox-dev
  - performance/streaming
type: api
last_updated: 2026-10-27
status: complete
---
# StreamingEnabled (Instance Streaming)

> **TL;DR:** With streaming, clients only receive `Workspace` content near them (plus replication foci). Joins get faster, client memory drops, and huge maps fit on phones. It's **required** for [[Server_Authority_Model|server authority]] and [[SLIM_and_Frustum_Streaming|SLIM]]. The cost is that **your client code must tolerate missing instances**: no direct indexing deep into Workspace, use `WaitForChild` with timeouts, use CollectionService binders, and be aware of streamed-out state.

## Recommended settings (official, 2026)
| Property | Recommendation |
| --- | --- |
| `StreamingEnabled` | On |
| `ModelStreamingBehavior` | **Improved** (most efficient for Models with BaseParts) |
| `StreamingIntegrityMode` | **PauseOutsideLoadedArea** (pauses only when the player leaves loaded content) |
| `StreamingMinRadius` | Default **64** (lets low-end devices scale down) |
| `StreamingTargetRadius` | Default **1024** |
| `StreamOutBehavior` | **Opportunistic** (aggressive cleanup, which reduces OOM crashes) |
| `EnableSLIMAvatars` | **Enabled** (lightweight animated avatar stand-ins) |

## Script patterns that survive streaming
```luau
-- ❌ breaks when the door hasn't streamed in yet
local door = workspace.Map.Castle.Door

-- ✅ tag-driven binders (fires on stream-in, cleans up on stream-out)
CollectionService:GetInstanceAddedSignal("Door"):Connect(setupDoor)
CollectionService:GetInstanceRemovedSignal("Door"):Connect(teardownDoor)
for _, d in CollectionService:GetTagged("Door") do setupDoor(d) end

-- ✅ ask the server to stream an area before teleporting a player there (server-side)
player:RequestStreamAroundAsync(targetPosition, 10)  -- timeout seconds
```
- Remotes may pass Instances **not yet streamed** on the receiving client, which arrive as `nil`. Send ids or positions and resolve them later ([[RemoteEvents_and_RemoteFunctions]]).
- `Player:AddReplicationFocus(part)` streams around extra points (spectator camera, controlled drones). Frustum streaming adds the camera view ([[SLIM_and_Frustum_Streaming]]).
- Client-side spatial queries only see **streamed** parts. Server-side checks see everything ([[Spatial_Queries_Overlap]]).

## Model controls
`Model.ModelStreamingMode`: `Default`/`Nonatomic`, `Atomic` (all or nothing), `Persistent` (always present, so use it sparingly), `PersistentPerPlayer` (persistent for specific players via `AddPersistentPlayer`) ([[Model_Streaming_Modes]]).

## Related
[[Model_Streaming_Modes]] · [[SLIM_and_Frustum_Streaming]] · [[CollectionService_Tags]] · [[Replication_Model]] · [[Server_Authority_Model]] · [[Mobile_and_Low_End_Optimization]] · [[Player_and_Character_Lifecycle]] · [[Access_Control_and_Confidentiality]] · [[Network_Bandwidth_Budget]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://create.roblox.com/docs/workspace/streaming · https://create.roblox.com/docs/workspace/streaming/techniques
