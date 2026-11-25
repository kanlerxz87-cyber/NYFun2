# NYFun2 Coordination Board

Shared task board tracking tasks, owning sessions, file scopes, official sources, verification logs, and flagged irregularities.

> **Branch Policy Note:** This Arena session works exclusively on branch `arena/aad75793-nyfun2` (branched from `main` at `a3a2848`). All commits and pushes target `arena/aad75793-nyfun2`.

## Active Tasks

| Task ID | Task Description | Status | Session ID | Branch | File Scope | Notes |
|---|---|---|---|---|---|---|
| T-01 | Repo audit & coordination setup | done | `arena-aad75793` | `arena/aad75793-nyfun2` | `COORDINATION.md`, `README.md` | Verified public repo `kanlerxz87-cyber/NYFun2`, GitHub Pages active on `main` `/`. Updated both docs. |
| T-02 | Michelin Guide NYC restaurant research, clusters, official hours, 2-adult costs & social review links | done | `arena-aad75793` | `arena/aad75793-nyfun2` | `data/michelin.json`, `data/meta.json` | Live 5-borough totals verified (`369` = `69` starred + `300` listed). All 27 curated restaurants verified against official websites + `guide.michelin.com` + live YT/TikTok/IG reviews; 3 unverified dinner prices left blank & flagged. |
| T-03 | NYC hotel research, private bath + queen/king verification, ≤1 hr MTA Michelin cluster ranking & Feb 15–Mar 23, 2027 7-night pricing analysis | done | `arena-aad75793` | `arena/aad75793-nyfun2` | `data/hotels.json`, `data/meta.json` | 11 hotels verified (Queen/King + private bath + ≤35 min MTA transit) across 6 date windows (Feb 15–Mar 22, 2027). Explicit pre-tax vs. all-in labels; Motto wall-bed & Ace full-bed tiers bypassed; AC Downtown unavailability logged. |
| T-04 | NYC activities research, official hours/exceptions, 2-adult pricing & social review links | done | `arena-aad75793` | `arena/aad75793-nyfun2` | `data/activities.json` | 18 activities verified against official sites (incl. AMNH $37 2026–27 rate, Bryant Park Feb 28 close, Wollman Mar 14–16 free days & Mar 16 close, Chinatown LNY Parade Sun Feb 21). |
| T-05 | Analysis: Executive Summary, Open Questions & Discovery Plan, Site Improvement Suggestions, Flagged for Review Audit | done | `arena-aad75793` | `arena/aad75793-nyfun2` | `data/analysis.json`, `data/itinerary.json` | Built 2 switchable 7-night couple itineraries, 3 total-cost scenarios, 8 prioritized Open Questions, 7 Roadmap Suggestions & 11 Flagged Audit items. |
| T-06 | GitHub Pages mobile-friendly dashboard build, line-by-line validation & link audit | done | `arena-aad75793` | `arena/aad75793-nyfun2` | `index.html`, `michelin.html`, `hotels.html`, `activities.html`, `itinerary.html`, `questions.html`, `suggestions.html`, `review.html`, `assets/styles.css`, `assets/app.js`, `.nojekyll` | All 8 pages + shared responsive CSS/JS built, validated programmatically & tested via live preview server. Ready for PR to `main`. |

## Session Activity Log

- **2026-11-25 UTC — `arena-aad75793`**: Audited repository (`NYFun2`, commit `a3a2848`). Confirmed GitHub Pages at `https://kanlerxz87-cyber.github.io/NYFun2/` (`main` `/`). Claimed `T-01`–`T-06`.
- **2026-11-25 UTC — `arena-aad75793`**: Completed primary-source verification of MTA 2026–27 fares (`$3.00`, `$35/pp` 7-day OMNY cap), NYC hotel occupancy tax (`14.75% + flat`), 11 hotels across 6 Booking.com 2027 windows, live 5-borough NYC Michelin totals (`369`), 27 curated Michelin restaurants with live social review links, and 18 winter/early-spring NYC activities with live social review links.
- **2026-11-25 UTC — `arena-aad75793`**: Built full structured JSON layer (`data/*.json`) and 8-page responsive GitHub Pages dashboard (`index.html` through `review.html` + `assets/*` + `.nojekyll`). Passed schema, cross-file math, internal link, and live local server checks.

## Verification Standards

1. Every table row MUST link to an official website (restaurant, hotel, attraction, or Michelin Guide / MTA official page).
2. Social media review links (YouTube, TikTok, Instagram) MUST be verified via live search results in this session — zero fabricated URLs or IDs.
3. Any value that cannot be confirmed from an official or verified primary source MUST be left blank (`null` / `""` rendered as `— Unverified`) and logged on `review.html` and in `data/analysis.json`.
4. All restaurant and activity costs are presented as **total for 2 adults** with explicit notes on tax, tip, or beverage exclusions per official menus.
5. Hotel costs are presented as **total for a 7-night stay (2 adults)** where verified, with exact check-in/check-out dates, tax basis, and booking source noted.
