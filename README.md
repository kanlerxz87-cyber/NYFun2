# NYFun2 — New York City trip plan, February 2027

A static, source-audited planning dashboard for two adults in New York City, built around MICHELIN-starred dining, qualifying hotels, and date-aware activities.

**Live site:** https://kanlerxz87-cyber.github.io/NYFun2/

**Travel window:** preferred 15–18 Feb 2027; hotel comparison case 15–22 Feb 2027 (Monday → Monday, 7 nights).

---

## The rule this project runs on

> Every factual table row carries an official or primary source. Values that cannot be confirmed stay blank and flagged — never estimated.

Hotel rates are a separately labelled exception in source type, not certainty: the dated rates are Booking.com aggregator snapshots, not hotel-official quotes. No modeled all-in total is presented; recheck the exact room, fee/tax line and cancellation plan at checkout.

Where the site performs arithmetic on a published per-person price, it shows the menu and basis. A review video is labelled third-party; it is never presented as an official endorsement.

## What is here

| Path | Purpose |
|---|---|
| `index.html` | Dashboard / overview |
| `pages/executive-summary.html` | Decision-ready summary |
| `pages/michelin-restaurants.html` | 72 rows: the 69 starred roster plus 3 Guide-listed additions, with 19 current menu/booking-price records |
| `pages/hotels.html` | 10 named Queen/King-bed + private-bath room options; 8 have dated 7-night aggregator snapshots |
| `pages/activities.html` | 15 attractions/events with official hours, exceptions and published couple costs where available |
| `pages/itinerary.html` | One-hour travel evidence, its limits and planning workflow |
| `pages/questions.html` | 12 open questions: known / missing / how to discover |
| `pages/suggestions.html` | 12 improvement options and implementation status |
| `pages/flagged.html` | 20 flags: unverified values, conflicts and date-sensitive caveats |
| `pages/sources.html` | Primary-source register and verification rules |
| `pages/repo-audit.html` | Repository history, integration notes and verification evidence |
| `data/restaurants.json` | Restaurant dataset and row-level price evidence |
| `data/hotels.json` | Qualifying hotel room specs and dated OTA observations |
| `data/activities.json` | Activity hours, seasonal dates and current prices |
| `data/decisions.json` | Questions, suggestions and flags |
| `assets/styles.css` · `assets/app.js` | Styling and table rendering (no dependencies) |
| `scripts/verify.py` | Pre-push structure, source and link verification |
| `COORDINATION.md` | Shared task board and session log |
| `alt/` | Independent alternate kit, preserved for comparison |
| `sessions/` | Other completed, namespaced research kits and data |
| `LICENSE` | MIT for code, CC BY 4.0 for data and prose |

## Headline findings

- **MICHELIN roster (checked 25 Nov 2026):** 5 three-star, 14 two-star and 50 one-star restaurants (69 starred), plus 3 Guide-listed additions without a star. The 14 Dec 2026 ceremony is between the research and the trip; distinctions may change.
- **Restaurant prices:** 19 venues now have an official menu or booking-channel price for two, checked 25–26 Nov 2026. These are current menu snapshots, not February–March 2027 quotes; tax, gratuity, beverages and administrative fees vary by source and are documented row by row.
- **Hotels:** 10 properties have a named Queen/King room and private bathroom verified on a primary room page. Eight have a 15–22 Feb 2027 Booking.com pre-tax snapshot (captured 25–26 Nov); two remain unpriced. Rates are volatile aggregator observations, not hotel quotes. Final checkout totals and the cheapest booking window remain blank.
- **Seasonal anchors:** Wollman Rink's season runs through 16 Mar 2027, but 15 Feb is a restricted Community Day; Bryant Park's rink/Lodge close 28 Feb; the Chinatown parade is announced for 21 Feb at 13:00, with a year typo in one Chinese-language line.
- **Travel-time evidence:** 25 Google Maps transit-mode “leave now” route snapshots, captured 25 Nov 2026 from five hotel origins to five MICHELIN clusters, ranged from 3–37 minutes. They include some walk-only results and are not future February schedules or a complete matrix for all ten shortlisted hotels.
- **MTA fare:** the official fare page checked 25 Nov 2026 lists $3 for subway/local bus and $7.25 for express bus.

## Deliberately blank / not guaranteed

No verified hotel final-checkout totals, no cheapest booking window, no February 2027 restaurant menu prices, no airfare, no show-specific theatre tickets, and no unconfirmed room or activity values. “Current” prices and hours may change; use the linked source and re-check before making a reservation. Google Maps times are live estimates from their capture moment, not a timetable or travel-date guarantee.

## Verify locally

```bash
python3 scripts/verify.py     # local links, JSON, official sources, hotel room/bath evidence
node --check assets/app.js    # JS syntax
python3 -m http.server 8000   # then open http://localhost:8000/
```

No build step and no third-party dependencies: the site is HTML, one stylesheet, one script and JSON.

## Publishing

GitHub Pages is configured to serve `main` at the repository root, so a merge to `main` deploys. `.nojekyll` is present so Jekyll does not process the folder.

## Sessions and coordination

Multiple agent sessions contributed on separate branches and namespaced kits. The root site is the canonical integrated version; independent kits are preserved under `alt/` and `sessions/`. See `COORDINATION.md` for ownership, sources, reconciliation decisions and the integration log.

## Licence

Code: MIT. Data and prose: CC BY 4.0. Third-party marks, quotations and source pages remain the property of their owners. See `LICENSE`.
