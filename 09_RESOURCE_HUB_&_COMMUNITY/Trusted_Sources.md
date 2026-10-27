---
aliases: [Sources, Source ranking, Research sources, Verification policy]
tags:
  - roblox-dev
  - community/sources
type: concept
last_updated: 2026-10-27
status: complete
---
# Trusted Sources (Ranking & Verification Policy)

> **TL;DR:** Facts in this vault are ranked by source. **Tier 1:** official Roblox Creator Docs/API reference and Luau's own docs, RFCs and repo. **Tier 2:** Roblox staff announcements and release notes. **Tier 3:** maintainers' repos and docs for community tools. **Tier 4:** reproducible community benchmarks and tutorials. **Tier 5:** Discord/DevForum showcases, videos and press, used for *inspiration and leads* and verified before becoming "fact". Anything below Tier 3 that isn't independently confirmed gets `status: needs-verification`.

## Tiers
| Tier | Sources | Use for |
| --- | --- | --- |
| 1 | create.roblox.com/docs (+ `Roblox/creator-docs` repo), API reference YAML, luau.org, `luau-lang/rfcs`, `luau-lang/luau` | Limits, signatures, behavior |
| 2 | DevForum **Announcements**, Creator Docs **release notes** ([[Release_Notes_and_Change_Tracking]]), RDC sessions | What changed and when |
| 3 | GitHub repos/docs of Rojo, Wally, Fusion, Jecs, etc. ([[Community_Modules_Index]]) | Tool APIs, maintenance status |
| 4 | DevForum Community Tutorials/Resources with code + benchmarks ([[DevForum_Guide]]) | Patterns, perf claims (re-benchmark: [[Benchmarking_Methodology]]) |
| 5 | Discord showcases ([[Roblox_Discord_Communities]]), YouTube, X, press | Ideas, leads. Break down with [[Showcase_Breakdown_Method]] |

## Rules for agents and humans
1. **Cite** every non-obvious fact in `## Sources` with a URL.
2. **Date-stamp.** Roblox changes weekly. Put the month in prose for numbers that move (limits, rates).
3. **Cross-check** Tier 4–5 claims against Tier 1–3 before marking `complete`.
4. **Prefer behavior over folklore.** "Everyone says X is faster" needs a benchmark.
5. **Never copy exploit code** or private messages. Summarize techniques at the defensive level ([[Exploit_Threat_Model]]).
6. Note **engine quirks** separately from bugs ([[Engine_Quirks_and_Gotchas]], [[Historical_Bugs_and_Outages]]).

## Related
[[DevForum_Guide]] · [[Roblox_Discord_Communities]] · [[Release_Notes_and_Change_Tracking]] · [[Community_Modules_Index]] · [[Showcase_Breakdown_Method]] · [[Benchmarking_Methodology]] · [[Luau_RFC_Tracker]] · [[Engine_Quirks_and_Gotchas]] · [[Exploit_Threat_Model]] · [[MOC_Resource_Hub_and_Community]]

## Sources
- https://create.roblox.com/docs · https://github.com/Roblox/creator-docs · https://luau.org · https://github.com/luau-lang/rfcs
