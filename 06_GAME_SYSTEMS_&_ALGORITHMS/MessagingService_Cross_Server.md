---
aliases: [MessagingService, Cross-server messaging, PublishAsync, SubscribeAsync, Global announcements]
tags:
  - roblox-dev
  - systems/cross-server
type: api
last_updated: 2026-10-27
status: complete
---
# MessagingService (Cross-Server Messaging)

> **TL;DR:** Pub/sub between live servers of one experience: `PublishAsync(topic, message)` and `SubscribeAsync(topic, callback)`. Messages are **≤ 1 KB**, **best-effort** (no delivery guarantee or ordering), and rate-limited per server and per topic. Use it for *notifications* ("event starting", "friend joined server X", "refresh your cache") and keep the truth in DataStores or MemoryStores.

## Limits (Oct 2026)
| Limit | Value |
| --- | --- |
| Message size | 1 KB |
| Topic name | 1–80 characters |
| Messages sent per server | 600 + 240 × players-in-server per minute |
| Messages received per topic | (40 + 80 × servers) per minute |
| Messages received, whole game | (400 + 200 × servers) per minute |
| Subscribe requests per server | 240 per minute |

## Pattern: global event announcement
```luau
local MessagingService = game:GetService("MessagingService")
local TOPIC = "GlobalEvent"

local ok, conn = pcall(function()
	return MessagingService:SubscribeAsync(TOPIC, function(msg)
		-- msg.Data, msg.Sent (unix time)
		local data = msg.Data
		if type(data) ~= "table" or type(data.kind) ~= "string" then return end
		if data.kind == "MeteorShower" then Events.start("MeteorShower", data.seed) end
	end)
end)

-- from an admin command (server-side permission check!) or Open Cloud
MessagingService:PublishAsync(TOPIC, { kind = "MeteorShower", seed = 1234 })
```
- **Open Cloud** can publish to live servers from external tools (Discord bots, dashboards) ([[Open_Cloud_APIs]]).
- **Validate** incoming messages. Anything with access to your API key or admin path can publish ([[Server_Side_Validation]]).

## Patterns and anti-patterns
- ✅ Cache invalidation, announcements, cross-server chat relays (filtered!), "player X is now in server Y".
- ✅ Combine with MemoryStore: publish "something changed", and receivers read the real state from MemoryStore.
- ❌ Per-frame sync, economy transactions, anything that must arrive exactly once.

## Related
[[MemoryStoreService]] · [[MemoryStore_Data_Structures]] · [[TeleportService_and_Reserved_Servers]] · [[Open_Cloud_APIs]] · [[DataStoreService]] · [[Server_Side_Validation]] · [[Text_Filtering_Compliance]] · [[Script_Capabilities]] · [[MOC_Game_Systems_and_Algorithms]]

## Sources
- https://create.roblox.com/docs/cloud-services/cross-server-messaging · https://create.roblox.com/docs/reference/engine/classes/MessagingService
