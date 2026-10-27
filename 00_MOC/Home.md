---
aliases: [Home, Start, Index, Roblox Dev Vault]
tags:
  - roblox-dev
  - moc/home
type: moc
last_updated: 2026-10-27
status: complete
---
# Roblox Dev Knowledge Vault

> **TL;DR:** An interconnected, source-cited knowledge graph for **production Roblox development**, current to **Oct 2026**. Start with the [[Learning_Path]] or jump into a domain hub. Every note is atomic, cites its sources and links 8+ related notes. The vault is maintained by Claude (scheduled research runs) and any agent that follows `AGENTS.md`, fed by your finds in the `_Inbox`.

## Domain hubs
| # | Hub | Covers |
| --- | --- | --- |
| 01 | [[MOC_Luau_Core_and_Compiler]] | Language, types, runtime, compiler, native codegen |
| 02 | [[MOC_Engine_and_DataModel]] | Instances, scheduler, replication, physics, rendering |
| 03 | [[MOC_Networking_Security_and_Buffers]] | Remotes, validation, anti-exploit, buffers, IDLs |
| 04 | [[MOC_UI_UX_and_Components]] | Layouts, StyleSheets, Fusion/React/Vide, HUDs |
| 05 | [[MOC_Frameworks_Toolchain_and_DevOps]] | Rojo/Script Sync, tooling, CI/CD, Studio MCP, libraries |
| 06 | [[MOC_Game_Systems_and_Algorithms]] | Data, combat, movement, weather, AI, patterns |
| 07 | [[MOC_Performance_and_Profiling]] | Profilers, memory, streaming, parallelism |
| 08 | [[MOC_Monetization_Analytics_and_Compliance]] | Purchases, payouts, analytics, policy & safety |
| 09 | [[MOC_Resource_Hub_and_Community]] | Sources, RFCs, release tracking, quirks, glossary |

## Cross-cutting hubs
[[MOC_Combat_Systems]] · [[MOC_Movement_and_ODM]] · [[MOC_VFX_and_Weather]] · [[MOC_Anti_Exploit]]

## Quick references
[[Glossary]] · [[Engine_Quirks_and_Gotchas]] · [[Legacy_Code_Smells]] · [[Community_Modules_Index]] · [[Luau_RFC_Tracker]] · [[RDC_2026_Recap]]

## How this vault stays fresh
1. You drop finds (Discord showcases, DevForum threads, ideas) into the inbox ([[Inbox_Guide]]).
2. The agent triages them into the [[Research_Queue]], verifies against [[Trusted_Sources]], writes or updates notes, runs the linter, and logs changes in the [[Changelog]].
3. Frontmatter `status` tells you how much to trust a note: `complete` (verified), `needs-verification` (secondary sources, re-check before relying on it), `draft` (in progress), `stub` (placeholder).

## Related
[[Learning_Path]] · [[Trusted_Sources]] · [[Showcase_Breakdown_Method]] · [[Roblox_Studio_MCP_Server]] · [[Release_Notes_and_Change_Tracking]]

## Sources
- Vault structure per the owner's master prompt. Each note cites its own primary sources.
