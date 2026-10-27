---
aliases: [Roblox Assistant, Studio Assistant, AI in Studio, Assistant skills, Planning Mode]
tags:
  - roblox-dev
  - devops/ai-tooling
type: concept
last_updated: 2026-10-27
status: complete
---
# Roblox Assistant & AI Tools

> **TL;DR:** **Assistant** is Studio's built-in agent. It answers questions, writes and edits scripts, creates and modifies instances, inserts Creator Store assets, generates materials, meshes and procedural models, and captures screenshots. **Planning Mode** (`/plan`) produces an editable Markdown plan that only runs when you click **Build**. **Skills** are Markdown files that teach it your conventions. External agents (Claude Code, Codex, Cursor) reach Studio through the [[Roblox_Studio_MCP_Server]].

## Features worth knowing
- **Chats:** multiple threads per place, synced to the cloud, with branching from any message. Chats are scoped to the *place*, not the experience.
- **Planning Mode:** plans persist across sessions, are private to you, are editable in a Markdown editor, and *never auto-execute*.
- **Generation:** `/generate_mesh` (text *or* image, optional triangle budget, default 10k, Part as bounding box), `/generate_procedural_model` (50 per rolling 24 h), segmentation into up to 8 named parts, `/segment_mesh` for imported meshes, `/insert_asset`.
- **Screen capture subagent:** "does this lighting look like night?" checks against the viewport.

## Skills
```markdown
---
name: combat-conventions
description: Apply our server-authoritative combat rules when writing or reviewing combat, hitbox or damage code.
enabled: true
---
All damage is computed on the server. Clients only send intent (attack id + aim direction).
Validate every remote argument with typeof + math.isfinite + range checks.
Use task.wait, never wait. Cleanup with Trove.
```
- Skill names are lowercase and unique. The `rbx-` prefix is reserved for Roblox's built-ins.
- Built-ins include `rbx-debug` (breakpoints, call stacks), `rbx-perf-profiling` (MicroProfiler traces), `rbx-scene-analysis` (SceneAnalysisService audits), `rbx-unit-test` (Jest-Lua/TestEZ detection with a fallback harness), `rbx-device-simulator-lua`, `rbx-docs-search` and `rbx-create-skill`.
- Skills belong to your **account**, so they're available in every place you open.

## Using AI well (team rules)
1. AI output is a **draft**. Review it for client trust, deprecated APIs and missing cleanup ([[Exploit_Threat_Model]], [[Deprecated_wait_spawn_delay]], [[Memory_Leaks]]).
2. Make it prove things: playtest via MCP, read the console, profile ([[MicroProfiler]], [[Scene_Analysis_Tool]]).
3. Encode conventions once as skills / `AGENTS.md` instead of repeating them in every prompt.
4. Inserted Creator Store assets can contain scripts. Audit them ([[Third_Party_Code_and_Backdoors]]).

## Related
[[Roblox_Studio_MCP_Server]] · [[Script_Sync]] · [[Testing_Frameworks]] · [[Studio_Debugger]] · [[MicroProfiler]] · [[Scene_Analysis_Tool]] · [[Third_Party_Code_and_Backdoors]] · [[Exploit_Threat_Model]] · [[Deprecated_wait_spawn_delay]] · [[Memory_Leaks]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://create.roblox.com/docs/assistant/guide · https://create.roblox.com/docs/assistant/skills
