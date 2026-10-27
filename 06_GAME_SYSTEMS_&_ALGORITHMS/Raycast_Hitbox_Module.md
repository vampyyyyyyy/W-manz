---
aliases: [RaycastHitbox, RaycastHitboxV4, Swordphin hitbox]
tags:
  - roblox-dev
  - systems/combat
type: framework
last_updated: 2026-10-27
status: complete
---
# RaycastHitbox (community module)

> **TL;DR:** RaycastHitbox (by Swordphin123 / TeamSwordphin, DevForum since 2019) attaches **raycast points** to a weapon (attachments named `DmgPoint`) and casts from each point's previous to current position every frame while the hitbox is active. Hits follow the animation exactly. It's legacy but still widely used. The GitHub repo hasn't been updated since 2021, so it's maintained via the DevForum thread. Verify the version you use.

## How it works
1. Place attachments along the blade (e.g. 6 `DmgPoint` attachments from hilt to tip).
2. `Hitbox:HitStart()` begins casting each frame from each point's last world position to its current one, which catches the swing arc.
3. `OnHit` fires once per humanoid per activation. Call `HitStop()` when the active window ends.

```luau
-- typical usage (API per the module's DevForum docs; check your version)
local RaycastHitbox = require(ReplicatedStorage.RaycastHitboxV4)
local hitbox = RaycastHitbox.new(swordModel)
hitbox.RaycastParams = params
hitbox.OnHit:Connect(function(hitPart, humanoid) Combat.claimHit(humanoid.Parent) end)

track:GetMarkerReachedSignal("HitStart"):Connect(function() hitbox:HitStart() end)
track:GetMarkerReachedSignal("HitEnd"):Connect(function() hitbox:HitStop() end)
```

## When to use it (and when not)
- ✅ Weapons with distinct shapes (long spears, scythes) where the swing path matters, and animation-driven combat on the **client** (feel). Validate on the server ([[Hit_Validation]]).
- ❌ Server-only detection for big lobbies: rays per point per frame per player add up. Use overlap boxes or cones on the server ([[Hitbox_Detection_Methods]]).
- ❌ Very low FPS clients: big gaps between frames can skip thin targets. Add more points or sweep with [[Shapecasting]].

## Alternatives
Overlap boxes ([[Spatial_Queries_Overlap]]), shapecast sweeps, or your own point-trail caster (about 60 lines once you understand the idea).

## Related
[[Hitbox_Detection_Methods]] · [[Raycasting]] · [[Shapecasting]] · [[Animation_Events_and_Markers]] · [[Hit_Validation]] · [[Combat_System_Architecture]] · [[Community_Modules_Index]] · [[Projectile_Systems]] · [[MOC_Combat_Systems]]

## Sources
- https://devforum.roblox.com/t/raycast-hitbox-module-for-all-your-melee-needs/374482
- https://github.com/Swordphin123/raycastHitboxRbxl (last commit 2021-02)
