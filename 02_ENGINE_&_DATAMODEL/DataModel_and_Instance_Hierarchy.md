---
aliases: [DataModel, game, Instance tree, Instance hierarchy, Explorer]
tags:
  - roblox-dev
  - engine/datamodel
type: concept
last_updated: 2026-10-27
status: complete
---
# DataModel & the Instance Hierarchy

> **TL;DR:** Everything in a Roblox place is an **Instance** in one tree rooted at `game` (the `DataModel`). Services sit at the top (`Workspace`, `Players`, `ReplicatedStorage`, …), and every object has exactly one `Parent`. Where an instance lives decides **whether it replicates, renders, simulates and runs scripts** ([[Container_Services_and_Replication_Scope]]).

## Core properties and methods
| Member | Notes |
| --- | --- |
| `Name`, `ClassName`, `Parent` | Names aren't unique. Avoid name-based lookups for gameplay identity, and use attributes or tags instead ([[Attributes]], [[CollectionService_Tags]]) |
| `:FindFirstChild(name, recursive?)` | Returns nil if missing. Recursive search is O(n), so avoid it in hot paths |
| `:WaitForChild(name, timeout?)` | Yields until the child exists. **Always** pass a timeout outside startup code ([[Player_and_Character_Lifecycle]]) |
| `:FindFirstChildOfClass`, `:FindFirstChildWhichIsA`, `:FindFirstAncestorOfClass` | Class-based lookup (`WhichIsA` respects inheritance) |
| `:GetChildren()`, `:GetDescendants()` | Allocate a new array per call |
| `:IsA(class)`, `:IsDescendantOf(x)` | Validation essentials ([[Server_Side_Validation]]) |
| `:GetFullName()` | `"Workspace.Map.Door"`, useful for logs |
| `.ChildAdded`, `.DescendantAdded`, `.AncestryChanged`, `.Destroying` | Lifecycle signals ([[Signals_and_Connections]]) |
| `:GetPropertyChangedSignal(prop)` | Fires only for that property (better than `.Changed`) |

## Mental model
```text
game (DataModel)
├─ Workspace          → 3D world: simulated + rendered (streams with StreamingEnabled)
├─ Players            → Player objects (+ PlayerGui, Backpack, PlayerScripts per player)
├─ Lighting           → sky, atmosphere, post effects
├─ ReplicatedFirst    → first thing clients get (loading screens)
├─ ReplicatedStorage  → shared modules/assets/remotes (replicated, not simulated)
├─ ServerScriptService / ServerStorage → server only, never replicated
├─ StarterGui / StarterPack / StarterPlayer → templates copied per player
└─ SoundService, TextChatService, … (other services)
```

## Gotchas
- **Set `Parent` last** when building instances, because each property change after parenting replicates and fires events ([[Instance_Lifecycle_and_Destroy]]).
- Instances have identity: `a == b` compares references. Names don't.
- `game.Workspace` and `workspace` are the same. `game:GetService("X")` is the safe way to get services ([[Services_Overview]]).
- With [[StreamingEnabled]], parts of `Workspace` may not exist on the client yet. Code must tolerate that.

## Related
[[Instance_Lifecycle_and_Destroy]] · [[Services_Overview]] · [[Container_Services_and_Replication_Scope]] · [[Replication_Model]] · [[Attributes]] · [[CollectionService_Tags]] · [[Signals_and_Connections]] · [[StreamingEnabled]] · [[Script_Types_and_RunContext]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/projects/data-model · https://create.roblox.com/docs/reference/engine/classes/Instance
