---
aliases: [Day night cycle, Time of day, ClockTime cycle, Dynamic lighting cycle]
tags:
  - roblox-dev
  - systems/weather
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Day/Night Cycle

> **TL;DR:** `Lighting.ClockTime` never advances by itself. A **server clock** advances game time (e.g. 30 real seconds per game hour = a 12-minute day, as in Roblox's weather sample) and writes `ClockTime` at a **throttled rate** (~15 Hz). Clients lerp **lighting profiles** keyed by time (ambient, color shift, atmosphere, exposure) for smooth dawn and dusk. Weather multiplies on top.

## Server clock (replicates via Lighting)
```luau
--!strict
local Lighting = game:GetService("Lighting")
local SECONDS_PER_HOUR = 30
local WRITE_HZ = 15
local clock, countdown = 14, 0

game:GetService("RunService").Heartbeat:Connect(function(dt)
	clock = (clock + dt / SECONDS_PER_HOUR) % 24
	countdown -= dt
	if countdown <= 0 then
		countdown = 1 / WRITE_HZ
		Lighting.ClockTime = clock     -- replicated; clients render sun/moon position from it
	end
end)
```
Alternatives: replicate only a start epoch + rate via an attribute and let **clients compute** ClockTime locally (zero ongoing replication, perfectly smooth). This needs `workspace:GetServerTimeNow()` for sync.

## Lighting profiles (client)
```luau
type Profile = { t: number, ambient: Color3, outdoor: Color3, exposure: number, haze: number }
local PROFILES: { Profile } = {
	{ t = 5.5,  ambient = Color3.fromRGB(40, 40, 60),  outdoor = Color3.fromRGB(90, 80, 110),  exposure = -0.3, haze = 1.5 },
	{ t = 7,    ambient = Color3.fromRGB(90, 80, 70),  outdoor = Color3.fromRGB(160, 130, 110), exposure = 0,   haze = 1.0 },
	{ t = 12,   ambient = Color3.fromRGB(110, 110, 110), outdoor = Color3.fromRGB(140, 140, 140), exposure = 0,  haze = 0.5 },
	{ t = 18.5, ambient = Color3.fromRGB(100, 70, 60), outdoor = Color3.fromRGB(170, 110, 90), exposure = 0.1, haze = 1.2 },
	{ t = 20,   ambient = Color3.fromRGB(30, 30, 50),  outdoor = Color3.fromRGB(50, 50, 80),  exposure = -0.5, haze = 1.0 },
}
-- each frame: find the surrounding profiles for ClockTime (wrapping at 24) and lerp the fields
```

## Gameplay hooks
NPC schedules, spawn tables, shop hours and stealth visibility can all read the clock from the server-side value, never from the client ([[NPC_Behavior_Trees]]).

## Related
[[Lighting_and_Post_Processing]] · [[Atmosphere_Clouds_and_Sky]] · [[Weather_System_Architecture]] · [[Rendering_Pipeline_and_Lighting_Technology]] · [[Wetness_Puddles_and_Drying]] · [[NPC_Behavior_Trees]] · [[Network_Bandwidth_Budget]] · [[Light_Sources_and_Highlights]] · [[MOC_VFX_and_Weather]]

## Sources
- https://create.roblox.com/docs/environment/lighting#clocktime-and-timeofday
- https://github.com/Roblox/resources/tree/main/experiences/weather-island (WeatherClock.luau)
