---
aliases: [Grappling hook, Grapple physics, Rope swing, Pendulum swing, Spring rope]
tags:
  - roblox-dev
  - systems/movement
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Grappling Hook Physics

> **TL;DR:** There are two good implementations. **(A) Engine constraint:** `RopeConstraint` between the character and an anchor attachment (winch to reel), robust and cheap, but less control over feel. **(B) Custom force model:** you compute pendulum constraint + spring + pull yourself every PreSimulation step, with full control (ODM, Spider-Man swing). Both need raycast anchors, max-range checks, and a beam for visuals.

## A. RopeConstraint grapple
```luau
--!strict
local function attachRope(root: BasePart, hit: RaycastResult)
	local anchor = Instance.new("Attachment")
	anchor.WorldPosition = hit.Position
	anchor.Parent = workspace.Terrain                  -- or hit.Instance to follow moving parts
	local a0 = root:FindFirstChild("GrappleAtt") :: Attachment
	local rope = Instance.new("RopeConstraint")
	rope.Attachment0, rope.Attachment1 = a0, anchor
	rope.Length = (hit.Position - root.Position).Magnitude
	rope.WinchEnabled = true
	rope.WinchTarget = rope.Length                     -- shrink this to reel in
	rope.WinchSpeed = 80
	rope.WinchForce = 60000
	rope.Visible = false                               -- draw with a Beam instead
	rope.Parent = root
	return rope, anchor
end
```
Ropes only resist **stretching**. Slack is free, so you get natural pendulum swings. Reeling = lowering `WinchTarget`.

## B. Custom pendulum + spring (more control)
```luau
--!strict
-- call in RunService.PreSimulation on the owning client
local function stepGrapple(root: BasePart, anchor: Vector3, ropeLen: number, dt: number, reel: number)
	local pos = root.Position
	local toAnchor = anchor - pos
	local dist = toAnchor.Magnitude
	if dist < 1e-3 then return ropeLen end
	local dir = toAnchor / dist
	local vel = root.AssemblyLinearVelocity

	-- 1) inextensible rope: kill outward radial velocity when taut (pendulum)
	if dist >= ropeLen then
		local radial = vel:Dot(dir)                      -- negative = moving away from anchor
		if radial < 0 then vel -= dir * radial end
		-- soft positional correction (spring) to avoid drift beyond rope length
		vel += dir * (dist - ropeLen) * 8 * dt
	end
	-- 2) reel in
	ropeLen = math.max(4, ropeLen - reel * dt)
	vel += dir * reel * 0.5 * dt

	root.AssemblyLinearVelocity = vel
	return ropeLen
end
```
Add tangential steering from input and gravity (applied by the engine already). Tune the correction stiffness (8) for snappy vs elastic.

## Choosing & tuning
| Concern | RopeConstraint | Custom |
| --- | --- | --- |
| Effort | Low | Medium |
| Feel control | Limited (winch params) | Total |
| Stability at high speed | Engine-solved (240 Hz) | Your integrator. Use PreSimulation and dt |
| Two hooks (ODM) | Two ropes (works) | Combine forces deliberately ([[ODM_Gear_System]]) |
| Prediction/rollback | Constraint state is predicted under server authority | Must live in `BindToSimulation` to roll back |

## Visual cable
Beam from hand to anchor. `CurveSize` scales with slack (`ropeLen - dist`), and gets thinner and straighter under tension. A short hook travel animation before attaching sells weight ([[Beams_and_Trails]]).

## Related
[[ODM_Gear_System]] · [[Mechanical_Constraints]] · [[Mover_Constraints]] · [[Physics_Engine_and_Assemblies]] · [[Raycasting]] · [[Beams_and_Trails]] · [[Custom_Movement_Abilities]] · [[Adaptive_Timestepping]] · [[Movement_Validation]] · [[MOC_Movement_and_ODM]]

## Sources
- https://create.roblox.com/docs/physics/constraints/rope · https://create.roblox.com/docs/reference/engine/classes/RopeConstraint
