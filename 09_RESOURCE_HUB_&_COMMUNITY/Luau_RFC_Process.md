---
aliases: [Luau RFCs, RFC process, luau-lang/rfcs, Language proposals]
tags:
  - roblox-dev
  - community/luau-rfcs
type: concept
last_updated: 2026-10-27
status: complete
---
# Luau RFC Process

> **TL;DR:** Every user-facing change to Luau (syntax, semantics, standard library) goes through an **RFC**: a PR adding a Markdown file to `luau-lang/rfcs/docs/` from `TEMPLATE.md`, open for **at least two weeks** of comments, guided by a **shepherd**, and merged by the Luau team once there's consensus. **Merged = accepted design**. A `**Status**: Implemented` line is added once it ships. On **Oct 15, 2026** the team lifted the blanket ban on features needing **parser backtracking / unbounded lookahead**, so those are now judged case by case (fully ambiguous grammar is still rejected).

## What reviewers look for (from the RFC README)
- **Examples** above all. Show real code before/after.
- **Backwards compatibility.** Luau has no editions or epochs, so a feature can't break existing scripts.
- **Composability.** Features are never removed, so ones that don't compose are stuck forever.
- **Type-system story** for runtime changes, and runtime behavior for type changes.
- **Sandboxing.** Semantics must stay safe under malicious use ([[Luau_Sandboxing]]).
- For stdlib additions: broadly useful? a real perf win over user code? typeable? ([[Builtin_Fastcalls_and_Imports]])

## Why you should care as a Roblox dev
- RFCs are the **earliest signal** of language features you'll get in Studio (const, read/write props, explicit instantiation, string.pack all shipped this way) ([[Luau_RFC_Tracker]]).
- Accepted but unimplemented RFCs (classes, `export` values, 64-bit integers, cyclic requires) tell you what *not* to build elaborate workarounds for ([[Luau_Classes_Proposal]]).
- You can participate: comment with concrete game-dev use cases.

## Related
[[Luau_RFC_Tracker]] · [[Luau_Classes_Proposal]] · [[Luau_Overview]] · [[Luau_Syntax_Extensions]] · [[Luau_Type_System]] · [[Luau_Sandboxing]] · [[Builtin_Fastcalls_and_Imports]] · [[Release_Notes_and_Change_Tracking]] · [[Trusted_Sources]] · [[MOC_Resource_Hub_and_Community]]

## Sources
- https://github.com/luau-lang/rfcs (README, TEMPLATE.md; checked 2026-10-27)
