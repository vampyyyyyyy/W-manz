---
aliases: [CanvasGroup, GroupTransparency, Fade whole panel, Flattened UI]
tags:
  - roblox-dev
  - ui/rendering
type: api
last_updated: 2026-10-27
status: complete
---
# CanvasGroup

> **TL;DR:** `CanvasGroup` renders its descendants into **one flattened texture**, then applies `GroupTransparency` and `GroupColor3` (and UICorner/UIGradient) to the *whole group*. That makes clean fades of entire panels possible without per-element transparency hacks. The costs: **extra texture memory** (capped by the client's QualityLevel; over the cap it renders **blank**), it always clips descendants, flattening only works with `ZIndexBehavior.Sibling`, and resizing re-allocates the texture.

## Panel fade
```luau
local group = shopPanel :: CanvasGroup
TweenService:Create(group, TweenInfo.new(0.18, Enum.EasingStyle.Quad), { GroupTransparency = 0 }):Play()
```
Without a CanvasGroup you'd tween Background/Text/Image/Stroke transparency on every child, and overlapping semi-transparent children would show seams.

## Use when / avoid when
| Use | Avoid |
| --- | --- |
| Fading menus, toasts, modal backdrops | Dozens of simultaneous groups (memory) |
| Rounded masks over complex content (UICorner on the group) | Constantly resizing groups (texture realloc each size) |
| Tinting a whole widget (`GroupColor3`) for disabled states | Huge full-screen groups on low-end mobile ([[Mobile_and_Low_End_Optimization]]) |

Respect **Reduce Motion**: swap long fades for instant toggles when `GuiService.ReducedMotionEnabled` is on ([[UI_Animation_and_Springs]]).

## Related
[[UI_Animation_and_Springs]] · [[TweenService]] · [[UI_Appearance_and_Size_Modifiers]] · [[UI_Performance]] · [[Mobile_and_Low_End_Optimization]] · [[Memory_Categories]] · [[Roblox_UI_Fundamentals]] · [[Game_UI_Art_Direction]] · [[MOC_UI_UX_and_Components]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/CanvasGroup · https://create.roblox.com/docs/ui/animation
