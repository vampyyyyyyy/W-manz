# CLAUDE.md

@AGENTS.md

## Claude-specific instructions

You are the vault's primary maintainer. Everything in `AGENTS.md` applies. This file adds how to research and run reliably from Claude Code (cloud scheduled runs or the owner's PC).

### Research mechanics
The cloud environment's network policy may block some sites (for example Google Drive, or direct page fetches from devforum.roblox.com). Never try to bypass the proxy or disable TLS. Use these routes instead:

1. **Official docs as source:** shallow, sparse clone of the Creator Docs repo (Markdown and API YAML only):
   ```bash
   git clone --depth 1 --filter=blob:none --sparse https://github.com/Roblox/creator-docs.git /tmp/creator-docs
   git -C /tmp/creator-docs sparse-checkout set --no-cone 'content/en-us/**/*.md' 'content/en-us/**/*.yaml'
   # pages: /tmp/creator-docs/content/en-us/<area>/<page>.md
   # API:   /tmp/creator-docs/content/en-us/reference/engine/classes/<Class>.yaml
   # release notes overview: content/en-us/releases.md
   ```
2. **Luau:** `git clone --depth 1 https://github.com/luau-lang/rfcs.git` (status lines live in `docs/*.md`), plus `luau-lang/luau` and `luau-lang/site` for docs.
3. **Community tools:** clone shallowly and read README/CHANGELOG. Get maintenance status with `git log -1 --format=%cs`.
4. **News, DevForum, RDC:** `WebSearch` (standard mode first, extended for very recent or niche topics). Cite the URLs. Press-only claims mean `status: needs-verification`.
5. Record verified numbers with their date in the note itself (and in the Changelog when they change).

### Verification with Roblox Studio (when running on the owner's PC)
If the Studio MCP server is connected (`Roblox_Studio` in your MCP list), test code examples before marking a note `complete`: use `execute_luau` for pure logic, or `start_stop_play` + `get_console_output` for runtime behavior. Mention "tested in Studio (date)" in the note. Never run destructive operations in the owner's open places. Use a scratch baseplate.

### Run budget & behavior
- Order: inbox → P1 queue → change sweep → P2/P3. Stop when the remaining work would be rushed. Depth beats count.
- Typical scheduled run: process all inbox items, then up to about 10 queue items or 15 note edits.
- Keep the linter at `0 error(s)` before committing. If a fix isn't possible this run, revert that partial note rather than committing broken links.
- Push to the publishing branch named in `AGENTS.md`, retrying network failures with exponential backoff (2s, 4s, 8s, 16s). Never force-push.
- End with a short report: notes added/updated, facts that changed, questions for the owner.

### Owner preferences (summary)
High-school Roblox developer: Luau combat systems, VFX, weather, ODM movement, UI, optimization. They want specific, production-quality, server-authoritative guidance, honest uncertainty labels, and no generic filler. If the inbox says a note isn't good enough, rewrite it properly with deeper research and working examples.
