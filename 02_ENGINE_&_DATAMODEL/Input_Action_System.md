---
aliases: [IAS, InputAction, InputContext, InputBinding, PlayerScriptsUseInputActionSystem]
tags:
  - roblox-dev
  - engine/input
type: api
last_updated: 2026-10-27
status: complete
---
# Input Action System (IAS)

> **TL;DR:** IAS is Roblox's cross-platform input layer. **`InputContext`** (enable/disable groups like `PlayContext` and `NavContext`, with `Priority` + `Sink`) → **`InputAction`** (`Bool`, `Direction1D/2D/3D`, `ViewportPosition`) → **`InputBinding`**s (keyboard, gamepad, touch `UIButton`, composite WASD, modifiers, thresholds, response curves). It's configured as instances at edit time. It's **required** for [[Server_Authority_Model|server authority]], where inputs are sent to the server and replayed during resimulation.

## Structure
```text
ReplicatedStorage/Inputs (Folder)
└─ PlayContext (InputContext: Priority 2000, Sink = true)
   ├─ CharacterSprint (InputAction, Type = Bool)
   │  ├─ KeyboardBinding (KeyCode = LeftShift)
   │  ├─ GamepadBinding  (KeyCode = ButtonY)
   │  └─ TouchBinding    (UIButton = StarterGui.HUD.SprintButton)
   └─ CameraRotate (InputAction, Type = Direction2D)
      ├─ KeyboardBinding (Up/Down/Left/Right = arrow keys)
      └─ GamepadBinding  (KeyCode = Thumbstick2)
```
Enable `Workspace.PlayerScriptsUseInputActionSystem` so default player scripts use IAS. Under server authority, **`InputContext`s must be descendants of the `Player`**, so clone the folder into each player on join.

## API
| Member | Notes |
| --- | --- |
| `InputAction.Pressed` / `Released` | `Bool` actions only, on transitions |
| `InputAction.StateChanged(state)` | All types. Fires **once per change**, so a held thumbstick won't keep firing. Poll `GetState()` per frame for continuous input |
| `InputAction:GetState()` | Current value (bool, number, Vector2, Vector3) |
| `InputAction.Enabled`, `PreferredBinding`, `DisplayName` | `PreferredBinding` follows the player's current device, which is ideal for button prompts ([[Cross_Platform_UI_Input]]) |
| `InputAction:Fire(state)` / `InputBinding:Fire()` | Programmatically trigger (tests, tutorials, accessibility) |
| `InputContext.Enabled`, `Priority`, `Sink` | Swap control schemes (combat vs menu vs vehicle). A higher priority + `Sink` consumes inputs |
| `InputBinding` thresholds and curves | `PressedThreshold`, `ReleasedThreshold`, `ResponseCurve`, `Scale`, `Vector2Scale`, `ClampMagnitudeToOne`, `PrimaryModifier`/`SecondaryModifier` (chords like Shift+Q) |

## Continuous input pattern
```luau
local cameraRotate = ReplicatedStorage.Inputs.PlayContext.CameraRotate :: InputAction
RunService:BindToRenderStep("CameraRotation", Enum.RenderPriority.Camera.Value, function(dt)
	local look = cameraRotate:GetState() :: Vector2
	CameraController.rotate(look * dt * SENSITIVITY)
end)
```

## Why use it over UserInputService
One binding table for keyboard, gamepad and touch. Contexts replace manual "is a menu open?" checks. It's required for server-authoritative prediction, and it integrates with the [[Character_Controllers_and_ControllerManager|CCL]] (`ActionSlot`) for automatic mobile buttons.

## Related
[[UserInputService_and_ContextActionService]] · [[Server_Authority_Model]] · [[Character_Controllers_and_ControllerManager]] · [[Cross_Platform_UI_Input]] · [[Combo_Systems_and_Input_Buffering]] · [[Camera_System]] · [[Client_Prediction_and_Reconciliation]] · [[Custom_Movement_Abilities]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/input/input-action-system
- https://create.roblox.com/docs/projects/server-authority#input-actions
