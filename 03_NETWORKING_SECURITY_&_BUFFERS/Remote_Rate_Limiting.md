---
aliases: [Rate limiting, Token bucket, Leaky bucket, Anti-spam]
tags:
  - roblox-dev
  - security/anti-exploit
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Remote Rate Limiting (Token Bucket)

> **TL;DR:** Every server action a client can trigger needs a **server-side** rate limit. That covers remotes, `Touched`, ProximityPrompts and ClickDetectors. Client cooldowns are UX only. The token bucket allows short bursts and caps the sustained rate, and it's the algorithm Roblox's own security guide recommends.

## Problem
- Exploiters can fire any remote at the engine's throttle (~500/s per client, shared per remote type). The engine **delays** reliable events rather than rejecting them, so every one still runs your handler ([[RemoteEvents_and_RemoteFunctions#Throttling]]).
- Spam hurts in three ways. It hits **rate-limited backends** (DataStores, BadgeService) and fails real requests. It burns **CPU** (cloning models, pathfinding). And it **exploits mechanics** (currency per click, i-frames, teleports) → [[Auto_Farm_and_Remote_Spam_Exploits]].

## Solution
```luau
--!strict
-- ServerScriptService/TokenBucket.luau
type Bucket = { tokens: number, last: number }
export type TokenBucket = {
	capacity: number,
	refillPerSecond: number,
	buckets: { [number]: Bucket },
	allow: (self: TokenBucket, userId: number, cost: number?) -> boolean,
}

local TokenBucket = {}
TokenBucket.__index = TokenBucket

-- capacity = max burst; refills to full over windowSeconds
function TokenBucket.new(capacity: number, windowSeconds: number): TokenBucket
	assert(capacity >= 1 and windowSeconds > 0, "invalid limiter config")
	local self = { capacity = capacity, refillPerSecond = capacity / windowSeconds, buckets = {} }
	return (setmetatable(self, TokenBucket) :: any) :: TokenBucket
end

function TokenBucket.allow(self: TokenBucket, userId: number, cost: number?): boolean
	local c = cost or 1
	local now = os.clock()
	local b = self.buckets[userId]
	if not b then
		b = { tokens = self.capacity, last = now }
		self.buckets[userId] = b
	else
		b.tokens = math.min(self.capacity, b.tokens + (now - b.last) * self.refillPerSecond)
		b.last = now
	end
	if b.tokens >= c then
		b.tokens -= c
		return true
	end
	return false
end

return TokenBucket
```
Usage: `TokenBucket.new(5, 10)` allows a burst of 5, then 1 every 2 s. Clear `buckets[userId]` on `Players.PlayerRemoving` so the table doesn't grow forever ([[Memory_Leaks]]).

## Why it works
Tokens refill continuously, so legitimate burst input (a combo, a double-click) passes. A sustained flood drains the bucket and gets dropped. **Cost weighting** (`allow(id, 3)` for heavy actions) lets one limiter cover several actions of different weight.

## Variations & pitfalls
- **Leaky bucket accumulator:** the mirror image. Add the observed amount, drain at the allowed rate, flag when it overflows. Roblox recommends it for [[Movement_Validation]] (burst-tolerant speed checks).
- **Fixed cooldowns** for discrete abilities are better kept as server timestamps ([[Server_Authoritative_Cooldowns]]). A bucket limits *frequency*, a cooldown enforces *game rules*.
- `os.clock()` is fine inside one server. Under [[Server_Authority_Model|server authority]], simulation code must use `time()` instead.
- Hitting the limit isn't automatically cheating. Laggy clients batch inputs. Feed **repeated** overflow into a suspicion score ([[Server_Side_Detection_Heuristics]]), don't kick on the first hit.
- Also rate-limit **server→all-clients relays** (e.g. a spell that shakes every player's camera). Otherwise one exploiter spams effects onto everyone ([[Client_Side_VFX_Replication]]).
- Rate limits can't replace validation, and validation can't replace rate limits. You need both ([[Server_Side_Validation]]).

## Related
[[RemoteEvents_and_RemoteFunctions]] · [[Remote_Architecture_Patterns]] · [[Auto_Farm_and_Remote_Spam_Exploits]] · [[Server_Side_Detection_Heuristics]] · [[Client_Triggered_Instance_Security]] · [[Server_Authoritative_Cooldowns]] · [[Movement_Validation]] · [[Exploit_Threat_Model]] · [[DataStore_Limits_and_Error_Codes]] · [[MOC_Anti_Exploit]]

## Sources
- https://create.roblox.com/docs/scripting/security/client-server-boundary#rate-limiting
- https://create.roblox.com/docs/scripting/security/network-ownership#movement-validation
