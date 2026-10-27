---
aliases: [RemoteEvent, RemoteFunction, Remotes, FireServer, InvokeServer]
tags:
  - roblox-dev
  - networking/remotes
type: api
last_updated: 2026-10-27
status: complete
---
# RemoteEvents and RemoteFunctions

> **TL;DR:** Remotes are the only general-purpose way for client code to ask the server to do something. Everything a client sends through one is attacker-controlled input. Validate it, rate-limit it, and design the payload so the server decides the outcome ([[Server_Side_Validation]], [[Remote_Rate_Limiting]]).

## The API surface
| Call | Direction | Yields? | Notes |
| --- | --- | --- | --- |
| `RemoteEvent:FireServer(...)` | client → server | no | Server handler receives `(player, ...)`. The engine fills in `player`, so it can't be spoofed. |
| `RemoteEvent:FireClient(player, ...)` | server → one client | no | |
| `RemoteEvent:FireAllClients(...)` | server → all clients | no | Make sure the server acts as a gatekeeper, not a relay. |
| `RemoteFunction:InvokeServer(...)` | client → server → client | **yes** | Client thread yields until the callback returns. |
| `RemoteFunction:InvokeClient(player, ...)` | server → client → server | **yes** | **Avoid.** A malicious or disconnected client can hang the server thread or return garbage. |

For fire-and-forget, high-frequency, droppable data, use [[UnreliableRemoteEvent]] instead.

## Delivery guarantees (official, per connection + direction)
- **RemoteEvents are reliable and ordered.** Ordering holds *across different RemoteEvent instances* on the same connection: fire A, B, A and the client receives A, B, A.
- Ordering applies to when a handler **starts**, not when it finishes. If a handler yields (`task.wait`, `WaitForChild`), the next message can start processing first. That's a classic race in [[Combat_State_Machine]] code.
- If no handler is connected, messages are **queued** and delivered once one connects. The queue is capped by count and memory. When it's full, Roblox logs a `Remote event invocation` error and drops messages.
- RemoteFunction invocations and RemoteEvent messages are queued separately, so their *relative* order isn't guaranteed. Add a sequence number if you depend on it.
- Remote messages are not guaranteed to be ordered with **property/attribute replication** either. If you set a property and then fire a remote, the other side may see the remote first ([[Replication_Model]]).

## Throttling
Client → server traffic is rate limited to **about 500 requests per second per client**. The limit is **shared by every remote of the same type**. Over the limit, RemoteEvents get *delayed* (queued, still in order), while unreliable ones get *dropped*. Don't treat engine throttling as anti-spam: an exploiter at 500/s still gets every message processed. Your own [[Remote_Rate_Limiting]] has to reject the excess.

## What survives the trip (argument rules)
- Tables are **copied**, so identity is lost, and **metatables are stripped**. A class instance arrives as a plain table ([[Metatables]]).
- **Non-string keys are converted to strings**, so don't send `{[Instance] = value}` maps. Avoid **mixed tables** (array + dictionary) and **`nil` holes**.
- **Functions arrive as `nil`.**
- **Instances the receiver can't see arrive as `nil`**: a `ServerStorage` descendant sent to a client, or a client-created part sent to the server ([[Container_Services_and_Replication_Scope]]).
- [[Buffer_Library|Buffers]] are encoded and compressed by the engine. That's why the [[Networking_Libraries_Comparison|buffer networking libraries]] exist.

## Example: a remote with the minimum professional hygiene
```luau
--!strict
-- ServerScriptService/Shop.server.luau
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Players = game:GetService("Players")

local BuyItem = ReplicatedStorage.Remotes.BuyItem :: RemoteFunction
local ItemCatalog = require(script.Parent.ItemCatalog) -- server-only prices
local TokenBucket = require(script.Parent.TokenBucket)
local PlayerData = require(script.Parent.PlayerData) -- your session-locked data layer
local limiter = TokenBucket.new(5, 10) -- 5 purchases per 10 s burst

BuyItem.OnServerInvoke = function(player: Player, itemId: unknown, quantity: unknown)
	if not limiter:allow(player.UserId) then return false, "slow down" end
	-- 1. type/structure
	if typeof(itemId) ~= "string" or typeof(quantity) ~= "number" then return false, "bad args" end
	-- 2. value (rejects NaN/inf, negatives, fractions)
	if not math.isfinite(quantity) or quantity < 1 or quantity > 99 or quantity % 1 ~= 0 then
		return false, "bad quantity"
	end
	-- 3. context: the server owns the price and the wallet
	local item = ItemCatalog[itemId]
	if not item then return false, "unknown item" end
	return PlayerData.TrySpend(player, item.Price * quantity, itemId, quantity)
end

Players.PlayerRemoving:Connect(function(p) limiter.buckets[p.UserId] = nil end)
```

## Gotchas
- `OnServerInvoke` is a **callback property**, not an event. Assigning it twice overwrites the first handler.
- Never let a remote take an arbitrary instance path or class to modify or destroy ([[Access_Control_and_Confidentiality]]).
- Remotes in `ReplicatedStorage` are visible to every client. Their names are a map of your attack surface ([[Exploit_Threat_Model]]).
- A server→client remote fired *from the client* is a free cheat signal ([[Honeypot_Remotes]]).

## Related
- [[UnreliableRemoteEvent]] · [[Remote_Architecture_Patterns]] · [[Server_Side_Validation]] · [[Remote_Rate_Limiting]]
- [[NaN_and_Infinity_Exploits]] · [[Auto_Farm_and_Remote_Spam_Exploits]] · [[Exploit_Threat_Model]] · [[Honeypot_Remotes]]
- [[Bindable_Events_and_Functions]] (same-side signalling) · [[Deferred_Events_and_SignalBehavior]]
- [[Network_Bandwidth_Budget]] · [[Buffer_Library]] · [[Networking_Libraries_Comparison]] · [[Blink_IDL]] · [[Zap_IDL]]
- Hub: [[MOC_Networking_Security_and_Buffers]]

## Sources
- https://create.roblox.com/docs/scripting/events/remote
- https://create.roblox.com/docs/reference/engine/classes/RemoteEvent
- https://create.roblox.com/docs/scripting/security/client-server-boundary
