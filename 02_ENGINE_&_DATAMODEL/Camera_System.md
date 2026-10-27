---
aliases: [Camera, CurrentCamera, CameraType Scriptable, FieldOfView, WorldToViewportPoint, Custom camera]
tags:
  - roblox-dev
  - engine/camera
type: api
last_updated: 2026-10-27
status: complete
---
# Camera System

> **TL;DR:** `workspace.CurrentCamera` is **client-only**. Default player scripts drive it in `Custom` mode. For combat or ODM cameras, take control (`CameraType = Scriptable`), or layer offsets on top of the default camera, and update in **PreRender / `BindToRenderStep`** so it matches the frame ([[Task_Scheduler]]). The camera is where game feel lives: FOV kicks, shake, over-the-shoulder offsets, smoothing.

## Key members
| Member | Use |
| --- | --- |
| `CFrame`, `Focus`, `CameraType`, `CameraSubject` | Pose and mode. `Scriptable` = you own it. `Custom` = default controller |
| `FieldOfView` (vertical, 1–120), `FieldOfViewMode` | Speed and dash FOV kick, zoom |
| `ViewportSize` | Screen size (UI math, responsive layouts) |
| `WorldToViewportPoint(pos)` / `WorldToScreenPoint` | Damage numbers, off-screen indicators ([[Damage_Numbers_and_Hit_Markers]]) |
| `ViewportPointToRay(x, y)` / `ScreenPointToRay` | Aim and click raycasts ([[Raycasting]]) |
| `GetPartsObscuringTarget(points, ignore)` | Camera occlusion / fade walls |
| `NearPlaneZ` (read-only) | Clipping considerations for view-models |

## Over-the-shoulder combat camera (sketch)
```luau
--!strict
local RunService = game:GetService("RunService")
local cam = workspace.CurrentCamera
local yaw, pitch = 0, 0
local offset = Vector3.new(2, 2, 9)
local smoothed: CFrame? = nil

RunService:BindToRenderStep("CombatCam", Enum.RenderPriority.Camera.Value + 1, function(dt)
	local root = Character.root()
	if not root then return end
	-- yaw/pitch come from mouse delta or the IAS CameraRotate action
	local base = CFrame.new(root.Position) * CFrame.Angles(0, yaw, 0) * CFrame.Angles(pitch, 0, 0)
	local target = base * CFrame.new(offset)
	smoothed = if smoothed then smoothed:Lerp(target, 1 - math.exp(-20 * dt)) else target
	cam.CFrame = (smoothed :: CFrame) * CameraShake.offset(dt)          -- additive shake layer
end)
```
Add a spherecast from the pivot to the camera position to prevent clipping into walls ([[Shapecasting]]).

## Feel toolkit
- **FOV kick** on dash, boost or grapple release: tween FOV +8–15 then settle ([[ODM_Gear_System]]).
- **Shake** as an additive layer, decaying, noise-based, and respecting accessibility ([[Camera_Shake]]).
- **Hitstop:** freeze or slow the camera follow for 2–4 frames on heavy hits ([[Hitstop_and_Impact_Feel]]).
- Respect **Reduce Motion** for big shakes and FOV pulses ([[Responsive_UI_and_Safe_Areas]]).

## Related
[[Camera_Shake]] · [[Hitstop_and_Impact_Feel]] · [[Task_Scheduler]] · [[RunService_Frame_Events]] · [[Input_Action_System]] · [[Shapecasting]] · [[Raycasting]] · [[ODM_Gear_System]] · [[Damage_Numbers_and_Hit_Markers]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/workspace/camera · https://create.roblox.com/docs/reference/engine/classes/Camera
