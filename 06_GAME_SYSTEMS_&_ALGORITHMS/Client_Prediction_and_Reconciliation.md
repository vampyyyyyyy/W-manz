---
aliases: [Client prediction, Reconciliation, Rollback netcode, Misprediction, Snapshot interpolation, Entity interpolation]
tags:
  - roblox-dev
  - networking/netcode
type: concept
last_updated: 2026-10-27
status: complete
---
# Client Prediction & Reconciliation

> **TL;DR:** **Prediction:** the client applies its own inputs immediately instead of waiting a round trip. **Reconciliation:** when the authoritative state arrives, the client compares it with what it predicted for that tick, and on mismatch **rewinds to the server state and replays unacknowledged inputs**. **Interpolation:** other entities are rendered slightly in the past between snapshots for smoothness. Roblox's [[Server_Authority_Model]] (beta) implements this in the engine. Without it, you build lighter versions yourself.

## The three techniques
| Technique | For | How |
| --- | --- | --- |
| Prediction | Your own character and actions | Simulate input locally now. Tag each input with a sequence/tick |
| Reconciliation | Fixing your own mispredictions | Server sends `(lastProcessedSeq, state)`. Client resets to the state and re-applies inputs with seq > lastProcessed |
| Interpolation | Other players and NPCs | Buffer snapshots ~100 ms behind and lerp between the two around `renderTime` |

## Minimal reconciliation loop (custom systems, e.g. a projectile ability or vehicle)
```text
client each tick:
   input = sample(); seq += 1; pending.push({seq, input})
   state = simulate(state, input, FIXED_DT)          -- predicted
   send(seq, input)
on server snapshot (ackSeq, authState):
   pending = pending.filter(i => i.seq > ackSeq)
   state = authState
   for i in pending: state = simulate(state, i.input, FIXED_DT)   -- replay
   if |renderedPos - state.pos| small: smooth toward it; else snap
```
Determinism matters: same `simulate`, same fixed `dt`, no wall-clock time or unseeded randomness ([[Fixed_Timestep_and_Tick_Rate]]).

## On Roblox specifically
- **Classic model:** characters are client-owned, so your own movement is already "predicted" by default. The server only *observes* and validates ([[Network_Ownership]], [[Movement_Validation]]). Prediction work is mostly for **actions** (attacks, abilities, projectiles) and **custom vehicles**.
- **Server authority model:** the engine predicts simulation-access properties and attributes on predicted instances, and handles rollback and resimulation with `BindToSimulation`, `Misprediction` and `Rollback` events, and `IsResimulating()`. You write deterministic simulation code and keep effects out of it.
- **Visual smoothing:** hide corrections with SmoothDamp on a render proxy ([[TweenService]]).
- **Interpolation of remote state:** for custom-replicated entities (e.g. NPCs via buffer snapshots at 10–20 Hz), keep a small buffer and interpolate. Extrapolate briefly on packet loss ([[UnreliableRemoteEvent]], [[Quantization]]).

## Related
[[Server_Authority_Model]] · [[Fixed_Timestep_and_Tick_Rate]] · [[Lag_Compensation]] · [[Movement_Validation]] · [[Network_Ownership]] · [[UnreliableRemoteEvent]] · [[Character_Controllers_and_ControllerManager]] · [[TweenService]] · [[Combat_System_Architecture]] · [[MOC_Movement_and_ODM]]

## Sources
- https://create.roblox.com/docs/projects/server-authority (client prediction, misprediction, rollback & resimulation)
