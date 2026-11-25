# Suggestions for improving the site (review before implementing)

These are options, not changes already made. Each has a benefit, a cost/risk, and a verification requirement. Nothing here should be implemented without a decision.

| # | Suggestion | Benefit | Cost / risk | Verification required before implementation |
|---|---|---|---|---|
| 1 | Add an official dated-rate table refreshed from each hotel's booking engine for all candidate windows | Answers "cheapest 7 nights" with real numbers | Rates change constantly; scraping may breach terms; need manual re-check | Capture dated URL + rate + screenshot from official site; never write a rate without a date and source |
| 2 | Connect a licensed transit-routing API and compute real door-to-door times | Replaces the cluster proxy with the requested ≤1-hour metric | API keys/cost; 2027 service changes unknown | Publish method, departure-time assumptions and raw responses; re-run near travel |
| 3 | Add a price-per-person menu column with official menu links | Makes dining cost comparison possible | Menus change; some restaurants publish no prices | Only use restaurant's own menu page; blank otherwise |
| 4 | Add Instagram/TikTok review links wherever available | Meets "as many links as you can" more fully | Platform links can rot; sponsored content bias | Open each link; record platform, creator and access date |
| 5 | Add a status column that updates after 14 Dec 2026 MICHELIN ceremony | Prevents stale star information | Requires a re-check task | Re-fetch all three official MICHELIN filter pages and diff against current table |
| 6 | Add a filterable "open on 15/16/17/18 Feb" view | Speeds itinerary decisions for the preferred 4-day trip | Needs complete hours per row | Fill all blank hours from official sources first |
| 7 | Add a map with official addresses and hotel markers | Visual clustering of Michelin restaurants | Map tiles/third-party script adds a dependency | Use only official address fields; note that marker positions are approximate if geocoded |
| 8 | Add a "confidence" score per row | Makes gaps obvious at a glance | Can be mistaken for a factual rating | Define the rubric explicitly and derive it only from flag counts |
| 9 | Add a decision log with dated choices | Helps a couple review why a hotel/date was picked | Requires user input, which this pass was asked to avoid | Only enable after the user supplies preferences |
| 10 | Add automated link checking in CI | Detects broken source links before publication | External sites may block CI requests | Keep failures as warnings; manual review before marking a link broken |
| 11 | Publish a printable one-page itinerary | Useful offline in NYC | Duplicated content can drift from tables | Generate from the same JSON data, not a separate hand-written file |
| 12 | Record hotel cancellation deadlines alongside rates | Reduces financial risk | Requires booking-engine detail per hotel | Capture from official rate rules only |

## Recommended path

1. First implement #5 and #1 (star-status refresh and dated rates) — they remove the biggest decision blockers.
2. Then #2 (real travel times), because the current hotel ranking is a proxy only.
3. Then #3 and #6 for dining/itinerary usability.
4. Treat #4, #7, #8, #9, #10, #11 and #12 as optional enhancements once the core numbers are verified.
