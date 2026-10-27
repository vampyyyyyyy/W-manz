---
aliases: [UI art direction, Game UI style, Avoid generic UI, UI design system]
tags:
  - roblox-dev
  - ui/design
type: concept
last_updated: 2026-10-27
status: complete
---
# Game UI Art Direction

> **TL;DR:** UI should look like it belongs to *your* game's world. Avoid the generic, default-looking look (identical rounded rectangles, flat gradients, emoji icons, default fonts). Pick a **visual concept** from the setting (military AOT-style leather and steel, anime ink brushwork, sci-fi holo), define a small **token set** (2–3 fonts, a constrained palette, corner and stroke rules, motion rules), and apply it consistently through StyleSheets and components.

## Build a UI identity
1. **Concept board.** Pull shapes and materials from the world: a sword-hilt motif for ability frames, map-paper textures for menus, ODM gas gauges as analog dials ([[ODM_Gear_System]]).
2. **Tokens.** Colors (base, surface, accent, danger, rarity tiers), fonts (display, UI, numbers), radii, stroke widths and shadows, as `StyleSheet` attributes ([[UI_Styling_StyleSheets]]).
3. **Shape language.** Angular cuts for aggressive combat games, soft pills for cozy games. Use 9-slice images for custom frames instead of only UICorner.
4. **Motion language.** Snappy for combat (60–120 ms), weighty for menus. One easing family across the game ([[UI_Animation_and_Springs]]).
5. **Hierarchy.** Size, contrast and placement do the work, and color supports it. Damage and danger always read first ([[Custom_HUD_Design]]).

## Common "AI-looking / generic" tells to avoid
- Every panel is a dark rounded rectangle with a 1 px white stroke and centered text.
- Rainbow gradients, emoji as icons, default Gotham/Arial everywhere.
- Too much on screen: everything is a button, nothing has priority.
- Inconsistent padding and alignment between screens.

## Diegetic & environmental UI
Put information in the world when it fits: an ammo counter on the weapon model, gas gauges on the ODM rig, a weather-reactive HUD that fogs and streaks during heavy rain while staying legible ([[World_Space_UI]], [[Rain_and_Precipitation]], [[VFX_Composition_and_Timing]]).

## Related
[[UI_Styling_StyleSheets]] · [[UI_Appearance_and_Size_Modifiers]] · [[UI_Animation_and_Springs]] · [[Custom_HUD_Design]] · [[World_Space_UI]] · [[ODM_Gear_System]] · [[Rain_and_Precipitation]] · [[VFX_Composition_and_Timing]] · [[Cross_Platform_UI_Input]] · [[UI_Labs]] · [[MOC_UI_UX_and_Components]]

## Sources
- https://create.roblox.com/docs/ui/styling · https://create.roblox.com/docs/ui/9-slice
