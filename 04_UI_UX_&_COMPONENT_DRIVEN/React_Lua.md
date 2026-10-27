---
aliases: [React Lua, react-lua, jsdotlua React, ReactRoblox, React hooks Roblox]
tags:
  - roblox-dev
  - ui/framework
type: framework
last_updated: 2026-10-27
status: complete
---
# React Lua

> **TL;DR:** React Lua is a faithful **Luau translation of ReactJS 17**: function components, hooks (`useState`, `useEffect`, `useMemo`, `useRef`, `useContext`, `useReducer`) and context, plus Roact-era **bindings** (`useBinding`) for cheap per-frame updates. Roblox uses it internally for its own app UI. The community fork **jsdotlua/react-lua** is the go-to distribution (Roblox's repo is a read-only mirror). Mount with `ReactRoblox.createRoot(container):render(element)`.

## Sketch
```luau
local React = require(Packages.React)
local ReactRoblox = require(Packages.ReactRoblox)
local e = React.createElement

local function HealthBar(props: { hp: number, maxHp: number })
	local fill = props.hp / props.maxHp
	return e("Frame", { Size = UDim2.fromOffset(240, 18), BackgroundColor3 = Color3.fromRGB(25, 25, 30) }, {
		Fill = e("Frame", { Size = UDim2.fromScale(fill, 1), BackgroundColor3 = Color3.fromRGB(220, 60, 60) }),
	})
end

local function App()
	local hp, setHp = React.useState(100)          -- returns two values, not an array (Lua deviation)
	React.useEffect(function()
		local conn = humanoid.HealthChanged:Connect(setHp)
		return function() conn:Disconnect() end      -- cleanup on unmount
	end, {})
	return e(HealthBar, { hp = hp, maxHp = 100 })
end

local root = ReactRoblox.createRoot(Instance.new("Folder"))
root:render(ReactRoblox.createPortal(e("ScreenGui", { ResetOnSpawn = false }, { App = e(App) }), playerGui))
```

## Notes
- **Re-render cost:** a state change re-renders the subtree. Use `useBinding` for values that change every frame (cooldown sweeps, timers) to update properties without re-rendering ([[UI_Performance]]).
- Dependency arrays with nil holes are ambiguous in Luau, so keep deps explicit and non-nil.
- Pairs well with a store (Reflex, Charm, Rodux-style) for global state ([[UI_State_Management]]).
- Migrating from [[Roact_Legacy]]: there's a compatibility layer (RoactCompat), but plan to adopt hooks.

## Related
[[Roact_Legacy]] · [[Fusion]] · [[Vide]] · [[UI_State_Management]] · [[UI_Performance]] · [[UI_Labs]] · [[Roblox_TS]] · [[Custom_HUD_Design]] · [[Connection_Management]] · [[Wally]] · [[MOC_UI_UX_and_Components]]

## Sources
- https://github.com/jsdotlua/react-lua · https://jsdotlua.github.io/react-lua/
