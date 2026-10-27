---
aliases: [UIStroke, UICorner, UIGradient, UIShadow, UIPadding, UIScale, UISizeConstraint, UIAspectRatioConstraint, AutomaticSize]
tags:
  - roblox-dev
  - ui/modifiers
type: api
last_updated: 2026-10-27
status: complete
---
# UI Appearance & Size Modifiers

> **TL;DR:** You build look-and-feel by parenting **modifier instances** to a GuiObject. Appearance: `UIStroke`, `UICorner`, `UIGradient`, `UIPadding`, `UIShadow`. Size: `UIScale`, `AutomaticSize`, `UISizeConstraint`, `UITextSizeConstraint`, `UIAspectRatioConstraint`. Constraints **override** layouts. As of Oct 2026, gradients gained Radial/Elliptical/Conical types, Scale and TileMode (beta "Upgraded UIGradients"), and `UIShadow` adds real drop and inset shadows (some features in beta "Upgraded UIShadows").

## Appearance
| Modifier | Key properties | Notes |
| --- | --- | --- |
| `UIStroke` | `Thickness`, `Color`, `Transparency`, `ApplyStrokeMode` (Contextual/Border), `BorderStrokePosition` (Center/Inner/Outer), `BorderOffset`, `StrokeSizingMode` (fixed/scaled), `LineJoinMode`, `ZIndex` | On text it's an outline, on frames a border. **Don't tween `Thickness` on text** (glyph cache churn and flicker) |
| `UICorner` | `CornerRadius`, plus per-corner `TopLeftRadius`… | Scale 0.5 = pill on the shortest edge |
| `UIGradient` | `Color` (ColorSequence), `Transparency` (NumberSequence), `Rotation`, `Offset`, `Type`, `Scale`, `TileMode` | Animate `Offset`/`Rotation` for shimmer and loading bars. Can be a child of a `UIStroke` for gradient borders |
| `UIPadding` | `PaddingTop/Bottom/Left/Right` | Inner margins (list `Padding` is *between* items) |
| `UIShadow` | `Mode` (Shape/Text), `BlurRadius`, `Offset`, `Spread`, `Inset`, `ShowBehindParent`, `ZIndex` | Follows UICorner and rotation. No Path2D or textures |

## Size
- `UIScale.Scale` multiplies the whole subtree, strokes included. Great for "pop" animations without fighting layouts ([[UI_Animation_and_Springs]]).
- `AutomaticSize` (X/Y/XY) grows to fit content, and `Size` becomes the **minimum**. ScrollingFrames use `AutomaticCanvasSize`. Essential for localization.
- `UISizeConstraint` (Min/Max px), `UITextSizeConstraint` (keep `MinTextSize` ≥ 9 for readability), `UIAspectRatioConstraint` (square icons, avatar thumbnails).

## Style at scale
Don't hand-place 300 UICorners. Declare them once with [[UI_Styling_StyleSheets|StyleSheets]] (`::UICorner` pseudo-instances) or bake them into components ([[Fusion]], [[React_Lua]]).

## Related
[[Position_Size_and_AnchorPoint]] · [[UI_Flex_and_List_Layouts]] · [[UI_Styling_StyleSheets]] · [[UI_Animation_and_Springs]] · [[CanvasGroup]] · [[Rich_Text]] · [[Game_UI_Art_Direction]] · [[UI_Performance]] · [[Fusion]] · [[React_Lua]] · [[MOC_UI_UX_and_Components]]

## Sources
- https://create.roblox.com/docs/ui/appearance-modifiers · https://create.roblox.com/docs/ui/size-modifiers
