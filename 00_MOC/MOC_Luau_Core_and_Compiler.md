---
aliases: [Luau MOC, Luau hub, Language hub]
tags:
  - roblox-dev
  - moc/luau
type: moc
last_updated: 2026-10-27
status: complete
---
# MOC: Luau Core & Compiler

> **TL;DR:** Everything about **the language itself**: syntax, the gradual type system, runtime semantics (metatables, closures, coroutines, GC) and how the compiler, VM and native codegen make it fast. Read this domain before optimizing anything, because most performance wins come from understanding how Luau executes.

*42 notes in this domain.*

## Start here
1. [[Luau_Overview]]: what Luau is and how it differs from Lua 5.1
2. [[Luau_Type_System]]: gradual typing, strict mode, and why it pays off
3. [[Metatables]]: the basis of OOP, proxies and operator overloading
4. [[Closures_and_Upvalues]]: how functions capture state (and leak memory)
5. [[Luau_Compiler_Optimizations]]: what the compiler does for you
6. [[Native_Code_Generation]]: when `--!native` helps and when it doesn't

## Language & syntax
- **Foundations:** [[Luau_Overview]] · [[Luau_Lua_Compatibility]] · [[Luau_Syntax_Extensions]] · [[Const_Bindings]] · [[String_Interpolation]] · [[Generalized_Iteration]] · [[Varargs_and_Tuples]] · [[Luau_Attributes]]
- **Modules & globals:** [[Require_and_Module_Resolution]] · [[Globals_G_shared_and_getfenv]] · [[Deprecated_wait_spawn_delay]]

## Type system
- **Foundations:** [[Luau_Type_System]] · [[Type_Checking_Modes]] · [[New_Type_Solver]] · [[Type_Annotations_and_Casts]] · [[Typeof_vs_type]]
- **Advanced:** [[Generics]] · [[Type_Refinements]] · [[Table_Types]] · [[Read_Write_Property_Modifiers]] · [[User_Defined_Type_Functions]]

## Runtime semantics
- **Objects & behavior:** [[Metatables]] · [[Metamethods]] · [[OOP_Class_Patterns]] · [[Closures_and_Upvalues]] · [[Coroutines]] · [[Error_Handling_pcall_xpcall]]
- **Memory:** [[Garbage_Collection]] · [[Weak_Tables]]
- **Numbers:** [[Numbers_and_Floating_Point]] · [[Bitwise_Operations_bit32]]

## Standard library
- **Libraries:** [[Math_Library]] · [[Vector_Library]] · [[Table_Library]] · [[String_Library_and_Patterns]] · [[String_Pack_and_Unpack]]

## Compiler, VM & embedding
- **Performance:** [[Luau_Compiler_Optimizations]] · [[Builtin_Fastcalls_and_Imports]] · [[Native_Code_Generation]]
- **Embedding & tools:** [[Luau_Sandboxing]] · [[Luau_C_API_and_Embedding]] · [[Luau_CLI_Tools]]

## Cross-domain
[[Home]] · [[Learning_Path]] · [[MOC_Performance_and_Profiling]] · [[MOC_Engine_and_DataModel]] · [[Luau_RFC_Tracker]] · [[Luau_Classes_Proposal]]

## Sources
- Each linked note cites its own primary sources. See [[Trusted_Sources]] for the ranking policy.
