---
aliases: [Schema migration, Data versioning, Save versions, Reconcile defaults]
tags:
  - roblox-dev
  - systems/persistence
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Data Versioning & Schema Migration

> **TL;DR:** Your save format **will** change. Store a `SchemaVersion` in every profile, run **ordered migration functions** on load (`v1 → v2 → v3`), **reconcile** new default fields, and never delete data you might need for rollback. Roblox's own DataStore versioning (30-day history) is your safety net for bad migrations.

## Pattern
```luau
--!strict
local CURRENT = 4
local TEMPLATE = { SchemaVersion = CURRENT, Coins = 0, Inventory = {}, Settings = { Sensitivity = 1 } }

local MIGRATIONS: { [number]: (any) -> any } = {
	[1] = function(d) d.Coins = d.Cash or 0; d.Cash = nil; return d end,                -- rename
	[2] = function(d) d.Inventory = d.Items or {}; d.Items = nil; return d end,
	[3] = function(d) -- convert array inventory → map of itemId -> count
		local map = {}
		for _, id in d.Inventory do map[id] = (map[id] or 0) + 1 end
		d.Inventory = map
		return d
	end,
}

local function reconcile(data: any, template: any)
	for k, v in template do
		if data[k] == nil then
			data[k] = if type(v) == "table" then table.clone(v) else v
		elseif type(v) == "table" and type(data[k]) == "table" and next(v) ~= nil then
			reconcile(data[k], v)   -- fill nested defaults (skip empty templates like {})
		end
	end
end

local function migrate(data: any): any
	local v = data.SchemaVersion or 1
	while v < CURRENT do
		data = MIGRATIONS[v](data)
		v += 1
		data.SchemaVersion = v
	end
	reconcile(data, TEMPLATE)
	return data
end
```

## Rules
- Migrations must be **deterministic and idempotent per step**. Test each one on real-looking fixtures with [[Testing_Frameworks]] or [[Lune]] scripts.
- **Never downgrade:** if `SchemaVersion > CURRENT` (an old server during a rolling update), load **read-only** and don't save, or you'll destroy new fields.
- Keep keys stable. Migrate *data*, not *key names*, unless you also migrate keys with a fallback read.
- [[ProfileStore]] has `:Reconcile()` for defaults, but you still own schema migrations.
- Big structural changes go through a **shadow field** for one release before deleting the old one.
- Rollback lever: `ListVersionsAsync`/`GetVersionAsync` within 30 days ([[DataStoreService]]).

## Related
[[DataStoreService]] · [[ProfileStore]] · [[UpdateAsync_Patterns]] · [[Session_Locking]] · [[Custom_Serialization]] · [[Inventory_Systems]] · [[Testing_Frameworks]] · [[Lune]] · [[MOC_Game_Systems_and_Algorithms]]

## Sources
- https://create.roblox.com/docs/cloud-services/data-stores/versioning-listing-and-caching
