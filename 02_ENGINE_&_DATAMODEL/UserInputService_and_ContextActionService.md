---
aliases: [UserInputService, UIS, ContextActionService, CAS, InputBegan, gameProcessedEvent]
tags:
  - roblox-dev
  - engine/input
type: api
last_updated: 2026-10-27
status: complete
---
# UserInputService & ContextActionService

> **TL;DR:** The classic input APIs. **UserInputService** gives raw events (`InputBegan`, `InputChanged`, `InputEnded`, plus `gameProcessedEvent` to ignore typing in chat or UI) and device state (`MouseBehavior`, `GetLastInputType`, `TouchEnabled`, `GamepadEnabled`). **ContextActionService** binds named actions to multiple inputs with priorities and auto-created touch buttons. New projects should prefer the [[Input_Action_System]]. These are still everywhere in existing code and remain useful for raw input.

## UserInputService
```luau
local UIS = game:GetService("UserInputService")
UIS.InputBegan:Connect(function(input: InputObject, gameProcessed: boolean)
	if gameProcessed then return end                  -- player is typing in chat/TextBox or clicking UI
	if input.KeyCode == Enum.KeyCode.Q then Abilities.cast("Dash") end
	if input.UserInputType == Enum.UserInputType.MouseButton1 then Combat.lightAttack() end
end)
UIS.MouseBehavior = Enum.MouseBehavior.LockCenter     -- shift-lock style aiming
local delta = UIS:GetMouseDelta()                     -- per-frame mouse movement (when locked)
local lastType = UIS:GetLastInputType()               -- switch UI prompts on device change
```

## ContextActionService
```luau
local CAS = game:GetService("ContextActionService")
local function onBlock(_actionName: string, state: Enum.UserInputState, _input: InputObject)
	if state == Enum.UserInputState.Begin then Combat.blockStart()
	elseif state == Enum.UserInputState.End then Combat.blockEnd() end
	return Enum.ContextActionResult.Sink                -- consume (Pass lets lower bindings see it)
end
CAS:BindActionAtPriority("Block", onBlock, true, Enum.ContextActionPriority.High.Value,
	Enum.KeyCode.F, Enum.KeyCode.ButtonL1)             -- `true` creates a mobile button
-- CAS:UnbindAction("Block") when leaving combat mode
```

## Gotchas
- **Always** check `gameProcessedEvent` for gameplay keys. Otherwise typing "w" in chat moves or attacks.
- Input is **client-side**. Send *intent* to the server and validate there ([[Remote_Architecture_Patterns]], [[Server_Side_Validation]]).
- Under [[Server_Authority_Model|server authority]], don't feed UIS events into the core simulation. Use InputActions.
- Mobile buttons from CAS look generic, so restyle them or build custom UI ([[Cross_Platform_UI_Input]], [[Game_UI_Art_Direction]]).

## Related
[[Input_Action_System]] · [[Cross_Platform_UI_Input]] · [[Combo_Systems_and_Input_Buffering]] · [[Camera_System]] · [[Remote_Architecture_Patterns]] · [[Server_Side_Validation]] · [[Server_Authority_Model]] · [[Responsive_UI_and_Safe_Areas]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/input · https://create.roblox.com/docs/reference/engine/classes/ContextActionService
