---
aliases: [SurfaceGui, BillboardGui, Nameplates, Overhead health bars, 3D UI]
tags:
  - roblox-dev
  - ui/world-space
type: api
last_updated: 2026-10-27
status: complete
---
# World-Space UI (SurfaceGui & BillboardGui)

> **TL;DR:** `SurfaceGui` draws UI on a part **face** (screens, signs, terminals). `BillboardGui` draws camera-facing UI anchored to a part or attachment (nameplates, health bars, damage numbers). Both support `AlwaysOnTop`, `LightInfluence` (0–1), `Brightness` and `MaxDistance` (SurfaceGui default 1000; BillboardGui default ∞). Buttons only receive input when the gui is under the player's **PlayerGui** (use `Adornee`). Billboard `Size` *scale* = **studs**, *offset* = **pixels**.

## Overhead bar (client-side, pooled)
```luau
local bb = Instance.new("BillboardGui")
bb.Adornee = character:WaitForChild("Head")
bb.Size = UDim2.new(4, 0, 0.5, 0)      -- 4 studs × 0.5 studs: shrinks with distance
bb.StudsOffset = Vector3.new(0, 2.5, 0)
bb.MaxDistance = 120                    -- don't render far-away bars
bb.LightInfluence = 0                   -- readable at night / in storms
bb.Parent = localPlayer.PlayerGui       -- parent here so input works if needed
```
- Use **offset** size for constant on-screen size (nameplates), **scale** size for world-sized signage.
- `PlayerToHideFrom` hides your own nameplate locally.
- SurfaceGui: `SizingMode = PixelsPerStud` + `PixelsPerStud` for consistent text density across part sizes. `ZOffset` layers multiple guis on one face.

## Production notes
- Build world UI **on the client** from replicated state (health attributes), not server-created guis per player ([[Attributes]], [[Client_Side_VFX_Replication]]).
- Many billboards = many draws. Cap by distance, pool instances, update only on change ([[Object_Pooling]], [[UI_Performance]]).
- During weather (fog, rain), `LightInfluence = 0` keeps critical info legible. Diegetic signage can keep `LightInfluence = 1` for realism ([[Weather_System_Architecture]]).
- `ProximityPrompt` covers most "press E to interact" cases with built-in input handling ([[Cross_Platform_UI_Input]]).

## Related
[[Damage_Numbers_and_Hit_Markers]] · [[Custom_HUD_Design]] · [[Object_Pooling]] · [[UI_Performance]] · [[Attributes]] · [[Client_Side_VFX_Replication]] · [[Cross_Platform_UI_Input]] · [[Weather_System_Architecture]] · [[Light_Sources_and_Highlights]] · [[Roblox_UI_Fundamentals]] · [[MOC_UI_UX_and_Components]]

## Sources
- https://create.roblox.com/docs/ui/in-experience-containers · https://create.roblox.com/docs/reference/engine/classes/BillboardGui
