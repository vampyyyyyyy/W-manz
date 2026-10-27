---
aliases: [Confidentiality, What replicates, Script decompilation, Secure teleports]
tags:
  - roblox-dev
  - security/confidentiality
type: concept
last_updated: 2026-10-27
status: complete
---
# Access Control & Confidentiality

> **TL;DR:** Anything that replicates to a client can be read, data-mined and leaked. That includes every LocalScript and every ModuleScript in replicated containers, even unused ones. Keep secrets and server logic in `ServerScriptService` or `ServerStorage`, keep unreleased content out of production, and lock subplaces with **"Secure within universe only"** teleports.

## What clients can read
- Every instance and attribute in replicated containers (`ReplicatedStorage`, `Workspace`, `ReplicatedFirst`, `StarterGui` copies, `Players` …) ([[Container_Services_and_Replication_Scope]]).
- **Decompiled source** of any `LocalScript`, client-`RunContext` Script, or **ModuleScript** they can see, even if it's disabled or never required. Server-only scripts in `ServerStorage` or `ServerScriptService` never replicate, so they can't be decompiled ([[Script_Types_and_RunContext]]).
- **Mixed modules leak server logic.** A `ReplicatedStorage` module with `if RunService:IsServer() then ... end` ships the server branch to every client, hardcoded passwords included. Split client and server code into separate modules.

## Subplace access
- Once in any place of a universe, a client can **teleport to any other place** in it. Disabling *Direct Access* only hides the website Join button.
- Kicking unauthorized users from a subplace **doesn't** stop content from replicating. Replication starts before your kick logic runs.
- **Fix:** Creator Dashboard → place **Access Control** → **"Secure within universe only"**. This allows server-initiated teleports only, so the client never joins and nothing replicates ([[TeleportService_and_Reserved_Servers]]).
- Defense in depth: keep dev and test places in a **separate private universe**, use streaming to limit initial replication ([[StreamingEnabled]]), verify group role, badge or progression server-side and **deny by default** when verification fails, and ban repeat offenders ([[Ban_API_and_Consequences]]).

## Naming and structure
Predictable hierarchies (`ReplicatedStorage.Remotes.GiveMoney`) make exploit scripts easy to write. Use neutral names, centralize networking ([[Remote_Architecture_Patterns]]), and keep the client-visible surface minimal.

## Secrets
API keys and webhooks **never** go in scripts, attributes or DataStores. Use the per-experience secrets store ([[HttpService_and_Secrets_Store]]), which is server-only.

## Related
[[Exploit_Threat_Model]] · [[Container_Services_and_Replication_Scope]] · [[Replication_Model]] · [[Script_Types_and_RunContext]] · [[HttpService_and_Secrets_Store]] · [[TeleportService_and_Reserved_Servers]] · [[StreamingEnabled]] · [[Remote_Architecture_Patterns]] · [[Third_Party_Code_and_Backdoors]] · [[MOC_Anti_Exploit]]

## Sources
- https://create.roblox.com/docs/scripting/security/access-control
- https://create.roblox.com/docs/projects/teleport#configure-secure-teleportation
