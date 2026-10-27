---
aliases: [Networking MOC, Security hub, Netcode hub]
tags:
  - roblox-dev
  - moc/networking
type: moc
last_updated: 2026-10-27
status: complete
---
# MOC: Networking, Security & Buffers

> **TL;DR:** How data crosses the client/server boundary **safely and cheaply**: remote design, rate limits and validation, the exploit threat model and server-side detection, plus binary serialization (buffers, bitpacking, quantization) and IDL networking libraries. The rule behind all of it: **the client asks, the server decides**.

*31 notes in this domain.*

## Start here
1. [[Exploit_Threat_Model]]: what exploiters can and can't do
2. [[RemoteEvents_and_RemoteFunctions]]: ordering, limits, argument rules
3. [[Server_Side_Validation]]: the validation checklist for every remote
4. [[Remote_Rate_Limiting]]: token buckets per player and per remote
5. [[Buffer_Library]]: binary payloads, the basis of efficient netcode
6. [[Networking_Libraries_Comparison]]: Blink vs Zap vs ByteNet

## Remote design
- **Transport:** [[RemoteEvents_and_RemoteFunctions]] · [[UnreliableRemoteEvent]] · [[Remote_Architecture_Patterns]] · [[Network_Bandwidth_Budget]]
- **Guards:** [[Remote_Rate_Limiting]] · [[Server_Side_Validation]] · [[NaN_and_Infinity_Exploits]]

## Anti-exploit & security
- **Threats:** [[Exploit_Threat_Model]] · [[Auto_Farm_and_Remote_Spam_Exploits]] · [[Data_Duplication_and_Trade_Exploits]] · [[Client_Triggered_Instance_Security]] · [[Third_Party_Code_and_Backdoors]]
- **Defense:** [[Defensive_Design]] · [[Movement_Validation]] · [[Hit_Validation]] · [[Lag_Compensation]] · [[Honeypot_Remotes]] · [[Server_Side_Detection_Heuristics]] · [[Ban_API_and_Consequences]]
- **Platform controls:** [[Access_Control_and_Confidentiality]] · [[Script_Capabilities]] · [[HttpService_and_Secrets_Store]]

## Binary data & serialization
- **Encoding:** [[Buffer_Library]] · [[Bitpacking]] · [[Quantization]] · [[Custom_Serialization]] · [[Packet_Compression]]
- **Libraries:** [[Networking_Libraries_Comparison]] · [[Blink_IDL]] · [[Zap_IDL]] · [[ByteNet]]

## Cross-domain
[[Home]] · [[Learning_Path]] · [[MOC_Anti_Exploit]] · [[MOC_Combat_Systems]] · [[MOC_Engine_and_DataModel]] · [[MOC_Performance_and_Profiling]]

## Sources
- Each linked note cites its own primary sources. See [[Trusted_Sources]] for the ranking policy.
