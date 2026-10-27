---
aliases: [ModelStreamingMode, Atomic models, Persistent models, PersistentPerPlayer, Model LOD]
tags:
  - roblox-dev
  - performance/streaming
type: api
last_updated: 2026-10-27
status: complete
---
# Model Streaming Modes

> **TL;DR:** `Model.ModelStreamingMode` controls how a model streams. **Nonatomic/Default:** parts stream independently. **Atomic:** the whole model arrives together (scripts can rely on all descendants existing). **Persistent:** always sent and never streamed out. **PersistentPerPlayer:** persistent for chosen players. Prefer Atomic over Persistent. Every Persistent model costs memory for every player forever.

## Modes
| Mode | Behavior | Use for |
| --- | --- | --- |
| `Default` / `Nonatomic` | Parts stream individually by distance | Most scenery |
| `Atomic` | Model + all descendants stream in and out as one unit | Interactive models your scripts traverse (doors with hinges, vehicles, NPC rigs) |
| `Persistent` | Sent at join, never streamed out | Truly global objects (a few landmarks, gameplay-critical props). Use sparingly. Overuse kills memory on mobile |
| `PersistentPerPlayer` | Persistent only for players added via `Model:AddPersistentPlayer(player)` | Player-owned bases, quest targets for that player |

## Model level of detail
`Model.LevelOfDetail`: `Disabled`, `StreamingMesh` (legacy imposter for streamed-out models), or **`SLIM`** (cloud-transcoded composite meshes with multiple LODs. It's the modern choice for static geometry) ([[SLIM_and_Frustum_Streaming]]).

## Pitfalls
- Persistent as a "fix" for scripts that index too deep is a band-aid. Refactor to tag binders instead ([[CollectionService_Tags]]).
- Atomic models that are huge still stream as one big unit, causing pops and spikes. Split them into logical sub-models.
- Official perf guidance: **reduce Persistent usage** and the streaming radii when memory is tight ([[Mobile_and_Low_End_Optimization]]).

## Related
[[StreamingEnabled]] · [[SLIM_and_Frustum_Streaming]] · [[CollectionService_Tags]] · [[Mobile_and_Low_End_Optimization]] · [[Rendering_Optimization]] · [[Memory_Categories]] · [[Draw_Calls_and_Instancing]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://create.roblox.com/docs/workspace/streaming#model-streaming-controls · https://create.roblox.com/docs/workspace/streaming/techniques#model-level-of-detail
