---
aliases: [TeleportService, TeleportAsync, Reserved servers, TeleportOptions, Teleport data, GetJoinData]
tags:
  - roblox-dev
  - systems/cross-server
type: api
last_updated: 2026-11-02
status: complete
---
# TeleportService & Reserved Servers

> **TL;DR:** Move players between places and servers with **`TeleportService:TeleportAsync(placeId, players, options)`** (server-side). **Reserved servers now use `TeleportOptions.ReservedServerId`** (as of Oct 2026). You generate a GUID on the server, the first teleport with it creates the server, and reusing it routes later teleports to the same server. `ReserveServerAsync`, `ReservedServerAccessCode` and `ShouldReserveServer` are **deprecated** but still work. Player-bought servers use `VipServerId`. Teleport **data is client-visible and unencrypted**, so persist anything valuable in DataStores or MemoryStores. Lock down subplaces with **"Secure within universe only"**.

## Core flow: send a match group to a fresh reserved server
```luau
--!strict
local HttpService = game:GetService("HttpService")
local TeleportService = game:GetService("TeleportService")
local MATCH_PLACE = 1234567890

local function sendToMatch(players: { Player }, matchId: string): string?
	-- Generate on the SERVER. Whoever knows this ID can route players into that server.
	local reservedServerId = HttpService:GenerateGUID(false)

	local options = Instance.new("TeleportOptions")
	options.ReservedServerId = reservedServerId           -- first teleport with a new ID creates the server
	options:SetTeleportData({ matchId = matchId })         -- NON-SECURE: visible to clients

	for attempt = 1, 3 do
		local ok, result = pcall(TeleportService.TeleportAsync, TeleportService, MATCH_PLACE, players, options)
		if ok then
			return reservedServerId                         -- store it (MemoryStore match record) for late joiners / reconnects
		end
		warn(`match {matchId} teleport attempt {attempt} failed: {result}`)
		task.wait(attempt * 2)
	end
	return nil
end

TeleportService.TeleportInitFailed:Connect(function(player, result, errorMessage, placeId, options)
	warn("teleport failed", player.UserId, result, errorMessage)  -- options = the original TeleportOptions, so you can retry the same destination
end)
```
- **Reconnect / late join:** store `reservedServerId` keyed by match ID in a MemoryStore hash map ([[MemoryStore_Data_Structures]]), or in a DataStore for persistent instances (housing, guild halls). Teleport again with the same ID to land in the **same** server.
- **On arrival:** `game.PrivateServerId` **equals the `ReservedServerId` you supplied** and stays constant across restarts of that reserved server (`game.JobId` changes per instance). A reserved server has `PrivateServerId ~= ""` and `PrivateServerOwnerId == 0`, so you can identify one and look up its match record with no teleport data at all.
- `TeleportAsyncResult.PrivateServerId` matches the destination's `game.PrivateServerId`. `ReservedServerAccessCode` on the result is only filled for legacy access-code teleports.
- Read `player:GetJoinData().TeleportData` on the server (client: `GetLocalPlayerTeleportData()`) and treat it as **hints**. Look up the truth server-side.

## Routing rules (official)
- Set **only one** of `ReservedServerId`, `VipServerId` or `ServerInstanceId` per `TeleportOptions`. Setting more than one errors.
- **VIP (player-bought) servers:** `VipServerId = <that server's PrivateServerId>`. It works with any place in the same experience and is rejected for other experiences. To keep a party in the same VIP server across places, set `VipServerId = game.PrivateServerId` on every teleport. Going from a VIP server to a reserved match and back requires carrying the VIP ID yourself (teleport data or a store), because inside the reserved server `game.PrivateServerId` is the reserved ID.
- With **no routing field**, the engine picks the server: public, or a VIP server the player recently joined in that experience. In that implicit case a full or flooded VIP server **falls back to a public join silently**. Only an explicit `VipServerId` reports failures to `TeleportInitFailed`.

## Security notes for reserved server IDs
- **Never accept a server ID from a client remote.** Generate and look up IDs on the server only (official best practice). *Our inference:* a reserved server ID now works like a join key. Anyone your server teleports with that ID lands in that match, so a remote like "join match <id>" lets an exploiter enter private matches. Map client requests to server-side records (party membership, invites) instead.
- Teleport data is visible to the client. If you put the ID there for convenience, assume the player can read it. That's fine for their *own* match, but never put other matches' IDs there.

## Migrating from access codes
| Deprecated | Use |
| --- | --- |
| `TeleportService:ReserveServerAsync(placeId)` → `ReservedServerAccessCode` | `HttpService:GenerateGUID(false)` → `ReservedServerId` |
| `TeleportOptions.ShouldReserveServer = true` | A fresh GUID in `ReservedServerId` |
| Storing access codes | Store the GUID instead |

Per the docs, `ReserveServerAsync` "does not actually reserve a server in advance, but simply generates a random GUID", and servers created with access codes keep working. Migrate when you next touch the code. There's no deadline announced (as of Nov 2, 2026).

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
[[Matchmaking_Customization]] · [[MemoryStore_Data_Structures]] · [[Device_Trust_API]] · [[Legacy_Code_Smells]] · [[Paid_Access_and_Private_Servers]] · [[Session_Locking]] · [[Access_Control_and_Confidentiality]] · [[MessagingService_Cross_Server]] · [[DataStoreService]] · [[Error_Handling_pcall_xpcall]] · [[Loading_Screens_and_ReplicatedFirst]] · [[MOC_Game_Systems_and_Algorithms]]

## Sources
- https://create.roblox.com/docs/projects/teleport · https://create.roblox.com/docs/projects/teleport-private-servers · https://create.roblox.com/docs/reference/engine/classes/TeleportService · https://create.roblox.com/docs/reference/engine/classes/TeleportOptions (Creator Docs repo @ 2026-10-29)
