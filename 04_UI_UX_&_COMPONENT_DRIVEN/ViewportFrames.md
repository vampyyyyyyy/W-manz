---
aliases: [ViewportFrame, WorldModel, 3D in UI, Item preview, Minimap]
tags:
  - roblox-dev
  - ui/3d
type: api
last_updated: 2026-10-27
status: complete
---
# ViewportFrames

> **TL;DR:** A `ViewportFrame` renders 3D objects through its `CurrentCamera` into a 2D GuiObject. Use it for item previews, character portraits, minimaps and equip screens. Add a **`WorldModel`** child for animated rigs and raycasts (parts aren't simulated). Caveats: **no shadows or post-processing**, Neon and Glass render at lowest quality, no nested GuiObjects, and env lighting is off unless you add a `Sky` child. Light it with `Ambient`, `LightColor` and `LightDirection`.

## Item preview (spin the camera, not the model)
```luau
local vf = Instance.new("ViewportFrame")
vf.Ambient, vf.LightColor = Color3.fromRGB(160, 160, 170), Color3.fromRGB(255, 244, 230)
vf.LightDirection = Vector3.new(-1, -1.5, -0.5)
local cam = Instance.new("Camera"); cam.FieldOfView = 40; cam.Parent = vf
vf.CurrentCamera = cam
local model = itemTemplate:Clone(); model:PivotTo(CFrame.identity); model.Parent = vf

local t = 0
local conn = RunService.PreRender:Connect(function(dt)
	t += dt
	cam.CFrame = CFrame.Angles(0, t * 0.8, 0) * CFrame.new(0, 1, 6)
end)
-- disconnect + destroy when the panel closes (Trove)
```

## Rules
- Update the **camera** to change the view. Moving many objects inside is costlier.
- Each visible ViewportFrame is an extra render. Limit concurrent ones and render static previews **once** (stop the loop) ([[UI_Performance]], [[Rendering_Optimization]]).
- `WorldModel`: needed for `Animator` playback on rigs and spatial queries. Create it only while shown, destroy when hidden. `UseWorkspaceCollisionGroups` controls query groups.
- Want reflections? Add a `Sky` child with the six skybox textures, and reflective materials then light like `EnvironmentSpecularScale = 1`.
- Clean up connections and clones ([[Cleanup_Libraries_Trove_Maid_Janitor]], [[Memory_Leaks]]).

## Related
[[UI_Grid_and_Table_Layouts]] · [[Inventory_Systems]] · [[Animation_System]] · [[Camera_System]] · [[Rendering_Optimization]] · [[UI_Performance]] · [[Memory_Leaks]] · [[Cleanup_Libraries_Trove_Maid_Janitor]] · [[RunService_Frame_Events]] · [[MOC_UI_UX_and_Components]]

## Sources
- https://create.roblox.com/docs/ui/viewport-frames · https://create.roblox.com/docs/reference/engine/classes/ViewportFrame · https://create.roblox.com/docs/reference/engine/classes/WorldModel
