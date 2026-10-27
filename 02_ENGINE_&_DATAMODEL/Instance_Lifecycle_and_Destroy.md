---
aliases: [Instance.new, Destroy, Clone, Destroying event, Parent last]
tags:
  - roblox-dev
  - engine/datamodel
type: concept
last_updated: 2026-10-27
status: complete
---
# Instance Lifecycle & `Destroy`

> **TL;DR:** Create with `Instance.new` (or `:Clone()`/`Instance.fromExisting`), **configure fully, then set `Parent` last**, and finish with `:Destroy()`. That locks `Parent` to nil, disconnects all connections on it and its descendants, and fires `Destroying`. Then drop your Lua references so the GC can reclaim it ([[Garbage_Collection]]).

## Create → configure → parent
```luau
local part = Instance.new("Part")
part.Size = Vector3.new(4, 1, 4)
part.Anchored = true
part.CanCollide = false
part.Material = Enum.Material.Neon
part:SetAttribute("Owner", player.UserId)
part.Parent = workspace.Effects      -- last: one replication packet, events fire once
```
Setting `Parent` first means every following property change replicates separately and can fire `Changed` handlers repeatedly. The second argument of `Instance.new(class, parent)` has the same problem, so avoid it.

## Destroy vs Parent = nil vs Remove
| Action | Parent | Connections | Reusable? |
| --- | --- | --- | --- |
| `:Destroy()` | Set to nil **and locked** | Disconnected (self + descendants), `Destroying` fires first | No |
| `.Parent = nil` | nil | **Kept** (leak risk) | Yes, so use it for pooling ([[Object_Pooling]]) |
| `:Remove()` | Deprecated | — | — |
| `Debris:AddItem(obj, t)` | Destroys after `t` seconds | — | Fine for fire-and-forget VFX ([[Client_Side_VFX_Replication]]) |

## Destroying and cleanup
```luau
model.Destroying:Connect(function()
	registry[model] = nil   -- remove from your own tables (connections are auto-cleaned)
end)
```
Under [[Deferred_Events_and_SignalBehavior|deferred events]], handlers queued before a `Destroy` still run, while `:Disconnect()` drops them.

## Character and player lifecycle
Characters get destroyed on respawn (`Players.CharacterAutoLoads`, `Humanoid.Died`). Per-character state must be cleaned up on `CharacterRemoving`/`Destroying` ([[Player_and_Character_Lifecycle]]).

## Clone
`:Clone()` copies descendants and properties (not connections). `Archivable = false` excludes an instance from cloning. Clones start with `Parent = nil`. Under [[Server_Authority_Model|server authority]], clones inside `BindToSimulation` are stitched with deterministic GUIDs.

## Related
[[DataModel_and_Instance_Hierarchy]] · [[Garbage_Collection]] · [[Memory_Leaks]] · [[Connection_Management]] · [[Object_Pooling]] · [[Deferred_Events_and_SignalBehavior]] · [[Player_and_Character_Lifecycle]] · [[Cleanup_Libraries_Trove_Maid_Janitor]] · [[Replication_Model]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/Instance#Destroy
- https://create.roblox.com/docs/scripting/events/deferred
