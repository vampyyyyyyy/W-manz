---
aliases: [Server authority, AuthorityMode, BindToSimulation, Client prediction (engine), Rollback, SetPredictionMode, Instance stitching]
tags:
  - roblox-dev
  - engine/netcode
type: architecture
last_updated: 2026-10-27
status: needs-verification
---
# Server Authority Model (beta)

> **TL;DR:** Roblox's engine-level netcode for competitive games (**beta, "releasing soon" per the docs as of Oct 2026**). The server is the single source of truth. Clients send only **inputs** (Input Action System), **predict** a few frames ahead, and **roll back + resimulate** on misprediction. It kills speed and fly hacks *by design*, because client-reported positions are never trusted ([[Movement_Validation]], [[Exploit_Threat_Model]]).

## Setup (Workspace)
`AuthorityMode = Server` automatically sets:
1. `NextGenerationReplication = true`
2. `PlayerScriptsUseInputActionSystem = true`
3. `SignalBehavior = Deferred` ([[Deferred_Events_and_SignalBehavior]])
4. `UseFixedSimulation = true` ([[Fixed_Timestep_and_Tick_Rate]])
5. `StreamingEnabled = true` ([[StreamingEnabled]])

## Programming model
```luau
-- ReplicatedStorage/Simulation (ModuleScript), required by BOTH a server Script and a client LocalScript
local RunService = game:GetService("RunService")
local Simulation = {}
function Simulation.Initialize()
	RunService:BindToSimulation(function(dt)
		-- read InputActions for each player, update predicted state (only "Simulation Access" APIs allowed)
		-- write custom state to ATTRIBUTES on predicted instances (synced + rolled back)
	end)
end
return Simulation
```
- **Prediction scope:** by default the engine predicts simulation-access properties near the local character. Override per instance with `RunService:SetPredictionMode()`, and inspect with `GetPredictionStatus()`, `IsResimulating()`, and the `Misprediction`/`Rollback` events.
- **Time:** use `time()`. It's synced and fixed-step, and it rewinds during resimulation. `tick()`, `os.time()` and `os.clock()` aren't synced.
- **Attributes** on predicted instances sync state, with mismatches triggering resimulation. Limits: first 64 attributes, names ≤ 50 chars, string values ≤ 50 chars ([[Attributes]]).
- **Inputs:** all simulation-affecting input goes through **InputActions**. InputContexts must be under the `Player` ([[Input_Action_System]]). Remotes are still fine for discrete events, but they're not ordered with property updates.
- `task.spawn` inside a simulation callback keeps sim restrictions. Use `task.defer` to escape them ([[task_Library]]).
- **Effects** (animations, sounds, VFX) go in **RenderStepped/PreRender**, reading simulation results. Don't cache `AnimationTrack`s across rollbacks: use `Animator:GetTrackByAnimationId()` ([[Animation_System]]).

## Advanced techniques (official)
- **Instance stitching:** `Instance.new`/`Clone`/`fromExisting` inside `BindToSimulation` gets a deterministic GUID (class + source + frame + per-script counter), so the client's predicted instance merges with the server's copy. Parent it before the frame ends.
- **Position smoothing:** render a visual-only clone that follows the invisible simulated object with `TweenService:SmoothDamp`, and only smooth after large jumps (as the Soccer template does) ([[TweenService]]).
- Templates: Racing, Soccer, Laser Tag server-authority places.

## When to adopt
| Game | Recommendation |
| --- | --- |
| Competitive PvP, racing, sports, ODM combat | Prototype on server authority now (beta). Ship when it's out of beta |
| Casual or co-op | Classic client-owned characters + validation is fine |
| Heavy custom physics | Test misprediction rates (MicroProfiler, `Misprediction` events) |

## Related
[[Client_Prediction_and_Reconciliation]] · [[Fixed_Timestep_and_Tick_Rate]] · [[Input_Action_System]] · [[Movement_Validation]] · [[Network_Ownership]] · [[Character_Controllers_and_ControllerManager]] · [[Lag_Compensation]] · [[Attributes]] · [[Exploit_Threat_Model]] · [[MOC_Movement_and_ODM]] · [[MOC_Combat_Systems]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/projects/server-authority · https://create.roblox.com/docs/projects/server-authority/techniques
- https://create.roblox.com/docs/reference/engine/classes/RunService
