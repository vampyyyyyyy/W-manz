---
aliases: [RFC status, Luau feature status, Implemented RFCs, Pending RFCs]
tags:
  - roblox-dev
  - community/luau-rfcs
type: concept
last_updated: 2026-10-27
status: complete
---
# Luau RFC Tracker (Oct 2026)

> **TL;DR:** A snapshot of `luau-lang/rfcs/docs` taken **2026-10-27**. **72 of the 89 RFCs are marked Implemented**, including the 2025–26 wave (`const`, read/write property syntax, explicit `f<<T>>()` instantiation, `string.pack`, `math.lerp/map/isnan/isinf/isfinite`, vector library, buffer bit ops, `@deprecated`, user-defined type functions). **Accepted but not yet implemented:** classes, cyclic requires, `export` for values, 64-bit `integer`, `coroutine.finally`, negation types, generic function subtyping, isorecursive type aliases, cast-by-inhabitance, and reserving `$`.

## Recently implemented (high impact for Roblox devs)
| RFC | Feature | Vault note |
| --- | --- | --- |
| const-keyword | `const x = 5` immutable bindings | [[Const_Bindings]] |
| syntax-property-access-modifiers | `read`/`write` table props | [[Read_Write_Property_Modifiers]] |
| explicit-type-parameter-instantiation | `f<<number>>(x)` | [[Generics]] |
| function-string-pack-unpack | `string.pack/unpack/packsize` | [[String_Pack_and_Unpack]] |
| function-math-lerp / map / isnan-isfinite-isinf | math helpers | [[Math_Library]] |
| vector-library (+ vector2 ctor, lerp) | `vector.*` | [[Vector_Library]] |
| function-buffer-bits | `buffer.readbits/writebits` | [[Buffer_Library]], [[Bitpacking]] |
| syntax-attribute-functions-deprecated / native | `@deprecated`, `@native` | [[Luau_Attributes]] |
| user-defined-type-functions (+ udtf-is-extern, generics, thread/buffer) | type functions | [[User_Defined_Type_Functions]] |
| new-require-by-string-semantics, aliases, init.luau | modern `require` | [[Require_and_Module_Resolution]] |

## Accepted, not implemented (no `Status` line yet)
| RFC | Idea |
| --- | --- |
| syntax-classes | Native `class` blocks, `public` fields, nominal types ([[Luau_Classes_Proposal]]) |
| support-for-cyclic-requires | `require` passes an export table so modules can import each other cyclically |
| export-keyword | `export` values/functions as module-table sugar |
| type-long-integer | Built-in 64-bit `integer` type |
| function-coroutine-finally | Callback when a coroutine terminates (structured concurrency) ([[Coroutines]]) |
| negation-types, generic-function-subtyping, relax-recursive-type-restriction, type-ascription-by-inhabitance | Type-system extensions ([[New_Type_Solver]]) |
| reserve-dollar-sign | Promise that `$` never becomes Luau syntax (safe for tooling) |
| disallow-proposals-leading-to-ambiguity-in-grammar | Policy RFC protecting existing parses |
| local-type-inference, new-nonstrict | Design docs behind the new solver work |

Abandoned: lower-bounds-calculation (superseded). `function-inlining` documents a decision to keep inlining automatic.

## Related
[[Luau_RFC_Process]] · [[Luau_Classes_Proposal]] · [[Luau_Syntax_Extensions]] · [[New_Type_Solver]] · [[Const_Bindings]] · [[Read_Write_Property_Modifiers]] · [[User_Defined_Type_Functions]] · [[Vector_Library]] · [[Buffer_Library]] · [[Require_and_Module_Resolution]] · [[MOC_Resource_Hub_and_Community]]

## Sources
- https://github.com/luau-lang/rfcs/tree/master/docs (snapshot 2026-10-27)
