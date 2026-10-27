---
aliases: [VFX design, VFX timing, Anticipation impact dissipation, Effect composition, VFX art direction]
tags:
  - roblox-dev
  - systems/vfx
type: concept
last_updated: 2026-10-27
status: complete
---
# VFX Composition & Timing

> **TL;DR:** Good VFX is **timing and shape language**, not particle count. Structure every effect as **Anticipation → Impact → Dissipation**. Layer by role (core flash, primary shape, secondary debris, tertiary atmosphere). Sync to animation markers and SFX. Make motion physically believable (drag, gravity, inherited velocity). Interact with the environment (ground decals, dust that takes the surface color, light on nearby surfaces).

## The three beats
| Beat | Duration | Elements | Purpose |
| --- | --- | --- | --- |
| **Anticipation** | 80–300 ms | Charge glow, inward-pulling particles, subtle light build, rising pitch SFX | Telegraph (fairness in PvP), build tension |
| **Impact** | 30–100 ms | White-hot flash, burst `Emit`, shockwave ring, light flash, hitstop, camera punch | Readability. "It hit" |
| **Dissipation** | 300–1500 ms | Smoke rising and expanding, embers with drag, fading decal, lingering light falloff | Weight, believability, a calm return |

## Layering by role
1. **Core** (hottest, brightest, shortest): small, high `LightEmission`, white→color.
2. **Primary shape** (what the player remembers): slash arc beam, explosion sphere, flipbook burst.
3. **Secondary** (motion detail): sparks with drag and gravity, debris taking `RaycastResult.Material` colors.
4. **Tertiary** (atmosphere): smoke, heat haze, dust, ground scorch decal, lingering light.

## Believable motion
- **Drag + gravity** on sparks and debris ([[Particle_Emitters]]). Nothing moves at constant velocity in reality.
- **Velocity inheritance** from the weapon or projectile (`VelocityInheritance`) so effects feel attached to motion.
- **Ease curves:** size grows with ease-out, transparency fades with ease-in at the end. No linear sequences for hero effects.
- **Environment interaction:** impacts orient to the **surface normal**, dust uses the floor material color, puddles splash differently than stone ([[Raycasting]], [[Wetness_Puddles_and_Drying]]).
- **Scale with power:** derive emit counts, light brightness and shake from the same `intensity` value so effects stay consistent across a kit.

## Sync & performance
- Fire beats from **animation markers** (`WindupStart`, `HitStart`) ([[Animation_Events_and_Markers]]).
- Budget per effect (particles alive, lights, transparent overdraw). Have LOD variants for mobile and distance ([[Mobile_and_Low_End_Optimization]]).
- **Flipbooks** sell complex motion with few particles, but they're memory-heavy and auto-disabled on low memory. Keep a non-flipbook fallback.

## Related
[[Particle_Emitters]] · [[Beams_and_Trails]] · [[Light_Sources_and_Highlights]] · [[Hitstop_and_Impact_Feel]] · [[Client_Side_VFX_Replication]] · [[Animation_Events_and_Markers]] · [[Camera_Shake]] · [[Audio_API]] · [[Showcase_Breakdown_Method]] · [[MOC_VFX_and_Weather]]

## Sources
- https://create.roblox.com/docs/effects/particle-emitters (flipbooks, memory note) · VFX craft conventions
