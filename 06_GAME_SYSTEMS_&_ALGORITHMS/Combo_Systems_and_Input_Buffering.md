---
aliases: [Combos, Input buffer, Combo strings, Attack chains, Cancel windows]
tags:
  - roblox-dev
  - systems/combat
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Combo Systems & Input Buffering

> **TL;DR:** Responsive combat needs an **input buffer**: remember the last input for a short window (~120–200 ms) and fire it at the first legal moment (end of recovery or a cancel window). Without one, players feel "dropped inputs". **Combos** are data: a graph of `attack → allowed next attacks` with a **combo window** and a **reset timeout**. The server validates the chain ([[Combat_State_Machine]]).

## Buffer
```luau
--!strict
local BUFFER_TIME = 0.15
type Buffered = { action: string, t: number }
local buffered: Buffered? = nil

local function press(action: string)
	buffered = { action = action, t = os.clock() }
end

-- called every frame by the combat controller
local function consume(canDo: (string) -> boolean): string?
	local b = buffered
	if not b then return nil end
	if os.clock() - b.t > BUFFER_TIME then buffered = nil return nil end
	if canDo(b.action) then buffered = nil return b.action end
	return nil
end
```
Wire `press` to the [[Input_Action_System]] (`Pressed`) or `UserInputService.InputBegan` (respect `gameProcessedEvent`) ([[UserInputService_and_ContextActionService]]).

## Combo strings as data
```luau
const COMBOS = table.freeze({
	Light1 = { next = { Light = "Light2", Heavy = "Launcher" }, window = 0.35 },
	Light2 = { next = { Light = "Light3" }, window = 0.35 },
	Light3 = { next = {}, window = 0 },                  -- finisher: longer recovery, knockback
	Launcher = { next = { Light = "AirLight1" }, window = 0.30 },
})
-- comboIndex resets if no follow-up within `window` after recovery begins (or on getting hit)
```

## Design levers (game feel)
- **Buffer window:** 0.1–0.2 s. Longer feels "laggy-responsive", shorter feels "eats inputs".
- **Cancel windows:** dash-cancel from recovery for mobility combat ([[Custom_Movement_Abilities]]), and jump-cancels for air combos.
- **Hitstop** extends windows by the freeze time so combos don't break on heavy hits ([[Hitstop_and_Impact_Feel]]).
- **Combo-breakers / bursts:** let victims escape long strings (a resource-gated burst with i-frames) ([[Block_Parry_and_IFrames]]).
- **Diminishing stun:** reduce stun per hit in a string to stop infinites ([[Status_Effects]]).

## Server-side
The server only tracks `lastAttackId`, `comboIndex` and timestamps. It accepts `Attack(nextId)` only if `nextId ∈ COMBOS[last].next` within the window (+ latency slack). Never trust a client-reported combo index.

## Related
[[Combat_State_Machine]] · [[Combat_System_Architecture]] · [[Input_Action_System]] · [[UserInputService_and_ContextActionService]] · [[Hitstop_and_Impact_Feel]] · [[Block_Parry_and_IFrames]] · [[Status_Effects]] · [[Const_Bindings]] · [[Animation_Events_and_Markers]] · [[MOC_Combat_Systems]]

## Sources
- Fighting-game design conventions; Roblox input APIs per https://create.roblox.com/docs/input
