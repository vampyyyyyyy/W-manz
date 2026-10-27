---
aliases: [darklua, Code transformation, Bundling Luau, darklua rules]
tags:
  - roblox-dev
  - toolchain/build
type: framework
last_updated: 2026-10-27
status: complete
---
# darklua (code transformer)

> **TL;DR:** darklua transforms Lua 5.1/Luau code with configurable rules: convert **require-by-string paths** to Roblox instance requires, **bundle** modules, inject globals and build flags, strip comments and types, rename, and minify. It's useful when you write code with file-path requires (shared with [[Lune]] or pesde packages) and need it to run in Roblox, or when you want build-time flags like `_G.DEV`.

## Typical config
```json5
// .darklua.json
{
  "rules": [
    "remove_comments",
    "remove_types",          // optional: ship smaller bytecode-irrelevant source
    { "rule": "convert_require", "current": "path", "target": { "name": "roblox", "rojo_sourcemap": "sourcemap.json" } },
    { "rule": "inject_global_value", "identifier": "DEV", "value": false },
    "compute_expression",
    "remove_unused_if_branch"
  ]
}
```
```bash
rokit add seaofvoices/darklua
darklua process src/ dist/      # then point Rojo at dist/
```

## When to use it
- Shared libraries written against require-by-string paths, targeting both Roblox and [[Lune]].
- Build variants (DEV vs PROD) without runtime checks. The `remove_unused_if_branch` rule deletes dead code.
- **Note:** Roblox now supports string requires natively (`./`, `../`, `@self/`, `@game/`) ([[Require_and_Module_Resolution]]), so check whether you still need conversion.

## Related
[[Rojo]] · [[Rokit]] · [[Lune]] · [[Pesde]] · [[Require_and_Module_Resolution]] · [[GitHub_Actions_CI_CD]] · [[Roblox_TS]] · [[Luau_C_API_and_Embedding]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://github.com/seaofvoices/darklua · https://darklua.com/docs
