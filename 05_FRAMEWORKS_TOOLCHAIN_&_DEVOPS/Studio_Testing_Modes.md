---
aliases: [Playtest, Test vs Run, Server and Clients, Team Test, Network Simulator, StudioTestService]
tags:
  - roblox-dev
  - toolchain/testing
type: concept
last_updated: 2026-10-27
status: complete
---
# Studio Testing Modes

> **TL;DR:** **Test (F5)** and **Test Here** run separate client and server simulations, which you can flip between with the Client/Server toggle. **Run (F8)** runs the server without a character. **Server & Clients** launches up to **8** client windows for replication and multiplayer bugs. **Team Test** brings in collaborators. **Network Simulator** (beta) adds latency, jitter and loss per direction, and it's essential for [[Server_Authority_Model]] prediction and [[UnreliableRemoteEvent]] testing. Scripted testing services (`StudioTestService`, `StudioDeviceSimulatorService`, `VirtualInput`) automate it all.

## Pick the right mode
| Bug type | Mode |
| --- | --- |
| UI, input, local VFX | Test (client view, blue border) |
| Server state, ServerStorage, physics ownership | Toggle to **Server** view (green border) |
| "Other players see it wrong", replication, ownership | **Server & Clients** (2+ clients) ([[Replication_Model]], [[Network_Ownership]]) |
| Party features | Party Simulator (simulated `PartyId`, `SocialService:GetPartyAsync`) |
| Real-latency combat feel | **Network Simulator** presets + Server & Clients ([[Lag_Compensation]]) |
| Phones/consoles/VR | Device Simulator + Controller Emulator. VR via OpenXR (Windows) |
| Localization/policy | Player Emulator (test profile) ([[PolicyService_Compliance]]) |

## Network Simulator presets (inbound / outbound: latency, jitter, loss)
- Wired Broadband: 25 ms, 3 ms, 0% each way
- Home Wi-Fi: 30 ms / 12 ms / 0.2% in, 30 ms / 15 ms / 0.3% out
- 4G/LTE: 45 ms / 20 ms / 0.4% in, 55 ms / 30 ms / 0.5% out
- Bad 3G: 150 ms / 70 ms / 0.5% in, 180 ms / 90 ms / 0.5% out

Values **add** to real conditions (important in Team Test). Enable via Beta Features ▸ *New Device Simulator*, then Test ▸ Device Simulator ▸ **Network** pill.

## Pause & step
Pause/Resume can target client, server or both. Step Forward advances 1/60 s. Only PreAnimation, PreSimulation, PostSimulation and Stepped pause. PreRender, Heartbeat and RenderStepped keep firing ([[RunService_Frame_Events]]). That's great for frame-by-frame inspection of hit frames and VFX timing ([[Hitstop_and_Impact_Feel]]).

## Automation
- `StudioTestService`: start a server with up to 8 clients, add players mid-test, pass args, trigger disconnects, end from the server. Good for join/leave stress and [[Session_Locking]] tests.
- `StudioDeviceSimulatorService`: cycle device presets and orientation for UI regression ([[Responsive_UI_and_Safe_Areas]]).
- `VirtualInput` (`UserInputService:CreateVirtualInput()`): scripted input processed like real hardware for end-to-end UI flows.
- Studio CLI: `--task RunScript --runScriptFile smoke.luau --outputFile out.log --quitAfterExecution` ([[GitHub_Actions_CI_CD]]).
- AI agents: playtest through `start_stop_play` + `get_console_output` ([[Roblox_Studio_MCP_Server]]).

## Related
[[Studio_Debugger]] · [[Testing_Frameworks]] · [[Roblox_Studio_MCP_Server]] · [[Replication_Model]] · [[Network_Ownership]] · [[Server_Authority_Model]] · [[UnreliableRemoteEvent]] · [[Lag_Compensation]] · [[RunService_Frame_Events]] · [[Session_Locking]] · [[Responsive_UI_and_Safe_Areas]] · [[GitHub_Actions_CI_CD]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://create.roblox.com/docs/studio/testing-modes · https://create.roblox.com/docs/studio/network-simulator · https://create.roblox.com/docs/studio/cli
