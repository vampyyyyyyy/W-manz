---
aliases: [Camera, CurrentCamera, CameraType Scriptable, FieldOfView, WorldToViewportPoint, Custom camera, Orthographic camera, ProjectionType, ViewStretch]
tags:
  - roblox-dev
  - engine/camera
type: api
last_updated: 2026-11-05
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
| `ProjectionType`, `OrthographicMode`, `OrthographicSize` | Orthographic projection (**Studio beta**, Nov 2026, see below) |
| `ViewStretch` | Non-square pixels: stretch the unpinned axis up to 2:1 (stun / disorientation effects) |

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

## Orthographic projection (Studio beta, as of Nov 5, 2026)
- `Camera.ProjectionType = Enum.ProjectionType.Orthographic`: parallel lines stay parallel and objects keep the same size at any distance. Use it for 2D, isometric and top-down games, and minimaps. **`FieldOfView` is ignored** in this mode.
- `OrthographicSize` (studs) is how much of the world one screen axis spans, and `OrthographicMode` picks the axis: `Vertical`, `Horizontal`, `Diagonal` or `MaxAxis` (the longer axis). Zoom = change `OrthographicSize`, not the camera distance.
- **Beta limits:** enable it in Studio ▸ File ▸ Beta Features. **During the beta it only works in Studio**, so don't ship a live game that depends on it yet (staff announcement "[Studio Beta] Build 2D, Isometric, and Top-Down Games With Orthographic Camera", late Oct 2026). The API reference documents the properties without a beta tag.
- **Not yet documented:** how `ScreenPointToRay` / `ViewportPointToRay`, shadows, and occlusion helpers like `GetPartsObscuringTarget` behave in orthographic mode. Test aim and click raycasts before relying on them ([[Raycasting]]).

## `ViewStretch`: disorientation without a shader
The FOV or orthographic size pins one axis and the other normally adjusts to keep pixels square. `ViewStretch` stretches that other axis, **up to a 2:1 ratio**, for both perspective and orthographic cameras. The API docs suggest animating it "to make the view feel not quite right, such as when stunned". A short stretch-and-recover on a stun reads well alongside shake ([[Camera_Shake]]):
```luau
--!strict
-- Client: pulse ViewStretch when the server tells us we're stunned
local TweenService = game:GetService("TweenService")
local cam = workspace.CurrentCamera

local function stunPulse(intensity: number)  -- 0..1
	local peak = 1 + 0.25 * math.clamp(intensity, 0, 1)  -- stay well inside the 2:1 limit
	cam.ViewStretch = peak
	TweenService:Create(cam, TweenInfo.new(0.35, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), { ViewStretch = 1 }):Play()
end
```
Skip or scale it down when `GuiService.ReducedMotionEnabled` is true ([[Responsive_UI_and_Safe_Areas]]). Values below 1 and anything past 2:1 are unverified, so keep it in the 1–2 range. **`ViewStretch` arrived in the same docs update as the orthographic beta, so it may also be Studio-only for now.** Not tested in Studio. Verify it in a live test place before shipping.

## Related
[[Camera_Shake]] · [[Hitstop_and_Impact_Feel]] · [[Responsive_UI_and_Safe_Areas]] · [[TweenService]] · [[Task_Scheduler]] · [[RunService_Frame_Events]] · [[Input_Action_System]] · [[Shapecasting]] · [[Raycasting]] · [[ODM_Gear_System]] · [[Damage_Numbers_and_Hit_Markers]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/workspace/camera/index · https://create.roblox.com/docs/reference/engine/classes/Camera (ProjectionType, OrthographicMode, OrthographicSize, ViewStretch added in the Creator Docs repo, Oct 30–Nov 5, 2026)
- https://devforum.roblox.com/t/studio-beta-build-2d-isometric-and-top-down-games-with-orthographic-camera/4966772 (Studio beta announcement; read via search excerpts)
