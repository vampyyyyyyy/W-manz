---
aliases: [Memory categories, PlaceMemory, LuaHeap, debug.setmemorycategory, PlaceScriptMemory]
tags:
  - roblox-dev
  - performance/memory
type: api
last_updated: 2026-10-27
status: complete
---
# Memory Categories

> **TL;DR:** The Developer Console **Memory** tab splits usage into **CoreMemory** (engine), **PlaceMemory** (your content: Instances, physics, graphics, textures, sounds, terrain, GUI, animation, navigation…), **PlaceScriptMemory** (your scripts, plus **custom tags** from `debug.setmemorycategory`), **CoreScriptMemory** and **UntrackedMemory**. PlaceMemory and PlaceScriptMemory are where you have control.

## PlaceMemory sub-categories (official)
| Category | What it holds | Typical fix |
| --- | --- | --- |
| `HttpCache` | Downloaded assets (images, meshes) | Dedupe assets, smaller textures |
| `Instances` | Instance objects | Stream, pool, delete unused |
| `Signals` | Event connections between instances | Disconnect ([[Connection_Management]]) |
| `LuaHeap` | Script heap (core + custom) | [[Luau_Heap_Analysis]] |
| `PhysicsCollision` / `PhysicsParts` | Collision data / physics geometry | Simplify `CollisionFidelity`, anchor ([[Physics_Optimization]]) |
| `GraphicsTexture` / `GraphicsTextureCharacter` | Texture memory | Fewer unique textures ([[Rendering_Optimization]]) |
| `GraphicsMeshParts` / `GraphicsParts` / `GraphicsSolidModels` / `GraphicsTerrain` / `GraphicsParticles` | Render data | LOD, SLIM, fewer particles ([[SLIM_and_Frustum_Streaming]]) |
| `Sounds` / `StreamingSounds` | Audio | Stream long audio |
| `TerrainVoxels` / `TerrainPhysics` | Terrain | Smaller terrain or streaming |
| `Gui` | UI elements | Destroy hidden screens, fewer frames ([[UI_Performance]]) |
| `Animation` | Poses, cached KeyframeSequences | Load each animation once per Animator |
| `Navigation` | Pathfinding structures | Limit navmesh regions ([[Pathfinding]]) |

## Custom script categories
```luau
debug.setmemorycategory("AI")        -- allocations from this thread now count under "AI"
AI.spawnWave()
debug.resetmemorycategory()          -- back to the default (script name)
print(debug.getmemorycategory())
```
Tag big subsystems (AI, Inventory, VFX pools) so leaks show up under a meaningful name in PlaceScriptMemory and the LuauHeap **Memory Categories** view.

## Related
[[Developer_Console]] · [[Luau_Heap_Analysis]] · [[Memory_Leaks]] · [[Connection_Management]] · [[Rendering_Optimization]] · [[Physics_Optimization]] · [[Scene_Analysis_Tool]] · [[Mobile_and_Low_End_Optimization]] · [[Garbage_Collection]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://create.roblox.com/docs/studio/optimization/memory-usage · https://create.roblox.com/docs/reference/engine/libraries/debug
