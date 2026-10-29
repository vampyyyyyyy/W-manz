---
aliases: [Humanoid, HumanoidRootPart, R15, R6, HumanoidStateType, WalkSpeed]
tags:
  - roblox-dev
  - engine/characters
type: api
last_updated: 2026-10-29
status: complete
---
# Humanoid & the Character Model

> **TL;DR:** A character is a `Model` with a `HumanoidRootPart` (the assembly root, ownership anchor and physics body), body parts joined by `Motor6D`s (R15: 15 parts, R6: 6 parts), and a `Humanoid` that runs the built-in state machine (walking, jumping, falling, climbing, swimming, ragdoll, dead), health and movement. For custom movement, the modern path is **physics controllers** or the new **Character Controller Library** ([[Character_Controllers_and_ControllerManager]]).

## Key members
| Member | Notes |
| --- | --- |
| `Health`, `MaxHealth`, `HealthChanged`, `Died`, `:TakeDamage(n)` | `TakeDamage` respects `ForceField`. Use your own [[Damage_Pipeline]] for armor and i-frames |
| `WalkSpeed`, `JumpPower`/`JumpHeight` (`UseJumpPower`) | **Client-writable on owned characters**, so validate on the server ([[Movement_Validation]]) |
| `MoveDirection`, `:Move(dir, relativeToCamera?)` | Read input intent and drive NPCs |
| `:GetState()`, `:ChangeState(state)`, `:SetStateEnabled(state, bool)`, `StateChanged` | `Enum.HumanoidStateType`. Disable states you replace (e.g. `Climbing`, `Ragdoll`) |
| `HipHeight`, `AutoRotate`, `PlatformStand`, `Sit` | Fine control over posture |
| `FloorMaterial` | Footsteps, surface effects ([[Wetness_Puddles_and_Drying]]) |
| `Humanoid.Animator` (child) | Animation playback and replication ([[Animation_System]]) |
| `HumanoidDescription`, `:ApplyDescription()` | Avatar appearance |
| `EvaluateStateMachine` | `false` to stop the Humanoid's state logic when a custom controller takes over |

## Character anatomy
```text
Character (Model, PrimaryPart = HumanoidRootPart)
├─ HumanoidRootPart   (invisible box: physics root, network ownership, CFrame of the character)
├─ Humanoid           (+ Animator)
├─ Head, UpperTorso, LowerTorso, Left/RightUpperArm ... (R15)  joined via Motor6D
└─ Accessories (welded), clothing, scripts from StarterCharacterScripts
```

## R6 games: `AvatarUnificationMode` is being removed (Dec 1, 2026)
- `Workspace.AvatarUnificationMode` turns on the **R6-to-R15 adapter**: R15 avatars join R6 games with invisible, R6-named adapter parts welded on, so they keep R6 scale and movement but gain layered clothing and animated heads. It's `NotScriptable` and only matters when the avatar type is R6 (API reference, Oct 2026).
- **Official (staff "Weekly Recap: October 19–23, 2026"):** the property is a planned deprecation. If your game or tooling depends on it, **test and update before Dec 1, 2026**. Roblox hasn't said what replaces it or what the post-Dec 1 default will be (as of Oct 29, 2026). A staff reply in May 2026 mentioned "a more appropriate feature".
- **What to check in an R6 combat game:** hitboxes and raycasts that assume exactly 6 parts, or that find limbs by name ("Left Arm", "Torso") ([[Hitbox_Detection_Methods]]), code that iterates `GetChildren()` on the character and trips over adapter parts, and ragdoll rigs that rebuild joints ([[Knockback_and_Ragdoll]]). Test in a copy of the place with the adapter both on and off before the date.

## Gotchas
- `Humanoid` internals are expensive at scale. **NPC crowds** should use light rigs, server-side simplification, or controllers without full Humanoids ([[Physics_Optimization]]).
- Respawn creates a **new** character. Don't cache Humanoid references across lives ([[Player_and_Character_Lifecycle]]).
- `Died` fires once per Humanoid. Health 0 doesn't always mean "dead" if you've disabled the `Dead` state.

## Related
[[Character_Controllers_and_ControllerManager]] · [[Animation_System]] · [[Player_and_Character_Lifecycle]] · [[Movement_Validation]] · [[Damage_Pipeline]] · [[Custom_Movement_Abilities]] · [[Knockback_and_Ragdoll]] · [[Network_Ownership]] · [[Physics_Engine_and_Assemblies]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/Workspace#AvatarUnificationMode · https://create.roblox.com/docs/characters/r6-to-r15-adapter
- https://devforum.roblox.com/t/weekly-recap-october-19%E2%80%9323-2026/4953263 (planned deprecation, Dec 1, 2026; read via search excerpts)
- https://create.roblox.com/docs/reference/engine/classes/Humanoid · https://create.roblox.com/docs/characters
