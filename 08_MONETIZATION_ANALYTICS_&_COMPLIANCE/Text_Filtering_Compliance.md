---
aliases: [Text filtering, FilterStringAsync, TextFilterResult, Filter user text, Sign filtering]
tags:
  - roblox-dev
  - compliance/text
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Text Filtering Compliance

> **TL;DR:** Any text that one user creates and another can see (pet names, signs, guild names, custom titles, even text built from random characters or fetched from the web) must go through **`TextService:FilterStringAsync(text, fromUserId)`** on the **server**. Then call `GetNonChatStringForBroadcastAsync()` (everyone sees it) or `GetNonChatStringForUserAsync(userId)` (one viewer). **Store the raw text, and filter at display time**, because filter rules change and results depend on the viewer. Chat itself goes through `TextChatService`.

## Server pattern
```luau
local TextService = game:GetService("TextService")

local function filterForBroadcast(text: string, fromUserId: number): string?
	if #text == 0 or #text > 60 then return nil end
	local ok, result = pcall(TextService.FilterStringAsync, TextService, text, fromUserId)
	if not ok then return nil end                                  -- fail closed: don't show unfiltered text
	local ok2, filtered = pcall(result.GetNonChatStringForBroadcastAsync, result)
	return if ok2 then filtered else nil
end

SetSignRemote.OnServerEvent:Connect(function(player, text)
	if typeof(text) ~= "string" then return end                    -- validate type first
	if not signCooldown:take(player) then return end               -- ≥ 1 min for signs/boards (chat guidelines)
	local filtered = filterForBroadcast(text, player.UserId)
	if filtered then sign:SetAttribute("Text", filtered) end
end)
```
([[Server_Side_Validation]], [[Remote_Rate_Limiting]])

## Gotchas
- Never trust the client to filter. Always the server.
- If you display filtered text with `RichText = true`, **escape** it first ([[Rich_Text]]).
- `TextService:FilterAndTranslateStringAsync` is **no longer supported**. Chat translation only exists via TextChatService.
- Filtering calls are async and rate-limited, so cache results per string+viewer while in session.

## Related
[[Age_Checks_and_Chat_Safety]] · [[Rich_Text]] · [[Server_Side_Validation]] · [[Remote_Rate_Limiting]] · [[PolicyService_Compliance]] · [[Content_Maturity_Labels]] · [[Error_Handling_pcall_xpcall]] · [[DataStoreService]] · [[MOC_Monetization_Analytics_and_Compliance]]

## Sources
- https://create.roblox.com/docs/ui/text-filtering · https://create.roblox.com/docs/chat/guidelines
