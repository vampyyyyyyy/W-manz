---
aliases: [Replication, FilteringEnabled, What replicates, Client-server model]
tags:
  - roblox-dev
  - engine/replication
type: concept
last_updated: 2026-10-27
status: complete
---
# Replication Model

> **TL;DR:** Roblox is **server-authoritative for Instances and properties**. Changes made on the server replicate to clients, while changes made on a client stay on that client. That's "FilteringEnabled", permanently on. The exceptions are deliberate: **physics of client-owned assemblies**, **animations on your own character**, some sound/input-driven state, and whatever you send through remotes ([[Network_Ownership]], [[RemoteEvents_and_RemoteFunctions]]).

## Rules (official, simplified)
1. An Instance must be **created on the server** to exist for everyone.
2. Most **properties** must be changed on the server to be seen by everyone.
3. An instance replicates to **all clients or none**. Exceptions: [[StreamingEnabled]] (spatial) and per-player containers (`PlayerGui`).
4. Client → server state travels only through **remotes**, **owned physics**, and a few engine-replicated behaviors (e.g. `Animator` tracks played on your own character replicate to others).

## Order and timing
- Property changes and remote events travel on different paths, so **don't assume ordering between them** ([[RemoteEvents_and_RemoteFunctions]]).
- Attribute changes replicate like properties ([[Attributes]]).
- Large instance trees created at runtime are expensive to replicate. Chunk them ([[Network_Bandwidth_Budget]]).

## Client-side "fake" state (and why it's fine)
A client can locally set its own WalkSpeed, delete a wall, or show itself as having 1M coins. **None of that replicates**, except effects through owned physics (moving through the wall). The server must never read client-reported state as truth ([[Exploit_Threat_Model]]).

## Next-gen replication and server authority
`Workspace.NextGenerationReplication` is required by the [[Server_Authority_Model]]. Under server authority, predicted instances sync properties with *simulation access* plus attributes, and mismatches trigger rollback.

## Practical guidance
- **Visual effects:** server sends an event, clients create visuals locally. Don't create VFX parts on the server ([[Client_Side_VFX_Replication]]).
- **Tweening:** tween on clients. Server-side tweens replicate every frame ([[TweenService]]).
- **UI** is always client-side. The server sends data, the client renders it.

## Related
[[Network_Ownership]] · [[Container_Services_and_Replication_Scope]] · [[RemoteEvents_and_RemoteFunctions]] · [[StreamingEnabled]] · [[Attributes]] · [[Server_Authority_Model]] · [[Exploit_Threat_Model]] · [[Client_Side_VFX_Replication]] · [[Network_Bandwidth_Budget]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/scripting/security/access-control#replication
- https://create.roblox.com/docs/projects/client-server
