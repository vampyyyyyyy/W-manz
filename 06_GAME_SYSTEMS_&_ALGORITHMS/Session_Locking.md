---
aliases: [Session lock, Profile locking, Data locking, LockId]
tags:
  - roblox-dev
  - systems/persistence
type: architecture
last_updated: 2026-10-27
status: complete
---
# Session Locking

> **TL;DR:** Only **one server at a time** may hold a player's data in memory. On load, a server atomically writes a **LockId (GUID) into the key's metadata** inside `UpdateAsync`. Other servers that see a fresh foreign lock wait or retry. The owner refreshes the lock on every autosave and **releases it in the final save**. Locks expire so a crashed server can't hold data forever. This prevents rollback dupes and lost progress ([[Data_Duplication_and_Trade_Exploits]]).

## Why it's needed (official scenarios)
A player leaves server A and joins server B *before A's final save lands*, because:
1. A's save failed and is still retrying.
2. A's save is queued behind throttled requests.
3. Code on `PlayerRemoving` yielded before saving.
4. Server A is lagging badly.
Teleports make this common, and exploiters deliberately abuse it to make actions "not persist" (dupes).

## Algorithm (as in Roblox's `SessionLockedDataStoreWrapper`)
```text
every request → UpdateAsync(key, transform)
transform(value, keyInfo):
  meta = keyInfo.metadata
  if meta.LockId exists, isn't mine, and was refreshed < LOCK_EXPIRY ago → return nil (abort; caller retries later)
  if I previously locked this key but meta.LockId is no longer mine → lock was stolen → fail (stop writing!)
  perform the operation (read, or write new value)
  lock:   meta.LockId = mySessionGuid, meta.LockTime = now
  unlock: meta.LockId = nil            (final save on PlayerRemoving / BindToClose)
  return value, userIds, meta
```
- **Refresh** the lock as part of the autosave loop (or `refreshLockAsync`) well within the expiry window.
- **Expiry** lets another server take over after a crash. The old server must then detect the theft and stop saving.
- On a lock conflict at join, show "loading your data..." and retry with backoff, or kick with a clear message after N attempts.

## Use a library
[[ProfileStore]] (loleris) and [[Lapis]] implement session locking, autosave, release and edge cases. Writing your own is educational. Shipping your own without heavy testing is risky ([[DataStore_Libraries_Comparison]]).

## Works with purchases
Because the in-memory copy is guaranteed fresh, `ProcessReceipt` can check `PurchaseId` history in memory, award, record, save and *then* return `PurchaseGranted` ([[ProcessReceipt_Idempotency]]).

## Related
[[DataStoreService]] · [[UpdateAsync_Patterns]] · [[ProfileStore]] · [[Lapis]] · [[DataStore_Libraries_Comparison]] · [[Data_Duplication_and_Trade_Exploits]] · [[ProcessReceipt_Idempotency]] · [[TeleportService_and_Reserved_Servers]] · [[Player_and_Character_Lifecycle]] · [[MOC_Game_Systems_and_Algorithms]]

## Sources
- https://create.roblox.com/docs/cloud-services/data-stores/player-data-purchasing#session-locking
