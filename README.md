# NYFun2 — New York City trip plan, February–March 2027

A mobile-friendly, source-audited planning dashboard for two adults. The preferred dates are **15–18 February 2027** (3 nights); the canonical seven-night hotel comparison uses **15–22 February 2027**. The full allowed trip window is 15 February–23 March 2027.

**Live site:** https://kanlerxz87-cyber.github.io/NYFun2/

## Use the dashboards

**Travel window:** preferred 15–18 Feb 2027; priced case 15–22 Feb 2027 (Monday → Monday, 7 nights); full allowed window 15 Feb–23 Mar 2027.
**Date-critical:** the 29th Chinatown Lunar New Year Parade is on Sun 21 Feb 2027 — it is only catchable on the 7-night window, not the preferred 15–18 Feb trip. Wollman Rink closes 16 Mar 2027; Bryant Park Winter Village closes 28 Feb 2027. Michelin's 2026 ceremony is 14 Dec 2026 (before the trip).

The root site is the canonical source-linked catalogue. The separate [T17 detailed planning kit](https://kanlerxz87-cyber.github.io/NYFun2/sessions/c1cf7b23/index.html) is a curated, independently researched comparison with additional dated hotel windows, measured transit data and social links. The kits retain separate datasets and assumptions; do not combine their prices without checking each source and flag.

| Path | Contents |
|---|---|
| `index.html` | Overview, decision warning, date-critical notice and links to all planning views |
| `pages/executive-summary.html` | Decision brief, risks and decision sequence |
| `pages/michelin-restaurants.html` | 72 records: 69 starred in the 25 Nov 2026 snapshot plus 3 Guide-listed additions; star status, hours, 16 verified couple menu totals (Sushi Sho $990 added 2026-11-26) and flags |
| `pages/hotels.html` | 12 hotel candidates; 4 dated 7-night totals from third-party rate pages, 8 unpriced |
| `pages/activities.html` | 15 activities with official hours, exceptions, costs where published, route-query links and official social accounts (incl. Wollman Rink, Bryant Park Winter Village, 21 Feb 2027 Chinatown LNY Parade) |
| `pages/itinerary.html` | Itinerary and one-hour routing limits |
| `pages/questions.html` | 12 open questions, known facts, information gaps and discovery steps |
| `pages/suggestions.html` | 12 options for improving decision-making, awaiting review |
| `pages/flagged.html` | 20 flags: irregularities, unverified fields and time-sensitive cautions |
| `pages/sources.html` | Primary-source register and verification rules |
| `pages/repo-audit.html` | Repository and integration history, with the latest consistency check |
| `sessions/c1cf7b23/` | Independent detailed kit: 31 curated Michelin venues, 10 hotels, 18 activities and its own datasets, flags and verifier |
| `sessions/33cfdba4/` | Kit with a measured 25-leg transit matrix and five hotel pricing windows |
| `sessions/657520df/` | Kit with 10 audited hotels (pre-tax + all-in 7-night totals), 27 Michelin rows and 23 verified prices |
| `data/` | Canonical JSON datasets |
| `assets/styles.css`, `assets/app.js` | Responsive layout and table rendering; no third-party runtime dependencies |
| `scripts/verify.py` | Local-link, JSON, source-URL and blank-field checks |
| `COORDINATION.md` | Shared task board, verification notes and integration log |

## Findings and limits

- **Michelin:** canonical records contain 69 starred restaurants (5 three-star, 14 two-star, 50 one-star) plus 3 Guide-listed additions with no star, based on the 25 Nov 2026 snapshot. Michelin's announced 14 Dec 2026 ceremony occurs before the trip; re-check distinctions after that date.
- **Restaurant costs:** 16 canonical restaurant records have an official-source two-adult menu total. Totals are menu/food amounts, not a full bill with tax, tip, drinks or add-ons unless a row explicitly says otherwise. Prices may change before travel.
- **Hotels:** four canonical rows have dated 15–22 Feb 2027 totals captured from Booking.com on 25 Nov 2026. They are third-party snapshots, not hotel quotes; eight of twelve candidates remain unpriced. The canonical dataset does not prove the cheapest week across the entire requested window. The separate T17 kit has a five-window sweep with its own rate evidence and eligibility checks.
- **Transit:** the canonical hotel ranking does not assert a one-hour Michelin-reach score. The T17 kit reports transit measurements for its own hotel/cluster set; see its methodology and flags before relying on a comparison.
- **Open decisions:** trip length, total budget, airport/airfare, dietary and accessibility requirements, and the exact hotel are unresolved. The Questions and Suggestions pages make the gaps and next steps explicit.

## Evidence policy

Every factual row in the category tables links to a primary or official source. Values that could not be confirmed are left blank and explained in the Flags page. Arithmetic (such as multiplying an official per-person menu price by two, or applying a published tax basis) is identified in context. User-generated reviews are labelled third-party and are not treated as official endorsements. Dated prices and hours are time-sensitive and should be rechecked before booking.

## Verify locally

```bash
python3 scripts/verify.py
python3 sessions/c1cf7b23/scripts/verify.py
node --check assets/app.js
python3 -m http.server 8000
```

The root dashboard is static HTML/CSS/JavaScript with local JSON data. GitHub Pages serves `main` from the repository root; `.nojekyll` is present.

## Repository review

## Sessions and coordination

GitHub Pages is configured to serve `main` at the repository root, so a merge to `main` deploys. `.nojekyll` is present so Jekyll does not process the folder. `COORDINATION.md` is the shared task board: it records task ownership, evidence sources, verification performed and irregularities. No claim is made that a static verifier can prove an external URL remains live or that every cited source is an official page; review row-level sources and flags before purchase. See `pages/repo-audit.html` for historical integration decisions and the latest audit.

On 2026-11-26 (session arena/45972379-nyfun2) the canonical data absorbed the verified official activity social accounts from `research/activity-socials.md`, added the three date-critical winter 2027 activity rows (re-verified live), re-verified Sushi Sho's Tock price ($990 for two) and Per Se's Tock pages (Salon now Four-Course at a $150/pp deposit — blank stays flagged), and linked the session kits from the dashboard.

## Licence

Code: MIT. Data and prose: CC BY 4.0. Third-party marks, quotations and linked source content remain the property of their owners. See `LICENSE`.
