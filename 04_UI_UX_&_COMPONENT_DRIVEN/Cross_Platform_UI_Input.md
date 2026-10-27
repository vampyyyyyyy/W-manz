---
aliases: [Gamepad UI, Controller navigation, PreferredInput, Touch buttons, UI selection]
tags:
  - roblox-dev
  - ui/input
type: concept
last_updated: 2026-10-27
status: complete
---
# Cross-Platform UI Input

> **TL;DR:** Design every screen for **mouse/keyboard, touch and gamepad** from day one. Read `UserInputService.PreferredInput` (KeyboardAndMouse / Touch / Gamepad…) and swap glyphs and layouts when it changes. Make menus **gamepad-navigable** (`Selectable`, `NextSelection*`, `GuiService.SelectedObject`, `SelectionImageObject`). Bind gameplay actions with the **Input Action System**, where `InputBinding.UIButton` lets a touch button drive the same action as a key.

## Glyph swapping
```luau
local function refresh()
	local input = UserInputService.PreferredInput
	if input == Enum.PreferredInput.Gamepad then
		hintIcon.Image = UserInputService:GetImageForKeyCode(Enum.KeyCode.ButtonL1) -- platform-correct glyph
		hintIcon.Visible, hintText.Visible = true, false
	elseif input == Enum.PreferredInput.Touch then
		hintIcon.Visible, hintText.Visible = false, false  -- the on-screen button is the hint
	else
		hintText.Text = UserInputService:GetStringForKeyCode(Enum.KeyCode.Q) -- respects keyboard layout
		hintIcon.Visible, hintText.Visible = false, true
	end
end
UserInputService:GetPropertyChangedSignal("PreferredInput"):Connect(refresh)
refresh()
```

## Gamepad navigation
- Set `GuiService.SelectedObject` when a menu opens, and restore the previous selection when it closes.
- Define `NextSelectionUp/Down/Left/Right` where the automatic guess is wrong. Use a custom `SelectionImageObject` that matches your art style ([[Game_UI_Art_Direction]]).
- Never trap selection. **B/Back** always closes the top modal.

## Touch
- `InputBinding.UIButton` (Input Action System) or ContextActionService touch buttons ([[Input_Action_System]], [[UserInputService_and_ContextActionService]]).
- Hold-to-confirm for destructive or purchase actions, since accidental taps happen ([[MarketplaceService]]).

## Related
[[Input_Action_System]] · [[UserInputService_and_ContextActionService]] · [[Responsive_UI_and_Safe_Areas]] · [[Cooldown_and_Ability_UI]] · [[Combo_Systems_and_Input_Buffering]] · [[Game_UI_Art_Direction]] · [[UI_Styling_StyleSheets]] · [[MarketplaceService]] · [[Studio_Testing_Modes]] · [[MOC_UI_UX_and_Components]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/UserInputService#PreferredInput · https://create.roblox.com/docs/reference/engine/classes/InputBinding · https://create.roblox.com/docs/reference/engine/classes/GuiService
