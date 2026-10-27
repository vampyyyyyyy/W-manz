---
aliases: [typeof, type(), type vs typeof, IsA]
tags:
  - roblox-dev
  - luau/types
type: concept
last_updated: 2026-10-27
status: complete
---
# `typeof` vs `type`

> **TL;DR:** `type(x)` returns the **Luau** type, so every Roblox value is just `"userdata"`. `typeof(x)` returns the **Roblox** type name (`"Vector3"`, `"Instance"`, `"CFrame"`, `"EnumItem"`…). For Instances, follow up with `x:IsA("ClassName")`. On the server, use `typeof` + `IsA` to validate remote input ([[Server_Side_Validation]]).

## Comparison
| Value | `type(v)` | `typeof(v)` |
| --- | --- | --- |
| `5` | `number` | `number` |
| `"hi"` | `string` | `string` |
| `{}` | `table` | `table` |
| `Vector3.zero` | `userdata` | `Vector3` |
| `workspace.Part` | `userdata` | `Instance` |
| `Enum.Material.Plastic` | `userdata` | `EnumItem` |
| `buffer.create(1)` | `buffer` | `buffer` |
| `vector.create(1,2,3)` | `vector` | `Vector3` (Roblox maps the native vector to `Vector3`) |

## Validation recipe
```luau
local function isPartIn(x: unknown, container: Instance): boolean
	return typeof(x) == "Instance" and (x :: Instance):IsA("BasePart") and (x :: Instance):IsDescendantOf(container)
end
```
- **Spoofed Instances:** an exploiter can send `{ ClassName = "Part" }`. `typeof` returns `"table"`, so the check fails correctly. Checking `x.ClassName == "Part"` would be fooled ([[Server_Side_Validation]]).
- `IsA` respects inheritance (`Part:IsA("BasePart")` is true). `ClassName ==` doesn't.

## Type-system interplay
Both `type(x) == "..."` and `typeof(x) == "..."` act as **refinements** in the analyzer ([[Type_Refinements]]). Under native codegen, `type(x) == "number"` compiles to a cheap tag check (2025 optimization: [[Native_Code_Generation]]).

## Related
[[Type_Refinements]] · [[Server_Side_Validation]] · [[Luau_Type_System]] · [[Vector_Library]] · [[Buffer_Library]] · [[Native_Code_Generation]] · [[DataModel_and_Instance_Hierarchy]] · [[Exploit_Threat_Model]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://create.roblox.com/docs/reference/engine/globals/RobloxGlobals#typeof
- https://luau.org/news/2025-12-19-luau-recap-runtime-2025
