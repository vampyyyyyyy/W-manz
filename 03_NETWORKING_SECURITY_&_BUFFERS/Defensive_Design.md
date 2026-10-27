---
aliases: [Security by design, Exploit-proof design, Defensive game design]
tags:
  - roblox-dev
  - security/design
type: concept
last_updated: 2026-10-27
status: complete
---
# Defensive Design

> **TL;DR:** Don't build a feature and then chase cheaters. Design it so cheating is **impossible or worthless**. Detection code is an arms race you lose. A design change ("no points for killing freshly spawned players") deletes the whole exploit category.

## Reactive vs defensive (Roblox examples)
| Exploit | Reactive (weak) | Defensive (strong) |
| --- | --- | --- |
| Kill-farming bots for points | Detect bots | No or reduced points for kills on newly spawned players (also stops spawn-camping) |
| Obby: teleport to the end | Check final position or time | **Mandatory sequential checkpoints**, validated in order server-side (+ time heuristic) |
| Combat: client reports huge damage | Filter impossible values | **Server computes damage** from server-side weapon stats and validates hits by server raycast ([[Damage_Pipeline]], [[Hit_Validation]]) |
| Economy: dupes via rapid requests | Detect duplicate patterns | Server-side cooldowns + validate every transaction against current inventory state ([[Data_Duplication_and_Trade_Exploits]]) |

## Principles
- **Server authority for rules:** prices, stats, inventories and cooldowns live on the server ([[Exploit_Threat_Model]]).
- **Minimize client influence:** clients send *intent*, the server resolves outcomes ([[Remote_Architecture_Patterns]]).
- **Bound everything:** caps per minute, per session, per trade. Diminishing returns kill farm bots ([[Auto_Farm_and_Remote_Spam_Exploits]]).
- **Partition early:** server logic in `ServerScriptService` from day one, never in replicated modules ([[Access_Control_and_Confidentiality]]).
- **Ask the question for every feature:** "How would someone with full control of their client abuse this, and can I change the design so that abuse is impossible or pointless?"

## Related
[[Exploit_Threat_Model]] · [[Server_Side_Validation]] · [[Server_Side_Detection_Heuristics]] · [[Auto_Farm_and_Remote_Spam_Exploits]] · [[Hit_Validation]] · [[Damage_Pipeline]] · [[Data_Duplication_and_Trade_Exploits]] · [[Monetization_Design_Principles]] · [[Combat_System_Architecture]] · [[MOC_Anti_Exploit]]

## Sources
- https://create.roblox.com/docs/scripting/security/defensive-design
