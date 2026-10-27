# Roblox Dev Knowledge Vault

An Obsidian vault of **300 interlinked, source-cited notes** on production Roblox development, current to **October 2026**. It covers Luau and the compiler, the engine, networking and anti-exploit, UI, tooling and DevOps, game systems (combat, ODM movement, weather, data), performance, and monetization and compliance. Every note follows the same contract: frontmatter, a TL;DR, real Luau examples, at least 8 links, and sources. A linter keeps the graph healthy, and Claude updates the vault on a schedule.

> Start in Obsidian at **[00_MOC/Home.md](00_MOC/Home.md)**, or follow the **[Learning Path](00_MOC/Learning_Path.md)**.

| Folder | Notes | Hub |
| --- | --- | --- |
| `01_LUAU_CORE_&_COMPILER` | 42 | [MOC](00_MOC/MOC_Luau_Core_and_Compiler.md) |
| `02_ENGINE_&_DATAMODEL` | 45 | [MOC](00_MOC/MOC_Engine_and_DataModel.md) |
| `03_NETWORKING_SECURITY_&_BUFFERS` | 31 | [MOC](00_MOC/MOC_Networking_Security_and_Buffers.md) |
| `04_UI_UX_&_COMPONENT_DRIVEN` | 25 | [MOC](00_MOC/MOC_UI_UX_and_Components.md) |
| `05_FRAMEWORKS_TOOLCHAIN_&_DEVOPS` | 31 | [MOC](00_MOC/MOC_Frameworks_Toolchain_and_DevOps.md) |
| `06_GAME_SYSTEMS_&_ALGORITHMS` | 47 | [MOC](00_MOC/MOC_Game_Systems_and_Algorithms.md) |
| `07_PERFORMANCE_OPTIMIZATION_&_PROFILING` | 22 | [MOC](00_MOC/MOC_Performance_and_Profiling.md) |
| `08_MONETIZATION_ANALYTICS_&_COMPLIANCE` | 27 | [MOC](00_MOC/MOC_Monetization_Analytics_and_Compliance.md) |
| `09_RESOURCE_HUB_&_COMMUNITY` | 15 | [MOC](00_MOC/MOC_Resource_Hub_and_Community.md) |
| `00_MOC` | 15 | Home, Learning Path, 9 domain MOCs, 4 cross-cutting (Combat, Movement & ODM, VFX & Weather, Anti-Exploit) |

---

## 1. Open it in Obsidian

You need [Git](https://git-scm.com/downloads) and [Obsidian](https://obsidian.md/download).

**Windows (PowerShell):** run from any folder. The vault lands in `Documents\Roblox Dev Vault`.
```powershell
cd $HOME\Documents
git clone --branch claude/roblox-dev-vault https://github.com/vampyyyyyyy/W-manz.git "Roblox Dev Vault"
```

**macOS / Linux (Terminal):**
```bash
cd ~/Documents
git clone --branch claude/roblox-dev-vault https://github.com/vampyyyyyyy/W-manz.git "Roblox Dev Vault"
```

If the repo is private, Git will ask you to sign in to GitHub (Windows opens a browser window). Then in Obsidian: **Open folder as vault** and pick `Roblox Dev Vault`. If Obsidian asks about plugins, choose **Trust author and enable plugins**.

> The vault currently lives on the `claude/roblox-dev-vault` branch. If you merge it into `main` later, change the **Publishing branch** line in [AGENTS.md](AGENTS.md) so the automation pushes there instead.

**On iPhone / iPad:** install Obsidian, create an empty vault, then install the community **Git** plugin and run its *Clone an existing remote repo* command with `https://github.com/vampyyyyyyy/W-manz.git` and branch `claude/roblox-dev-vault`. Mobile Git needs a GitHub **personal access token** (GitHub ▸ Settings ▸ Developer settings ▸ fine-grained token with *Contents: read and write* on this repo only). Keep the token private. Mobile Git is slower than desktop. If it struggles, the *Working Copy* app can clone the repo into an Obsidian folder instead.

**Graph view tips:** the folders are color-coded (`.obsidian/graph.json`). Filter with `path:06_` to see one domain, and open `Home` to see the hubs.

## 2. Get automatic updates (Obsidian Git)
1. Settings ▸ Community plugins ▸ Browse ▸ install **Git** (by Vinzent03) ▸ Enable.
2. In the Git plugin settings, turn on **Pull on startup**, set **Auto pull interval** to `30` minutes, and set **Auto commit-and-sync interval** to `10` minutes. The last one makes the things you drop in `_Inbox/` reach GitHub so the agent can see them.
3. Edit mainly in `_Inbox/` and let the agent rewrite notes. That avoids merge conflicts with automated updates.

## 3. Feed it (Discord, DevForum, your own ideas)
Agents can't read Discord (it needs your login, and scraping breaks Discord's rules), so **you are the scout**:
1. Create a new note in Obsidian. It lands in `_Inbox/`.
2. Paste the link (Discord message, DevForum thread, video), credit the author, and write one line about what you want to learn.
3. On its next run the agent verifies it, breaks it down, writes or updates notes, archives your raw note, and logs everything in `_System/Changelog.md`.

Full guide: [_System/Inbox_Guide.md](_System/Inbox_Guide.md). Not satisfied with a note? Drop an inbox item saying what's missing, and it gets rewritten as a priority.

## 4. Connect Claude
- **Scheduled research (cloud):** a scheduled task named **"Roblox vault research"** wakes a persistent Claude session, **"Roblox vault maintainer"** (it has this repo attached), every **Monday and Thursday at 19:40 UTC** (mid-afternoon US Eastern time). Each run processes your inbox, verifies `needs-verification` notes, checks Roblox release notes, Luau RFCs and DevForum announcements, updates notes, runs the linter, logs to `_System/Changelog.md`, and pushes to this branch, following [CLAUDE.md](CLAUDE.md) and [AGENTS.md](AGENTS.md). Open that session in the Claude app to read run reports or ask about the vault. To change the cadence, run it now, or pause it, ask Claude or use the app's scheduled tasks.
- **Claude Code on your PC:** run this from the vault folder:
  ```powershell
  cd "$HOME\Documents\Roblox Dev Vault"
  claude
  ```
  Then say, for example: `process my inbox` or `research Server Authority changes and update the vault`. Claude Code reads `CLAUDE.md` automatically.
- **Use the vault while coding a game:** start Claude Code in your game project and add the vault as a second folder, so Claude can consult it:
  ```powershell
  cd "C:\path\to\your\game"
  claude --add-dir "$HOME\Documents\Roblox Dev Vault"
  ```
- **Claude Desktop:** add a filesystem MCP server pointing at the vault (needs [Node.js](https://nodejs.org)). Edit `claude_desktop_config.json` via Settings ▸ Developer ▸ Edit Config:
  ```json
  {
    "mcpServers": {
      "roblox-vault": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\YOU\\Documents\\Roblox Dev Vault"]
      }
    }
  }
  ```
- **Roblox Studio:** connect Claude to Studio itself with the built-in Studio MCP server (Assistant ▸ ⋯ ▸ Manage MCP Servers ▸ Quick connect). See [Roblox_Studio_MCP_Server](05_FRAMEWORKS_TOOLCHAIN_&_DEVOPS/Roblox_Studio_MCP_Server.md).

## 5. Connect ChatGPT
- **Codex (ChatGPT's coding agent):** connect this GitHub repo in Codex and ask it to work on the vault. Codex reads [AGENTS.md](AGENTS.md) automatically, so it follows the same rules and runs the same linter.
- **ChatGPT chat:** enable the **GitHub** connector (ChatGPT Settings ▸ Connectors) and point it at this repo to ask questions about the notes. Menu names change, so check ChatGPT's help if it moved.
- **Inside Obsidian:** community plugins such as *Copilot* or *Smart Connections* can chat with your notes using your own OpenAI (or Anthropic) API key. Keys cost money per use, so keep them private and never commit them.

## 6. Google Drive
- **Don't put this Git folder inside Google Drive sync.** Two sync systems fighting over the same files causes conflicts and corruption. Git (plus Obsidian Git) is the sync layer.
- To use Drive files as research input, either download the file and drop it into `_Inbox/`, or connect the **Google Drive connector** in Claude so Claude can read Drive directly in chats.
- For a Drive backup, export a zip occasionally (GitHub ▸ Code ▸ Download ZIP) and upload it to Drive.

## 7. Maintenance commands
Run these from the vault folder (Python 3.8+):
```bash
python3 _System/scripts/vault_lint.py --stats   # frontmatter, links, orphans; must say 0 error(s)
python3 _System/scripts/vault_lint.py --weak    # notes with few backlinks
```
On Windows, use `py` instead of `python3` if needed. GitHub Actions runs the same linter on every push.

## Note status legend
`complete` = verified against official sources · `needs-verification` = depends on press or a beta, re-check before relying on it · `draft` / `stub` = in progress.

---
Notes cite their sources (Roblox Creator Docs, Luau RFCs, maintainers' repos). Community work is credited to its authors. The `source` file in the repo root is unrelated to the vault and was left untouched.
