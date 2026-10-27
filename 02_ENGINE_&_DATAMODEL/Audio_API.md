---
aliases: [Audio API, AudioPlayer, AudioEmitter, AudioListener, Wire, Sound, SoundGroup, SoundService]
tags:
  - roblox-dev
  - engine/audio
type: api
last_updated: 2026-10-27
status: complete
---
# Audio API (Wires) & Sound Objects

> **TL;DR:** Roblox has two audio stacks. The classic **`Sound`/`SoundGroup`/`SoundEffect`** objects are simple and fine for most SFX. The newer **wire-based Audio API** builds a processing graph: `AudioPlayer` → effects (`AudioEqualizer`, `AudioReverb`, `AudioCompressor`, `AudioFilter`…) → `AudioEmitter` (in the world) → `AudioListener` (camera or character) → `AudioDeviceOutput`. Voice uses `AudioDeviceInput`, and there's also `AudioAnalyzer`, `AudioRecorder`, `AudioSpeechToText`/`AudioTextToSpeech`.

## Wire graph example (3D gunshot with reverb send)
```luau
local player = Instance.new("AudioPlayer")
player.Asset = "rbxassetid://1234567890"
player.Parent = gunAttachment

local reverb = Instance.new("AudioReverb")
reverb.Parent = gunAttachment

local emitter = Instance.new("AudioEmitter")
emitter.Parent = gunAttachment            -- position comes from the parent (Attachment/PVInstance/Camera)

local function wire(src: Instance, dst: Instance)
	local w = Instance.new("Wire")
	w.SourceInstance = src
	w.TargetInstance = dst
	w.Parent = dst
end
wire(player, reverb)
wire(reverb, emitter)
player:Play()
```
An `AudioListener` (usually on the camera, created by default player scripts in the new API) hears emitters with 3D spatialization, then wires to `AudioDeviceOutput`.

## Classic Sound objects (still valid)
- `Sound` parented to a part or attachment is **positional** (`RollOffMinDistance`, `RollOffMaxDistance`, `RollOffMode`). Parented elsewhere (e.g. `SoundService`) it's **background** audio.
- `SoundGroup` for mixing (Music, SFX, UI) with nested groups and **ducking**. `SoundEffect` children (Equalizer, Compressor, Reverb, Chorus, Distortion, Echo, Flange, PitchShift, Tremolo).
- `SoundService:PlayLocalSound(sound)` for UI clicks.

## Game-feel tips
- **Layer** impacts: a transient "crack" plus a body "thump" plus a tail (reverb). Randomize pitch ±5% to avoid machine-gun repetition.
- **Distance cues:** low-pass filter far sounds. With wires, use `AudioFilter` driven by distance or occlusion raycasts ([[Raycasting]]).
- **Weather beds:** loop rain or wind ambience with volume tied to the replicated intensity, and duck it indoors with roof detection ([[Rain_and_Precipitation]]).
- Play combat SFX **client-side** from replicated events. Don't create sounds on the server for every hit ([[Client_Side_VFX_Replication]]).

## Related
[[Client_Side_VFX_Replication]] · [[VFX_Composition_and_Timing]] · [[Hitstop_and_Impact_Feel]] · [[Rain_and_Precipitation]] · [[Weather_System_Architecture]] · [[Raycasting]] · [[Age_Checks_and_Chat_Safety]] · [[Services_Overview]] · [[MOC_VFX_and_Weather]] · [[MOC_Engine_and_DataModel]]

## Sources
- https://create.roblox.com/docs/audio · https://create.roblox.com/docs/sound/objects · https://create.roblox.com/docs/reference/engine/classes/Wire
