---
aliases: [Dash, Wall run, Slide, Double jump, Air dash, Movement tech, Parkour]
tags:
  - roblox-dev
  - systems/movement
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Custom Movement Abilities (Dash, Slide, Wall-Run, Double Jump)

> **TL;DR:** Build movement abilities as **states** in a locomotion FSM (or as CCL abilities) that temporarily take over velocity with **mover constraints or controlled velocity writes in PreSimulation**, with server-side cooldowns and movement budgets. The 2026 options are the Humanoid + your FSM, `ControllerManager`, or the beta **Character Controller Library** with declarative abilities and prediction support ([[Character_Controllers_and_ControllerManager]]).

## Recipes
| Ability | Core technique | Details |
| --- | --- | --- |
| **Dash** | Short `LinearVelocity` (0.15–0.25 s) along camera-flat or move direction | `MaxForce` high, restore after. I-frames optional ([[Block_Parry_and_IFrames]]). FOV kick + trail |
| **Slide** | Lower `HipHeight` / crouch anim, friction-like decay `v *= (1 - k·dt)`, boost on slopes | End on low speed or on jump. Ceiling check before standing ([[Raycasting]]) |
| **Wall-run** | Side raycasts detect a wall (normal mostly horizontal), project velocity onto the wall plane, cancel gravity partially for N seconds | Jump off = wall normal + up impulse. Cooldown per wall |
| **Double jump** | Track `airJumps`. On jump while Freefall: `AssemblyLinearVelocity = Vector3.new(v.X, jumpVel, v.Z)` | Reset on landing (`Humanoid.StateChanged` → Landed) |
| **Air dash / glide** | `VectorForce` countering part of gravity + forward thrust | Stamina or gas resource ([[ODM_Gear_System]]) |
| **Ledge grab / mantle** | Forward + down rays find the ledge top. Tween or align the root to the mantle point | Disable collisions briefly to avoid snagging |

## Dash example (client-owned character)
```luau
--!strict
local function dash(root: BasePart, dir: Vector3, speed: number, duration: number)
	local att = root:FindFirstChild("RootAttachment") :: Attachment
	local lv = Instance.new("LinearVelocity")
	lv.Attachment0 = att
	lv.VelocityConstraintMode = Enum.VelocityConstraintMode.Plane      -- horizontal only
	lv.PrimaryTangentAxis = Vector3.xAxis
	lv.SecondaryTangentAxis = Vector3.zAxis
	lv.PlaneVelocity = Vector2.new(dir.X, dir.Z).Unit * speed
	lv.MaxForce = math.huge
	lv.RelativeTo = Enum.ActuatorRelativeTo.World
	lv.Parent = root
	task.delay(duration, lv.Destroy, lv)
end
```
Request it via a remote or InputAction. The server validates cooldown and state, then sets a **movement-budget grace** so validation doesn't flag the burst ([[Server_Authoritative_Cooldowns]], [[Movement_Validation]]).

## Architecture tips
- One **locomotion FSM** (Grounded, Airborne, Sliding, WallRunning, Dashing, Grappling) owns velocity, so abilities never fight each other ([[Finite_State_Machines]]).
- Keep tunables in data: speeds, durations, cooldowns, stamina costs.
- With the CCL, express conflicts declaratively (`ExclusiveGroup = { Name = "Locomotion", Priority = … }`, `Stops`, `Suspends`) and use `TimedLabels` for cooldowns (`OnStop = { DashCooldown = 1.5 }`).
- Test at 30, 60 and 240 FPS. Velocity writes must use `dt` or fixed-step logic ([[Fixed_Timestep_and_Tick_Rate]]).

## Related
[[Character_Controllers_and_ControllerManager]] · [[ODM_Gear_System]] · [[Grappling_Hook_Physics]] · [[Mover_Constraints]] · [[Movement_Validation]] · [[Finite_State_Machines]] · [[Server_Authoritative_Cooldowns]] · [[Humanoid_and_Character_Model]] · [[Fixed_Timestep_and_Tick_Rate]] · [[MOC_Movement_and_ODM]]

## Sources
- https://create.roblox.com/docs/physics/constraints/linear-velocity · https://create.roblox.com/docs/characters/character-controller-library
