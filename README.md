# NYFun2 — NYC Couples Trip Intelligence Dashboard (Feb 15 – Mar 23, 2027)

Live GitHub Pages site (published from `main` `/`): **https://kanlerxz87-cyber.github.io/NYFun2/**

A verified, mobile-friendly travel planning dashboard built for **2 adults (a couple)** visiting New York City during **February 15 – March 23, 2027** — focused on Michelin Guide dining, Queen/King private-bath hotels within ≤ 1 hour MTA subway transit, winter/early-spring activities, 7-night budget modeling, and radical source transparency.

## Dashboard Pages

| Page | Purpose |
|---|---|
| `index.html` | Executive Summary, KPI Snapshot, 5-Borough Michelin Guide Overview, Feb vs. Mar 2027 Hotel Surge Bars & 2026–2027 Action Timeline |
| `michelin.html` | Live Official NYC 5-Borough Michelin Totals (`369` total: `69` Starred vs. `300` Listed), 5 Subway Clusters & Filterable Table of 27 Curated Restaurants (2-Adult Prices, Hours, Drop Windows & Verified YouTube/TikTok/IG Reviews) |
| `hotels.html` | Live 2027 Booking.com USD Rate Comparison across 6 Stay Windows (Feb 15 – Mar 22), 3-Phase When-to-Book Playbook & 11 Verified Queen/King Private-Bath Hotels |
| `activities.html` | 18 Verified Winter/Early-Spring NYC Activities with 2-Adult Total Pricing, 2027 Seasonal Closing Alerts (Chinatown LNY Parade Feb 21, Bryant Park closes Feb 28, Wollman Rink FREE Mar 14–16 & closes Mar 16) & Verified Social Reviews |
| `itinerary.html` | Switchable Zero-Backtracking 7-Night Itineraries (`Feb 22 – Mar 1` Recommended & `Feb 15 – Feb 22` Lunar New Year Alternative), 3 Couple Budget Scenarios & Interactive Live 2-Adult Budget Calculator |
| `questions.html` | Prioritized P0 / P1 / P2 Open Questions & Discovery Plan with browser-saved notes and 1-click brief export |
| `suggestions.html` | Prioritized Site & Trip-Planning Improvement Roadmap |
| `review.html` | Complete **Flagged for Review** Audit Ledger tracking every intentionally blank/unverified price, schedule discrepancy, bed-size safeguard, tax-basis label & upcoming Dec 2026 Michelin update |

## Verified Data Architecture (`data/`)

- `data/meta.json` — Official MTA 2026–2027 fare schedule (`$3.00` base ride, `$35/person` = `$70/couple` 7-day OMNY rolling cap), NYC Hotel Tax law (`5.875%` occupancy + `8.875%` sales = `14.75%` + flat nightly fees), live 5-borough Michelin Guide totals (`guide.michelin.com`, verified Nov 25, 2026), and key 2026–2027 calendar milestones.
- `data/michelin.json` — 5 subway clusters & 27 deeply verified restaurants (all 5×3★, 6×2★, 7×1★, 5 Bib Gourmand, 4 Selected).
- `data/hotels.json` — 11 shortlisted hotels (verified Queen/King + private bath + ≤35 min MTA transit to all clusters), 6 date-window pricing comparisons & booking timing playbook.
- `data/activities.json` — 18 verified NYC activities with official hours, holiday/winter exceptions, 2-adult prices & verified social reviews.
- `data/itinerary.json` — Two 7-night couple itineraries + 3 transparent budget scenarios.
- `data/analysis.json` — Executive Summary, 8 Open Questions, 7 Improvement Suggestions & 11 Flagged Audit items.

## Verification & Zero-Inference Standards

- **Verified Date:** November 25, 2026.
- **Official Primary Sources Only:** Every hotel, restaurant, and attraction links directly to its official website (plus `guide.michelin.com`, `mta.info`, `nyc.gov`, and Booking.com live quotes).
- **Zero Hallucinated Prices or Links:** Prices that could not be verified from official menus (`The Four Horsemen`, `Laser Wolf Brooklyn`, and `Manhatta` regular Dining Room prix fixe) and missing room square footage (`Artezen Hotel`) are intentionally left **blank / flagged as Unverified** rather than inferred.
- **Verified Social Media Reviews:** Every YouTube, TikTok, and Instagram link was gathered directly from live search results during verification.

## Local Preview

```bash
python3 -m http.server 8000 --bind 0.0.0.0
```

Then open `http://localhost:8000/`.
