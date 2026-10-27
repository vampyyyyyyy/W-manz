---
aliases: [UI MOC, UI hub, Interface hub]
tags:
  - roblox-dev
  - moc/ui
type: moc
last_updated: 2026-10-27
status: complete
---
# MOC: UI/UX & Component-Driven UI

> **TL;DR:** Building **game UI that looks intentional and runs well**: layout and sizing primitives, modifiers and engine StyleSheets, 3D and world-space UI, declarative frameworks (Fusion, React Lua, Vide), state management, HUD and combat feedback, animation, cross-platform input, responsiveness and performance. Client renders, server decides.

*25 notes in this domain.*

## Start here
1. [[Roblox_UI_Fundamentals]]: containers, PlayerGui, and client ownership
2. [[Position_Size_and_AnchorPoint]]: UDim2 scale vs offset, anchors
3. [[UI_Styling_StyleSheets]]: engine-level CSS: tokens, themes, queries
4. [[Fusion]]: reactive UI with explicit cleanup scopes
5. [[Custom_HUD_Design]]: what a combat HUD should show, and where
6. [[Game_UI_Art_Direction]]: avoiding the generic AI-made look

## Layout & visuals
- **Foundations:** [[Roblox_UI_Fundamentals]] · [[Position_Size_and_AnchorPoint]] · [[UI_Flex_and_List_Layouts]] · [[UI_Grid_and_Table_Layouts]]
- **Look:** [[UI_Appearance_and_Size_Modifiers]] · [[UI_Styling_StyleSheets]] · [[Rich_Text]] · [[Game_UI_Art_Direction]]
- **Special renderers:** [[ViewportFrames]] · [[CanvasGroup]] · [[World_Space_UI]] · [[Loading_Screens_and_ReplicatedFirst]]

## Frameworks & architecture
- **Libraries:** [[Fusion]] · [[React_Lua]] · [[Vide]] · [[Roact_Legacy]]
- **State & tooling:** [[UI_State_Management]] · [[UI_Labs]]

## Game UI patterns
- **Combat feedback:** [[Custom_HUD_Design]] · [[Damage_Numbers_and_Hit_Markers]] · [[Cooldown_and_Ability_UI]]
- **Motion:** [[UI_Animation_and_Springs]]

## Platforms & performance
- **Reach:** [[Responsive_UI_and_Safe_Areas]] · [[Cross_Platform_UI_Input]]
- **Cost:** [[UI_Performance]]

## Cross-domain
[[Home]] · [[Learning_Path]] · [[MOC_Combat_Systems]] · [[MOC_Performance_and_Profiling]] · [[MOC_Frameworks_Toolchain_and_DevOps]] · [[MOC_Engine_and_DataModel]]

## Sources
- Each linked note cites its own primary sources. See [[Trusted_Sources]] for the ranking policy.
