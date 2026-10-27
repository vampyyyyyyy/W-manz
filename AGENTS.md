# AGENTS.md: Rules for any AI agent working on this vault

This repository is an **Obsidian knowledge vault for production Roblox development** (Luau, engine, networking/security, UI, tooling, game systems, performance, monetization/compliance, community). Claude, ChatGPT/Codex, and any other agent must follow these rules exactly. Humans should too.

- **Publishing branch:** `claude/roblox-dev-vault`. Commit and push vault updates here. If the owner merges the vault into another branch and wants agents to follow, they change this line.
- **Owner's focus:** combat systems, VFX, weather, ODM/movement, UI, optimization, debugging, game architecture. Prioritize depth there.

## 1. Layout

| Path | Contents |
| --- | --- |
| `00_MOC/` | Hubs: `Home`, `Learning_Path`, one MOC per domain, cross-cutting MOCs (Combat, VFX & Weather, Movement & ODM, Anti-Exploit) |
| `01_LUAU_CORE_&_COMPILER/` … `09_RESOURCE_HUB_&_COMMUNITY/` | Content notes (one topic per note) |
| `_Inbox/` | Raw finds dropped by the owner. **Process first.** Ignore files starting with `_` |
| `_System/Templates/` | Note templates (`Concept`, `API`, `Framework`, `Code_Pattern`, `Forum_Archive`, `Architecture`, `MOC`) |
| `_System/Research_Queue.md` | Prioritized backlog |
| `_System/Changelog.md` | Run log (newest first) |
| `_System/Inbox_Archive/YYYY-MM/` | Processed inbox items (raw, never linked to) |
| `_System/scripts/vault_lint.py` | The linter. Must pass before every commit |
| `source` | Unrelated legacy file. **Never read, run, modify or delete it** |

## 2. Note contract (enforced by the linter)

### File names
`Title_Case_With_Underscores.md`, unique across the whole vault. Obsidian resolves `[[Links]]` by file name, so duplicates break links.

### Frontmatter (exact keys, YAML)
```yaml
---
aliases: [Alternate name, Common search term]
tags:
  - roblox-dev
  - category/subcategory        # at least one tag containing "/"
type: concept                   # concept | api | framework | code-pattern | forum-archive | architecture | moc
last_updated: 2026-10-27        # YYYY-MM-DD, bump on every substantive edit
status: complete                # complete | needs-verification | draft | stub
---
```
- `complete`: every non-obvious claim is backed by a Tier 1–3 source.
- `needs-verification`: relies on secondary sources or a beta that may change. Say what's unverified in the note.
- `draft` / `stub`: work in progress. Only allowed when the queue explicitly says so.

### Body
1. `# Title`
2. `> **TL;DR:**` one to three sentences with the key facts and numbers.
3. Sections with real substance: how it works, Luau examples, gotchas, performance and security notes, decision tables.
4. `## Related`: links, including the folder's MOC.
5. `## Sources`: URLs (official docs first).

### Links
- **8–15 distinct `[[WikiLinks]]` to existing content notes** per note, placed in context where possible, not only in Related.
- Link to **file names**, never aliases. Use `[[File_Name|display text]]` for different wording.
- No ghost links: every target must exist. Create the note first or rephrase.
- **No orphans:** every note needs at least one backlink. Add every new note to its folder MOC (`00_MOC/MOC_*`) and, if relevant, a cross-cutting MOC.
- Wikilinks inside code blocks are ignored by the linter (Luau `[[ ]]` strings are safe).

## 3. Quality bar ("useful, not filler")
- **Specific and actionable:** real APIs, limits, numbers, failure modes, and code that runs.
- **Production mindset:** server-authoritative designs, validation, rate limits, cleanup, mobile performance, replication cost.
- **Luau style:** typed where it helps (`--!strict` for modules), the `task` library (never `wait`/`spawn`/`delay`), `Connect` + cleanup (Trove/Janitor), no deprecated APIs (see `Legacy_Code_Smells`), and `pcall` around every async engine call.
- **Verify facts** against sources ranked in `09_RESOURCE_HUB_&_COMMUNITY/Trusted_Sources.md`: Creator Docs/API reference and Luau first, then staff announcements and release notes, then maintainers' repos, then community posts. Discord, video and press are leads, not facts.
- **Date-sensitive facts** (limits, rates, beta status) must say when they were true ("as of Oct 2026").
- **Uncertainty is labeled.** Distinguish *confirmed*, *likely* and *possible*. Never present a guess as fact.
- **No exploit code, ever.** Describe attacks only at the level needed to defend against them. No credential, cookie or account tooling. No bypasses of Roblox safety systems.
- **Respect people:** credit showcase authors and never store personal data, DMs or private-channel content.

## 4. Run workflow (scheduled or on request)
1. `git fetch origin` and check out the publishing branch, then pull. Read `_System/Changelog.md` (latest entry) and `_System/Research_Queue.md`.
2. **Inbox:** for each `_Inbox/*.md` not starting with `_`:
   - Understand what the owner wants. If they're unhappy with a note, treat it as a high-priority rewrite.
   - Verify claims (`09_RESOURCE_HUB_&_COMMUNITY/Showcase_Breakdown_Method.md` for showcases).
   - Create or update notes. Use `forum-archive` for a specific showcase or thread, and fold durable knowledge into the system notes.
   - Move the raw file to `_System/Inbox_Archive/YYYY-MM/` (keep the date prefix; rename if it clashes).
   - Unresolved questions go to the Research Queue.
3. **Queue:** work top-down (P1 first). Spend effort where it matters. Fewer excellent notes beat many thin ones.
4. **Change sweep** (weekly): Creator Docs release notes, DevForum Announcements, `luau-lang/rfcs`, tool releases in `Community_Modules_Index`. Update affected notes and bump `last_updated`.
5. **Lint:** `python3 _System/scripts/vault_lint.py --stats` → fix until `0 error(s)`. Check `--weak` and add backlinks to notes with fewer than 3.
6. **Log:** prepend an entry to `_System/Changelog.md` (date, notes added/updated, sources, open questions).
7. **Commit & push:** one commit per run (or per logical change), with a message like `vault: process inbox (ODM showcase), update Server_Authority_Model`. Push to the publishing branch with retry. **Never force-push, rewrite history, or delete notes without a replacement.**
8. **Report:** summarize what changed and what needs the owner's input.

## 5. Tool-specific notes
- **Claude:** see `CLAUDE.md` for research mechanics under network restrictions.
- **ChatGPT / Codex:** you may have no web access. Only add facts you can source from the repo or provided material, and mark anything else `needs-verification` in the Research Queue rather than inventing it. Still run the linter.
- **Any agent:** if you can't satisfy a rule (e.g. no network to verify), leave the note's status honest and add a queue item. Don't lower the bar silently.

## 6. Commands
```bash
python3 _System/scripts/vault_lint.py            # must print 0 error(s)
python3 _System/scripts/vault_lint.py --stats    # graph stats, notes per folder, top hubs
python3 _System/scripts/vault_lint.py --weak     # notes with < 3 backlinks
```
The linter is stdlib-only Python 3.8+. CI runs it on every push (`.github/workflows/vault-lint.yml`).
