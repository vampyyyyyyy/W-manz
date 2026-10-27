---
aliases: [PlayerAdded, CharacterAdded, CharacterAutoLoads, Respawn, WaitForChild race]
tags:
  - roblox-dev
  - engine/players
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Player & Character Lifecycle

> **TL;DR:** Players join, their character spawns and despawns many times, then they leave. Handle **players that joined before your script connected**, **characters that already exist**, and **cleanup on removal**. Most "works in Studio, breaks live" bugs are lifecycle races.

## The canonical server setup
```luau
--!strict
local Players = game:GetService("Players")

local function onCharacterAdded(player: Player, character: Model)
	local humanoid = character:WaitForChild("Humanoid", 10) :: Humanoid?
	if not humanoid then return end
	humanoid.Died:Once(function() --[[ drop combat state, start respawn timer ]] end)
end

local function onPlayerAdded(player: Player)
	-- load data first (session lock) ...
	player.CharacterAdded:Connect(function(char) onCharacterAdded(player, char) end)
	if player.Character then onCharacterAdded(player, player.Character) end  -- already spawned
end

Players.PlayerAdded:Connect(onPlayerAdded)
for _, p in Players:GetPlayers() do task.spawn(onPlayerAdded, p) end      -- joined before us

Players.PlayerRemoving:Connect(function(player)
	-- save + release session lock, clear per-player tables (rate limiters, caches)
end)
game:BindToClose(function()
	-- server shutdown: save everyone (you get a limited time window)
end)
```

## Client side
```luau
local player = game.Players.LocalPlayer
local function setup(char: Model) --[[ bind camera, input, UI to this character ]] end
if player.Character then setup(player.Character) end
player.CharacterAdded:Connect(setup)
```
Scripts in `StarterCharacterScripts` run fresh each spawn. Use them for per-life client logic ([[Script_Types_and_RunContext]]).

## Gotchas
- `WaitForChild` without a timeout can **hang forever**, leaking the thread. Use a timeout in anything except boot code.
- With [[StreamingEnabled]], other players' characters and far parts may not exist on your client. Also, `CharacterAdded` can fire before all descendants have streamed in.
- **Character appearance loads asynchronously.** `CharacterAppearanceLoaded` fires later, and accessories can still arrive afterwards.
- `Players.CharacterAutoLoads = false` → you spawn characters yourself with `player:LoadCharacterAsync()` (the yielding, Async-named API; `LoadCharacterWithHumanoidDescriptionAsync` for custom looks). Use it for lobbies, custom spawn flows and round-based games. It also clears `Backpack` and `PlayerGui`.
- Per-player state keyed by `Player` must be cleared on `PlayerRemoving` ([[Memory_Leaks]]).

## Related
[[Humanoid_and_Character_Model]] · [[Session_Locking]] · [[DataStoreService]] · [[Instance_Lifecycle_and_Destroy]] · [[Memory_Leaks]] · [[StreamingEnabled]] · [[Script_Types_and_RunContext]] · [[Character_Controllers_and_ControllerManager]] · [[Signals_and_Connections]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/Players · https://create.roblox.com/docs/reference/engine/classes/Player#CharacterAdded
