---
aliases: [Projectiles, FastCast, Bullets, Bullet drop, Hitscan vs projectile]
tags:
  - roblox-dev
  - systems/combat
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Projectile Systems

> **TL;DR:** Don't make bullets out of physics parts. Simulate projectiles **mathematically** (position = p0 + v·t + ½·g·t²), **raycast each step** from the last position to the new one, and render a cosmetic part or beam on each client. The **server** runs (or validates) the authoritative simulation from the same parameters. This is the approach the classic FastCast module popularized (now unmaintained).

## Hitscan vs projectile
| | Hitscan | Simulated projectile |
| --- | --- | --- |
| Check | One raycast at fire time | Segment raycasts per step over the flight |
| Feel | Instant (rifles, lasers) | Travel time, drop, dodgeable (bows, rockets, magic) |
| Netcode | Validate origin and target with lag comp | Replicate fire events (origin, dir, speed, seed). Each side simulates |

## Core stepper
```luau
--!strict
type Projectile = { pos: Vector3, vel: Vector3, age: number, maxAge: number, ownerId: number }
local GRAVITY = Vector3.new(0, -workspace.Gravity * 0.5, 0)   -- tune per weapon
local active: { Projectile } = {}
local params = RaycastParams.new()
params.FilterType = Enum.RaycastFilterType.Exclude

local function step(dt: number, onHit: (Projectile, RaycastResult) -> ())
	for i = #active, 1, -1 do
		local p = active[i]
		local nextVel = p.vel + GRAVITY * dt
		local displacement = (p.vel + nextVel) * 0.5 * dt         -- trapezoid integration
		local result = workspace:Raycast(p.pos, displacement, params)
		if result then
			onHit(p, result)
			active[i] = active[#active]; active[#active] = nil     -- swap-remove (O(1))
		else
			p.pos += displacement
			p.vel = nextVel
			p.age += dt
			if p.age > p.maxAge then active[i] = active[#active]; active[#active] = nil end
		end
	end
end
game:GetService("RunService").Heartbeat:Connect(function(dt) step(dt, Damage.onProjectileHit) end)
```

## Netcode pattern
1. Client fires: plays effects instantly, sends `Fire(weaponId, origin, direction, clientTime)`.
2. Server validates origin, fire rate and ammo, then **simulates the same projectile** (optionally advanced by the client's latency) and decides hits.
3. Server tells other clients `ProjectileSpawned(origin, dir, speed, seed)`, and they render a cosmetic copy locally ([[Client_Side_VFX_Replication]]).
4. For fast shooters, the client may claim hits, and the server validates with rewind ([[Lag_Compensation]], [[Hit_Validation]]).

## Performance
- Hundreds of projectiles: keep state in arrays and `vector`s, batch-step them in one Heartbeat. Consider [[Parallel_Luau]] for raycast-heavy batches (raycasts are parallel-safe).
- Pool the visual parts ([[Object_Pooling]]). Use `Workspace:BulkMoveTo` for many cosmetic parts.
- Thick projectiles: use `Spherecast` per step instead of `Raycast` ([[Shapecasting]]).

## Related
[[Raycasting]] · [[Shapecasting]] · [[Hit_Validation]] · [[Lag_Compensation]] · [[Client_Side_VFX_Replication]] · [[Object_Pooling]] · [[Damage_Pipeline]] · [[Parallel_Luau]] · [[Global_Wind]] · [[MOC_Combat_Systems]]

## Sources
- https://create.roblox.com/docs/workspace/raycasting
- https://etithespirit.github.io/FastCastAPIDocs/ (FastCast docs; module no longer actively maintained)
