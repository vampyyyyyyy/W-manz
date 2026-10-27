---
aliases: [Lighting service, Post-processing, Bloom, ColorCorrection, DepthOfField, SunRays, ColorGradingEffect, ClockTime]
tags:
  - roblox-dev
  - engine/rendering
type: api
last_updated: 2026-10-27
status: complete
---
# Lighting & Post-Processing

> **TL;DR:** The `Lighting` service sets global color, intensity, shadows and time of day. Post-processing effects parented to `Lighting` (or the camera) grade the final image: `BloomEffect`, `BlurEffect`, `ColorCorrectionEffect`, `DepthOfFieldEffect`, `SunRaysEffect`, and the newer **`ColorGradingEffect`** (tonemapper presets). Animating these on the **client** is the cheapest way to sell mood shifts: storms, low HP, hit flashes, abilities.

## Lighting properties by category
| Category | Properties |
| --- | --- |
| Color | `Ambient` (everywhere), `OutdoorAmbient`, `ColorShift_Top`, `ColorShift_Bottom` |
| Intensity | `Brightness`, `ExposureCompensation` |
| Shadows | `GlobalShadows`, `ShadowSoftness` (Realistic style) |
| Appearance | `LightingStyle`, `PrioritizeLightingQuality` ([[Rendering_Pipeline_and_Lighting_Technology]]) |
| Environment | `ClockTime` (0–24) / `TimeOfDay` ("14:00:00"), `GeographicLatitude`, `EnvironmentDiffuseScale`, `EnvironmentSpecularScale` |

`ClockTime` doesn't advance by itself. Drive it from a script ([[Day_Night_Cycle]]).

## Post effects (what each sells)
| Effect | Use |
| --- | --- |
| `BloomEffect` (`Intensity`, `Size`, `Threshold`) | Neon glow, magic, sun glints. Raise `Threshold` so only true highlights bloom |
| `ColorCorrectionEffect` (`Brightness`, `Contrast`, `Saturation`, `TintColor`) | Storm desaturation, low-HP red tint, hit flash |
| `DepthOfFieldEffect` | Cinematics, menus, scoped aim |
| `SunRaysEffect` | God rays through clouds or trees |
| `BlurEffect` | Pause menus. Avoid in gameplay (motion-sickness and readability) |
| `ColorGradingEffect.TonemapperPreset` | `Default` (vivid, post-2019) or `Retro` (pre-2019 look; pair with light brightness ≤ 1) |

## Client-side mood pattern
```luau
-- Client: react to replicated weather intensity (e.g. workspace attribute set by the server)
local TweenService = game:GetService("TweenService")
local cc = game.Lighting:FindFirstChildOfClass("ColorCorrectionEffect") or Instance.new("ColorCorrectionEffect", game.Lighting)
workspace:GetAttributeChangedSignal("RainIntensity"):Connect(function()
	local i = workspace:GetAttribute("RainIntensity") or 0
	TweenService:Create(cc, TweenInfo.new(3), {
		Saturation = -0.35 * i,
		Brightness = -0.05 * i,
		TintColor = Color3.new(1, 1, 1):Lerp(Color3.fromRGB(205, 215, 235), i),
	}):Play()
end)
```
Effects are per-client when created by LocalScripts, so each player can have their own screen effects (damage flash) without replication ([[Client_Side_VFX_Replication]]).

## Related
[[Rendering_Pipeline_and_Lighting_Technology]] · [[Atmosphere_Clouds_and_Sky]] · [[Day_Night_Cycle]] · [[Weather_System_Architecture]] · [[Light_Sources_and_Highlights]] · [[TweenService]] · [[Hitstop_and_Impact_Feel]] · [[Camera_System]] · [[MOC_VFX_and_Weather]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/environment/lighting · https://create.roblox.com/docs/environment/post-processing-effects
