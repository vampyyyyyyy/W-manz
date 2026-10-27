---
aliases: [UIListLayout, Flex layout, UIFlexItem, HorizontalFlex, ItemLineAlignment]
tags:
  - roblox-dev
  - ui/layout
type: api
last_updated: 2026-10-27
status: complete
---
# UI List & Flex Layouts

> **TL;DR:** `UIListLayout` arranges siblings in a row or column (`FillDirection`, `SortOrder` = LayoutOrder or Name, `Padding`, `Wraps`). Its **flex** features (`HorizontalFlex`/`VerticalFlex`, `ItemLineAlignment`, and per-item `UIFlexItem` with `FlexMode` Fill/Grow/Shrink/Custom) give you CSS-flexbox-like responsive bars, tab strips and toolbars without manual math. Flex costs a bit more, so use it with purpose.

## Recipes
```luau
-- Tab bar: tabs share width equally regardless of count
local list = Instance.new("UIListLayout")
list.FillDirection = Enum.FillDirection.Horizontal
list.HorizontalFlex = Enum.UIFlexAlignment.Fill
list.Padding = UDim.new(0, 6)
list.SortOrder = Enum.SortOrder.LayoutOrder
list.Parent = tabBar

-- Slider row: fixed labels, track flexes to fill the rest
local flex = Instance.new("UIFlexItem")
flex.FlexMode = Enum.UIFlexMode.Fill
flex.Parent = sliderTrack
```
- Reverse order by negating `LayoutOrder` values.
- `Padding` is *between* items. Use `UIPadding` on the parent for outer margins ([[UI_Appearance_and_Size_Modifiers]]).
- `Wraps = true` turns a row into a wrapping toolbar or tag cloud.
- Prefer [[UI_Grid_and_Table_Layouts|UIGridLayout]] when cells must align strictly on both axes (inventory grids).

## Gotchas
- The layout **overrides** child Position/Rotation/Size, so animate an inner child instead, or use `UIScale` ([[UI_Animation_and_Springs]]).
- Size constraints on children win over the layout ([[Position_Size_and_AnchorPoint]]).
- Adding or removing many items per frame forces relayout. Batch updates or pool items ([[UI_Performance]], [[Object_Pooling]]).

## Related
[[UI_Grid_and_Table_Layouts]] · [[Position_Size_and_AnchorPoint]] · [[UI_Appearance_and_Size_Modifiers]] · [[UI_Animation_and_Springs]] · [[UI_Performance]] · [[Object_Pooling]] · [[Custom_HUD_Design]] · [[Responsive_UI_and_Safe_Areas]] · [[UI_Styling_StyleSheets]] · [[MOC_UI_UX_and_Components]]

## Sources
- https://create.roblox.com/docs/ui/list-flex-layouts
