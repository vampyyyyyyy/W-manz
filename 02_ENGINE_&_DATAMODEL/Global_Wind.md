---
aliases: [GlobalWind, Workspace.GlobalWind, Wind, Wind gusts]
tags:
  - roblox-dev
  - engine/environment
type: api
last_updated: 2026-10-27
status: complete
---
# Global Wind

> **TL;DR:** `Workspace.GlobalWind` (a `Vector3`: direction × strength) moves **terrain grass, dynamic clouds, and particles** whose emitter has `WindAffectsDrag = true` and `Drag > 0`. `Fire` and `Smoke` follow it too. One property gives your whole world coherent wind. Script it for gusts, and read it from your own systems (rain lean, flags, trees, projectile drift).

## Facts
- Edit in Properties or with the **Wind Direction** widget (View menu): a wind sock showing Speed, Yaw and Pitch.
- Particles follow wind only with **`WindAffectsDrag` + non-zero `Drag`**. Drag also slows falling, so raise downward `Acceleration` for rain ([[Particle_Emitters]]).
- Grass animation *speed* is reduced if the player turns on the **Reduce Motion** accessibility setting.
- It replicates. Set it on the server for shared weather, or on the client for local-only effects.

## Gust pattern (eased with sine, like the official sample)
```luau
local base = Vector3.new(5, 0, 2)
local gust = Vector3.new(25, 0, 10)
task.spawn(function()
	while true do
		local duration, steps = 3.5, 70
		for i = 1, steps do
			workspace.GlobalWind = base + gust * math.sin(math.pi * i / steps)
			task.wait(duration / steps)
		end
		workspace.GlobalWind = base
		task.wait(2 + math.random() * 5)
	end
end)
```

## Using wind in your own systems
- **Rain lean / roof detection:** a drop at terminal fall speed `g / drag` drifts sideways at wind speed. Offset occlusion rays by `wind * (drop * drag / g)`, as Roblox's `RoofShelter` does ([[Rain_and_Precipitation]]).
- **Cloth, flags, foliage:** sample `GlobalWind` in client animation (bones or Motor6D sway).
- **Projectiles:** add `wind * k` to arrow velocity for archery skill expression ([[Projectile_Systems]]).
- **Weather states** set wind targets per storm and lerp toward them ([[Weather_System_Architecture]]).

## Related
[[Particle_Emitters]] · [[Atmosphere_Clouds_and_Sky]] · [[Terrain_and_Materials]] · [[Rain_and_Precipitation]] · [[Snow_Accumulation]] · [[Weather_System_Architecture]] · [[Projectile_Systems]] · [[Lightning_Generation]] · [[MOC_VFX_and_Weather]]

## Sources
- https://create.roblox.com/docs/environment/global-wind
