---
aliases: [VFX MOC, Weather MOC, Effects hub, Environment hub]
tags:
  - roblox-dev
  - moc/vfx-weather
type: moc
last_updated: 2026-10-27
status: complete
---
# MOC: VFX & Weather

> **TL;DR:** Believable effects come from **timing, layering and environmental response**, not particle count. Weather should *behave*: build-up and decay, wind-driven precipitation, shelter, wetness that accumulates and dries, snow that settles, lightning with correct light and sound delay, all lighting-aware. Simulate state on the server at low frequency, render on clients, and budget for mobile.

## Primitives
[[Particle_Emitters]] · [[Beams_and_Trails]] · [[Light_Sources_and_Highlights]] · [[Lighting_and_Post_Processing]] · [[Atmosphere_Clouds_and_Sky]] · [[Rendering_Pipeline_and_Lighting_Technology]] · [[Terrain_and_Materials]] · [[Global_Wind]] · [[EditableImage_and_EditableMesh]] · [[Audio_API]] · [[TweenService]]

## Composition & replication
[[VFX_Composition_and_Timing]] · [[Client_Side_VFX_Replication]] · [[Object_Pooling]] · [[Hitstop_and_Impact_Feel]] · [[Camera_Shake]] · [[World_Space_UI]]

## Weather simulation
1. [[Weather_System_Architecture]]: state machine, server authority, transitions
2. [[Rain_and_Precipitation]]: wind, shelter, density, splash
3. [[Wetness_Puddles_and_Drying]]: accumulation and evaporation over time
4. [[Snow_Accumulation]]: settling and melt
5. [[Lightning_Generation]]: branching bolts, flash, thunder delay
6. [[Day_Night_Cycle]]: the light and color context everything sits in
7. [[Noise_Functions]]: organic variation for clouds, gusts, puddles

## Performance budget
[[Rendering_Optimization]] · [[Draw_Calls_and_Instancing]] · [[Time_Slicing_and_Frame_Budget]] · [[Mobile_and_Low_End_Optimization]] · [[MicroProfiler]] · [[Memory_Categories]]

## Research & art direction
[[Showcase_Breakdown_Method]] · [[Roblox_Discord_Communities]] · [[Game_UI_Art_Direction]]

## Related hubs
[[Home]] · [[MOC_Engine_and_DataModel]] · [[MOC_Game_Systems_and_Algorithms]] · [[MOC_Combat_Systems]] · [[MOC_Performance_and_Profiling]]

## Sources
- Each linked note cites its own primary sources. See [[Trusted_Sources]].
