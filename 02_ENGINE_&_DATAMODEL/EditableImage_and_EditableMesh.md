---
aliases: [EditableImage, EditableMesh, CreateEditableImage, CreateEditableMeshAsync, Content.fromObject, Runtime mesh]
tags:
  - roblox-dev
  - engine/rendering
type: api
last_updated: 2026-10-27
status: complete
---
# EditableImage & EditableMesh

> **TL;DR:** Runtime-created and runtime-modified **images** (pixel buffers) and **meshes** (vertices, faces, UVs). Create them with `AssetService:CreateEditableImage(options)` / `CreateEditableImageAsync(content, options)` and `CreateEditableMesh` / `CreateEditableMeshAsync`. Display them with `Content.fromObject(editable)` in any `Content` property. They're **disabled by default in published games**, so turn on *Enable Mesh / Image APIs* in experience settings, and mind the asset permission rules.

## Uses
- **Decals that change:** paint, blood or graffiti splats, minimaps, procedural textures (`WritePixelsBuffer` with a [[Buffer_Library|buffer]]).
- **Deformation:** dents, terrain-like meshes, procedural foliage, ocean surfaces, soft bodies.
- **Weather surfaces:** dynamic puddle masks or snow layers on meshes ([[Wetness_Puddles_and_Drying]], [[Snow_Accumulation]]).

## Rules & limits (official)
- **Opt-in for published games:** Creator Dashboard ▸ Configure ▸ Settings ▸ *Enable Mesh / Image APIs*, or Studio *Experience Settings ▸ Security ▸ Allow Mesh / Image APIs*. Review the Terms of Use first.
- **Permissions:** `CreateEditableMeshAsync`/`CreateEditableImageAsync` only load assets owned by or shared with the game owner, the Studio user, the client player (client-side), or a group where they have edit permission.
- **Update throughput:** only **one displayed `EditableImage` updates per frame**. Three changed images take three frames to show.
- They consume a per-device **memory budget**. Creation can fail on low-memory devices, so always handle `nil` or errors and fall back.

## Pattern
```luau
local AssetService = game:GetService("AssetService")
local ok, img = pcall(AssetService.CreateEditableImage, AssetService, { Size = Vector2.new(256, 256) })
if ok and img then
	local pixels = buffer.create(256 * 256 * 4)          -- RGBA8
	-- fill pixels ...
	img:WritePixelsBuffer(Vector2.zero, img.Size, pixels)
	decal.TextureContent = Content.fromObject(img)
end
```

## Related
[[Buffer_Library]] · [[Terrain_and_Materials]] · [[Wetness_Puddles_and_Drying]] · [[Snow_Accumulation]] · [[Procedural_Generation]] · [[Rendering_Optimization]] · [[Mobile_and_Low_End_Optimization]] · [[Error_Handling_pcall_xpcall]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/EditableImage · https://create.roblox.com/docs/reference/engine/classes/EditableMesh
