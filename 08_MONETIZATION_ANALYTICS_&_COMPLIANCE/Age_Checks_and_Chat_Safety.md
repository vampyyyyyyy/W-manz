---
aliases: [Age checks, Chat safety, TextChatService compliance, Chat groups, PromptAgeCheck, Voice chat safety]
tags:
  - roblox-dev
  - compliance/safety
type: api
last_updated: 2026-10-27
status: complete
---
# Age Checks & Chat Safety

> **TL;DR:** Any in-game text chat **must** use **`TextChatService`** and `TextChannel`s, which handle filtering, privacy and parental settings, reporting and age rules. `Player.AgeChecked` (`Enum.AgeCheckStatus`) shows whether a player passed an age check, and `Player:PromptAgeCheck()` asks them to. For matchmaking and teleport grouping, `TextChatService:GetChatGroupsAsync(players)` returns which players can chat together (enable **Chat & Voice Groups APIs**, works in Studio only in Team Test, never store the result). Any other user-to-user text must be **filtered** and, for signs and bulletin boards, **rate-limited to at least 1 minute**.

## Rules (chat guidelines)
- DMs, team chat, squad chat → `TextChannel`s. Use `TextChannel:SetDirectChatRequester()` for direct-chat channels.
- `TextChannel:SendAsync()` applies privacy and parental settings automatically.
- Non-chat communication (signs, pet names, guild descriptions) → `TextService:FilterStringAsync` ([[Text_Filtering_Compliance]]).
- Communication must be **reportable**. TextChannels handle this.
- `CanUserChatAsync` / `CanUsersChatAsync` / `CanUsersDirectChatAsync` gate custom social features.
- Console platforms can report restrictions (`Player.ThirdPartyTextChatRestrictionStatus`).

## Matchmaking with chat groups
Group players who share a chat group ID into the same squad or server when your game relies on chat-heavy co-op. Otherwise lean on non-text communication (pings, quick chat) ([[Matchmaking_Customization]], [[TeleportService_and_Reserved_Servers]]).

## Design for every tier
Kids and Select tiers may have chat off. Make coordination possible without text: pings, emotes, preset quick-words, clear UI ([[Cross_Platform_UI_Input]], [[Custom_HUD_Design]]).

## Related
[[Text_Filtering_Compliance]] · [[Content_Maturity_Labels]] · [[PolicyService_Compliance]] · [[Matchmaking_Customization]] · [[TeleportService_and_Reserved_Servers]] · [[Cross_Platform_UI_Input]] · [[Custom_HUD_Design]] · [[Remote_Rate_Limiting]] · [[MOC_Monetization_Analytics_and_Compliance]]

## Sources
- https://create.roblox.com/docs/chat/guidelines · https://create.roblox.com/docs/reference/engine/classes/TextChatService · https://create.roblox.com/docs/reference/engine/classes/Player#AgeChecked · https://create.roblox.com/docs/production/publishing/kids-and-select
