---
aliases: [Mobile optimization, Low-end devices, Phone performance, Memory crashes, Test on hardware]
tags:
  - roblox-dev
  - performance/mobile
type: concept
last_updated: 2026-10-27
status: complete
---
# Mobile & Low-End Optimization

> **TL;DR:** A large share of Roblox players are on phones and tablets with **tight memory, weak GPUs and thermal throttling**. Out-of-memory crashes are the #1 silent killer of retention. Stream aggressively, keep textures and audio lean, cap particles and effects by device, design touch-friendly UI, and **test on real low-end hardware**, not just Studio's device emulator.

## Priorities (in order)
1. **Memory:** StreamingEnabled with the recommended radii and `StreamOutBehavior = Opportunistic`. Fewer Persistent models. Deduped assets. Smaller textures ([[StreamingEnabled]], [[Memory_Categories]]).
2. **Rendering:** SLIM for static geometry, fewer shadows and transparent layers, particle caps ([[Rendering_Optimization]], [[SLIM_and_Frustum_Streaming]]).
3. **Scripts:** no per-frame work for off-screen systems. Time-slice ([[Time_Slicing_and_Frame_Budget]]).
4. **Network:** compact remotes. Mobile networks have higher latency and loss ([[Network_Bandwidth_Budget]]).
5. **UI:** large touch targets, safe areas, fewer frames ([[Responsive_UI_and_Safe_Areas]], [[Cross_Platform_UI_Input]]).

## Adaptive quality pattern
```luau
-- client: degrade effects when frame time is consistently high
local samples, sum = 0, 0
game:GetService("RunService").Heartbeat:Connect(function(dt)
	samples += 1; sum += dt
	if samples >= 120 then
		local avg = sum / samples
		VFXSettings.tier = if avg > 1/35 then "Low" elseif avg > 1/55 then "Medium" else "High"
		samples, sum = 0, 0
	end
end)
```
Effects read `VFXSettings.tier` to scale emit counts, light counts and distances ([[Client_Side_VFX_Replication]]). Respect the user's Graphics Quality setting as well.

## Engine behaviors to know
- Clients **auto-disable particle flipbooks** under memory pressure ([[Particle_Emitters]]).
- Particle limits are much lower on mobile, which shows as distant rain flickering ([[Rain_and_Precipitation]]).
- Highlights cost more on mobile in proportion to screen coverage ([[Light_Sources_and_Highlights]]).
- EditableImage/EditableMesh creation can fail on low memory, so always have a fallback ([[EditableImage_and_EditableMesh]]).

## Test on hardware
Use the official "test on hardware" guidance: a few representative low-end phones, plus long sessions to catch memory growth and thermal throttling ([[Performance_Optimization_Workflow]], [[Studio_Testing_Modes]]).

## Related
[[StreamingEnabled]] · [[Memory_Categories]] · [[Rendering_Optimization]] · [[SLIM_and_Frustum_Streaming]] · [[Particle_Emitters]] · [[Responsive_UI_and_Safe_Areas]] · [[Time_Slicing_and_Frame_Budget]] · [[Performance_Optimization_Workflow]] · [[Studio_Testing_Modes]] · [[MOC_Performance_and_Profiling]]

## Sources
- https://create.roblox.com/docs/performance-optimization/test-on-hardware · https://create.roblox.com/docs/performance-optimization/improve
