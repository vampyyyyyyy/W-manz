---
aliases: [Damage numbers, Damage indicators, Hit markers, Floating combat text]
tags:
  - roblox-dev
  - ui/combat-feedback
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Damage Numbers & Hit Markers

> **TL;DR:** Spawn damage numbers **on the client** from **server-confirmed** hit events (or locally predicted hits that the server confirms). Use pooled `BillboardGui`s (offset-sized so they stay readable), add a short pop → drift → fade animation, merge rapid hits into one counter, and differentiate crit/block/kill with color, size and sound. Hit markers on the crosshair confirm "the server agreed".

## Pooled number
```luau
type Item = { gui: BillboardGui, att: Attachment }
local pool: { Item } = {}

local function acquire(): Item
	local item = table.remove(pool)
	if item then return item end
	local att = Instance.new("Attachment")
	att.Parent = workspace.Terrain              -- world-space anchor, pooled with its gui
	local gui = Template:Clone()                -- BillboardGui > TextLabel (+ UIStroke, UIScale)
	gui.AlwaysOnTop = true
	gui.Size = UDim2.fromOffset(120, 40)        -- offset size: constant on-screen size
	gui.Adornee = att
	return { gui = gui, att = att }
end

local function show(worldPos: Vector3, amount: number, kind: "normal" | "crit" | "blocked")
	local item = acquire()
	local label = item.gui.Label :: TextLabel
	label.Text = tostring(math.round(amount))
	label.TextColor3 = if kind == "crit" then Color3.fromRGB(255, 196, 64)
		elseif kind == "blocked" then Color3.fromRGB(150, 160, 180)
		else Color3.new(1, 1, 1)
	item.att.WorldPosition = worldPos + Vector3.new((math.random() - 0.5) * 1.5, 2, 0)
	item.gui.Parent = localPlayer.PlayerGui
	-- pop (UIScale) -> rise (tween StudsOffset) -> fade (TextTransparency), then recycle:
	task.delay(0.7, function()
		item.gui.Parent = nil
		table.insert(pool, item)
	end)
end
```

## Design rules
- **Aggregate** multi-hits (shotguns, DoT ticks) into a rising total on one label per target per ~0.3 s ([[Status_Effects]]).
- **Kill feedback** gets a distinct marker and sound. Headshot/weak point gets its own color.
- **Readability:** stroke + slight shadow, clamp the count on screen (e.g., 12 max), and respect Reduce Motion (no bounce, shorter drift).
- **Never trust client hits.** Numbers render after the server validates ([[Hit_Validation]]). For responsiveness, show a *predicted* marker instantly and correct if rejected ([[Client_Prediction_and_Reconciliation]]).

## Related
[[World_Space_UI]] · [[Object_Pooling]] · [[Rich_Text]] · [[Hit_Validation]] · [[Damage_Pipeline]] · [[Hitstop_and_Impact_Feel]] · [[Client_Side_VFX_Replication]] · [[Status_Effects]] · [[UI_Animation_and_Springs]] · [[Custom_HUD_Design]] · [[Client_Prediction_and_Reconciliation]] · [[MOC_UI_UX_and_Components]]

## Sources
- https://create.roblox.com/docs/ui/in-experience-containers · https://create.roblox.com/docs/reference/engine/classes/BillboardGui
