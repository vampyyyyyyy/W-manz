---
aliases: [UDim2, Scale vs Offset, AnchorPoint, ZIndex, AbsoluteSize]
tags:
  - roblox-dev
  - ui/layout
type: concept
last_updated: 2026-10-27
status: complete
---
# Position, Size & AnchorPoint

> **TL;DR:** `Position` and `Size` are `UDim2`s = **Scale** (fraction of the parent) + **Offset** (pixels), added together per axis. `AnchorPoint` (0–1 per axis) is the object's origin, so `(0.5, 0.5)` + `Position = UDim2.fromScale(0.5, 0.5)` centers it. `ZIndex` orders siblings. Read `AbsolutePosition`/`AbsoluteSize` for real pixels. Mix scale for layout with offset or constraints for touch targets and borders.

## Patterns
```luau
-- Centered panel that scales with screen but never gets tiny or huge
panel.AnchorPoint = Vector2.new(0.5, 0.5)
panel.Position = UDim2.fromScale(0.5, 0.5)
panel.Size = UDim2.fromScale(0.4, 0.5)
local c = Instance.new("UISizeConstraint")
c.MinSize, c.MaxSize = Vector2.new(320, 240), Vector2.new(720, 540)
c.Parent = panel

-- Health bar fill: scale on X only, anchored left
fill.AnchorPoint = Vector2.new(0, 0.5)
fill.Position = UDim2.fromScale(0, 0.5)
fill.Size = UDim2.fromScale(hp / maxHp, 1)
```

## Gotchas
- Pure **offset** UI breaks across resolutions. Pure **scale** UI stretches text and icons. Use scale + [[UI_Appearance_and_Size_Modifiers|UIAspectRatioConstraint / UISizeConstraint]].
- AnchorPoint also controls the **growth direction** for `AutomaticSize` and size tweens ([[UI_Animation_and_Springs]]).
- Under a layout ([[UI_Flex_and_List_Layouts]], [[UI_Grid_and_Table_Layouts]]), the layout owns Position (and often Size). Setting them manually does nothing.
- Mobile **reserved zones** (thumbstick and jump, bottom corners) and **thumb reach** differ between phones and tablets. Place custom buttons *relative to the jump button* ([[Responsive_UI_and_Safe_Areas]]).
- `ZIndex` only orders within a container. `DisplayOrder` orders ScreenGuis ([[Roblox_UI_Fundamentals]]).

## Related
[[Roblox_UI_Fundamentals]] · [[UI_Flex_and_List_Layouts]] · [[UI_Grid_and_Table_Layouts]] · [[UI_Appearance_and_Size_Modifiers]] · [[UI_Animation_and_Springs]] · [[Responsive_UI_and_Safe_Areas]] · [[Custom_HUD_Design]] · [[Cooldown_and_Ability_UI]] · [[MOC_UI_UX_and_Components]]

## Sources
- https://create.roblox.com/docs/ui/position-and-size
