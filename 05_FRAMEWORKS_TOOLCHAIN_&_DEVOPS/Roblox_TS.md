---
aliases: [roblox-ts, TypeScript to Luau, rbxts, @rbxts]
tags:
  - roblox-dev
  - toolchain/compiler
type: framework
last_updated: 2026-10-27
status: complete
---
# roblox-ts

> **TL;DR:** roblox-ts compiles **TypeScript to Luau** for Roblox, with typings for the full engine API and an npm ecosystem of `@rbxts/*` packages (ports of Fusion, React, Janitor, Charm, and more). It brings TypeScript's mature tooling and type system. The costs are a compile step, TS↔Luau semantic gaps, and a smaller hiring and tutorial pool than plain Luau.

## What it is / maintenance status
- Repo: https://github.com/roblox-ts/roblox-ts (active, Oct 2026). Docs: roblox-ts.com. Community Discord linked from the README.

## Workflow
```bash
npx create-roblox-ts my-game      # scaffolds tsconfig + Rojo project
npm run watch                     # rbxtsc -w → out/ (Luau), Rojo syncs out/ into Studio
```

## Should you use it?
| Pro | Con |
| --- | --- |
| TS generics, unions and editor tooling are mature | Extra build step, source maps for debugging are imperfect |
| Huge npm-style package workflows | Some Luau idioms don't map cleanly (multiple returns, metatables) |
| Great for teams coming from web dev | Most Roblox tutorials and DevForum answers are Luau |
In 2026, Luau's own type system (new solver, type functions, read/write props) has narrowed the gap considerably ([[Luau_Type_System]]).

## Related
[[Rojo]] · [[Luau_Type_System]] · [[New_Type_Solver]] · [[Darklua]] · [[Wally]] · [[Pesde]] · [[Fusion]] · [[React_Lua]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://github.com/roblox-ts/roblox-ts · https://roblox-ts.com/docs
