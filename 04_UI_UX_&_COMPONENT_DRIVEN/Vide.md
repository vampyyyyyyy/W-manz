---
aliases: [Vide UI, centau vide, Solid-like Luau UI]
tags:
  - roblox-dev
  - ui/framework
type: framework
last_updated: 2026-10-27
status: complete
---
# Vide

> **TL;DR:** Vide (centau) is a **fine-grained reactive** UI library inspired by SolidJS. Sources (`source(0)`) are functions you call to read and call with a value to write, and properties bound to functions update automatically, without a virtual DOM or re-rendering components. It's fully Luau-typecheckable, concise and actively developed (Oct 2026). It's a strong choice when you want Fusion-level performance with a terser API.

## Sketch
```luau
local vide = require(Packages.vide)
local create, source, derive, spring = vide.create, vide.source, vide.derive, vide.spring

local function StaminaBar(stamina: () -> number)
	local width = spring(derive(function() return UDim2.fromScale(stamina() / 100, 1) end), 0.25)
	return create "Frame" {
		Size = UDim2.fromOffset(220, 10), BackgroundColor3 = Color3.fromRGB(30, 30, 36),
		create "Frame" { Size = width, BackgroundColor3 = Color3.fromRGB(90, 200, 120) },
	}
end

local stamina = source(100)
vide.mount(function() return create "ScreenGui" { ResetOnSpawn = false, StaminaBar(stamina) } end, playerGui)
stamina(42)   -- write: the bar animates
```
`spring(source, period = 1, dampingRatio = 1)` returns a new source that eases toward the input. `mount(component, target)` returns a destroy function, so call it on teardown.

## When to choose Vide
- HUD-heavy games with many fast-changing values (stamina, gas, cooldowns) ([[ODM_Gear_System]], [[Cooldown_and_Ability_UI]]).
- Teams that like Solid's mental model: components run once, reactivity is per-property.
- Pair with Charm for shared state across UI and gameplay ([[UI_State_Management]]).

## Related
[[Fusion]] · [[React_Lua]] · [[UI_State_Management]] · [[UI_Animation_and_Springs]] · [[Cooldown_and_Ability_UI]] · [[ODM_Gear_System]] · [[UI_Performance]] · [[UI_Labs]] · [[Wally]] · [[MOC_UI_UX_and_Components]]

## Sources
- https://github.com/centau/vide · https://centau.github.io/vide/
