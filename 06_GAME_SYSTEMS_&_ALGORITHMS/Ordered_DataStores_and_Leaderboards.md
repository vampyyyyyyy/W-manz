---
aliases: [OrderedDataStore, Leaderboards, GetSortedAsync, Global leaderboard, leaderstats]
tags:
  - roblox-dev
  - systems/persistence
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Ordered DataStores & Leaderboards

> **TL;DR:** **In-server** leaderboards use a `leaderstats` folder under each Player (IntValue/NumberValue children show in the player list). **All-time global** leaderboards use an `OrderedDataStore` (integer values, `GetSortedAsync` pages). **Live, seasonal** global boards fit **MemoryStore sorted maps** better: fast, TTL-based, and real-time ([[MemoryStore_Data_Structures]]).

## leaderstats (per server, built-in UI)
```luau
game.Players.PlayerAdded:Connect(function(player)
	local stats = Instance.new("Folder")
	stats.Name = "leaderstats"
	local kills = Instance.new("IntValue")
	kills.Name = "Kills"
	kills.Parent = stats
	stats.Parent = player
end)
```
The server owns these values. Clients editing their own copies doesn't replicate ([[Replication_Model]]).

## OrderedDataStore (all-time)
```luau
local ods = game:GetService("DataStoreService"):GetOrderedDataStore("AllTimeWins")
ods:UpdateAsync(tostring(userId), function(old) return (old or 0) + 1 end)  -- integers only

local pages = ods:GetSortedAsync(false, 50)      -- descending, 50 per page
for rank, entry in pages:GetCurrentPage() do
	print(rank, entry.key, entry.value)
end
```
- Values must be **integers**. Store fixed-point (e.g. time × 1000) for decimals. For "fastest time" boards, sort ascending.
- Budget: list requests are only `300 + 2×CCU`/min **experience-wide**, so refresh boards every 1–5 minutes with **cached results**, not per player join ([[DataStore_Limits_and_Error_Codes]]).
- Display names: resolve `UserId → name` with `Players:GetNameFromUserIdAsync` (cache it), and thumbnails with `GetUserThumbnailAsync`.

## Seasonal and live boards
Write scores to a sorted map with an expiry at season end, read the top N every 30–60 s per server, and snapshot to an OrderedDataStore or DataStore at season close for history ([[MemoryStoreService]]).

## Anti-cheat
Leaderboards attract cheaters. Score only from **server-side events**, apply rate-of-gain heuristics, and exclude flagged accounts ([[Server_Side_Detection_Heuristics]]).

## Related
[[DataStoreService]] · [[DataStore_Limits_and_Error_Codes]] · [[MemoryStoreService]] · [[MemoryStore_Data_Structures]] · [[UpdateAsync_Patterns]] · [[Server_Side_Detection_Heuristics]] · [[Replication_Model]] · [[Custom_HUD_Design]] · [[MOC_Game_Systems_and_Algorithms]]

## Sources
- https://create.roblox.com/docs/cloud-services/data-stores#ordered-data-stores · https://create.roblox.com/docs/players/leaderboards
