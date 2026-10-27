---
aliases: [Roblox UI, GUI basics, ScreenGui, PlayerGui, StarterGui]
tags:
  - roblox-dev
  - ui/fundamentals
type: concept
last_updated: 2026-10-27
status: complete
---
# Roblox UI Fundamentals

> **TL;DR:** UI lives in **containers**: `ScreenGui` (on-screen), `SurfaceGui` (on a part face) and `BillboardGui` (camera-facing in 3D). Containers hold `GuiObject`s (Frame, TextLabel, ImageButton, TextBox, ScrollingFrame, ViewportFrame, CanvasGroup…). On-screen UI is **client-owned**. `StarterGui` contents clone into each player's `PlayerGui`, so build, animate and read UI only in client code, and treat UI state as **untrusted** on the server.

## Core model
| Piece | Role |
| --- | --- |
| `StarterGui` | Template. `ScreenGui`s clone into `PlayerGui` when the character first spawns (or on `LoadCharacterAsync` if `CharacterAutoLoads` is off) |
| `ScreenGui.ResetOnSpawn` | `true` (default) re-clones on respawn. Set `false` for persistent HUDs so you don't rebuild state or leak connections ([[Connection_Management]]) |
| `ScreenGui.DisplayOrder` | Layering *between* ScreenGuis (modals above HUD) |
| `ZIndexBehavior = Sibling` | Default for new ScreenGuis. Required for [[CanvasGroup]] flattening |
| `ScreenGui.ScreenInsets` | Safe areas: `CoreUISafeInsets` (default; avoids top bar and notches) / `DeviceSafeInsets` / `TopbarSafeInsets` / `None` ([[Responsive_UI_and_Safe_Areas]]) |
| `StarterGui:SetCoreGuiEnabled(Enum.CoreGuiType.X, false)` | Hide default PlayerList/Health/Backpack/Chat/EmotesMenu/SelfView/Captures |

## Rules for production UI
1. **Client builds UI, server sends state.** Replicate data (attributes, remotes, a state library) and let the client render it ([[UI_State_Management]], [[Attributes]]).
2. **Never trust UI.** Exploiters can click any button, fire any remote and edit any label. Purchases, cooldowns and damage are validated server-side ([[Server_Side_Validation]], [[Server_Authoritative_Cooldowns]]).
3. **One owner per screen.** A component or framework ([[Fusion]], [[React_Lua]], [[Vide]]) owns its instance tree. Don't mix manual `Instance.new` edits into managed trees.
4. **Design for every input.** Touch, gamepad and mouse/keyboard ([[Cross_Platform_UI_Input]]).
5. **Budget it.** UI has a real CPU/GPU cost ([[UI_Performance]]).

## Related
[[Position_Size_and_AnchorPoint]] · [[UI_Flex_and_List_Layouts]] · [[UI_Appearance_and_Size_Modifiers]] · [[UI_Styling_StyleSheets]] · [[World_Space_UI]] · [[CanvasGroup]] · [[UI_State_Management]] · [[Responsive_UI_and_Safe_Areas]] · [[Cross_Platform_UI_Input]] · [[UI_Performance]] · [[Server_Side_Validation]] · [[Game_UI_Art_Direction]] · [[MOC_UI_UX_and_Components]]

## Sources
- https://create.roblox.com/docs/ui · https://create.roblox.com/docs/ui/on-screen-containers
