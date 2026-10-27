---
aliases: [HttpService, GetSecret, Secrets store, RequestAsync, Webhooks]
tags:
  - roblox-dev
  - networking/http
type: api
last_updated: 2026-10-27
status: complete
---
# HttpService & the Secrets Store

> **TL;DR:** Game servers can call external HTTPS APIs with `HttpService` once **Allow HTTP Requests** is enabled. Budget **500 requests/min per server** for general HTTP, plus a separate **2,500/min** for Open Cloud endpoints. API keys belong in the **secrets store** (`HttpService:GetSecret`), never in scripts or DataStores.

## Requests
- `RequestAsync({Url, Method, Headers, Body})` is the full-control method. `GetAsync` and `PostAsync` are shortcuts. All of them yield and can error, so wrap in `pcall` and use **exponential backoff** (2 s, 4 s, 8 s…) on recoverable errors ([[Error_Handling_pcall_xpcall]]).
- `JSONEncode`, `JSONDecode` and `GenerateGUID` work without HTTP enabled.
- **Server only** for external requests. Clients can't make HTTP calls.
- Open Cloud from in-game: some `apis.roblox.com/cloud/...` endpoints are callable from game servers. Only the `x-api-key` and `content-type` headers are allowed, `..` is disallowed in path params, and there's a 2,500 req/min per-server limit that **doesn't** consume the 500/min budget ([[Open_Cloud_APIs]]).

## Secrets store
- Creator Dashboard → game → **Secrets**. Up to **500 secrets per game**, each up to **1,024 chars**, each scoped to a domain (`my.example.com` best, `*.example.com` OK, `*` discouraged). It's also manageable via Open Cloud.
- Live servers and collaborative testing only. In local playtests, define **Local Secrets** under *File ▸ Experience Settings ▸ Security*. Clients get `Can't find secret with given key`.
```luau
--!strict
local HttpService = game:GetService("HttpService")
local apiKey = HttpService:GetSecret("analytics_key")     -- Secret, not a string
print(apiKey)                                              --> Secret(analytics_key)

local url = apiKey:AddPrefix("https://my.example.com/ingest?key=") -- Secret again
local ok, res = pcall(HttpService.RequestAsync, HttpService, {
	Url = url,
	Method = "POST",
	Headers = { ["Content-Type"] = "application/json" },
	Body = HttpService:JSONEncode({ event = "match_end", players = 12 }),
})
```
- Secrets can go in the **URL or headers only, never the body**. You can't concatenate or print the raw value. That's the point.

## Security notes
- Discord webhooks as a logging sink are rate-limited and leak-prone. Proxy them, and keep the URL in secrets.
- Never send player-identifying data off-platform without a compliant reason ([[Right_to_Erasure_GDPR]]).
- Third-party code with the `Network` capability can exfiltrate data, so sandbox it ([[Script_Capabilities]]).

## Related
[[Access_Control_and_Confidentiality]] · [[Script_Capabilities]] · [[Third_Party_Code_and_Backdoors]] · [[Open_Cloud_APIs]] · [[Error_Handling_pcall_xpcall]] · [[Right_to_Erasure_GDPR]] · [[Services_Overview]] · [[Exploit_Threat_Model]] · [[MOC_Networking_Security_and_Buffers]]

## Sources
- https://create.roblox.com/docs/cloud-services/http-service
- https://create.roblox.com/docs/cloud-services/secrets
