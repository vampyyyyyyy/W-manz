---
aliases: [Blink, blink networking, .blink files]
tags:
  - roblox-dev
  - networking/libraries
type: framework
last_updated: 2026-10-27
status: complete
---
# Blink (IDL Networking Compiler)

> **TL;DR:** Blink compiles a `.blink` schema into server and client Luau modules that send **buffer-packed, batched, validated** messages over remotes. It's the most actively maintained buffer-networking tool as of late 2026 (`1Axen/blink`).

## What it is / maintenance status
- Repo: https://github.com/1Axen/blink (MIT). Active, with commits in Sept 2026. CLI plus a Studio plugin with autocomplete.
- Goals per README: lower bandwidth (→ lower ping) and lower CPU than generic remotes. Data sent by clients is **validated** before reaching game code.
- Credits [[Zap_IDL]] for its range and array syntax. `f16` implementation by ArvidSilverlock.

## Core syntax
```text
option ClientOutput = "src/client/Net.luau"
option ServerOutput = "src/server/Net.luau"

type Health = u8(0..100)

event Damage {
    From: Server,
    Type: Reliable,
    Call: ManyAsync,
    Data: (Target: Instance, Amount: Health)
}

event Aim {
    From: Client,
    Type: Unreliable,          -- 1000-byte cap applies
    Call: SingleSync,
    Data: vector
}
```
- `From`: `Server` | `Client`. `Type`: `Reliable` | `Unreliable`.
- `Call`: `SingleSync`, `ManySync`, `SingleAsync`, `ManyAsync`, `Polling` (iterate with `Event.Iter()`). **Sync listeners must not yield or error.** The docs warn of undefined, game-breaking behavior.
- Types: `u8…u32`, `i8…i32`, `f16`/`f32`/`f64`, bounded strings, `buffer(..900)`, `vector` (with magnitude ranges), type packs `(u8, u16, u32)`, plus structs, enums, maps and more (see docs).

## Generated API
```luau
-- server
local Net = require(game.ServerScriptService.Net)
Net.Damage.FireAll(targetModel, 25)

-- client
local Net = require(game.ReplicatedStorage.Net)
Net.Damage.On(function(target, amount) DamageNumbers.show(target, amount) end)
```

## When to use it (and when not)
- ✅ Combat or shooter games, lots of entities, frequent state sync, bandwidth-sensitive mobile audiences.
- ❌ A jam game with five remotes. The build step and learning curve aren't worth it there.

## Alternatives
[[Zap_IDL]] (similar IDL) · [[ByteNet]] (runtime, no build step) · plain remotes ([[RemoteEvents_and_RemoteFunctions]])

## Related
[[Networking_Libraries_Comparison]] · [[Zap_IDL]] · [[ByteNet]] · [[Buffer_Library]] · [[Bitpacking]] · [[UnreliableRemoteEvent]] · [[Remote_Architecture_Patterns]] · [[Server_Side_Validation]] · [[Rojo]] · [[MOC_Networking_Security_and_Buffers]]

## Sources
- https://github.com/1Axen/blink (README, docs/pages/language/*.mdx)
