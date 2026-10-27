---
aliases: [Capabilities, Sandboxed, SandboxedInstanceMode, Script sandboxing]
tags:
  - roblox-dev
  - security/sandboxing
type: api
last_updated: 2026-10-27
status: complete
---
# Script Capabilities (Sandboxed Containers)

> **TL;DR:** Mark a Model, Folder or Script as **`Sandboxed`** and give it a `Capabilities` set. Scripts inside can then only touch the APIs and instances you allowed. Use it for third-party models, user-generated code, and libraries that should provably not phone home. *Status: experimental / client beta (Oct 2026).*

## Enable
1. `Workspace.SandboxedInstanceMode` → `Experimental`.
2. On a container: `Sandboxed = true`, then edit `Capabilities` in Properties.

Violations raise errors like `The current thread cannot call 'GetSecret' (lacking capability Network)`.

## Capability groups
| Group | Capabilities |
| --- | --- |
| Execution | `RunClientScript`, `RunServerScript` (ModuleScripts need neither to be required) |
| Instance access | `AccessOutsideWrite`: without it, scripts only see their own container, and events pass `nil` for outside instances |
| Script functionality | `CreateInstances`, `LoadString`, `LoadUnownedAsset` (`require(assetId)`, `LoadAssetAsync`), `ScriptGlobals` (`_G`, `shared`) |
| Engine APIs | `Animation`, `Audio`, `AvatarAppearance`, `AvatarBehavior`, `Basic`, `CSG`, `CapabilityControl`, `Chat`, `Consequences` (kick or ban), `DataStore`, `Environment`, `Input`, `Material`, `Monetization`, `Network` (HTTP), `Physics`, `Players`, `RemoteEvent`, `ServerCommunication` (MessagingService), `Social`, `Teleport`, `UI`, … |

Instances not yet assigned a capability can't be used from a sandbox at all ("lacking capability Unassigned").

## Rules worth remembering
- **Nested containers intersect.** Inner capabilities are limited by outer ones. No overlap means no capabilities.
- `getfenv` and `setfenv` are unavailable inside sandboxes ([[Globals_G_shared_and_getfenv]]).
- Sandboxed code **can't fire** Bindable or Remote events whose container has *more* capabilities than its own. Callbacks run with the capabilities of the code that **registered** them, which makes Bindables the safe bridge ([[Bindable_Events_and_Functions]]).
- Even without `AccessOutsideWrite`, `game`, `workspace` and services are reachable for method calls, but child access is validated.
- `JSONEncode`, `JSONDecode` and `GenerateGUID` need no capability.

## Example use
Insert a free vehicle model, sandbox it with `Basic, Physics, Input, RunServerScript`, and it can still drive. A hidden backdoor inside fails on `require(assetId)` (`LoadUnownedAsset`) and HTTP (`Network`) ([[Third_Party_Code_and_Backdoors]]).

## Related
[[Third_Party_Code_and_Backdoors]] · [[Luau_Sandboxing]] · [[Exploit_Threat_Model]] · [[HttpService_and_Secrets_Store]] · [[Bindable_Events_and_Functions]] · [[Globals_G_shared_and_getfenv]] · [[Ban_API_and_Consequences]] · [[Script_Types_and_RunContext]] · [[MOC_Anti_Exploit]]

## Sources
- https://create.roblox.com/docs/scripting/capabilities
