---
aliases: [SLIM, Scalable Lightweight Interactive Models, Frustum streaming, FrustumStreaming, SLIM avatars, ModelLevelOfDetail SLIM]
tags:
  - roblox-dev
  - performance/streaming
type: api
last_updated: 2026-10-27
status: complete
---
# SLIM & Frustum Streaming

> **TL;DR:** **SLIM** (Scalable Lightweight Interactive Models): set `Model.LevelOfDetail = SLIM` on static models and Roblox's cloud transcodes them into **composite meshes with multiple LODs**, so distant models stay visible and detailed with far fewer draw calls, triangles and memory. `Workspace.EnableSLIMAvatars` does the same for avatars. **Frustum streaming** (`Player.FrustumStreaming`, server-set) streams content **in the camera view beyond the normal radius**, for scopes, high-speed travel and free cameras.

## SLIM
**Requirements:** StreamingEnabled on, the place **saved to Roblox** (cloud transcoding, not a local file), and **Team Create enabled**.
**How it works:** on publish or playtest, render-relevant data (geometry, materials, textures, transforms) uploads to a transcoder. It generates an optimized composite with LODs, strips hidden internal geometry and optimizes textures. Clients fetch it from the CDN and render the SLIM composite when it's more efficient, or when the original is streamed out (only a minimal placeholder stays in the DataModel).
**Best for:** static world geometry like buildings, props, parked vehicles and terrain features. Runtime changes (adding or removing parts, changing materials or geometry) **prevent** SLIM rendering for that model.
**Migration:** batch-convert legacy `StreamingMesh` models to `SLIM` with a command-bar loop over `workspace:GetDescendants()`. The first generation can take 1–2 minutes before it shows.

## Frustum streaming
`Player.FrustumStreaming` (`Enum.FrustumStreamingMode`), **server-only**:
| Mode | Behavior |
| --- | --- |
| `Default`/`Disabled` | Off |
| `Automatic` | Engine enables it on narrow FOV (scopes), high speed toward the look direction (racing, **ODM flight**), or a camera far from the focus (free cam), with a short activation delay |
| `Enabled` | Always on (manual control, e.g. during a cutscene) |
It's **additive** to the normal streaming radius and replication foci, so it costs more memory and CPU, and normal bandwidth quotas still apply.
```luau
game.Players.PlayerAdded:Connect(function(player)
	player.FrustumStreaming = Enum.FrustumStreamingMode.Automatic
end)
```

## Related
[[StreamingEnabled]] · [[Model_Streaming_Modes]] · [[Draw_Calls_and_Instancing]] · [[Rendering_Optimization]] · [[Mobile_and_Low_End_Optimization]] · [[ODM_Gear_System]] · [[Camera_System]] · [[Memory_Categories]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://create.roblox.com/docs/workspace/streaming/slim · https://create.roblox.com/docs/workspace/streaming/frustum
