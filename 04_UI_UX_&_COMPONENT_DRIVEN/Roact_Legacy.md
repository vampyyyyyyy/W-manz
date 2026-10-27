---
aliases: [Roact, Roblox Roact, Roact deprecated]
tags:
  - roblox-dev
  - ui/framework
type: framework
last_updated: 2026-10-27
status: complete
---
# Roact (Legacy)

> **TL;DR:** **Roact is deprecated and unmaintained.** Its README points to React Lua. It introduced declarative Roblox UI (`Roact.createElement`, `Roact.mount`, class components, bindings) and still runs in many older codebases. New work should use [[React_Lua]] (closest migration path), [[Fusion]] or [[Vide]].

## Recognize it
```luau
local tree = Roact.createElement("ScreenGui", {}, {
	Label = Roact.createElement("TextLabel", { Text = "Hello", Size = UDim2.fromScale(1, 1) }),
})
local handle = Roact.mount(tree, Players.LocalPlayer.PlayerGui, "HelloWorld")
-- Roact.update(handle, newTree); Roact.unmount(handle)
```
Class components use `Roact.Component:extend("Name")` with `init`, `render`, `didMount`, `willUnmount`. State goes through `self:setState`.

## Migration path
1. Swap the package for React Lua and use its **RoactCompat** layer to keep old call sites compiling.
2. Convert leaf components to function components + hooks first, then containers.
3. Replace Rodux connections with your chosen store ([[UI_State_Management]]).
4. Test visually in [[UI_Labs]] stories during the migration.

Treat this as part of a general legacy cleanup ([[Legacy_Code_Smells]]).

## Related
[[React_Lua]] · [[Fusion]] · [[Vide]] · [[UI_State_Management]] · [[UI_Labs]] · [[Legacy_Code_Smells]] · [[Community_Modules_Index]] · [[Roblox_TS]] · [[MOC_UI_UX_and_Components]]

## Sources
- https://github.com/Roblox/roact (deprecated notice) · https://jsdotlua.github.io/react-lua/
