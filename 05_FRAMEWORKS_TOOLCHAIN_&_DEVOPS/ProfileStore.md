---
aliases: [ProfileStore, ProfileService, loleris ProfileStore, Profile sessions]
tags:
  - roblox-dev
  - framework/persistence
type: framework
last_updated: 2026-10-27
status: complete
---
# ProfileStore (loleris / MAD STUDIO)

> **TL;DR:** ProfileStore is the successor to ProfileService and the community's go-to **player-data wrapper**: **session locking**, **auto-save**, a final save on `EndSession`, `Reconcile()` defaults, cross-server **messages**, version queries and a mock store for testing. It's one ModuleScript, server-only. It's **not for leaderboards or global state** (the README says so explicitly).

## What it is / maintenance status
- Repo: https://github.com/MadStudioRoblox/ProfileStore (last commit July 2025, stable). Docs: madstudioroblox.github.io/ProfileStore. Creator Store asset + Wally. DevForum thread for support.

## Standard implementation (from the official tutorial)
```luau
local ProfileStore = require(game.ServerScriptService.ProfileStore)
local Players = game:GetService("Players")
local PROFILE_TEMPLATE = { Cash = 0, Items = {} }
local PlayerStore = ProfileStore.New("PlayerStore", PROFILE_TEMPLATE)
local Profiles: { [Player]: typeof(PlayerStore:StartSessionAsync()) } = {}

local function PlayerAdded(player: Player)
	local profile = PlayerStore:StartSessionAsync(`{player.UserId}`, {
		Cancel = function() return player.Parent ~= Players end,   -- stop waiting if they left
	})
	if profile == nil then
		player:Kick("Profile load fail - Please rejoin")           -- e.g. server shutting down
		return
	end
	profile:AddUserId(player.UserId)   -- GDPR/erasure association (Right_to_Erasure_GDPR)
	profile:Reconcile()                -- fill missing template fields
	profile.OnSessionEnd:Connect(function()
		Profiles[player] = nil
		player:Kick("Profile session end - Please rejoin")
	end)
	if player.Parent == Players then
		Profiles[player] = profile
	else
		profile:EndSession()           -- left during load
	end
end
for _, p in Players:GetPlayers() do task.spawn(PlayerAdded, p) end
Players.PlayerAdded:Connect(PlayerAdded)
Players.PlayerRemoving:Connect(function(p) local pr = Profiles[p] if pr then pr:EndSession() end end)
```

## API highlights
`ProfileStore.New(name, template)`, `:StartSessionAsync(key, params)`, `:GetAsync`, `:VersionQuery`, `:RemoveAsync`, `:MessageAsync(key, msg)` · `Profile.Data`, `:Save()`, `:EndSession()`, `:IsActive()`, `:Reconcile()`, `:AddUserId`/`:RemoveUserId`, `:MessageHandler(fn)`, `OnSave`/`OnAfterSave`/`OnLastSave`/`OnSessionEnd` · `ProfileStore.Mock` (tests, Studio without API access) · `IsCriticalState`, `OnCriticalToggle`, `OnError`.

## Integration notes
- Developer Products: the official ProfileStore docs include a ProcessReceipt pattern built on sessions ([[ProcessReceipt_Idempotency]]).
- Schema migrations are still yours ([[Data_Versioning_and_Schema_Migration]]).
- Keep `Profile.Data` JSON-safe (no Instances, no NaN) ([[DataStoreService]]).

## Related
[[Session_Locking]] · [[DataStoreService]] · [[DataStore_Libraries_Comparison]] · [[Lapis]] · [[ProcessReceipt_Idempotency]] · [[Data_Versioning_and_Schema_Migration]] · [[Right_to_Erasure_GDPR]] · [[Data_Duplication_and_Trade_Exploits]] · [[Inventory_Systems]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://github.com/MadStudioRoblox/ProfileStore (README, docs/tutorial, docs/api) · https://devforum.roblox.com/t/profilestore/3190543
