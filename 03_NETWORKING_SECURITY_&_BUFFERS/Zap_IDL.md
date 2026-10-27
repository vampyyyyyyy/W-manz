---
aliases: [Zap, zap networking, .zap files]
tags:
  - roblox-dev
  - networking/libraries
type: framework
last_updated: 2026-10-27
status: complete
---
# Zap (IDL Networking Compiler)

> **TL;DR:** Zap compiles a `.zap` config into typed server and client modules that pack data into buffers "with no overhead" and validate everything received. It's the IDL that popularized this approach on Roblox. As of Oct 2026, **0.6.x is maintained** and a **rewrite** is in progress.

## What it is / maintenance status
- Repo: https://github.com/red-blox/zap. Docs at zap.redblox.dev cover 0.6.x.
- Status per README: rewrite on the `rewrite` branch; `0.6.x` branch maintained by @sasial-dev. Last default-branch activity was June 2026. **Pin your version.**
- Install: GitHub releases CLI (the docs show `aftman add red-blox/zap`; [[Rokit]] works the same way), the community **Zappy** Studio plugin, or the web **playground**.

## Core syntax
```text
opt server_output = "src/server/Zap.luau"
opt client_output = "src/client/Zap.luau"

event MyEvent = {
	from: Server,
	type: Reliable,
	call: ManyAsync,
	data: (Foo: u32, Bar: string),
}
```
- `from`: `Server` | `Client` (no two-way events; "add more events instead").
- `type`: `Reliable` | `Unreliable` (1,000-byte cap).
- `call`: `ManyAsync`, `ManySync`, `SingleAsync`, `SingleSync`, `Polling` (0.6.18+, iterate `event.iter()`). Sync callbacks that yield cause undefined behavior, and erroring drops the packet.
- Generate: `zap path/to/config.zap`.

```luau
-- Server
local Zap = require(path.to.server.output)
Zap.MyEvent.FireAll(123, "hello world")
-- Client
Zap.MyEvent.On(function(foo, bar) print(foo, bar) end)
```

## Alternatives
[[Blink_IDL]] (more active, similar syntax) · [[ByteNet]] · plain remotes

## Related
[[Networking_Libraries_Comparison]] · [[Blink_IDL]] · [[ByteNet]] · [[Buffer_Library]] · [[Custom_Serialization]] · [[Remote_Architecture_Patterns]] · [[UnreliableRemoteEvent]] · [[Rokit]] · [[Server_Side_Validation]] · [[MOC_Networking_Security_and_Buffers]]

## Sources
- https://github.com/red-blox/zap (README, docs/config/events.md, docs/intro/getting-started.md)
