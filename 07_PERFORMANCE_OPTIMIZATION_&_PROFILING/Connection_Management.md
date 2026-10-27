---
aliases: [Disconnect, Connection cleanup, RBXScriptConnection management, Event cleanup]
tags:
  - roblox-dev
  - performance/memory
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Connection Management

> **TL;DR:** Every `:Connect` returns a connection that keeps its callback, and everything that callback captures, **alive until it's disconnected** or the instance is **destroyed**. Group connections by **lifetime** (session, character life, UI screen open, ability active) and clean up each group at its end, using a cleanup object (Trove/Maid/Janitor) or a plain array.

## Patterns
```luau
--!strict
-- 1) Lifetime bag (no library)
local function bag()
	local conns: { RBXScriptConnection } = {}
	return {
		add = function(c: RBXScriptConnection) table.insert(conns, c) return c end,
		clean = function()
			for _, c in conns do c:Disconnect() end
			table.clear(conns)
		end,
	}
end

-- per-character lifetime
player.CharacterAdded:Connect(function(char)
	local life = bag()
	local hum = char:WaitForChild("Humanoid") :: Humanoid
	life.add(RunService.Heartbeat:Connect(function(dt) updateStamina(char, dt) end)) -- long-lived signal!
	life.add(hum.HealthChanged:Connect(onHealth))
	char.Destroying:Once(life.clean)          -- or hum.Died / CharacterRemoving
end)

-- 2) One-shots
humanoid.Died:Once(onDied)                    -- auto-disconnects after first fire
```

## Rules
- **Long-lived source + short-lived listener = must disconnect** (`RunService`, `Players`, `UserInputService`, module-level signals).
- Connections **on** an instance die with `:Destroy()` of that instance. Connections **to services** don't.
- Avoid connecting inside loops or frequently called functions without a matching disconnect. Search your code for `:Connect(` inside functions that run per hit or per frame.
- Use the cleanup libraries for complex lifetimes ([[Cleanup_Libraries_Trove_Maid_Janitor]]).
- Under [[Deferred_Events_and_SignalBehavior|deferred events]], `Disconnect` drops pending invocations, while `Destroy` still runs them.

## Related
[[Memory_Leaks]] · [[Signals_and_Connections]] · [[Cleanup_Libraries_Trove_Maid_Janitor]] · [[Instance_Lifecycle_and_Destroy]] · [[Player_and_Character_Lifecycle]] · [[Deferred_Events_and_SignalBehavior]] · [[Closures_and_Upvalues]] · [[Garbage_Collection]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://create.roblox.com/docs/reference/engine/datatypes/RBXScriptConnection · https://create.roblox.com/docs/scripting/events/deferred
