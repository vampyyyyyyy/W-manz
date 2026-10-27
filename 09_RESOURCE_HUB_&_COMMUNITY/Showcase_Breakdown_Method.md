---
aliases: [Showcase breakdown, Reverse engineering showcases, VFX breakdown, How was this made]
tags:
  - roblox-dev
  - community/method
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Showcase Breakdown Method

> **TL;DR:** A repeatable way to turn a 10-second Discord or DevForum clip into knowledge you can actually use. **Capture** (link, author, claims) → **decompose frame by frame** into engine primitives → **hypothesize** an implementation for each layer → **estimate cost** (CPU, GPU, memory, network) → **prototype the smallest version** → **record** a `forum-archive` note that separates confirmed facts from guesses and credits the author.

## 1. Capture
Link, author, date, platform shown (PC/mobile), and any claims ("no lag on mobile", "fully server-sided"). Drop it in `_Inbox/` ([[Roblox_Discord_Communities]]).

## 2. Decompose (slow-mo, frame step)
Ask, per layer:
| Layer | Likely primitives | Notes |
| --- | --- | --- |
| Anticipation/impact flashes | `ParticleEmitter` bursts, `Highlight`, `PointLight` pulses | [[Particle_Emitters]], [[Light_Sources_and_Highlights]] |
| Slashes/trails | `Beam`/`Trail` with curved attachments, mesh flipbooks | [[Beams_and_Trails]] |
| Screen feel | Camera shake, FOV punch, hitstop, color correction | [[Camera_Shake]], [[Hitstop_and_Impact_Feel]] |
| Environment response | Decals/terrain changes, debris pools, wetness | [[Wetness_Puddles_and_Drying]], [[Object_Pooling]] |
| Movement | `LinearVelocity`/`AlignOrientation`, custom controllers, ropes | [[Mover_Constraints]], [[ODM_Gear_System]] |

## 3. Hypothesize & cost it
- Who owns it? Usually the server decides *that* a hit happened and clients render *how it looks* ([[Client_Side_VFX_Replication]]).
- Count instances per effect × players. Estimate particle fill rate on mobile ([[Rendering_Optimization]], [[Mobile_and_Low_End_Optimization]]).
- Network: one event with a seed, not a stream of CFrames ([[Network_Bandwidth_Budget]]).

## 4. Prototype → measure
Build the minimal version in a test place, profile it ([[MicroProfiler]]), and compare against the clip. Timing usually matters more than particle count ([[VFX_Composition_and_Timing]]).

## 5. Record
Use the `Forum_Archive` template: **Source · What they showed · How it works (confirmed vs guesses) · What we can reuse · Open questions**. Link it from the system notes it informs.

## Related
[[Roblox_Discord_Communities]] · [[DevForum_Guide]] · [[Trusted_Sources]] · [[VFX_Composition_and_Timing]] · [[Client_Side_VFX_Replication]] · [[Particle_Emitters]] · [[Beams_and_Trails]] · [[Hitstop_and_Impact_Feel]] · [[MicroProfiler]] · [[Auto_Farm_and_Remote_Spam_Exploits]] · [[MOC_Resource_Hub_and_Community]]

## Sources
- Method synthesized for this vault. Primitives per https://create.roblox.com/docs/effects
