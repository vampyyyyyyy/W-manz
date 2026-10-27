---
aliases: [Inventory, Items, Backpack system, Item database, Equipment]
tags:
  - roblox-dev
  - systems/inventory
type: architecture
last_updated: 2026-10-27
status: complete
---
# Inventory Systems

> **TL;DR:** Separate **item definitions** (static, shared, frozen data: name, rarity, stats, icon) from **item instances** (per-player data: unique id, definition id, durability, rolls). The **server owns** inventories inside the session-locked profile. Clients get a replicated **view** and send *intent* ("equip uid X", "move slot 3→7"). Unique ids per instance make trades, audits and dupe detection possible.

## Data model
```luau
--!strict
-- Shared/ItemDefs.luau (frozen, safe to replicate)
export type ItemDef = { read id: string, read name: string, read rarity: "Common" | "Rare" | "Epic" | "Legendary",
	read stackable: boolean, read maxStack: number, read icon: string, read stats: { read [string]: number } }

-- Profile.Data.Inventory (server, persisted)
export type ItemInstance = { uid: string, def: string, count: number, rolls: { [string]: number }?, obtainedAt: number }
export type Inventory = { items: { [string]: ItemInstance }, slots: { [number]: string }, capacity: number }
```
- `uid` via `HttpService:GenerateGUID(false)` at **server** creation time.
- Stackables: one instance with `count`. Uniques (rolled weapons): one instance each.
- Equipment references uids: `equipped = { Weapon = uid }`.

## Operations (server)
| Op | Validation |
| --- | --- |
| Add | Capacity, stack limits, source legitimacy (loot table, purchase receipt) |
| Remove / consume | Ownership by uid, count ≥ n |
| Move / swap slots | Both slots valid, cheap. Debounce spam ([[Remote_Rate_Limiting]]) |
| Equip | Ownership, class restrictions, combat state (no equipping mid-attack) |
| Trade | Atomic two-sided transaction, locked both profiles ([[Data_Duplication_and_Trade_Exploits]]) |
| Sell / craft | Server prices and recipes only |

## Replication to the client
Send a full snapshot on join, then deltas (`added`, `removed`, `changed` by uid) over a reliable remote. The UI renders from the client copy, and the server never reads it back ([[UI_State_Management]], [[Packet_Compression]]).

## Persistence
The inventory lives in the profile ([[ProfileStore]]). Migrations handle definition renames ([[Data_Versioning_and_Schema_Migration]]). Keep an audit log for high-value uids (obtained, traded, deleted).

## Related
[[Data_Duplication_and_Trade_Exploits]] · [[ProfileStore]] · [[Session_Locking]] · [[Data_Versioning_and_Schema_Migration]] · [[Server_Side_Validation]] · [[UI_State_Management]] · [[Paid_Random_Items_Policy]] · [[Developer_Products]] · [[Read_Write_Property_Modifiers]] · [[MOC_Game_Systems_and_Algorithms]]

## Sources
- https://create.roblox.com/docs/cloud-services/data-stores/player-data-purchasing · https://create.roblox.com/docs/scripting/security/client-server-boundary#data-store-manipulation
