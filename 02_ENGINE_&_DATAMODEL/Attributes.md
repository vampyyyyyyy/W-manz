---
aliases: [SetAttribute, GetAttribute, Instance attributes, GetAttributeChangedSignal]
tags:
  - roblox-dev
  - engine/datamodel
type: api
last_updated: 2026-10-27
status: complete
---
# Attributes

> **TL;DR:** Attributes are custom key-value properties on any Instance (`SetAttribute`, `GetAttribute`, `GetAttributes`, `GetAttributeChangedSignal`). They're **saved with the place**, visible in Studio, and they **replicate** like properties when set on the server. They're perfect for configuration and lightweight replicated state (`State = "Stunned"`). Under [[Server_Authority_Model|server authority]], attributes on predicted instances are *the* way to sync custom simulation state.

## Usage
```luau
model:SetAttribute("MaxHealth", 250)
model:SetAttribute("Team", "Red")
model:SetAttribute("State", "Idle")
model:GetAttributeChangedSignal("State"):Connect(function()
	print("state ->", model:GetAttribute("State"))
end)
for name, value in model:GetAttributes() do print(name, value) end
model:SetAttribute("Temp", nil)  -- remove
```

## Supported value types
string, boolean, number, `UDim`, `UDim2`, `BrickColor`, `Color3`, `Vector2`, `Vector3`, `CFrame`, `NumberSequence`, `ColorSequence`, `NumberRange`, `Rect`, `Font`, `EnumItem` (see the Studio properties docs for the current full list). **Not supported:** tables, Instances, functions. Serialize tables to strings if you must (but consider whether a module or remote is more appropriate).

## Replication and security
- Server-set attributes replicate to all clients that can see the instance.
- **Client-set attributes don't replicate.** A client can fake its own copy, so the server never reads client attributes as truth ([[Exploit_Threat_Model]]).
- Exploiters can read every replicated attribute. Don't store secrets or hidden loot rolls on replicated instances ([[Access_Control_and_Confidentiality]]).
- Server authority sync limits: only the **first 64 attributes** of an instance, names ≤ **50 chars**, string values ≤ **50 chars**, and writes only inside `BindToSimulation` on predicted instances.

## Attributes vs alternatives
| Need | Use |
| --- | --- |
| Designer-tunable config on a model | Attributes |
| Cheap replicated state for many instances | Attributes (+ [[CollectionService_Tags]] for "what kind of thing is this") |
| Complex or nested data | Module state + remotes ([[Remote_Architecture_Patterns]]) |
| Legacy `IntValue`/`StringValue` objects | Attributes are lighter and cleaner |

## Related
[[CollectionService_Tags]] · [[DataModel_and_Instance_Hierarchy]] · [[Replication_Model]] · [[Server_Authority_Model]] · [[Signals_and_Connections]] · [[Exploit_Threat_Model]] · [[Access_Control_and_Confidentiality]] · [[Combat_State_Machine]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/scripting/attributes · https://create.roblox.com/docs/studio/properties#instance-attributes
- https://create.roblox.com/docs/projects/server-authority#attribute-limits
