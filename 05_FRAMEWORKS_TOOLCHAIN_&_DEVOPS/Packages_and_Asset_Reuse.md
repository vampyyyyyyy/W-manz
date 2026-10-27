---
aliases: [Roblox Packages, PackageLink, Auto-update packages, Asset reuse, Nested packages]
tags:
  - roblox-dev
  - devops/assets
type: api
last_updated: 2026-10-27
status: complete
---
# Packages & Asset Reuse

> **TL;DR:** **Packages** are versioned, shareable instance hierarchies. Right-click ▸ **Convert to Package**, and a `PackageLink` child appears. Enable `PackageLink.AutoUpdate` so copies update when a place is **opened** in Studio, use **Update All** to mass-update copies across a game's places, and nest packages for modular rigs. They're the Studio-side complement to code packages ([[Wally]]/[[Pesde]]), ideal for shared VFX rigs, weather props, UI templates and map kits.

## Rules that bite
- **Never delete or move the `PackageLink`.** That converts the copy back into a normal object.
- **Ownership can't be transferred**, so create group-game packages under the **group**.
- Modifying a copy disables auto-update until you **Publish to Package** or revert. Root name, root position/rotation, `ScreenGui.Enabled` and welds pointing outside don't count as modifications.
- Package scripts are **read-only** until unlocked, and unlocking flags the package as modified.
- **Nested packages:** publish the child before the parent. AutoUpdate only applies at the top-level parent.
- Mass update **saves** places but doesn't **publish** them, and it skips modified copies.

## Configuration pattern
Attributes on the package root become **default configurations**. Each copy can override them, and scripts inside read them at runtime:
```luau
-- Inside a "RainEmitterKit" package
local root = script.Parent
local rate = root:GetAttribute("Rate") or 80          -- copy-specific override
local windScale = root:GetAttribute("WindScale") or 1
```
([[Attributes]], [[Rain_and_Precipitation]])

## Permissions
- **Use & View:** collaborators can insert and see versions. Revoking blocks re-insertion and updates, but existing copies stay.
- **Edit:** collaborators can publish new versions.
- Grant to whole **experiences** by universe ID from the Creator Dashboard.
- Restricted assets inside a package won't render or play unless the target experience has permission.

## Security
Packages from others can contain scripts, so audit them like any third-party asset ([[Third_Party_Code_and_Backdoors]], [[Script_Capabilities]]). Save the place first so you can revert.

## Related
[[Wally]] · [[Pesde]] · [[Version_Control_Workflow]] · [[Attributes]] · [[Third_Party_Code_and_Backdoors]] · [[Script_Capabilities]] · [[Rain_and_Precipitation]] · [[VFX_Composition_and_Timing]] · [[Open_Cloud_Place_Publishing]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://create.roblox.com/docs/projects/assets/packages
