---
aliases: [Lapis, nezuo lapis, Lapis DataStore]
tags:
  - roblox-dev
  - framework/persistence
type: framework
last_updated: 2026-10-27
status: complete
---
# Lapis

> **TL;DR:** Lapis (nezuo) is a DataStore abstraction with **session locking, validation, migrations, retries, throttling (never exceeds budgets), a Promise-based API, immutable (deep-frozen) documents, save batching, 5-minute autosave and BindToClose handling**. It's feature-rich and opinionated. Its README warns it **hasn't been battle-tested in a large production game**, so weigh that against [[ProfileStore]].

## What it is / maintenance status
- Repo: https://github.com/nezuo/lapis (last commit Feb 2025). Inspired by Quicksave (evaera). Install via Wally.

## Why consider it
| Feature | Benefit |
| --- | --- |
| **Built-in migrations** | Versioned schema upgrades on load ([[Data_Versioning_and_Schema_Migration]]) |
| **Validation hook** | Rejects invalid data before saving (NaN, bad shapes) ([[Server_Side_Validation]]) |
| **Immutability** | Updates must be explicit (`document:write(newData)`), so no accidental mutations |
| **Throttling** | Respects DataStore budgets automatically ([[DataStore_Limits_and_Error_Codes]]) |
| Promise API | Composable async flows ([[Promise_Library]]) |

## When not to
If you want the most battle-tested option with a large user base, or a yielding (non-Promise) style, use [[ProfileStore]] ([[DataStore_Libraries_Comparison]]).

## Related
[[ProfileStore]] · [[DataStore_Libraries_Comparison]] · [[Session_Locking]] · [[Data_Versioning_and_Schema_Migration]] · [[Promise_Library]] · [[DataStoreService]] · [[Server_Side_Validation]] · [[Wally]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://github.com/nezuo/lapis (README)
