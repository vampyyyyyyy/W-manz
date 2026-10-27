---
aliases: [Fusion UI, dphfox Fusion, Elttob Fusion, Fusion 0.3, scoped Fusion]
tags:
  - roblox-dev
  - ui/framework
type: framework
last_updated: 2026-10-27
status: complete
---
# Fusion

> **TL;DR:** Fusion (dphfox/Elttob) is a **reactive state + declarative instance** library. State objects (`Value`, `Computed`, `ForValues`/`ForPairs`/`ForKeys`, `Observer`, `Spring`, `Tween`) drive properties of instances created with `New`/`Hydrate`. Since 0.3, every object belongs to a **scope** (`scope:Value(...)`, `Fusion.doCleanup(scope)`), which makes cleanup explicit and leak-resistant. It's lighter-weight than React (no virtual DOM) and very popular for game UI.

## Component sketch (0.3 scoped API)
```luau
local Fusion = require(ReplicatedStorage.Packages.Fusion)
local Children, OnEvent, peek = Fusion.Children, Fusion.OnEvent, Fusion.peek
type UsedAs<T> = Fusion.UsedAs<T>

local function CooldownButton(scope: Fusion.Scope, props: {
	Remaining: UsedAs<number>, Duration: number, Icon: string, OnPress: () -> (),
})
	local ratio = scope:Computed(function(use) return math.clamp(use(props.Remaining) / props.Duration, 0, 1) end)
	return scope:New "ImageButton" {
		Size = UDim2.fromOffset(72, 72), Image = props.Icon,
		[OnEvent "Activated"] = function() if peek(props.Remaining) <= 0 then props.OnPress() end end,
		[Children] = scope:New "Frame" {
			BackgroundTransparency = 0.4, AnchorPoint = Vector2.new(0, 1), Position = UDim2.fromScale(0, 1),
			Size = scope:Spring(scope:Computed(function(use) return UDim2.fromScale(1, use(ratio)) end), 30),
		},
	}
end

local scope = Fusion.scoped(Fusion)       -- scope with Fusion's constructors as methods
local remaining = scope:Value(0)
CooldownButton(scope, { Remaining = remaining, Duration = 5, Icon = "rbxassetid://0", OnPress = useAbility })
-- later: Fusion.doCleanup(scope)
```

## Practices
- `use(...)` inside Computed tracks dependencies. `peek(...)` reads without tracking (event handlers).
- Feed server state in via Values updated from remotes or attributes. The UI never decides outcomes ([[Server_Authoritative_Cooldowns]], [[UI_State_Management]]).
- Springs are great for HUD feel (bars, popups), but gate them on Reduce Motion ([[UI_Animation_and_Springs]]).
- Install: GitHub release `.rbxm` or Wally ([[Wally]]). Pin the version, since 0.2 → 0.3 was a breaking API change.

## Related
[[React_Lua]] · [[Vide]] · [[UI_State_Management]] · [[UI_Animation_and_Springs]] · [[Cooldown_and_Ability_UI]] · [[Server_Authoritative_Cooldowns]] · [[Cleanup_Libraries_Trove_Maid_Janitor]] · [[Memory_Leaks]] · [[UI_Labs]] · [[Wally]] · [[Roblox_TS]] · [[MOC_UI_UX_and_Components]]

## Sources
- https://github.com/dphfox/Fusion · https://elttob.uk/Fusion/latest
