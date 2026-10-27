---
aliases: [Release notes, Change tracking, Weekly updates, Pending updates, What changed in Roblox]
tags:
  - roblox-dev
  - community/changes
type: concept
last_updated: 2026-10-27
status: complete
---
# Release Notes & Change Tracking

> **TL;DR:** Roblox ships weekly. The Creator Docs **release notes** split changes into **Current updates** (the latest weekly summary of *live* items), **Current/Recent versions** (numbered pages with "Introduced in version N", including still-pending changes) and **Pending updates** (introduced but not yet live, defaulting to the last 30 days). A change can sit in a version page while **flag-gated** and inactive, so check *weekly updates* for availability. Pair this with DevForum Announcements, the Luau RFC repo and GitHub releases of your tools.

## Tracking stack (what the vault's automation checks)
| Source | Signal | Cadence |
| --- | --- | --- |
| Creator Docs release notes (`Roblox/creator-docs`) | API/engine changes, deprecations | Weekly |
| DevForum Announcements | Betas, policy, payout changes ([[DevForum_Guide]]) | As posted |
| `luau-lang/rfcs` + Luau releases | Language features ([[Luau_RFC_Tracker]]) | Weekly |
| GitHub releases (Rojo, Wally, luau-lsp, Fusion, Jecs, …) | Tool updates ([[Community_Modules_Index]]) | Weekly |
| RDC / newsroom | Platform direction ([[RDC_2026_Recap]]) | Yearly + ad hoc |

## Reading entries correctly
- **Introduced ≠ live.** Flags gate code that has shipped. Rollouts can be partial, and experiments can enable features for a subset ([[Fast_Flags_and_Beta_Features]]).
- Each change belongs to its **earliest** version page, even if it is carried forward.
- Dropping off "Pending" doesn't prove it went live, because the window is time-based.

## Turning changes into vault updates
1. New API or behavior → update the relevant note, bump `last_updated`, cite the release note.
2. Deprecation → add to [[Legacy_Code_Smells]] and the note's gotchas.
3. Limit change (DataStore, MemoryStore, remotes) → update numbers everywhere they appear ([[DataStore_Limits_and_Error_Codes]]).
4. Log it in `_System/Changelog.md`.

## Related
[[Fast_Flags_and_Beta_Features]] · [[Luau_RFC_Tracker]] · [[DevForum_Guide]] · [[Community_Modules_Index]] · [[RDC_2026_Recap]] · [[Legacy_Code_Smells]] · [[Trusted_Sources]] · [[DataStore_Limits_and_Error_Codes]] · [[Deprecated_wait_spawn_delay]] · [[MOC_Resource_Hub_and_Community]]

## Sources
- https://create.roblox.com/docs/releases · https://github.com/Roblox/creator-docs
