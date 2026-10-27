---
aliases: [Studio MCP, Roblox MCP, MCP server, Connect Claude to Studio, Connect Codex to Studio]
tags:
  - roblox-dev
  - devops/ai-tooling
type: api
last_updated: 2026-10-27
status: complete
---
# Roblox Studio MCP Server

> **TL;DR:** Studio ships a **built-in MCP server** (stdio). Enable it at **Assistant ▸ ⋯ ▸ Manage MCP Servers ▸ Enable Studio as MCP server**, then use **Quick connect** for Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, VS Code or Antigravity. Agents can then read and edit scripts, inspect the DataModel, run Luau, **playtest**, read console output and take screenshots. The old `Roblox/studio-rust-mcp-server` repo is no longer actively developed, so use the built-in one.

## Connect
| Method | How |
| --- | --- |
| Quick connect | Assistant Settings ▸ MCP Servers ▸ Quick connect ▸ toggle your client (restart Studio if the client was installed while Studio was open) |
| JSON (Windows) | `"Roblox_Studio": { "command": "cmd.exe", "args": ["/c", "%LOCALAPPDATA%\\Roblox\\mcp.bat"] }` |
| JSON (macOS) | `"Roblox_Studio": { "command": "/Applications/RobloxStudio.app/Contents/MacOS/StudioMCP" }` |
| CLI command | Windows `cmd.exe /c %LOCALAPPDATA%\Roblox\mcp.bat` · macOS `/Applications/RobloxStudio.app/Contents/MacOS/StudioMCP` |

Claude Code manual add (run from a **cmd.exe** prompt on Windows so `%LOCALAPPDATA%` expands):
```bash
claude mcp add Roblox_Studio -- cmd.exe /c %LOCALAPPDATA%\Roblox\mcp.bat          # Windows (cmd)
claude mcp add Roblox_Studio -- /Applications/RobloxStudio.app/Contents/MacOS/StudioMCP   # macOS
```
A green indicator in Manage MCP Servers shows the number of connected clients.

## Tool surface (Oct 2026)
- **Scripts:** `script_read`, `multi_edit` (creates the script if missing; needs `datamodel_type`), `script_search`, `script_grep`
- **DataModel:** `search_game_tree` (flat JSON, filters, depth), `inspect_instance`, `execute_luau`, `get_studio_state`
- **Playtest:** `start_stop_play`, `get_console_output`, `screen_capture`, `character_navigation`, `user_keyboard_input`, `user_mouse_input`
- **Assets/generation:** `search_asset`, `insert_asset`, `generate_mesh`, `generate_material`, `generate_procedural_model`
- **Other:** `http_get`, `skill`, `subagent` (`explore` / `playtest`), `list_roblox_studios`
- Every call takes a **`studio_id`**. Use `list_roblox_studios` when several Studio windows are open.

## Agent workflow that actually works
1. Code lives on disk via [[Script_Sync]] (or [[Rojo]]) and in Git ([[Version_Control_Workflow]]). The agent edits files, and MCP covers what sync can't reach (StarterGui, instances, properties).
2. The agent verifies with a **playtest loop**: `start_stop_play` → `get_console_output` → `screen_capture` → stop. Check `InstanceFileSyncService:GetStatus(script)` to confirm sync.
3. Keep project rules in `CLAUDE.md` / `AGENTS.md`: server authority, remote validation, no deprecated APIs ([[Server_Side_Validation]], [[Deprecated_wait_spawn_delay]]).

## Safety
- "MCP clients can read and modify content in your open Roblox places", so only connect trusted clients.
- `execute_luau` runs with command-bar-level permissions in Edit. Review destructive operations and commit before big agent runs.
- Don't paste API keys or secrets into prompts ([[HttpService_and_Secrets_Store]]).

## Related
[[Roblox_Assistant_and_AI_Tools]] · [[Script_Sync]] · [[Rojo]] · [[Version_Control_Workflow]] · [[Studio_Testing_Modes]] · [[Studio_Debugger]] · [[Testing_Frameworks]] · [[Developer_Console]] · [[Server_Side_Validation]] · [[HttpService_and_Secrets_Store]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://create.roblox.com/docs/studio/mcp · https://create.roblox.com/docs/ai/coding-harness
