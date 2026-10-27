---
aliases: [UI Labs, Storybook Roblox, UI stories, Hoarcekat alternative]
tags:
  - roblox-dev
  - ui/tooling
type: framework
last_updated: 2026-10-27
status: complete
---
# UI Labs

> **TL;DR:** UI Labs (PepeElToro41) is a **Storybook-style Studio plugin**. You write *stories* (ModuleScripts) that mount a component in isolation, and it renders them live in Studio **without running the game**, with hot reload and **controls** (knobs) for props. It supports React/Roact, Fusion, Vide, Roblox-TS and plain functions. Use it to build HUD pieces quickly and to catch layout bugs across sizes.

## Why it matters
- **Iteration speed:** tweak a cooldown widget's props in seconds instead of playtesting into combat ([[Cooldown_and_Ability_UI]]).
- **Edge cases:** controls let you test 0%, 100%, long localized strings and huge numbers ([[Damage_Numbers_and_Hit_Markers]]).
- **Design review:** a story library doubles as your UI kit or design system documentation ([[Game_UI_Art_Direction]]).

## Story shape (function story)
```luau
-- HealthBar.story.luau
return function(target: Frame)
	local bar = HealthBar.new({ hp = 35, maxHp = 100 })
	bar.Instance.Parent = target
	return function() bar:Destroy() end   -- cleanup when the story unmounts
end
```
Framework-specific story formats (with typed controls) come from the `ui-labs` utility package (Wally/npm).

## Related
[[Fusion]] · [[React_Lua]] · [[Vide]] · [[Roact_Legacy]] · [[Cooldown_and_Ability_UI]] · [[Damage_Numbers_and_Hit_Markers]] · [[Game_UI_Art_Direction]] · [[Testing_Frameworks]] · [[Roblox_TS]] · [[MOC_UI_UX_and_Components]]

## Sources
- https://github.com/PepeElToro41/ui-labs · https://pepeeltoro41.github.io/ui-labs/
