---
aliases: [RTBF, Right to be forgotten, Right to erasure, GDPR deletion, Deletion templates, Erasure webhook]
tags:
  - roblox-dev
  - compliance/privacy
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Right to Erasure (RTBF / GDPR)

> **TL;DR:** When a user asks Roblox to delete their account, **you** (the data controller for your game's data) must permanently delete their personal data. Roblox helps in three ways: a **daily inbox message** listing affected games, **automated DataStore deletion templates** (up to **100**, using a case-sensitive `{UserId}` token, e.g. `User_{UserId}`), and a **creator webhook** ("Right to Erasure Request" trigger) for custom deletion. You stay responsible even with automation, so verify.

## Design for erasure from day one
- **Static key patterns:** `PlayerData` store, key `User_{UserId}` ([[DataStoreService]]). Never key by display name.
- Keep the user ID in the key **name or scope**, so templates can match standard keys, ordered keys and entire standard data stores.
- Know *every* place PII lives: leaderboards ([[Ordered_DataStores_and_Leaderboards]]), MemoryStores ([[MemoryStoreService]]), external DBs/webhooks ([[HttpService_and_Secrets_Store]]), logs, other players' data (friend lists, trade history).

## Automation options
| Option | Use |
| --- | --- |
| Deletion templates (Creator Hub ▸ Configurations ▸ Data stores manager ▸ **RTBF Deletion**, or Open Cloud Configs `user_data_templates`) | Standard/ordered keys and standard stores matching `{UserId}` patterns |
| Creator webhook + your service | Anything else: external DBs, complex schemas. Use Open Cloud DataStore APIs to delete ([[Open_Cloud_APIs]]) |

## Verify webhook authenticity
Set a **secret**. Roblox sends `roblox-signature: t=<timestamp>,v1=<signature>`. Recompute `HMAC-SHA256(secret, "<timestamp>." .. rawBody)` (base64) and compare in constant time. **Reject timestamps older than ~10 minutes** (the docs' suggested replay window). Without verification, anyone who learns your URL can trigger deletions ([[Defensive_Design]]).

## Gotchas
- Group-owned games: only the **group owner** receives requests and can configure the webhook.
- Data-store versions: deletion via API removes the key, but plan for version history retention too ([[Data_Versioning_and_Schema_Migration]]).

## Related
[[DataStoreService]] · [[Ordered_DataStores_and_Leaderboards]] · [[MemoryStoreService]] · [[Open_Cloud_APIs]] · [[HttpService_and_Secrets_Store]] · [[Configs_Remote_Configuration]] · [[Data_Versioning_and_Schema_Migration]] · [[Defensive_Design]] · [[Session_Locking]] · [[MOC_Monetization_Analytics_and_Compliance]]

## Sources
- https://create.roblox.com/docs/production/publishing/RTBF-and-creators · https://create.roblox.com/docs/cloud-services/data-stores/right-to-be-forgotten · https://create.roblox.com/docs/cloud/webhooks/automate-right-to-erasure · https://create.roblox.com/docs/cloud/webhooks/webhook-notifications
