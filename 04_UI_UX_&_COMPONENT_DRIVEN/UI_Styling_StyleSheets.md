---
aliases: [StyleSheet, StyleRule, StyleLink, Style tokens, Themes, StyleQuery, Universal styling, Style Editor]
tags:
  - roblox-dev
  - ui/styling
type: api
last_updated: 2026-10-27
status: complete
---
# UI Styling (StyleSheets, Tokens, Themes, Queries)

> **TL;DR:** Roblox has **engine-level, CSS-like styling**. A `StyleSheet` holds `StyleRule`s with selectors (class `Frame`, tag `.ButtonPrimary`, name `#Title`, pseudo-instance `::UICorner`, state `:Hover`, query `@WideContainer`). `StyleLink` attaches **one** sheet to a ScreenGui tree. **Tokens** are sheet attributes referenced as `"$Token"`, **themes** are swappable token sheets (via `StyleDerive`), and **StyleQuery** gives container/media queries (size, aspect ratio, input type, reduced motion, display size). `SetPropertyTransitions` adds CSS-style transitions. Use it instead of per-instance styling code.

## Minimal setup
```luau
local sheet = Instance.new("StyleSheet")
sheet:SetAttribute("Accent", Color3.fromHex("E8A33D"))        -- token
sheet:SetAttribute("Radius", UDim.new(0, 10))

local button = Instance.new("StyleRule")
button.Selector = "TextButton.Primary"                         -- class + tag
button:SetProperties({ BackgroundColor3 = "$Accent", AutoButtonColor = false })
button:SetPropertyTransitions({
	BackgroundColor3 = TweenInfo.new(0.12, Enum.EasingStyle.Quad, Enum.EasingDirection.Out),
})
button.Parent = sheet

local corner = Instance.new("StyleRule")
corner.Selector = "TextButton.Primary::UICorner"               -- phantom UICorner
corner:SetProperty("CornerRadius", "$Radius")
corner.Parent = sheet

local hover = Instance.new("StyleRule")
hover.Selector = "TextButton.Primary:Hover"                    -- GuiState selector
hover:SetProperty("BackgroundColor3", Color3.fromHex("FFC266"))
hover.Parent = sheet

local link = Instance.new("StyleLink")
link.StyleSheet = sheet
link.Parent = hudScreenGui
```
Tag buttons with `CollectionService:AddTag(btn, "Primary")` ([[CollectionService_Tags]]).

## Queries
- **Custom:** a `::StyleQuery #Wide` rule with `MinSize`/`MaxSize`/`AspectRatioRange`/`PreferredInputType`/`ReduceMotionEnabled`/`ViewportDisplaySize`, then `@Wide Frame > TextButton` rules.
- **Built-in:** `@ViewportDisplaySizeSmall|Medium|Large`, `@PreferredInputTouch|Gamepad|KeyboardAndMouse`, `@ReducedMotionEnabledTrue|False`, `@PreferredTextSize…`. These are responsive and accessible UI with zero scripts ([[Responsive_UI_and_Safe_Areas]], [[Cross_Platform_UI_Input]]).

## Architecture tips
- **Tokens → theme → design sheet** layering (StyleDerive) mirrors design-system tokens. Swap themes for seasonal events or team colors.
- Selectors support child (`>`) and descendant combinators, plus nesting and merging rules.
- The Studio **Style Editor** is a visual front-end over the same instances, so designers and scripters share one source of truth.
- Frameworks still own *structure and state*. StyleSheets own *appearance*. Don't set the same property both ways ([[Fusion]], [[React_Lua]]).

## Related
[[UI_Appearance_and_Size_Modifiers]] · [[CollectionService_Tags]] · [[Attributes]] · [[Responsive_UI_and_Safe_Areas]] · [[Cross_Platform_UI_Input]] · [[Game_UI_Art_Direction]] · [[Fusion]] · [[React_Lua]] · [[UI_Animation_and_Springs]] · [[TweenService]] · [[MOC_UI_UX_and_Components]]

## Sources
- https://create.roblox.com/docs/ui/styling · https://create.roblox.com/docs/ui/styling/css-comparisons · https://create.roblox.com/docs/ui/styling/editor
