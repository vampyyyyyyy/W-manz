---
aliases: [Responsive UI, Safe area, ScreenInsets, Notch, ViewportDisplaySize, PreferredTextSize]
tags:
  - roblox-dev
  - ui/responsive
type: concept
last_updated: 2026-10-27
status: complete
---
# Responsive UI & Safe Areas

> **TL;DR:** Players run your UI on phones (notches, small screens), tablets, PCs, consoles (TV distance) and VR. Use `ScreenGui.ScreenInsets = CoreUISafeInsets` for interactive UI, `DeviceSafeInsets` / `None` only for decorative full-bleed art. Adapt with scale + constraints, `GuiService.ViewportDisplaySize` (Small/Medium/Large) or style queries, and respect `GuiService.PreferredTextSize` and `PreferredTransparency`. Test in Device Simulator.

## Toolkit
| Tool | Use |
| --- | --- |
| `ScreenInsets` (CoreUISafeInsets / DeviceSafeInsets / TopbarSafeInsets / None) | Keep buttons clear of the top bar, notches and cutouts |
| `GuiService.TopbarInset` | Rect of the top-bar area. Align custom top UI with it |
| `GuiService.ViewportDisplaySize` + `@ViewportDisplaySize*` queries | Switch layouts per class of screen ([[UI_Styling_StyleSheets]]) |
| `UISizeConstraint`, `UIAspectRatioConstraint`, `UIScale` | Bounds, proportions, global zoom ([[UI_Appearance_and_Size_Modifiers]]) |
| `AutomaticSize` | Localization-safe containers |
| `PreferredTextSize` (Medium → Largest) | Scale text for accessibility |
| `PreferredTransparency` | Players who want more opaque backgrounds get them |

```luau
-- Scale whole HUD by display class (fallback when not using StyleSheets)
local SCALE = { [Enum.DisplaySize.Small] = 0.8, [Enum.DisplaySize.Medium] = 1, [Enum.DisplaySize.Large] = 1.15 }
local function apply() hudScale.Scale = SCALE[GuiService.ViewportDisplaySize] or 1 end
GuiService:GetPropertyChangedSignal("ViewportDisplaySize"):Connect(apply); apply()
```

## Mobile specifics
- Keep the bottom corners (thumbstick, jump) clear, and anchor ability buttons *relative to the jump button*.
- Touch targets: at least ~44 px on the smallest supported phone. Don't rely on hover.
- Orientation changes and split-screen tablets fire size changes, so listen to `AbsoluteSize` changes.

## Related
[[Roblox_UI_Fundamentals]] · [[Position_Size_and_AnchorPoint]] · [[UI_Styling_StyleSheets]] · [[UI_Appearance_and_Size_Modifiers]] · [[Cross_Platform_UI_Input]] · [[Studio_Testing_Modes]] · [[Mobile_and_Low_End_Optimization]] · [[Custom_HUD_Design]] · [[Game_UI_Art_Direction]] · [[MOC_UI_UX_and_Components]]

## Sources
- https://create.roblox.com/docs/ui/on-screen-containers#screen-insets · https://create.roblox.com/docs/reference/engine/classes/GuiService · https://create.roblox.com/docs/ui/position-and-size#cross-platform-factors
