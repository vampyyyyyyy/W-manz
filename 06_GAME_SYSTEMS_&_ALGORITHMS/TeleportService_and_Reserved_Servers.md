---
aliases: [TeleportService, TeleportAsync, Reserved servers, TeleportOptions, Teleport data, GetJoinData]
tags:
  - roblox-dev
  - systems/cross-server
type: api
last_updated: 2026-10-27
status: complete
---
# TeleportService & Reserved Servers

> **TL;DR:** Move players between places and servers with **`TeleportService:TeleportAsync(placeId, players, options)`** (server-side). Reserved (private) servers come from `ReserveServerAsync` or `TeleportOptions.ShouldReserveServer`, and they're perfect for matches, dungeons and parties. Teleport **data is client-visible and unencrypted**, so persist anything valuable in DataStores or MemoryStores. Lock down subplaces with **"Secure within universe only"**.

## Core flow
```luau
--!strict
local TeleportService = game:GetService("TeleportService")
local MATCH_PLACE = 1234567890

local function sendToMatch(players: { Player }, matchId: string)
	local options = Instance.new("TeleportOptions")
	options.ShouldReserveServer = true                    -- fresh private server for this group
	options:SetTeleportData({ matchId = matchId })        -- NON-SECURE: visible to clients
	for attempt = 1, 3 do
		local ok, result = pcall(TeleportService.TeleportAsync, TeleportService, MATCH_PLACE, players, options)
		if ok then return result end                      -- TeleportAsyncResult (ReservedServerAccessCode, PrivateServerId)
		task.wait(attempt * 2)
	end
	return nil
end

TeleportService.TeleportInitFailed:Connect(function(player, result, errorMessage)
	warn("teleport failed", player.Name, result, errorMessage)      -- retry or show UI
end)
```
- On arrival, read `player:GetJoinData().TeleportData` on the server (client: `GetLocalPlayerTeleportData()`).
- Treat teleport data as **hints** (matchId), and look up truth server-side (MemoryStore match record) ([[MemoryStore_Data_Structures]]).
- `ReserveServerAsync(placeId)` returns an access code you can store and reuse for persistent instances (housing, guild halls).

## Security settings (official)
| Setting | Effect |
| --- | --- |
| Access Control for Places: **Fully open** | Join any place from anywhere (friend-follow friendly) |
| **Limited to same universe** | Non-start places only via teleports within your game (client or server) |
| **Secure within universe only** | Non-start places only via **server-initiated** teleports. Blocks client teleports to test or locked places ([[Access_Control_and_Confidentiality]]) |
| Allow Third Party Teleports | Teleports to games you don't own |
Migrating to secure: replace client `Teleport()` calls with remotes → server `TeleportAsync`, then flip the setting.

## Data continuity
Session locks plus a teleport create the classic "joined new server before old save finished" race. Save with a lock release *before* the teleport completes, and let the destination wait or retry the lock ([[Session_Locking]]).

## Related
[[Matchmaking_Customization]] · [[MemoryStore_Data_Structures]] · [[Session_Locking]] · [[Access_Control_and_Confidentiality]] · [[MessagingService_Cross_Server]] · [[DataStoreService]] · [[Error_Handling_pcall_xpcall]] · [[Loading_Screens_and_ReplicatedFirst]] · [[MOC_Game_Systems_and_Algorithms]]

## Sources
- https://create.roblox.com/docs/projects/teleport · https://create.roblox.com/docs/reference/engine/classes/TeleportService
