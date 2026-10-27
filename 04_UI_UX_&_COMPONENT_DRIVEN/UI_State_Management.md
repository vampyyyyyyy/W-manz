---
aliases: [UI state, Charm, Reflex, Rodux, Stores, Producers, Client state sync]
tags:
  - roblox-dev
  - ui/state
type: architecture
last_updated: 2026-10-27
status: complete
---
# UI State Management

> **TL;DR:** Separate three kinds of state. **Server truth** (inventory, currency, cooldowns, HP) is authoritative and replicated. **Client view state** (which tab is open, hover, drag) is local only. **Derived state** (sorted lists, "can afford?") is computed, never stored. Feed server truth into a client store (Charm signals, a Reflex producer, framework Values) and let components render from it. UI never mutates truth directly. It sends *intent* to the server.

## Flow
```text
Server (authoritative) ──remotes / attributes / replication──▶ Client store (read-only mirror)
        ▲                                                        │ derived selectors
        └──────── intent remote (validated) ◀─── UI components ◀─┘
```

## Options
| Library | Model | Fit |
| --- | --- | --- |
| **Charm** (littensy) | Fine-grained signals: `signal`, `computed`, `effect`, `observe`, plus `charm-sync` for server→client replication | Shared state for gameplay + UI. Pairs with Vide/React |
| **Reflex** (littensy) | Producers + actions (Rodux-inspired), selectors, middleware | Redux-style apps, Roblox-TS projects |
| Framework-native | Fusion `Value`/`Computed`, Vide `source`/`derive`, React `useState`/`useReducer` | Local component state |
| Attributes | `GetAttributeChangedSignal` | Small per-instance values (HP, stamina) ([[Attributes]]) |

```luau
-- Charm: client mirror of server-owned coins
local Charm = require(Packages.Charm)
local getCoins, setCoins = Charm.signal(0)
Remotes.CoinsChanged.OnClientEvent:Connect(setCoins)        -- server pushes truth
local canBuy = Charm.computed(function() return getCoins() >= price end)
```

## Anti-patterns
- Client increments coins optimistically and never reconciles, so the UI lies ([[Client_Prediction_and_Reconciliation]]).
- Storing derived data (sorted inventory) and forgetting to update it.
- One giant store update per frame, which re-renders everything ([[UI_Performance]]).
- Server-side UI construction per player (wastes bandwidth and server CPU) ([[Roblox_UI_Fundamentals]]).

## Related
[[Fusion]] · [[React_Lua]] · [[Vide]] · [[Attributes]] · [[Client_Prediction_and_Reconciliation]] · [[Server_Side_Validation]] · [[Remote_Architecture_Patterns]] · [[Inventory_Systems]] · [[UI_Performance]] · [[Signal_Libraries]] · [[Roblox_UI_Fundamentals]] · [[MOC_UI_UX_and_Components]]

## Sources
- https://github.com/littensy/charm · https://github.com/littensy/reflex · https://elttob.uk/Fusion/latest
