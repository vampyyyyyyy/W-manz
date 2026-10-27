---
aliases: [Networking architecture, Remote layout, Net module]
tags:
  - roblox-dev
  - networking/architecture
type: architecture
last_updated: 2026-10-27
status: complete
---
# Remote Architecture Patterns

> **TL;DR:** Treat networking as a module with one choke point, not hundreds of ad-hoc `FireServer` calls. Every inbound message then passes the same validation and rate-limit middleware, payloads can be batched or bit-packed, and you can swap the transport (raw remotes → [[Blink_IDL]] or [[Zap_IDL]]) without touching gameplay code.

## Goals & constraints
- One place to **validate** ([[Server_Side_Validation]]), **rate-limit** ([[Remote_Rate_Limiting]]) and **log** suspicious traffic ([[Server_Side_Detection_Heuristics]]).
- Keep the global per-client budget (~500 msgs/s shared per remote type) far away. See [[RemoteEvents_and_RemoteFunctions#Throttling]].
- Minimize what an exploiter learns from your remote list ([[Access_Control_and_Confidentiality]]).
- Gameplay code reads like an API (`Net.Combat.Swing:Fire(dir)`), not like plumbing.

## The four common layouts
| Layout | How | Pros | Cons |
| --- | --- | --- | --- |
| **One remote per action** | `Remotes/BuyItem`, `Remotes/Swing`… | Simple, easy to debug, per-remote `OnServerEvent` | Grows messy; names advertise intent; no shared middleware |
| **Namespaced folders** | `Remotes/Combat/Swing` created by a server module at startup | Organized; server is the single creator | Still one handler per remote unless wrapped |
| **Multiplexed single remote** | One RemoteEvent; first arg is a packet id (`u8`) | One choke point; trivial to batch | Hand-rolled dispatch; mistakes affect everything |
| **IDL-generated** | Schema file → generated Luau ([[Blink_IDL]], [[Zap_IDL]]) | Typed, validated, buffer-packed, batched per frame | Build step; another tool to learn ([[Networking_Libraries_Comparison]]) |

## Data flow (middleware pattern)
```text
client action ──► Net.Fire(name, ...) ──► [batch per frame] ──► RemoteEvent
                                                         │
server: OnServerEvent ─► rateLimit(player, name) ─► validate(schema) ─► handler(player, args)
                               │ fail                    │ fail
                               └──────► suspicion score / drop (never trust, never crash)
```

## Implementation sketch
```luau
--!strict
-- ReplicatedStorage/Net/Server.luau (required only by the server)
local Players = game:GetService("Players")
local TokenBucket = require(script.Parent.TokenBucket)

type Validator = (...unknown) -> boolean
type Handler = (player: Player, ...any) -> ()

local Net = {}
local folder = Instance.new("Folder")
folder.Name = "Net"

function Net.on(name: string, opts: { burst: number, window: number, validate: Validator }, handler: Handler)
	local remote = Instance.new("RemoteEvent")
	remote.Name = name
	remote.Parent = folder
	local limiter = TokenBucket.new(opts.burst, opts.window)
	remote.OnServerEvent:Connect(function(player, ...)
		if not limiter:allow(player.UserId) then return end      -- drop silently
		if not opts.validate(...) then                          -- malformed = suspicious
			-- Suspicion.add(player, "bad_packet:" .. name, 1)
			return
		end
		handler(player, ...)
	end)
	Players.PlayerRemoving:Connect(function(p) limiter.buckets[p.UserId] = nil end)
	return remote
end

folder.Parent = game:GetService("ReplicatedStorage") -- parent LAST (Instance_Lifecycle_and_Destroy)
return Net
```
Client side: `ReplicatedStorage:WaitForChild("Net"):WaitForChild(name)`. Because the server creates remotes at runtime, the client must wait for them. That's the standard [[Player_and_Character_Lifecycle]] race.

## Batching
Collect outgoing messages in a table during the frame and flush once per `Heartbeat` as a single [[Buffer_Library|buffer]]. This cuts per-message overhead and handler wake-ups, and it's exactly what Blink and Zap generate for you. Unreliable traffic must stay under 1,000 bytes per packet ([[UnreliableRemoteEvent]]).

## Rules of thumb
- **Server decides outcomes.** Clients send *intent* (`"swing", direction`), never results (`"I hit Bob for 50"`) ([[Hit_Validation]], [[Defensive_Design]]).
- **Never `InvokeClient`.** Use event + reply with a correlation id if the server needs data from a client.
- **Directional remotes:** a remote meant for server→client should never fire `OnServerEvent`. If it does, that's a [[Honeypot_Remotes|honeypot]] hit.
- Keep server-only logic out of ModuleScripts in `ReplicatedStorage`: they get decompiled ([[Access_Control_and_Confidentiality]]).
- Under [[Server_Authority_Model|server authority]], simulation-affecting input should go through the [[Input_Action_System]], not remotes.

## Related
[[RemoteEvents_and_RemoteFunctions]] · [[UnreliableRemoteEvent]] · [[Networking_Libraries_Comparison]] · [[Blink_IDL]] · [[Zap_IDL]] · [[ByteNet]] · [[Remote_Rate_Limiting]] · [[Server_Side_Validation]] · [[Custom_Serialization]] · [[Single_Script_Architecture]] · [[Exploit_Threat_Model]] · [[MOC_Networking_Security_and_Buffers]]

## Sources
- https://create.roblox.com/docs/scripting/events/remote
- https://create.roblox.com/docs/scripting/security/client-server-boundary
- https://github.com/1Axen/blink · https://github.com/red-blox/zap
