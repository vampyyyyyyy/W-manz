---
aliases: [PolicyService, GetPolicyInfoForPlayerAsync, Regional compliance, ArePaidRandomItemsRestricted]
tags:
  - roblox-dev
  - compliance/policy
type: api
last_updated: 2026-10-27
status: complete
---
# PolicyService Compliance

> **TL;DR:** `PolicyService:GetPolicyInfoForPlayerAsync(player)` returns per-player flags based on **geolocation, age group and platform**. Gate features with them: **`AreAdsAllowed`**, **`ArePaidRandomItemsRestricted`**, **`IsPaidItemTradingAllowed`**, **`IsContentSharingAllowed`**, **`IsEligibleToPurchaseSubscription`**, **`IsEligibleToPurchaseCommerceProduct`**, **`IsPhotoToAvatarAllowed`**, **`IsSubjectToChinaPolicies`**, **`IsEndlessContentLoadAllowed`**, **`IsEndlessContentAutoplayAllowed`**. (`AllowedExternalLinkReferences` is legacy and always empty.) Wrap the call in `pcall`, cache it per session, and **fail closed**.

## Pattern
```luau
local PolicyService = game:GetService("PolicyService")
local cache: { [Player]: any } = {}

local RESTRICTIVE = {
	AreAdsAllowed = false, ArePaidRandomItemsRestricted = true, IsPaidItemTradingAllowed = false,
	IsContentSharingAllowed = false, IsEligibleToPurchaseSubscription = false,
}

local function policy(player: Player)
	if cache[player] then return cache[player] end
	local ok, info = pcall(PolicyService.GetPolicyInfoForPlayerAsync, PolicyService, player)
	cache[player] = if ok then info else RESTRICTIVE           -- fail closed on errors
	return cache[player]
end
Players.PlayerRemoving:Connect(function(p) cache[p] = nil end)
```
Enforce on the **server** (the client can read its own policy for UI, but the server decides what's purchasable or tradeable) ([[Server_Side_Validation]]).

## Feature map
| Feature | Flag | Treatment |
| --- | --- | --- |
| Loot crates/spins (paid) | `ArePaidRandomItemsRestricted` | Direct purchase at EV price, or block ([[Paid_Random_Items_Policy]]) |
| Player trading of paid items | `IsPaidItemTradingAllowed` | Disable trade UI and server trade handler ([[Inventory_Systems]]) |
| Ads | `AreAdsAllowed` | Fallback content ([[Immersive_Ads]]) |
| UGC sharing (screenshots, custom signs) | `IsContentSharingAllowed` | Hide and refuse ([[Text_Filtering_Compliance]]) |
| Subscriptions / commerce | `IsEligibleToPurchase…` | Hide the offer ([[Subscriptions]], [[Commerce_Products]]) |

## Related
[[Paid_Random_Items_Policy]] · [[Immersive_Ads]] · [[Subscriptions]] · [[Commerce_Products]] · [[Text_Filtering_Compliance]] · [[Age_Checks_and_Chat_Safety]] · [[Inventory_Systems]] · [[Server_Side_Validation]] · [[MarketplaceService]] · [[MOC_Monetization_Analytics_and_Compliance]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/PolicyService
