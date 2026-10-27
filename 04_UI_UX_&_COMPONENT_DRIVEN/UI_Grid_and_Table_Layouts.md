---
aliases: [UIGridLayout, UITableLayout, UIPageLayout, Inventory grid, ScrollingFrame]
tags:
  - roblox-dev
  - ui/layout
type: api
last_updated: 2026-10-27
status: complete
---
# UI Grid, Table & Page Layouts

> **TL;DR:** `UIGridLayout` puts siblings into **uniform cells** (`CellSize`, `CellPadding`, `FillDirection`, `FillDirectionMaxCells`), which is perfect for inventories and shops. `UITableLayout` makes rows of rows (like HTML tables), with cell size taken from the children unless `FillEmptySpaceColumns`/`Rows` is set. `UIPageLayout` turns siblings into swipeable or scriptable **pages**. Pair grids with a `ScrollingFrame` using `AutomaticCanvasSize`.

## Inventory grid
```luau
local grid = Instance.new("UIGridLayout")
grid.CellSize = UDim2.fromOffset(84, 84)
grid.CellPadding = UDim2.fromOffset(8, 8)
grid.SortOrder = Enum.SortOrder.LayoutOrder
grid.Parent = scrollingFrame

scrollingFrame.AutomaticCanvasSize = Enum.AutomaticSize.Y  -- canvas grows with items
scrollingFrame.CanvasSize = UDim2.new()                    -- let automatic sizing drive it
```
- Square cells that scale: use scale `CellSize` plus a `UIAspectRatioConstraint` on the cells ([[UI_Appearance_and_Size_Modifiers]]).
- Constraints on cells are respected (a `MinSize` larger than the cell wins).
- Big inventories: render only visible rows (virtualize) and reuse cell instances ([[Object_Pooling]], [[UI_Performance]]).

## Data flow
The server owns the inventory ([[Inventory_Systems]]). The client renders slots from replicated state and sends **intent** ("equip slot 12"), which the server validates ([[Server_Side_Validation]]). Item previews can use [[ViewportFrames]].

## Related
[[UI_Flex_and_List_Layouts]] · [[Position_Size_and_AnchorPoint]] · [[UI_Appearance_and_Size_Modifiers]] · [[Inventory_Systems]] · [[ViewportFrames]] · [[Object_Pooling]] · [[UI_Performance]] · [[Server_Side_Validation]] · [[UI_State_Management]] · [[MOC_UI_UX_and_Components]]

## Sources
- https://create.roblox.com/docs/ui/grid-table-layouts · https://create.roblox.com/docs/ui/page-layouts · https://create.roblox.com/docs/ui/scrolling-frames
