---
aliases: [Backdoors, Free model viruses, Malicious plugins, Toolbox security]
tags:
  - roblox-dev
  - security/supply-chain
type: concept
last_updated: 2026-10-27
status: complete
---
# Third-Party Code & Backdoors

> **TL;DR:** The fastest way to lose a game is a **backdoor**: a hidden server script in a free model or plugin that gives its author server-side code execution. Inspect every script you insert, sandbox third-party models with [[Script_Capabilities]], and never grant `Network`, `DataStore`, `LoadUnownedAsset`, `CapabilityControl` or `LoadString` to code you didn't write.

## How backdoors usually look
- `require(<number>)` with a raw **asset id**. It loads a remote module the attacker can update later, and the capability `LoadUnownedAsset` gates it. Also `AssetService:LoadAssetAsync`.
- `loadstring` with `ServerScriptService.LoadStringEnabled = true`. Keep it **off** ([[Luau_Sandboxing]]).
- Obfuscation: string escapes (`"\114\101..."`), `getfenv` tricks ([[Globals_G_shared_and_getfenv]]), huge files, or **code pushed far right with whitespace** so it's off-screen in the editor.
- Triggers: activates only when a specific UserId joins, on a chat command, after N minutes, or only on live servers (`not RunService:IsStudio()`).
- Plugins can also inject scripts into your place on save. Treat plugin authors with the same suspicion.

## Defense checklist
1. **Prefer packages you control** ([[Packages_and_Asset_Reuse]]) and vendored, reviewed open-source code via [[Wally]] or [[Pesde]] with pinned versions.
2. When inserting from the Creator Store, check the "contains scripts" indicator. **Search the whole place** for `require(`, `getfenv`, `loadstring`, `HttpService`, `TeleportService`, and long numeric literals. The [[Roblox_Studio_MCP_Server]] `script_grep` tool makes this quick to automate.
3. **Sandbox it**: `Workspace.SandboxedInstanceMode = Experimental`, then on the model set `Sandboxed = true` and grant the minimum `Capabilities` ([[Script_Capabilities]]). Roblox says it plans to auto-sandbox Creator Store assets in the future.
4. Audit **plugins**: install from authors you trust, review permissions (script injection, HTTP domains), and remove the ones you don't use.
5. Monitor production: unexpected HTTP traffic, admin panels you didn't build, players with powers they shouldn't have.

## Related
[[Script_Capabilities]] · [[Luau_Sandboxing]] · [[Globals_G_shared_and_getfenv]] · [[Exploit_Threat_Model]] · [[Access_Control_and_Confidentiality]] · [[HttpService_and_Secrets_Store]] · [[Packages_and_Asset_Reuse]] · [[Wally]] · [[Roblox_Studio_MCP_Server]] · [[MOC_Anti_Exploit]]

## Sources
- https://create.roblox.com/docs/scripting/security/third-party-vulnerabilities
- https://create.roblox.com/docs/scripting/capabilities
