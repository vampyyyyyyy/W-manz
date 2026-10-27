---
aliases: [Cooldown UI, Ability bar, Radial cooldown, Skill icons, Ability slots]
tags:
  - roblox-dev
  - ui/combat-feedback
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Cooldown & Ability UI

> **TL;DR:** The **server owns cooldowns**. It replicates an *end timestamp* (`workspace:GetServerTimeNow()` + duration), and the client renders the remaining time locally each frame. That gives smooth sweeps with zero per-frame networking, and the UI is always reconcilable. Show a radial or vertical sweep, a number under ~10 s, a "ready" flash, and input-glyph hints per platform.

## Data contract
```luau
-- Server (after validating the cast)
player:SetAttribute("CD_Dash", workspace:GetServerTimeNow() + 4.0)

-- Client widget
local function remaining(): number
	local ends = player:GetAttribute("CD_Dash") or 0
	return math.max(0, ends - workspace:GetServerTimeNow())
end
```
See [[Server_Authoritative_Cooldowns]] for the authoritative side and [[Attributes]] for replication.

## Radial sweep with a conical gradient (beta "Upgraded UIGradients")
```luau
local EPS = 1e-3
local function setFill(gradient: UIGradient, frac: number) -- frac 0..1 = portion still cooling
	local f = math.clamp(frac, EPS, 1 - 2 * EPS)
	gradient.Type = Enum.GradientType.Conical
	gradient.Transparency = NumberSequence.new({
		NumberSequenceKeypoint.new(0, 0.35), NumberSequenceKeypoint.new(f, 0.35),
		NumberSequenceKeypoint.new(f + EPS, 1), NumberSequenceKeypoint.new(1, 1),
	})
end
```
Without the beta, use the classic **two half-circle masks** technique, or a vertical fill (Frame anchored at the bottom, `Size.Y` = fraction).

## UX checklist
- **Prediction:** start the sweep on input for responsiveness. If the server rejects the cast, snap back and play a "denied" cue ([[Client_Prediction_and_Reconciliation]]).
- **Charges:** show a pip count plus a recharge sweep for the next charge.
- **Buffered input:** pressing during the last ~150 ms queues the cast. Show it ([[Combo_Systems_and_Input_Buffering]]).
- **Glyphs:** swap key labels (Q/E ↔ LB/RB ↔ touch buttons) on `UserInputService.PreferredInput` changes ([[Cross_Platform_UI_Input]]).
- Run the per-frame update only while any cooldown is active ([[UI_Performance]]).

## Related
[[Server_Authoritative_Cooldowns]] · [[Attributes]] · [[Client_Prediction_and_Reconciliation]] · [[Combo_Systems_and_Input_Buffering]] · [[Cross_Platform_UI_Input]] · [[UI_Appearance_and_Size_Modifiers]] · [[Custom_HUD_Design]] · [[UI_Performance]] · [[Fusion]] · [[Custom_Movement_Abilities]] · [[MOC_UI_UX_and_Components]]

## Sources
- https://create.roblox.com/docs/ui/appearance-modifiers#gradient · https://create.roblox.com/docs/reference/engine/classes/Workspace#GetServerTimeNow
