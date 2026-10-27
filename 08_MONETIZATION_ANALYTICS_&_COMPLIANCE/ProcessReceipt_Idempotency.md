---
aliases: [ProcessReceipt, BindReceiptHandler, Receipt handling, Purchase idempotency, PurchaseId]
tags:
  - roblox-dev
  - monetization/receipts
type: code-pattern
last_updated: 2026-10-27
status: complete
---
# ProcessReceipt & Receipt Idempotency

> **TL;DR:** Receipts are **at-least-once**. Roblox redelivers until you acknowledge, so a handler can run more than once for the same `PurchaseId`, possibly on a different server. Correct handling: (1) the player's data is loaded and **session-locked**, (2) if `PurchaseId` is already recorded, acknowledge without granting, (3) grant + record `PurchaseId` in the *same* save, (4) acknowledge only after the save succeeds. Otherwise return `NotProcessedYet`. Prefer **`BindReceiptHandler`** (per-product routing, also handles Robux-transfer receipts). It takes precedence over and falls back to `ProcessReceipt`.

## Pattern (BindReceiptHandler + ProfileStore-style session data)
```luau
local MarketplaceService = game:GetService("MarketplaceService")
local Players = game:GetService("Players")

local MAX_HISTORY = 100
local GRANTS: { [number]: (profile: any) -> () } = {
	[1234567] = function(p) p.Data.Coins += 500 end,     -- 500 coins pack
	[2345678] = function(p) p.Data.Revives += 1 end,
}

local function handle(receipt): Enum.ReceiptDecision
	local player = Players:GetPlayerByUserId(receipt.PlayerId)
	local profile = player and Profiles[player]          -- only exists while session-locked
	if not profile then return Enum.ReceiptDecision.NotProcessedYet end

	local history = profile.Data.PurchaseHistory
	if table.find(history, receipt.PurchaseId) then
		return Enum.ReceiptDecision.Processed            -- already granted: just acknowledge
	end

	local grant = GRANTS[receipt.ProductId]
	if not grant then return Enum.ReceiptDecision.NotProcessedYet end
	grant(profile)
	table.insert(history, receipt.PurchaseId)
	if #history > MAX_HISTORY then table.remove(history, 1) end

	-- Persist before acknowledging (ProfileStore saves on its own cadence; force or await a save here)
	local ok = SaveNow(profile)                           -- your wrapper: returns true only after a successful write
	return if ok then Enum.ReceiptDecision.Processed else Enum.ReceiptDecision.NotProcessedYet
end

local ids = {}
for id in GRANTS do table.insert(ids, id) end
MarketplaceService:BindReceiptHandler(Enum.ReceiptType.DeveloperProduct, handle, ids)
```
Legacy `ProcessReceipt` has the same logic but returns `Enum.ProductPurchaseDecision.PurchaseGranted` / `NotProcessedYet` and receives `receiptInfo.PlayerId/ProductId/PurchaseId`.

## Failure modes this prevents
- **Double grant:** a server crashes after granting but before acknowledging, and the receipt replays on a new server. The `PurchaseId` check catches it ([[Data_Duplication_and_Trade_Exploits]]).
- **Lost purchase:** acknowledging before the save, then the save fails. The player paid and got nothing.
- **Wrong server state:** granting into an unlocked or stale profile ([[Session_Locking]]).

## Rules
- The handler must always **return** a decision. Don't yield indefinitely.
- Only one catch-all handler per receipt type, and filtered handlers can't overlap product IDs (that throws).
- Track grants as analytics economy *sources* after success ([[AnalyticsService_Events]]).

## Related
[[MarketplaceService]] · [[Developer_Products]] · [[Session_Locking]] · [[ProfileStore]] · [[UpdateAsync_Patterns]] · [[Data_Duplication_and_Trade_Exploits]] · [[DataStoreService]] · [[AnalyticsService_Events]] · [[Rewarded_Video_Ads]] · [[MOC_Monetization_Analytics_and_Compliance]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/MarketplaceService#BindReceiptHandler · https://create.roblox.com/docs/reference/engine/classes/MarketplaceService#ProcessReceipt
