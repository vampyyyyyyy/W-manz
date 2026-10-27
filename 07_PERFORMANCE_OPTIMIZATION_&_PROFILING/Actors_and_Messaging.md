---
aliases: [Actor, SendMessage, BindToMessage, BindToMessageParallel, GetActor]
tags:
  - roblox-dev
  - performance/parallel
type: api
last_updated: 2026-10-27
status: complete
---
# Actors & Actor Messaging

> **TL;DR:** An `Actor` is a unit of execution isolation. Scripts under it share one thread context, and different actors can run in parallel. Talk to actors asynchronously with **`actor:SendMessage(topic, ...)`**, received by `actor:BindToMessage(topic, fn)` (serial) or **`BindToMessageParallel`** (parallel). Use `script:GetActor()` to find your own actor.

## Setup patterns
- **Actor per entity:** replace an NPC's top-level `Model` with an `Actor` (it inherits Model-like behavior), and put its brain script inside.
- **Worker pool:** N actors under `ServerScriptService.Workers`, each running a generic worker script. A dispatcher round-robins jobs with `SendMessage`.
- **Don't nest actors** unless deliberate. A script belongs to its **closest** ancestor actor.

## Worker pool sketch
```luau
-- Dispatcher (serial, normal Script)
local workers = script.Parent.Workers:GetChildren() -- Actor instances, each with a Worker script
local i = 0
local function dispatch(job: { kind: string, data: any })
	i = i % #workers + 1
	(workers[i] :: Actor):SendMessage("Job", job)
end

-- Worker script (inside each Actor)
local actor = script:GetActor()
local Jobs = require(game.ServerScriptService.Jobs)   -- require during serial init
actor:BindToMessageParallel("Job", function(job)
	local result = Jobs.compute(job)                   -- parallel work
	task.synchronize()
	Jobs.commit(job, result)                           -- serial writes
end)
```

## Notes
- Messages are **copied** like Bindable arguments (no shared identity), except [[SharedTable]]s, which are shared by reference.
- `buffer`s can't be shared across actors, so send copies or use SharedTable ([[Buffer_Library]]).
- Only scripts that are **descendants of an actor** can receive its messages.

## Related
[[Parallel_Luau]] · [[SharedTable]] · [[task_Library]] · [[Bindable_Events_and_Functions]] · [[NPC_Behavior_Trees]] · [[Procedural_Generation]] · [[MicroProfiler]] · [[Buffer_Library]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://create.roblox.com/docs/scripting/multithreading#actor-messaging · https://create.roblox.com/docs/reference/engine/classes/Actor
