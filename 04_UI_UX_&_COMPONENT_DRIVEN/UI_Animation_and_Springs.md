---
aliases: [UI tweens, UI springs, SmoothDamp, Reduced motion, UI juice]
tags:
  - roblox-dev
  - ui/animation
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# UI Animation & Springs

> **TL;DR:** Use **TweenService** for authored, fixed-length transitions (menus sliding in, fades). Use **springs** (Fusion `Spring`, Vide `spring`, or `TweenService:SmoothDamp`) for values that change unpredictably (HP bars, cursors, follow-cams), because springs retarget smoothly mid-motion. Animate `UIScale`, `CanvasGroup.GroupTransparency` and inner children rather than layout-owned properties, and **honor Reduce Motion** (`GuiService.ReducedMotionEnabled`).

## Recipes
```luau
-- Button press "pop" (doesn't fight layouts)
local scale = button:FindFirstChildOfClass("UIScale") :: UIScale
local pop = TweenService:Create(scale, TweenInfo.new(0.08, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), { Scale = 1.08 })
local back = TweenService:Create(scale, TweenInfo.new(0.12, Enum.EasingStyle.Back, Enum.EasingDirection.Out), { Scale = 1 })
button.Activated:Connect(function() pop:Play(); pop.Completed:Once(function() back:Play() end) end)

-- Spring a ghost HP bar with SmoothDamp (critically damped, retargetable)
local current, vel = 1, 0
RunService.PreRender:Connect(function(dt)
	local target = humanoid.Health / humanoid.MaxHealth
	current, vel = TweenService:SmoothDamp(current, target, vel, 0.25, nil, dt)
	ghost.Size = UDim2.fromScale(current, 1)
end)
```

## Timing guide (game UI)
| Interaction | Duration | Easing |
| --- | --- | --- |
| Hover/press feedback | 60–120 ms | Quad/Cubic Out |
| Panel open | 150–250 ms | Cubic/Quint Out (+ slight overshoot via Back) |
| Panel close | 100–180 ms | Quad In (faster than open) |
| Toasts/notifications | in 200 ms, hold, out 200 ms | Out / In |

## Accessibility & performance
- If `ReducedMotionEnabled`, replace slides and bounces with fades or instant changes (or use the `@ReducedMotionEnabledTrue` style query) ([[UI_Styling_StyleSheets]]). This also applies to [[Camera_Shake]].
- Don't tween `UIStroke.Thickness` on text. Don't tween properties a layout overrides ([[UI_Flex_and_List_Layouts]]).
- Disconnect per-frame springs when settled or hidden ([[Connection_Management]]).
- Many simultaneous tweens are fine. Thousands of per-frame property writes are not ([[UI_Performance]]).

## Related
[[TweenService]] · [[CanvasGroup]] · [[Fusion]] · [[Vide]] · [[UI_Styling_StyleSheets]] · [[Camera_Shake]] · [[UI_Flex_and_List_Layouts]] · [[Connection_Management]] · [[UI_Performance]] · [[RunService_Frame_Events]] · [[Custom_HUD_Design]] · [[MOC_UI_UX_and_Components]]

## Sources
- https://create.roblox.com/docs/ui/animation · https://create.roblox.com/docs/reference/engine/classes/TweenService#SmoothDamp · https://create.roblox.com/docs/reference/engine/classes/GuiService
