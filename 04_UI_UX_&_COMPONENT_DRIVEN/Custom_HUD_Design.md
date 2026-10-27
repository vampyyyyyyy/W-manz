---
aliases: [HUD, Heads-up display, Combat HUD, Health bar, Stamina bar]
tags:
  - roblox-dev
  - ui/hud
type: architecture
last_updated: 2026-10-27
status: complete
---
# Custom HUD Design

> **TL;DR:** A good game HUD shows **only what the player needs right now**, where their eyes already are, with feedback that matches game feel. Build it as small, independent components (health, stamina/gas, abilities, objectives, ammo) that read from a client state mirror. Keep them in a `ResetOnSpawn = false` ScreenGui, respect safe areas and thumb zones, and animate *changes* rather than idling.

## Layout zones (16:9 baseline)
| Zone | Typical content |
| --- | --- |
| Bottom-center | Abilities/cooldowns, combo meter ([[Cooldown_and_Ability_UI]]) |
| Bottom-left | HP/stamina/ODM gas bars (clear of the mobile thumbstick) |
| Top-center | Objective, round timer, boss bar |
| Center | Crosshair + hit markers only ([[Damage_Numbers_and_Hit_Markers]]) |
| Top-right | Minimap/compass (avoid core top-bar buttons via `ScreenInsets`) ([[Responsive_UI_and_Safe_Areas]]) |

## Feel techniques
- **Delayed damage chunk:** the HP bar drops instantly, and a lighter "ghost" bar trails behind (spring or tween), so big hits *read* as big ([[Hitstop_and_Impact_Feel]]).
- **State color, not just numbers:** low stamina pulses, and gas turns amber at 25% ([[ODM_Gear_System]]).
- **Context visibility:** hide ammo out of combat, and show interaction prompts only near targets (ProximityPrompt).
- **Weather/legibility:** add stroke/shadow and semi-opaque plates so bars read during rain, snow and night ([[Weather_System_Architecture]], [[UI_Appearance_and_Size_Modifiers]]).

## Engineering
- Each widget subscribes to *its* values only (attributes, signals). No global per-frame refresh ([[UI_State_Management]], [[UI_Performance]]).
- Per-frame visuals (cooldown sweeps) update only while active, then disconnect.
- Server-authoritative numbers. The client may *predict* (e.g., stamina drain) but snaps to server values ([[Client_Prediction_and_Reconciliation]]).

## Related
[[Cooldown_and_Ability_UI]] · [[Damage_Numbers_and_Hit_Markers]] · [[UI_State_Management]] · [[Responsive_UI_and_Safe_Areas]] · [[UI_Animation_and_Springs]] · [[Game_UI_Art_Direction]] · [[ODM_Gear_System]] · [[Hitstop_and_Impact_Feel]] · [[Weather_System_Architecture]] · [[UI_Performance]] · [[Combat_System_Architecture]] · [[MOC_UI_UX_and_Components]]

## Sources
- https://create.roblox.com/docs/ui/position-and-size#cross-platform-factors · https://create.roblox.com/docs/ui/on-screen-containers
