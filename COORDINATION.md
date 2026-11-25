# NYFun2 Coordination Board

Shared task board tracking tasks, owning sessions, file scopes, official sources, verification logs, and flagged irregularities.

> **Branch Policy Note:** This Arena session works exclusively on branch `arena/aad75793-nyfun2` (branched from `main` at `a3a2848`). All commits and pushes target `arena/aad75793-nyfun2`.

## Active Tasks

| Task ID | Task Description | Status | Session ID | Branch | File Scope | Notes |
|---|---|---|---|---|---|---|
| T-01 | Repo audit & coordination setup | in progress | `arena-aad75793` | `arena/aad75793-nyfun2` | `COORDINATION.md`, `README.md` | Initial repo contained only `README.md` (`# NYFun2`). GitHub Pages already enabled on `main` `/`. |
| T-02 | Michelin Guide NYC restaurant research, clusters, official hours, 2-adult costs & social review links | in progress | `arena-aad75793` | `arena/aad75793-nyfun2` | `data/michelin.json` | Verify every entry against `guide.michelin.com` and official restaurant sites; collect verified YouTube/TikTok/Instagram review links. |
| T-03 | NYC hotel research, private bath + queen/king verification, ≤1 hr MTA Michelin cluster ranking & Feb 15–Mar 23, 2027 7-night pricing analysis | in progress | `arena-aad75793` | `arena/aad75793-nyfun2` | `data/hotels.json`, `data/booking-windows.json` | Verify official hotel specs, transit distances, and real verified pricing; leave unconfirmed cells blank & flag. |
| T-04 | NYC activities research, official hours/exceptions, 2-adult pricing & social review links | in progress | `arena-aad75793` | `arena/aad75793-nyfun2` | `data/activities.json` | Verify every entry against official attraction sites; collect verified YouTube/TikTok/Instagram review links. |
| T-05 | Analysis: Executive Summary, Open Questions & Discovery Plan, Site Improvement Suggestions, Flagged for Review Audit | in progress | `arena-aad75793` | `arena/aad75793-nyfun2` | `data/analysis.json`, `data/flagged.json` | Capture date/duration conflicts, unverified values, booking timing insights, and decision gaps. |
| T-06 | GitHub Pages mobile-friendly dashboard build, line-by-line validation & link audit | in progress | `arena-aad75793` | `arena/aad75793-nyfun2` | `index.html`, `michelin.html`, `hotels.html`, `activities.html`, `itinerary.html`, `questions.html`, `suggestions.html`, `review.html`, `assets/*`, `.nojekyll` | Build clean responsive UI, verify zero broken internal links/data mismatches, test locally via preview server, publish via PR to `main`. |

## Session Activity Log

- **2026-11-25 UTC — `arena-aad75793`**: Audited repository (`NYFun2`, commit `a3a2848`). Found only `README.md` (`# NYFun2`). Confirmed GitHub Pages is configured at `https://kanlerxz87-cyber.github.io/NYFun2/` (legacy build from `main` `/`). Created `COORDINATION.md` and claimed tasks `T-01` through `T-06` for full end-to-end verified delivery.

## Verification Standards

1. Every table row MUST link to an official website (restaurant, hotel, attraction, or Michelin Guide / MTA official page).
2. Social media review links (YouTube, TikTok, Instagram) MUST be verified via live search results in this session — zero fabricated URLs or IDs.
3. Any value that cannot be confirmed from an official or verified primary source MUST be left blank (`null` / `""` rendered as `— Unverified`) and logged on `review.html` and in `data/flagged.json`.
4. All restaurant and activity costs are presented as **total for 2 adults** with explicit notes on tax, tip, or beverage exclusions per official menus.
5. Hotel costs are presented as **total for a 7-night stay (2 adults)** where verified, with exact check-in/check-out dates and booking source noted.
