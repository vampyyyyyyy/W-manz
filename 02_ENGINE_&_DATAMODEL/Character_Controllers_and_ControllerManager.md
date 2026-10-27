---
aliases: [Character Controller Library, CCL, AvatarAbilities, ControllerManager, GroundController, AirController, Physics controllers]
tags:
  - roblox-dev
  - engine/characters
type: framework
last_updated: 2026-10-27
status: complete
---
# Character Controllers: CCL & ControllerManager

> **TL;DR:** Two layers replace the rigid Humanoid state machine. **`ControllerManager`** with its controllers (`GroundController`, `AirController`, `ClimbController`, `SwimController`) gives you physics-based character movement driven by `MovingDirection`/`FacingDirection`. The **Character Controller Library (CCL)**, a **beta** (`require("@rbx/AvatarAbilities")`), sits on top as a data-driven *ability* system with labels, conditions, conflicts, inputs and replicated state. It's built for [[Server_Authority_Model|server authority]] prediction and maps directly onto dash, slide, wall-run and ODM-style mechanics ([[Custom_Movement_Abilities]], [[ODM_Gear_System]]).

## ControllerManager (physics controllers)
- `ControllerManager.RootPart` + `ActiveController` (Ground, Air, Climb, Swim…) + `GroundSensor`/`ClimbSensor` (`ControllerPartSensor`).
- Set `MovingDirection` (world vector) and `FacingDirection` every frame. Each controller has tunables (e.g. `GroundController.GroundOffset`, `Friction`, acceleration settings, `AirController.MaintainAngularMomentum`).
- You decide which controller is active (your own state machine), so the engine never fights your custom states.

## Character Controller Library (beta, Oct 2026)
**Enable:** *File ▸ Beta Features ▸ AvatarAbilities Character Controller Library*, then *Avatar Settings ▸ Movement ▸ Abilities ▸ Character Controller Library*. Standard abilities (Running, Jumping, Climbing, Swimming, FallingDown/GettingUp…) are on by default. Keep **Running** enabled, and keep **Getting Up** enabled if **Falling Down** is.

**Ability definition** (a Luau table):
| Field | Purpose |
| --- | --- |
| `Name` | Unique id (conditions and conflicts reference it) |
| `Labels`, `TimedLabels` (`OnStart`, `OnStop`, `Consumes`) | Bits on a shared **64-bit mask**, the coordination bus. E.g. `OnStop = { DashCooldown = 2 }` |
| `StartsWhen`, `RunsWhile` | Conditions built with `Rule.All/Any/Not` over labels and **sensors** |
| `Blocks`, `Stops`, `Suspends`, `ExclusiveGroup = { Name, Priority }` | Conflict resolution |
| `Input = { InputName, Mode, Repeats, OutlivesInputWhile, ActionSlot, CustomIcon… }` | `Mode`: `Press` (dash, attack, throw), `Hold`/`Toggle` (sprint, aim, block, crouch, glide), `Hold` + `Repeats`. Never reference the input in `StartsWhen`/`RunsWhile`, because that errors. Wired via the [[Input_Action_System]], with auto touch buttons |
| `Config`, `State` | Read-only config. `State` **replicates and is restored on rollback** |
| `OnSetup/OnStart/OnStop/OnUpdate/OnTeardown(managerCtx, abilityCtx)` | Behavior. `managerCtx` exposes `ControllerManager`, `BodyParts`, `RootCFrame`, `RootLookVector`, … |
Sensors include `Ground`, `IsMoving`, `MoveInput`, `Ceiling`, `Climb`, `Water`/`WaterSurface`, `Sit`, `Tipped`, `Tool`, `LookDirectionInput`.

```luau
local AvatarAbilities = require("@rbx/AvatarAbilities")
local Sensor, Rule = AvatarAbilities.Identifiers.Sensor, AvatarAbilities.Rule

local Dash: AvatarAbilities.AbilityDefinition = {
	Name = "Dash",
	StartsWhen = Rule.All(Sensor.Ground, Rule.Not("DashCooldown")),
	TimedLabels = { OnStart = { Dashing = 0.25 }, OnStop = { DashCooldown = 1.5 } },
	Input = { InputName = "Dash", Mode = "Press", ActionSlot = 5 }, -- Modes: Press | Hold | Hold+Repeats | Toggle
	OnStart = function(managerCtx, abilityCtx)
		-- apply impulse / set ControllerManager directions deterministically
	end,
}
```
**Determinism rule:** abilities register on the server, but callbacks run in **both** the predicted client simulation and the authoritative server simulation. Keep them deterministic (no `math.random` without shared seeds, no wall-clock time) ([[Client_Prediction_and_Reconciliation]]).

## Which to use
| Situation | Choice |
| --- | --- |
| Standard platformer/RPG movement | Default Humanoid ([[Humanoid_and_Character_Model]]) |
| Custom feel, custom states, full control | `ControllerManager` + your own [[Finite_State_Machines|FSM]] |
| Many interacting abilities, prediction, mobile buttons for free | **CCL** (beta: pin behavior with tests, expect API changes) |

## Related
[[Humanoid_and_Character_Model]] · [[Custom_Movement_Abilities]] · [[ODM_Gear_System]] · [[Server_Authority_Model]] · [[Input_Action_System]] · [[Client_Prediction_and_Reconciliation]] · [[Finite_State_Machines]] · [[Mover_Constraints]] · [[Movement_Validation]] · [[MOC_Movement_and_ODM]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/characters/character-controller-library
- https://create.roblox.com/docs/reference/engine/classes/ControllerManager
