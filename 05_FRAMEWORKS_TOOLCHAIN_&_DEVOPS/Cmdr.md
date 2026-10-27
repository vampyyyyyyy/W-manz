---
aliases: [Cmdr, Admin console, Command framework, Developer console commands]
tags:
  - roblox-dev
  - framework/tools
type: framework
last_updated: 2026-10-27
status: complete
---
# Cmdr

> **TL;DR:** Cmdr (evaera) is a **type-safe, extensible command console** for Roblox. Custom commands, argument types, validators, autocomplete and hooks make it ideal for dev tools, moderation and live-ops commands (`give`, `teleport`, `spawn boss`, `set weather`). It's active (Oct 2026). Protect it with **server-side permission hooks**, because every command is a privileged remote.

## Shape
```luau
-- Server: register commands + a permission hook
local Cmdr = require(ReplicatedStorage.Packages.Cmdr)
Cmdr:RegisterDefaultCommands()
Cmdr:RegisterCommandsIn(script.Commands)              -- Command definitions + server implementations
Cmdr.Registry:RegisterHook("BeforeRun", function(context)
	if context.Group == "Admin" and not Admins.isAdmin(context.Executor) then
		return "You don't have permission to run this command."
	end
end)

-- Command definition (Commands/SetWeather.luau)
return {
	Name = "setweather",
	Group = "Admin",
	Args = { { Type = "string", Name = "state", Description = "Clear|Rain|Storm|Snow" } },
}
-- Implementation (Commands/SetWeatherServer.luau)
return function(context, state) Weather.force(state) return `Weather set to {state}` end
```

## Security checklist
- The `BeforeRun` hook must check permissions **on the server**. Never rely on hiding the console UI ([[Exploit_Threat_Model]]).
- Log every privileged command (who, what, when) to analytics or a webhook ([[AnalyticsService_Events]], [[HttpService_and_Secrets_Store]]).
- Treat command arguments like remote input: validate ranges and targets ([[Server_Side_Validation]]).

## Related
[[Exploit_Threat_Model]] · [[Server_Side_Validation]] · [[Ban_API_and_Consequences]] · [[Weather_System_Architecture]] · [[AnalyticsService_Events]] · [[Wally]] · [[Community_Modules_Index]] · [[HttpService_and_Secrets_Store]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://github.com/evaera/Cmdr
