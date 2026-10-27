---
aliases: [Place publishing API, Deploy place, CI publish, versionType Published]
tags:
  - roblox-dev
  - devops/deployment
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# Open Cloud Place Publishing

> **TL;DR:** `POST https://apis.roblox.com/universes/v1/{universeId}/places/{placeId}/versions?versionType=Published` with your `.rbxl` (octet-stream) or `.rbxlx` (application/xml) body and an API key that has **universe-places Write** on that game. The response returns the new version number. Use `versionType=Saved` to upload without publishing (e.g. to a test place).

## Steps
1. Creator Dashboard ▸ API key with **universe-places** permission + **Write** for the target game.
2. Get the **Universe ID** (Creations ▸ ⋯ ▸ Copy Universe ID) and the **Place ID** (from the place's configure URL).
3. Build the place: `rojo build -o build/game.rbxl` ([[Rojo]]).
4. Publish:
```bash
curl --fail --location -X POST \
  "https://apis.roblox.com/universes/v1/${UNIVERSE_ID}/places/${PLACE_ID}/versions?versionType=Published" \
  --header "x-api-key: ${ROBLOX_API_KEY}" \
  --header "Content-Type: application/octet-stream" \
  --data-binary @build/game.rbxl
```

## Limitations (official)
- HTTPS only.
- The API **doesn't update** some instance types: `EditableImage`, `EditableMesh`, `PartOperation` (unions), `SurfaceAppearance`, `BaseWrap`. Publish from Studio after modifying those.

## Safe release flow
1. CI builds → publish `Saved` to a **staging** place in a separate universe ([[Access_Control_and_Confidentiality]]).
2. Smoke tests (Luau Execution / MCP playtest) ([[Testing_Frameworks]]).
3. Publish `Published` to production. Optionally announce via MessagingService. Old servers keep running until they shut down (soft shutdown or migrate flows) ([[MessagingService_Cross_Server]]).
4. Tag the Git commit with the returned version number ([[Version_Control_Workflow]]).

## Related
[[Open_Cloud_APIs]] · [[GitHub_Actions_CI_CD]] · [[Rojo]] · [[Version_Control_Workflow]] · [[Testing_Frameworks]] · [[Access_Control_and_Confidentiality]] · [[MessagingService_Cross_Server]] · [[EditableImage_and_EditableMesh]] · [[MOC_Frameworks_Toolchain_and_DevOps]]

## Sources
- https://create.roblox.com/docs/cloud/guides/usage-place-publishing
