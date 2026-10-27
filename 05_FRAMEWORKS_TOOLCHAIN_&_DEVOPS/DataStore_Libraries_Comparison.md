---
aliases: [DataStore libraries, ProfileStore vs Lapis, DataStore2, Data wrappers]
tags:
  - roblox-dev
  - framework/persistence
type: framework
last_updated: 2026-10-27
status: complete
---
# DataStore Libraries Comparison

> **TL;DR:** For player data, use a **session-locking** library rather than raw DataStore calls. **[[ProfileStore]]** is the default choice: proven at scale, simple yielding API, auto-save, messages. **[[Lapis]]** if you want built-in migrations, validation and immutability, and accept less battle testing. **DataStore2** and the original **ProfileService** are legacy, so migrate new work to ProfileStore. Roblox's own docs also publish a reference implementation (`SessionLockedDataStoreWrapper`) you can study.

## Comparison (Oct 2026)
| Library | Session lock | Auto-save | Migrations | API style | Status |
| --- | --- | --- | --- | --- | --- |
| **ProfileStore** (loleris) | ✔️ | ✔️ | Manual (+`Reconcile`) | Yielding (`StartSessionAsync`) | Stable, widely used |
| **Lapis** (nezuo) | ✔️ | ✔️ (5 min) | ✔️ built-in | Promises, immutable docs | Active-ish. README warns not battle-tested at scale |
| **ProfileService** (loleris) | ✔️ | ✔️ | Manual | Yielding | Superseded by ProfileStore |
| **DataStore2** (Kampfkarren) | ❌ (ordered backups pattern) | ✔️ | Manual | Yielding | Legacy |
| **Roblox reference wrappers** (`DataStoreWrapper`, `SessionLockedDataStoreWrapper`) | ✔️ | your call | your call | Yielding + queues | Official sample code to learn from |
| Raw `DataStoreService` | You build it | You build it | You build it | — | Fine for simple global keys |

## Decision guide
1. Trading, rare items or real-money purchases → **must** have session locking ([[Data_Duplication_and_Trade_Exploits]]).
2. Need cross-server messages to a player's profile (gifts, mail) → ProfileStore `MessageAsync`.
3. Frequent schema churn → Lapis migrations, or your own migration layer on ProfileStore ([[Data_Versioning_and_Schema_Migration]]).
4. Global state (events, pools, leaderboards) → **not** these libraries. Use DataStore keys with `UpdateAsync`, MemoryStores or OrderedDataStores ([[UpdateAsync_Patterns]], [[MemoryStoreService]]).

## Related
[[ProfileStore]] · [[Lapis]] · [[Session_Locking]] · [[DataStoreService]] · [[UpdateAsync_Patterns]] · [[Data_Versioning_and_Schema_Migration]] · [[MemoryStoreService]] · [[Data_Duplication_and_Trade_Exploits]] · [[Ordered_DataStores_and_Leaderboards]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://github.com/MadStudioRoblox/ProfileStore · https://github.com/nezuo/lapis
- https://create.roblox.com/docs/cloud-services/data-stores/player-data-purchasing (official sample wrappers)
