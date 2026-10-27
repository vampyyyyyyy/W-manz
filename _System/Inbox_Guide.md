# Inbox Guide: feeding the vault

The vault grows from **your finds**. Anything you see in Discord (e.g. discord.gg/robloxstudio showcases), on the DevForum, on YouTube or in your own experiments can go in `_Inbox/`. The next research run turns it into verified notes.

## Drop a find (30 seconds)
1. In Obsidian, create a new note. New notes land in `_Inbox/` automatically.
2. Name it `YYYY-MM-DD_short-title` (e.g. `2026-10-27_odm-wall-run-showcase`). Don't reuse an existing note name.
3. Paste whatever you have. Structure is optional, but these fields help:

```markdown
source: <link to the Discord message / DevForum thread / video>
author: <who made it, for credit>
what: <what it shows or claims, in your words>
why I care: <what you want to learn or build from it>
questions: <what you want answered>
priority: high | normal
```

Screenshots go in `_System/Attachments/` (Obsidian does this when you paste an image).

## What happens next
1. The agent reads `_Inbox/` first on every run (files starting with `_` are ignored).
2. It verifies claims against official docs and repos ([[Trusted_Sources]]) and breaks showcases down with the [[Showcase_Breakdown_Method]].
3. It creates or updates notes (often a `forum-archive` note plus updates to system notes like [[VFX_Composition_and_Timing]] or [[ODM_Gear_System]]).
4. It moves your raw note to `_System/Inbox_Archive/YYYY-MM/` and records what it did in the [[Changelog]].
5. Anything it couldn't resolve goes to the [[Research_Queue]] with the open question.

## Rules
- Links and descriptions only. Don't paste DMs, personal info, or content from private channels you were asked not to share ([[Roblox_Discord_Communities]]).
- Never paste API keys, webhook URLs or passwords.
- Exploit scripts don't go in the vault. Describe the behavior you saw and the agent documents the **defense** ([[MOC_Anti_Exploit]]).
- Unhappy with a note? Drop an inbox item saying what's wrong (e.g. "the ODM note is too shallow on swing momentum; I want the math and a working prototype"). The agent treats it as a high-priority rewrite request.

## Related
[[Home]] · [[Research_Queue]] · [[Changelog]] · [[DevForum_Guide]] · [[Release_Notes_and_Change_Tracking]]
