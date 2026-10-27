---
aliases: [RichText, Rich text markup, font tags, stroke tag]
tags:
  - roblox-dev
  - ui/text
type: api
last_updated: 2026-10-27
status: complete
---
# Rich Text

> **TL;DR:** Set `RichText = true` on a TextLabel, TextButton or TextBox and use XML-like tags: `<b>`, `<i>`, `<u>`, `<s>`, `<br/>`, `<font color size face family weight transparency>`, `<stroke color thickness transparency joins sizing>`, `<uppercase>`/`<uc>`, `<smallcaps>`/`<sc>`, `<mark>`, `<!-- -->`. Escape `< > " ' &` as `&lt; &gt; &quot; &apos; &amp;`. **Never** interpolate unescaped player text into rich text, and localization drops tags.

## Examples
```luau
label.RichText = true
label.Text = `<b>CRIT!</b> <font color="#FF5A3C" size="32">{dmg}</font>`
label.Text = `<stroke color="#000000" thickness="2">Round <font weight="heavy">{round}</font></stroke>`

local function escape(s: string): string
	return (s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"):gsub('"', "&quot;"):gsub("'", "&apos;"))
end
label.Text = `<b>{escape(filteredName)}</b> joined`
```
(Escape `&` first so you don't double-escape.)

## Rules
- Close tags in **reverse** order of opening.
- Player-generated text must be **filtered** via TextService first, then escaped ([[Text_Filtering_Compliance]]).
- Localized strings lose formatting, so re-apply tags in the translated strings ([[Roblox_UI_Fundamentals]]).
- Changing rich text every frame is costly (text layout reflow). Update on change only ([[UI_Performance]]).
- For a uniform outline, a `UIStroke` child is simpler than `<stroke>` ([[UI_Appearance_and_Size_Modifiers]]).

## Related
[[Text_Filtering_Compliance]] · [[UI_Appearance_and_Size_Modifiers]] · [[Damage_Numbers_and_Hit_Markers]] · [[Custom_HUD_Design]] · [[UI_Performance]] · [[String_Interpolation]] · [[String_Library_and_Patterns]] · [[Roblox_UI_Fundamentals]] · [[MOC_UI_UX_and_Components]]

## Sources
- https://create.roblox.com/docs/ui/rich-text
