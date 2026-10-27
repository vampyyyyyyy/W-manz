---
aliases: [Loading screen, ReplicatedFirst, RemoveDefaultLoadingScreen, PreloadAsync, game.Loaded]
tags:
  - roblox-dev
  - ui/loading
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Loading Screens & ReplicatedFirst

> **TL;DR:** Put a LocalScript (and optionally your loading `ScreenGui`) in **`ReplicatedFirst`**, which replicates to the client before anything else. Parent the gui to `PlayerGui`, call `ReplicatedFirst:RemoveDefaultLoadingScreen()`, wait for `game:IsLoaded()` / `game.Loaded`, optionally `ContentProvider:PreloadAsync` the **first-seen** assets, then fade out. Don't preload the whole game. That delays play and hurts retention.

## Pattern
```luau
-- ReplicatedFirst/Loading.client.luau
local Players = game:GetService("Players")
local ReplicatedFirst = game:GetService("ReplicatedFirst")
local ContentProvider = game:GetService("ContentProvider")
local TweenService = game:GetService("TweenService")

local gui = ReplicatedFirst:WaitForChild("LoadingScreen") :: ScreenGui
gui.IgnoreGuiInset = true
gui.Parent = Players.LocalPlayer:WaitForChild("PlayerGui")
ReplicatedFirst:RemoveDefaultLoadingScreen()

if not game:IsLoaded() then game.Loaded:Wait() end

-- Preload only what the first screen shows (logo, menu icons, intro music)
local critical = { gui.Logo, ReplicatedFirst:WaitForChild("MenuMusic") }
local ok, err = pcall(ContentProvider.PreloadAsync, ContentProvider, critical)
if not ok then warn("preload failed:", err) end

local fade = TweenService:Create(gui.Root, TweenInfo.new(0.35), { GroupTransparency = 1 }) -- Root is a CanvasGroup
fade:Play(); fade.Completed:Wait()
gui:Destroy()
```

## Production guidance
- **Time to first interaction** matters more than a pretty bar. Show the menu as soon as it's usable, and keep streaming the rest ([[StreamingEnabled]]).
- Data loading is separate: show "Loading your profile…" until the server confirms session data ([[Session_Locking]], [[ProfileStore]]).
- Teleports have their own loading screen (`TeleportService:SetTeleportGui`) ([[TeleportService_and_Reserved_Servers]]).
- Respect Reduce Motion for animated spinners ([[UI_Animation_and_Springs]]).
- Keep ReplicatedFirst tiny. Everything there blocks the first frame.

## Related
[[StreamingEnabled]] · [[Session_Locking]] · [[ProfileStore]] · [[TeleportService_and_Reserved_Servers]] · [[UI_Animation_and_Springs]] · [[CanvasGroup]] · [[Container_Services_and_Replication_Scope]] · [[Retention_and_Engagement_Metrics]] · [[Mobile_and_Low_End_Optimization]] · [[MOC_UI_UX_and_Components]]

## Sources
- https://create.roblox.com/docs/players/loading-screens · https://create.roblox.com/docs/reference/engine/classes/ContentProvider
