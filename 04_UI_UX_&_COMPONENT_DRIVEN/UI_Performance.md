---
aliases: [UI optimization, GUI lag, UI draw calls, Layout cost]
tags:
  - roblox-dev
  - ui/performance
type: concept
last_updated: 2026-10-27
status: complete
---
# UI Performance

> **TL;DR:** UI costs come from **layout recalculation** (layouts, AutomaticSize, flex, text reflow), **per-frame property writes** from scripts, **render cost** (overdraw from stacked transparent frames, many ViewportFrames, big CanvasGroups, hundreds of BillboardGuis) and **instance churn** (creating and destroying UI every update). Profile with the MicroProfiler (look at GUI/layout and script labels), then fix by updating only on change, pooling, virtualizing long lists and disabling hidden ScreenGuis.

## Checklist
1. **Event-driven updates.** Write a property when the data changes, not every frame ([[UI_State_Management]]).
2. **Per-frame only while animating.** Disconnect when settled ([[UI_Animation_and_Springs]], [[Connection_Management]]).
3. **Hide = `Enabled = false`** on ScreenGuis (or `Visible = false` on the root) so hidden trees don't render or relayout.
4. **Pool** rows, damage numbers and nameplates ([[Object_Pooling]], [[Damage_Numbers_and_Hit_Markers]]).
5. **Virtualize** long lists (leaderboards, inventories): render only visible rows ([[UI_Grid_and_Table_Layouts]]).
6. **Limit special renderers:** few live [[ViewportFrames]] (render static previews once), bounded [[CanvasGroup]] count and size.
7. **Text:** avoid `TextScaled` on hundreds of labels that change often. Prefer fixed sizes + `UITextSizeConstraint`. Rich text reflows on every change ([[Rich_Text]]).
8. **World UI:** `MaxDistance` on billboards, and cull off-screen ones ([[World_Space_UI]]).

## Measuring
- [[MicroProfiler]]: frame time spikes when opening menus point to layout or instance creation.
- [[Developer_Console]] memory: watch GUI and texture categories when CanvasGroups or ViewportFrames are involved ([[Memory_Categories]]).
- Test on the lowest-end target device, not your PC ([[Mobile_and_Low_End_Optimization]]).

## Related
[[MicroProfiler]] · [[Developer_Console]] · [[Memory_Categories]] · [[Object_Pooling]] · [[ViewportFrames]] · [[CanvasGroup]] · [[World_Space_UI]] · [[Rich_Text]] · [[UI_State_Management]] · [[Mobile_and_Low_End_Optimization]] · [[Rendering_Optimization]] · [[MOC_UI_UX_and_Components]]

## Sources
- https://create.roblox.com/docs/performance-optimization/improve · https://create.roblox.com/docs/ui/list-flex-layouts#flex-layouts
