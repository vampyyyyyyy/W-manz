---
aliases: [FFlags, Fast flags, Beta features, Studio beta, RolloutState, Feature flags Roblox]
tags:
  - roblox-dev
  - community/flags
type: concept
last_updated: 2026-10-29
status: complete
---
# Fast Flags & Beta Features

> **TL;DR:** Roblox ships code **behind flags** and turns behavior on gradually (and off if it breaks), so availability can differ between Studio, clients and servers during a rollout. Creators interact with this through **Studio ▸ File ▸ Beta Features** (opt-in betas) and **RolloutState-style properties** on services, e.g. `Workspace.UseNewLuauTypeSolver` (`Default` / `Disabled` / `Enabled`) and `Workspace.SignalBehavior`. Internal FFlags are not an API: never depend on them or ask players to change them.

## Betas worth knowing (Oct 2026)
Server Authority graduated to **full release** in 2026 ([[Server_Authority_Model]]).

| Beta | Where | Vault note |
| --- | --- | --- |
| Character Controller Library (`@rbx/AvatarAbilities`) | File ▸ Beta Features | [[Character_Controllers_and_ControllerManager]] |
| Script Sync | File ▸ Beta Features | [[Script_Sync]] |
| New Device Simulator + Network Simulator | File ▸ Beta Features | [[Studio_Testing_Modes]] |
| Upgraded UIGradients / UIShadows | File ▸ Beta Features | [[UI_Appearance_and_Size_Modifiers]] |
| Script Capabilities (client-side) | Beta | [[Script_Capabilities]] |
| `if local` / `if const` syntax (Oct 6, 2026) | Beta | [[If_Local_Bindings]] |

## Rules for production
- **Betas can change or disappear.** Isolate beta-dependent code behind your own feature switch ([[Configs_Remote_Configuration]]).
- Test with the **future default** where one is announced (Deferred events, new type solver) so the flip doesn't break you ([[Deferred_Events_and_SignalBehavior]], [[New_Type_Solver]]).
- A beta enabled in Studio may need publishing settings or rollout to work in live servers, so verify in a live test place.
- **Client FFlag overrides are allowlisted.** Roblox's DevForum announcement "Allowlist for local client configuration via Fast Flags" says the client only honors flags on an official allowlist set through `ClientAppSettings.json`, ignores every other flag, and may change the list at any time. The stated reasons are cheating, abuse and stability. A third-party source dates the rollout to about Sept 29, 2025 (unverified). Staff also said old flags get removed regularly because they "do not want to have to maintain every old code path".
- Still treat the client as hostile. The allowlist reduces flag-based cheats but doesn't make client state trustworthy, so keep authority on the server ([[Exploit_Threat_Model]], [[Server_Authority_Model]]).

## Related
[[Release_Notes_and_Change_Tracking]] · [[Server_Authority_Model]] · [[Script_Sync]] · [[Studio_Testing_Modes]] · [[UI_Appearance_and_Size_Modifiers]] · [[Script_Capabilities]] · [[Configs_Remote_Configuration]] · [[Deferred_Events_and_SignalBehavior]] · [[New_Type_Solver]] · [[Exploit_Threat_Model]] · [[MOC_Resource_Hub_and_Community]]

## Sources
- https://create.roblox.com/docs/releases (flags & availability) · https://create.roblox.com/docs/reference/engine/classes/Workspace
- https://devforum.roblox.com/t/allowlist-for-local-client-configuration-via-fast-flags/3966569 (official allowlist announcement; read via search excerpts)
