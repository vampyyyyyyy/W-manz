---
aliases: [Configs, ConfigService, Remote config, Live tuning, Feature flags Roblox]
tags:
  - roblox-dev
  - analytics/configs
type: api
last_updated: 2026-10-27
status: complete
---
# Configs (Remote Configuration)

> **TL;DR:** **Configs** are key → value pairs (string, number, boolean, JSON; strings/JSON up to **100,000 chars**) that you change **without publishing**. Publish takes ~15 s–1 min, or a gradual 15-minute rollout, and comes with history and restore. Read them with `ConfigService:GetConfigAsync()` → `ConfigSnapshot:GetValue(key)`, refresh via `snapshot:Refresh()` / `UpdateAvailable`, and use `GetConfigForPlayerAsync(player)` for **targeting** (country, language, new vs returning, payer and activity segments…) and **experiments**.

## Pattern: live-tunable combat & weather
```luau
local ConfigService = game:GetService("ConfigService")
local snapshot = ConfigService:GetConfigAsync()

local Tuning = {}
local function reload()
	Tuning.dashCooldown = snapshot:GetValue("dash_cooldown") or 4
	Tuning.rainChancePerHour = snapshot:GetValue("rain_chance_per_hour") or 0.25
	Tuning.eventBanner = snapshot:GetValue("event_banner")          -- JSON-object config (nested types autocomplete in Studio)
end
reload()
snapshot.UpdateAvailable:Connect(function() snapshot:Refresh(); reload() end)
-- or per key: snapshot:GetValueChangedSignal("dash_cooldown"):Connect(reload)
```
Always ship **safe defaults** in code (`or 4`) so a missing key never breaks the game.

## Uses
- Balance numbers (cooldowns, damage multipliers) without a deploy ([[Server_Authoritative_Cooldowns]], [[Damage_Pipeline]]).
- Kill switches for risky features (new trade system, an event) ([[Data_Duplication_and_Trade_Exploits]]).
- Live events: weather schedules, double-XP windows ([[Weather_System_Architecture]]).
- Sync staging → live with **Publish As** from the Studio Configs widget ([[Version_Control_Workflow]]).

## Cautions
- Configs are **server-readable game data**. If clients need values, replicate them deliberately and don't put secrets there ([[HttpService_and_Secrets_Store]]).
- Rule ordering for conditional values is global, so review it before publishing.
- Also manageable via Open Cloud Configs APIs, including RTBF templates (`user_data_templates`) ([[Right_to_Erasure_GDPR]], [[Open_Cloud_APIs]]).

## Related
[[Experiments_and_AB_Testing]] · [[Analytics_Dashboard_and_Metrics]] · [[Server_Authoritative_Cooldowns]] · [[Damage_Pipeline]] · [[Weather_System_Architecture]] · [[Data_Duplication_and_Trade_Exploits]] · [[HttpService_and_Secrets_Store]] · [[Version_Control_Workflow]] · [[Right_to_Erasure_GDPR]] · [[Open_Cloud_APIs]] · [[MOC_Monetization_Analytics_and_Compliance]]

## Sources
- https://create.roblox.com/docs/production/configs
