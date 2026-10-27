---
aliases: [Beam, Trail, Lightning beam, Sword trail, Grapple rope visual]
tags:
  - roblox-dev
  - engine/vfx
type: api
last_updated: 2026-10-27
status: complete
---
# Beams & Trails

> **TL;DR:** A **Beam** draws a textured ribbon between two Attachments, optionally curved (Bezier via `CurveSize0/1`). Use it for lasers, ropes, grapple cables, lightning segments and auras. A **Trail** draws a ribbon behind a *moving* pair of Attachments over `Lifetime`, for sword slashes, dash streaks and projectile tails. Both are cheap, stylish, and tuned through `Color`/`Transparency` sequences, `Width`, `TextureSpeed` and `LightEmission`.

## Beam essentials
| Property | Effect |
| --- | --- |
| `Attachment0`, `Attachment1` | Endpoints (move them to animate) |
| `CurveSize0`, `CurveSize1` | Bezier handles along each attachment's axis (rope sag, arcs) |
| `Width0`, `Width1`, `FaceCamera` | Thickness at each end. Camera-facing for "fat" lasers |
| `Texture`, `TextureMode` (Wrap/Stretch/Static), `TextureLength`, `TextureSpeed` | Scrolling energy or electricity |
| `Segments` | Curve smoothness (more = smoother + costlier) |
| `LightEmission`, `LightInfluence`, `Brightness` | Glow vs lit |
| `ZOffset` | Layering with other transparent effects |

## Trail essentials
`Attachment0`/`Attachment1` (the trail's width is the distance between them), `Lifetime`, `MinLength`, `MaxLength`, `WidthScale` (NumberSequence over the trail), `Color`, `Transparency`, `FaceCamera`, `TextureMode`, `Enabled` (toggle for swing windows).

## Recipes
- **Grapple cable:** beam between hand and anchor attachments, with sag `CurveSize` scaled by slack and a low `Segments` count while the cable is taut ([[Grappling_Hook_Physics]]).
- **Sword slash:** a trail on two attachments along the blade, enabled only during the active frames from [[Animation_Events_and_Markers]].
- **Lightning:** several beams with jittered midpoint attachments, flashed for 0.05–0.15 s, plus a light flash ([[Lightning_Generation]]).
- **Dash streak:** trail on the root plus a short `Lifetime` and a transparency ramp ([[Custom_Movement_Abilities]]).

## Gotchas
- Trails emit based on **attachment movement**. Teleporting the attachments draws a long streak, so disable the trail, move, then re-enable.
- Beams with `FaceCamera = false` disappear when viewed edge-on. Cross two beams at 90° for volume.
- Transparent ribbons stack overdraw. Keep them short-lived ([[Rendering_Optimization]]).

## Related
[[Particle_Emitters]] · [[Light_Sources_and_Highlights]] · [[VFX_Composition_and_Timing]] · [[Grappling_Hook_Physics]] · [[Lightning_Generation]] · [[Animation_Events_and_Markers]] · [[Client_Side_VFX_Replication]] · [[ODM_Gear_System]] · [[MOC_VFX_and_Weather]]

## Sources
- https://create.roblox.com/docs/effects/beams · https://create.roblox.com/docs/effects/trails
