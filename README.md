# NYFun2 — New York City trip plan, February 2027

A static, source-audited planning dashboard for two adults in New York City, built around
MICHELIN-starred dining, hotels with a private bathroom and a queen-or-larger bed, and a
one-hour travel goal.

**Live site:** https://kanlerxz87-cyber.github.io/NYFun2/

**Travel window:** preferred 15–18 Feb 2027 (3 nights); priced case 15–22 Feb 2027 (7 nights,
Monday → Monday). The permitted range is 15 Feb – 23 Mar 2027.

---

## The rule this project runs on

> Every table row carries a source URL. Values that cannot be confirmed are left blank and
> flagged — never estimated.

Where the site performs arithmetic itself (a published adult price × 2, or a published tax rate
added to a published pre-tax total), the formula is printed next to the result. A review video is
labelled third-party; it is never presented as an official endorsement or used to establish a
price or opening hour.

## What is here

| Path | Purpose |
|---|---|
| `index.html` | Dashboard / overview |
| `pages/executive-summary.html` | Decision-ready summary |
| `pages/michelin-restaurants.html` | 72 restaurant rows — star level, opening days, hours, couple prices, social links, sources |
| `pages/hotels.html` | 16 hotel candidates, 8 with dated 7-night totals, 10 with verified room/bath facts |
| `pages/activities.html` | 18 activities and date-specific events with opening days, hours, exceptions and social links |
| `pages/itinerary.html` | How the ≤1-hour travel goal is handled |
| `pages/research.html` | 25 measured transit legs, 5 price windows, hotel ranking and cross-session findings |
| `pages/questions.html` | 13 questions: known / missing / how to discover |
| `pages/suggestions.html` | 14 improvement options, each awaiting review |
| `pages/flagged.html` | 23 flags: every unverified value, conflict and irregularity |
| `pages/sources.html` | Primary-source register and verification rules |
| `pages/repo-audit.html` | Repository audit and the session integration log |
| `data/*.json` | Restaurants, hotels, activities, decisions and cross-session evidence |
| `assets/styles.css` · `assets/app.js` | Styling and table rendering (no dependencies) |
| `scripts/integrate_final.py` | Reproducible final-integration merge from the read-only session kits |
| `scripts/verify.py` | Pre-push verification |
| `COORDINATION.md` | Shared task board and session log |
| `alt/`, `sessions/**` | Independent parallel kits preserved verbatim for comparison |
| `LICENSE` | MIT for code, CC BY 4.0 for data and prose |

## Headline findings

- **MICHELIN counts (official filter panel, 25 Nov 2026):** 5 three-star, 14 two-star, 50 one-star,
  76 Bib Gourmand, 224 guide-listed with no star. The canonical roster has all 69 starred rows
  plus 3 Guide-listed additions. **19 couple food totals** were verified from official menus,
  FAQs and booking pages; Per Se remains blank because its Tock page shows deposits only.
- **Hotels:** 16 candidates; 10 have an official queen/king + private-bath specification and 8
  have a dated 7-night total for 15–22 Feb 2027. Four totals were captured independently by two
  sessions and agree: Hyatt Place Chelsea $1,305 · Arlo NoMad $1,428 · 11 Howard $1,774 ·
  Beekman $5,220 (all-in, aggregator snapshots).
- **Cheapest qualifying week:** 15–22 Feb 2027, $848 pre-tax / ~$998 all-in at Eurostars Wall
  Street. The $836 22 Feb–1 Mar result is a twin room and is disqualified. No source forecasts a
  future date when rates will be lowest, so the site does not assert one (flag F23).
- **Transit:** 25 measured door-to-door legs (Google Maps transit, 25 Nov 2026, 17:14–17:31 ET)
  are all ≤37 minutes; the one-hour rule does not separate the tested Manhattan hotels.
- **Date-critical activities:** Chinatown Lunar New Year parade on Sun 21 Feb 2027 at 13:00;
  Bryant Park Winter Village closes 28 Feb 2027; Wollman Rink runs to 16 Mar 2027.
- **Risk:** the MICHELIN Northeast Cities ceremony is on 14 Dec 2026, between research and travel;
  star levels may change (F1). All Nov-2026 prices need re-confirmation before booking.

## Verify locally

```bash
python3 scripts/verify.py     # local links, JSON validity, source-per-row, blank-implies-flag
node --check assets/app.js    # JS syntax
python3 -m http.server 8000   # then open http://localhost:8000/
```

No build step and no third-party dependencies at runtime: the site is HTML, one stylesheet, one
script and JSON. `.github/workflows/verify.yml` runs the same checks on pushes and pull requests.

## Publishing

GitHub Pages serves `main` at the repository root; `.nojekyll` is present so Jekyll does not
process the folder. Merging a verified pull request to `main` deploys the site.

## Coordination

Many agent sessions worked this repository on separate branches. Their work was merged, not
overwritten: the canonical tables are the shared output, and `alt/` plus `sessions/**` preserve
the independent kits as evidence. See `COORDINATION.md` for the task board, source log and
flagged irregularities, and `pages/repo-audit.html` for the integration history.

## Licence

Code: MIT. Data and prose: CC BY 4.0. Third-party marks, quotations and source pages remain the
property of their owners. See `LICENSE`.
