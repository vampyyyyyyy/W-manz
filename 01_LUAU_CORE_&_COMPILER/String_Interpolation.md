---
aliases: [Backtick strings, Template strings, Interpolated strings]
tags:
  - roblox-dev
  - luau/syntax
type: concept
last_updated: 2026-10-27
status: complete
---
# String Interpolation

> **TL;DR:** Backtick strings embed expressions: `` `HP: {hp}/{maxHp}` ``. They're cleaner than `..` chains or `string.format`, and the compiler constant-folds the constant parts (2025). Escape a literal brace with `\{`.

## Usage
```luau
local name, kills = "Ari", 7
print(`{name} has {kills} {if kills == 1 then "kill" else "kills"}`)
print(`Position: {root.Position}`)             -- calls tostring on each value
print(`Escaped \{braces}, backtick \`, backslash \\`)
print(`Multi-line expression {
	table.concat(list, ", ")
}`)
```

## Restrictions
- `{{` is a **parse error** on purpose (people from other languages try it to escape `{`). Use `\{`.
- Not allowed in type annotations (`` type T = `x` `` is invalid).
- **Function-call sugar doesn't work**: `` print`hi` `` is invalid. Use ``print(`hi`)``.

## Performance
- Equivalent to `string.format` with `%*`-style formatting under the hood. Constant segments are folded by the compiler, even partially constant expressions ([[Luau_Compiler_Optimizations]]).
- In very hot loops, building strings still allocates. Avoid formatting debug text every frame in production ([[Luau_Micro_Optimizations]]).
- For numeric precision control, use `string.format("%.2f", x)` ([[String_Library_and_Patterns]]).

## Gotchas
- `tostring` of a table without `__tostring` prints `table: 0x…`. Implement `__tostring` for debug-friendly classes ([[Metamethods]]).
- User-visible text from players must go through text filtering before you show it to others ([[Text_Filtering_Compliance]]).

## Related
[[Luau_Syntax_Extensions]] · [[String_Library_and_Patterns]] · [[Metamethods]] · [[Luau_Compiler_Optimizations]] · [[Luau_Micro_Optimizations]] · [[Text_Filtering_Compliance]] · [[Rich_Text]] · [[Luau_Overview]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://luau.org/syntax#string-interpolation · https://rfcs.luau.org/syntax-string-interpolation.html
