---
aliases: [Weather system, Weather state machine, Storm system, Dynamic weather]
tags:
  - roblox-dev
  - systems/weather
type: architecture
last_updated: 2026-10-27
status: complete
---
# Weather System Architecture

> **TL;DR:** A production weather system is a **server-owned state machine** (Clear → RampUp → Raining → RampDown) driven by a **game clock**. It outputs a few **normalized intensities** (sky, rain coverage, rain rate, mist) that every subsystem reads. Replicate *state*, not effects: one attribute like `workspace.RainIntensity`, plus the engine's own replicated `GlobalWind`, `Clouds` and `Atmosphere`. Each client then renders surfaces, audio and screen effects locally. Roblox's official **weather-island** sample (Oct 2026) follows this shape.

## Data flow
```text
WeatherClock (scaled game hours)
   └─► Phase FSM: Clear ─► RampUp ─► Raining ─► RampDown ─► Clear
          │ targets(): sky, coverage, rate, mist  (0..1 each)
          ├─► SkyState   : GlobalWind, Clouds.Cover/Density/Color, Atmosphere.Haze   (written at 15 Hz)
          ├─► RainField  : grid of emitter cells, grown/shrunk ≤32 parts/frame, rate quantized to 10 steps
          │      └─► RoofShelter: leaning raycasts shorten particle Lifetime under roofs (time-sliced)
          ├─► MistField  : ground-level grid of slow emitters (follows rain's half of the transition)
          └─► workspace:SetAttribute("RainIntensity", round(sky, 0.01))   ← one cheap replicated signal
Clients: read RainIntensity → wetness shaders/MaterialVariants, ambience volume, screen-space rain overlay,
         color grading, footstep splashes, indoor/outdoor ducking.
```

## Key design decisions (and why)
| Decision | Reason |
| --- | --- |
| **Rain lags the sky at both ends** (nothing falls until clouds and wind are halfway in, and the last cell is gone halfway out) | Matches how storms read visually. Clouds arrive before rain |
| **Mist runs on rain's half** of the transition | Fog and rain arrive together, so the haze doesn't race ahead |
| **Throttle replicated writes** (15 Hz, change-only, rounded) | Each property write replicates to every client ([[Network_Bandwidth_Budget]]) |
| **Budgeted building** (≤32 cells per frame) and **quantized rates** | No frame spikes and fewer replicated property changes ([[Time_Slicing_and_Frame_Budget]]) |
| **Storm placement rolled per storm** (covers ~40% of the map) | Variety, plus locality: players can walk out of a storm |
| **Probabilistic start** between min and max hours since the last rain | Natural-feeling cadence without fixed timers |

## Server vs client split
- **Server:** clock, phase, intensity, wind target, storm location, anything gameplay-relevant (wet = slippery, lightning damage, visibility affecting AI).
- **Client:** all *looks*: rain near the camera or a screen overlay, puddle shine, wet materials, sound beds, post-processing ([[Lighting_and_Post_Processing]], [[Client_Side_VFX_Replication]]).
- The official sample keeps rain emitters **server-owned and replicated via streaming**, so it needs no remotes. Many community systems instead spawn rain **client-side around the camera** to save bandwidth. Both work. Pick based on whether rain must be visible identically at a distance (cinematic) or just around each player (performance).

## Extending the FSM
Add states like `Snow`, `Thunderstorm`, `Fog`, `Sandstorm`. Each maps to a profile of target values (wind range, cloud cover, haze, emitter template, ambience) and inherits the same ramp logic ([[Finite_State_Machines]]). Accumulation and drying run on their own timers driven by intensity ([[Wetness_Puddles_and_Drying]], [[Snow_Accumulation]]).

## Related
[[Rain_and_Precipitation]] · [[Wetness_Puddles_and_Drying]] · [[Snow_Accumulation]] · [[Lightning_Generation]] · [[Day_Night_Cycle]] · [[Global_Wind]] · [[Atmosphere_Clouds_and_Sky]] · [[Particle_Emitters]] · [[Finite_State_Machines]] · [[Time_Slicing_and_Frame_Budget]] · [[MOC_VFX_and_Weather]]

## Sources
- https://github.com/Roblox/resources/tree/main/experiences/weather-island (init.luau, SkyState.luau, RainField.luau, WeatherClock.luau; repo commit 2026-10-20)
- https://create.roblox.com/docs/effects/particle-emitters#simulate-rain
