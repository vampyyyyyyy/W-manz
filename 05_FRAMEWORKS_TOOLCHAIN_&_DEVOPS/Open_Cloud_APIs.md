---
aliases: [Open Cloud, Roblox web APIs, API keys, OAuth 2.0, apis.roblox.com, rbxcloud]
tags:
  - roblox-dev
  - devops/open-cloud
type: api
last_updated: 2026-10-27
status: complete
---
# Open Cloud APIs

> **TL;DR:** Open Cloud is Roblox's **stable, officially supported REST API** (`apis.roblox.com`, API keys or OAuth 2.0) for automating your games from outside Roblox: DataStores and MemoryStores, MessagingService publishing, place publishing, assets, **user restrictions (bans)**, secrets, configs, notifications, developer products and game passes, Creator Store, and **Luau Execution** (run Luau against a place). Avoid legacy cookie-auth web APIs for production.

## Auth
- **API keys** (Creator Dashboard ▸ Open Cloud ▸ API Keys): scoped per API, operation and experience, with optional IP allowlists and expiry. Store them as **secrets** in CI, never in Git.
- **OAuth 2.0** for apps acting on behalf of users (third-party tools).
- Every request: `x-api-key: <key>` header.

## High-value endpoints for game teams
| Area | Use |
| --- | --- |
| DataStores / OrderedDataStores / MemoryStores | Admin panels, support tools (restore a profile version), migrations, **right-to-erasure** deletion ([[Right_to_Erasure_GDPR]]) |
| Messaging | Publish to live servers (announcements, events) ([[MessagingService_Cross_Server]]) |
| Place publishing | CI/CD deploys ([[Open_Cloud_Place_Publishing]]) |
| **Luau Execution** | Run Luau tasks against a place version and read logs (CI tests, batch jobs) ([[Testing_Frameworks]]) |
| User restrictions | Bans from moderation bots and dashboards ([[Ban_API_and_Consequences]]) |
| Secrets, Configs | Manage secrets and live config values ([[HttpService_and_Secrets_Store]], [[Configs_Remote_Configuration]]) |
| Dev products / game passes | Create and update monetization items in bulk ([[Developer_Products]], [[Game_Passes]]) |
| Notifications | Experience notifications to opted-in users ([[Experience_Notifications]]) |
| Webhooks | Refunds, subscription changes, erasure requests pushed to your server |

## Rate limits & budgets
Per-endpoint limits per API key owner, and **DataStore budgets are shared with live game servers**. Rate-limit your tools (leaky bucket) so admin scripts don't starve production ([[DataStore_Limits_and_Error_Codes]]). Some endpoints are also callable **from game servers** via HttpService (2,500 req/min per server, only the `x-api-key` and `content-type` headers).

## Tooling
- `rbxcloud` CLI and library (Sleitnick, Rust) for deployments, DataStore debugging and erasure handling.
- [[Lune]] scripts for Luau-native automation. OpenAPI descriptions for Postman or codegen.

## Related
[[Open_Cloud_Place_Publishing]] · [[GitHub_Actions_CI_CD]] · [[DataStore_Limits_and_Error_Codes]] · [[MessagingService_Cross_Server]] · [[Ban_API_and_Consequences]] · [[Right_to_Erasure_GDPR]] · [[HttpService_and_Secrets_Store]] · [[Lune]] · [[Testing_Frameworks]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://create.roblox.com/docs/cloud · https://create.roblox.com/docs/cloud/auth/api-keys
- https://create.roblox.com/docs/cloud-services/http-service#supported-endpoints · https://github.com/Sleitnick/rbxcloud
