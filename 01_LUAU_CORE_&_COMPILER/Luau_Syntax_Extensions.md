---
aliases: [continue, compound assignment, "+=", if-then-else expression, floor division, number literals, Luau syntax]
tags:
  - roblox-dev
  - luau/syntax
type: concept
last_updated: 2026-10-29
status: complete
---
# Luau Syntax Extensions (beyond Lua 5.1)

> **TL;DR:** The small syntax additions that make Luau pleasant: `continue`, compound assignment (`+=` and friends), `if … then … else` **expressions**, floor division `//`, binary and underscore-separated number literals, `\u{}`/`\x`/`\z` escapes. The bigger ones have their own notes: [[Const_Bindings]], [[String_Interpolation]], [[Generalized_Iteration]], [[Luau_Attributes]], types ([[Luau_Type_System]]).

## `continue`
```luau
for _, part in workspace.Map:GetDescendants() do
	if not part:IsA("BasePart") then continue end
	part.CastShadow = false
end
```
It must be the last statement of its block, and it's a contextual keyword (`continue()` is still a function call). In `repeat … until`, it can't skip a local that the `until` condition uses.

## Compound assignment
`+=  -=  *=  /=  //=  %=  ^=  ..=` are **statements**, not expressions (`print(a += 1)` is invalid). The left side is evaluated **once**: `t[f()] += 1` calls `f` once. They respect `__add`, `__index` and `__newindex`.

## If-then-else expressions
```luau
local color = if hp > 50 then Color3.new(0, 1, 0) elseif hp > 20 then Color3.new(1, 1, 0) else Color3.new(1, 0, 0)
local label = `{if count == 1 then "kill" else "kills"}`
```
The `else` is required. Unlike `a and b or c`, this works when `b` is `false` or `nil`. A Studio beta (Oct 2026) adds bindings in the condition (`if local p = … then p.Name else "?"`). See [[If_Local_Bindings]].

## Floor division `//`
`7 // 2 == 3`, `-7 // 2 == -4` (floors toward −∞). `//=` exists, overloaded via `__idiv`. On native vectors it floors component-wise. `x // 0` gives ±inf and `0 // 0` gives NaN, so validate client numbers ([[NaN_and_Infinity_Exploits]]).

## Number and string literals
- `0xFF`, `0b1010_1010`, `1_000_000` (underscores anywhere in integers).
- One number type only: 64-bit double, exact integers up to 2^53 ([[Numbers_and_Floating_Point]]).
- `"\x41"`, `"\u{1F525}"` (braces required), `"\z"` skips following whitespace and newlines.

## Not in Luau
`goto`, labels, `::` as label syntax (`::` is a type cast in Luau: [[Type_Annotations_and_Casts]]), bitwise operators ([[Bitwise_Operations_bit32]]).

## Related
[[Const_Bindings]] · [[If_Local_Bindings]] · [[String_Interpolation]] · [[Generalized_Iteration]] · [[Luau_Attributes]] · [[Luau_Lua_Compatibility]] · [[Numbers_and_Floating_Point]] · [[Metamethods]] · [[Type_Annotations_and_Casts]] · [[Luau_Overview]] · [[MOC_Luau_Core_and_Compiler]]

## Sources
- https://luau.org/syntax · https://rfcs.luau.org/syntax-compound-assignment.html · https://rfcs.luau.org/syntax-if-expression.html
