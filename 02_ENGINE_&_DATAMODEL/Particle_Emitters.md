---
aliases: [ParticleEmitter, Emit, Flipbooks, Particles, Particle VFX]
tags:
  - roblox-dev
  - engine/vfx
type: api
last_updated: 2026-10-27
status: complete
---
# Particle Emitters

> **TL;DR:** `ParticleEmitter` spawns camera-facing (or velocity-aligned) textured sprites from a part or attachment. Combat VFX mostly use **bursts** (`emitter:Emit(n)` with `Rate = 0`). Ambient effects use `Rate`. The properties that create *believable* motion are **Drag, Acceleration, Speed/SpreadAngle, Size and Transparency sequences, Squash, Flipbooks, LightEmission/LightInfluence and WindAffectsDrag**. More particles almost never fixes a bad effect. Better curves and timing do ([[VFX_Composition_and_Timing]]).

## Properties that matter (grouped)
| Group | Properties |
| --- | --- |
| Emission | `Rate`, `Emit(count)`, `Enabled`, `Clear()`, `Lifetime` (range), `Shape` (Box/Sphere/Cylinder/Disc), `ShapeStyle` (Volume/Surface), `ShapeInOut`, `ShapePartial`, `EmissionDirection` |
| Motion | `Speed` (range), `SpreadAngle`, `Acceleration` (gravity, buoyancy), `Drag`, `VelocityInheritance`, `LockedToPart`, `WindAffectsDrag` (+ `Drag` > 0 to follow [[Global_Wind]]), `TimeScale` (slow-mo) |
| Look | `Texture`/`TextureContent`, `Color` (ColorSequence), `Size` & `Transparency` (NumberSequences with envelopes), `Squash` (stretch), `Orientation` (FacingCamera, VelocityParallel…), `Rotation`/`RotSpeed`, `ZOffset` |
| Lighting | `LightEmission` (additive glow: fire, magic, sparks), `LightInfluence` (0 = unlit, 1 = lit by the scene: rain, dust) |
| Flipbooks | `FlipbookLayout` (Grid2x2, 4x4, 8x8, Custom + `FlipbookSizeX/Y`), `FlipbookMode` (Loop, OneShot, PingPong, Random), `FlipbookFramerate` (max 30), `FlipbookStartRandom`, `FlipbookBlendFrames` |

## Burst pattern for combat
```luau
local function burst(template: Attachment, at: CFrame, scale: number)
	local a = template:Clone()
	a.WorldCFrame = at
	a.Parent = workspace.Terrain                 -- attachments can live on Terrain
	for _, e in a:GetDescendants() do
		if e:IsA("ParticleEmitter") then
			e:Emit(math.round((e:GetAttribute("EmitCount") or 10) * scale))
		end
	end
	task.delay(2, a.Destroy, a)                    -- after the longest Lifetime
end
```
Store `EmitCount` per emitter as an [[Attributes|attribute]] so artists tune effects without touching code. Pool attachments for rapid-fire hits ([[Object_Pooling]]).

## Believability checklist
- **Size curves:** sparks shrink, smoke grows. **Transparency curves:** fade in quickly, fade out slowly.
- **Drag** makes impact debris decelerate naturally. Combine it with gravity `Acceleration`.
- **Rain:** `Orientation = VelocityParallel` + negative `Squash`, high `Speed`, gray `Color`, `LightInfluence` ~0.5 ([[Rain_and_Precipitation]]).
- **Flipbook textures need spacing between frames** (mip bleeding), and clients **auto-disable flipbooks on low memory** (older phones). Design a fallback look ([[Mobile_and_Low_End_Optimization]]).
- There's a global particle budget per device, and mobile limits are much lower. Distant rain flickering means you hit it.

## Related
[[Beams_and_Trails]] · [[Light_Sources_and_Highlights]] · [[VFX_Composition_and_Timing]] · [[Client_Side_VFX_Replication]] · [[Object_Pooling]] · [[Rain_and_Precipitation]] · [[Global_Wind]] · [[Hitstop_and_Impact_Feel]] · [[Mobile_and_Low_End_Optimization]] · [[MOC_VFX_and_Weather]]

## Sources
- https://create.roblox.com/docs/effects/particle-emitters · https://create.roblox.com/docs/reference/engine/classes/ParticleEmitter
