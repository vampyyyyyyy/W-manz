---
aliases: [ProximityPrompt security, ClickDetector security, Touched exploits, DragDetector security]
tags:
  - roblox-dev
  - security/validation
type: concept
last_updated: 2026-10-27
status: complete
---
# Client-Triggered Instance Security

> **TL;DR:** ProximityPrompts, ClickDetectors, DragDetectors and `Touched` aren't remotes, but exploiters can fire them **from any distance, at any time, ignoring `Enabled`**. Re-validate distance, state and rate on the server in every handler, exactly like a remote ([[Server_Side_Validation]]).

## What the engine does (and doesn't) check
| Instance | Server-side checks | Exploitable |
| --- | --- | --- |
| **ProximityPrompt** | Only `Triggered` has a server distance check | `Enabled`, `MaxActivationDistance`, `RequiresLineOfSight` and `HoldDuration` can be changed client-side. Hold events are accepted even when server `HoldDuration` is 0. `PromptButtonHoldBegan` and `TriggerEnded` have **no** distance check. |
| **ClickDetector** | **None** | Any event, any distance, even when disabled (`MaxActivationDistance = 0`) or parented to something unclickable. |
| **DragDetector** | Drag events respect `Enabled` + `PermissionPolicy` | Inherited ClickDetector events have no checks. Other properties aren't checked. |
| **`BasePart.Touched`** | None beyond physics | Clients firing touches for parts they own. They can also *suppress* touches (e.g. a kill brick never "touches" them) ([[Network_Ownership]]). |

**Network ownership trap:** if the prompt or detector is under an **unanchored** assembly, the exploiter can take ownership and pull it to themselves, which beats your distance check. Anchor interactables, or set ownership to the server.

## Secure handler template
```luau
--!strict
local TokenBucket = require(game.ServerScriptService.TokenBucket)
local openLimiter = TokenBucket.new(3, 5)

local function canInteract(player: Player, part: BasePart, maxDist: number): boolean
	local char = player.Character
	local root = char and char:FindFirstChild("HumanoidRootPart") :: BasePart?
	local hum = char and char:FindFirstChildOfClass("Humanoid")
	if not (root and hum and hum.Health > 0) then return false end
	return (root.Position - part.Position).Magnitude <= maxDist + 4 -- latency slack
end

prompt.Triggered:Connect(function(player: Player)
	if not prompt.Enabled then return end -- server's view of Enabled
	if not openLimiter:allow(player.UserId) then return end
	if not canInteract(player, chestPart, prompt.MaxActivationDistance) then return end
	if ChestState.isLooted(chestPart) then return end
	ChestState.loot(chestPart, player) -- server-side state change
end)
```
For hold interactions, record `PromptButtonHoldBegan` time on the server and require `now - began >= HoldDuration` at `Triggered`.

## Pickups via Touched
Prefer **server-side spatial queries** ([[Spatial_Queries_Overlap]]) or proximity checks on an interval over trusting `Touched` for valuable pickups. If you do use `Touched`, validate that the touching part belongs to a living character close enough on the server.

## Related
[[Server_Side_Validation]] · [[Remote_Rate_Limiting]] · [[Exploit_Threat_Model]] · [[Network_Ownership]] · [[Spatial_Queries_Overlap]] · [[Physics_Engine_and_Assemblies]] · [[Defensive_Design]] · [[Movement_Validation]] · [[MOC_Anti_Exploit]]

## Sources
- https://create.roblox.com/docs/scripting/security/client-server-boundary#securing-client-triggered-instances
