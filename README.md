# NYFun2 — New York City trip plan, February–March 2027

A static, source-audited planning dashboard for **two adults** in New York City inside the
**15 Feb – 23 Mar 2027** window, built around MICHELIN dining and hotels that publish a
**queen-or-larger bed and a private bathroom**.

**Live site:** https://kanlerxz87-cyber.github.io/NYFun2/

**Preferred trip:** 15–18 Feb 2027 (Mon–Thu, 3 nights).
**Priced case:** 15–22 Feb 2027 (Mon–Mon, 7 nights) — the window the brief asked to price.

**Travel window:** preferred 15–18 Feb 2027; priced case 15–22 Feb 2027 (Monday → Monday, 7 nights); full allowed window 15 Feb–23 Mar 2027.
**Date-critical:** the 29th Chinatown Lunar New Year Parade is on Sun 21 Feb 2027 — it is only catchable on the 7-night window, not the preferred 15–18 Feb trip. Wollman Rink closes 16 Mar 2027; Bryant Park Winter Village closes 28 Feb 2027. Michelin's 2026 ceremony is 14 Dec 2026 (before the trip).

The root site is the canonical source-linked catalogue. The separate [T17 detailed planning kit](https://kanlerxz87-cyber.github.io/NYFun2/sessions/c1cf7b23/index.html) is a curated, independently researched comparison with additional dated hotel windows, measured transit data and social links. The kits retain separate datasets and assumptions; do not combine their prices without checking each source and flag.

> Every table row carries a link to the official page it came from. A value that cannot be
> confirmed is **blank and flagged** — never estimated, and never inferred from a similar venue.

Where the site does arithmetic (2 × a published per-person menu price, or a published pre-tax
hotel total plus the stated 14.75% NYC occupancy/sales tax), the formula is printed next to the
result. Review videos are labelled third-party; they are never presented as official.

Each row also carries a dated verification badge:

| Badge | Meaning |
|---|---|
| **checked YYYY-MM-DD** | The official source was read on the date shown; this does not imply it was rechecked today. A row's notes and the verification log describe any field-specific scope. |
| **carried YYYY-MM-DD** | The value comes from the dated capture shown; the source link is on the row |

## Pages

| Page | What it answers |
|---|---|
| `index.html` | Overview, headline numbers, how to read a row |
| `pages/executive-summary.html` | Bottom line, findings, decision order, illustrative weekly budget |
| `pages/michelin-restaurants.html` | All 72 rows (69 starred + 3 guide-listed), verified couple prices, the five cluster anchors |
| `pages/hotels.html` | 16 candidates, ranking rule, dated 7-night totals, five booking windows, when to book |
| `pages/activities.html` | 18 activities with official hours, closures and couple costs |
| `pages/itinerary.html` | 7-night skeleton from verified opening days, plus the 3-night variant |
| `pages/questions.html` | 13 questions: known / missing / provisional answer / how to close |
| `pages/suggestions.html` | 17 improvement options with status and effort |
| `pages/flagged.html` | 33 flags: unverified values, conflicts, irregularities |
| `pages/verification.html` | Dated log of 25 baseline records from 2026-11-26 plus 21 addendum checks from 2026-11-27; per-row status shows verified vs carried |
| `pages/sources.html` | Rules, primary-source register, reproduce steps |
| `pages/repo-audit.html` | What each session contributed, what this integration changed |
| `pages/compare.html` | The five parallel session kits and their disagreements |

## Findings and limits

- **MICHELIN census (re-checked 2026-11-26):** 5 three-star, 14 two-star, 50 one-star (69 starred),
  76 Bib Gourmand, 224 Selected.
- **Dining money:** 25 restaurants have a couple total built from an official menu/FAQ/booking
  page — from **$156** (Gramercy Tavern tavern three-course) and **$168** (Cote Butcher's Feast)
  to **$1,900** (Masa hinoki counter). Atera and Per Se stay blank because captures
  disagree or the page only shows a deposit (flag F24); Atomix carries its verified
  November Tock price ($848/$628) with December ($990/$704+) flagged.
- **Hotels:** 16 candidates; 8 carry a dated 7-night total for two adults for 15–22 Feb 2027 —
  from **$998 all-in** (Eurostars Wall Street, non-refundable) to **$5,220** (The Beekman).
  Best value with free cancellation: **DoubleTree Chelsea, $1,110 all-in**.
- **The one-hour rule:** 25 measured hotel→MICHELIN-cluster legs were all **3–37 minutes**, so
  the rule does not separate central Manhattan hotels. It is used as a pass/fail gate; the ranking
  falls through to verified price, then average transit.
- **Cheapest week:** 15–22 Feb 2027 is the cheapest of the five weeks tested ($848 pre-tax floor)
  versus $1,087–$1,260 for the March windows. The $836 figure for 22 Feb–1 Mar is a **twin room**
  and fails the queen-bed rule.
- **Dates that matter:** Presidents' Day Mon 15 Feb; **Chinatown Lunar New Year parade Sun 21 Feb
  2027, 13:00** (catchable only on the 7-night window); Bryant Park rink to 28 Feb; Wollman Rink to
  16 Mar (16–21 Feb peak, 22 Feb–13 Mar off-peak); the Met closes Wednesdays.
- **Michelin ceremony:** 14 Dec 2026 — after this research, before the trip (flag F1).

## Data and build

| Path | Purpose |
|---|---|
| `data/restaurants.json` | 72 rows, per-field `provenance`, verification badge |
| `data/hotels.json` | 16 rows + 5 booking windows + transit objects + ranking |
| `data/activities.json` | 18 rows with hours, exceptions, costs, socials |
| `data/decisions.json` | 13 questions, 17 suggestions, 33 flags |
| `data/verification.json` | Dated verification log and coverage counters |
| `data/conflicts.json` | Every kit disagreement and out-of-census venue name |
| `research/canonical/` | Pristine pre-merge datasets (the merge input) |
| `scripts/build_data.py` | Idempotent merge of the kits into `data/*.json` |
| `scripts/build_site.py` | Renders `index.html` and `pages/*.html` |
| `scripts/verify.py` | Links, sources, duplicates, blank-implies-flag, hotel arithmetic |
| `assets/styles.css` · `assets/app.js` | Styling and table rendering (no dependencies) |

```bash
python3 scripts/build_data.py     # merge kits -> data/*.json
python3 scripts/build_site.py     # data/*.json -> html
python3 scripts/verify.py         # 0 errors / 0 warnings required
node --check assets/app.js
python3 -m http.server 8000       # then open http://localhost:8000/
```

`.github/workflows/verify.yml` repeats the JSON/link/source and JavaScript-syntax checks on every
push and pull request, so a broken site cannot merge silently.

There is no build step on the host: GitHub Pages serves the repository root from `main`, and
`.nojekyll` stops Jekyll processing.

## What is deliberately blank

Airfare; theatre tickets; the 3-night hotel total; per-dish à-la-carte totals; one hotel (The Maritime)
without a published bed-and-bathroom line; 45 of 72 restaurant social links that could not be confirmed; every
transit pair that was never routed. Each gap is on `pages/flagged.html` with its cause and the
step that would close it.

## Sessions and coordination

Several agent sessions worked this repository in parallel. Their kits are preserved verbatim under
`sessions/` and `alt/`, and the comparison is on `pages/compare.html`. The shared task board
`COORDINATION.md` records ownership, sources and irregularities.

This build ran as task **T24** on branch `arena/9bc6abed-nyfun2`, after sessions
`arena/547ee3a3-nyfun2` (T18) and `arena/45972379-nyfun2` (T21–T23) merged PRs #18–#22 to `main`
mid-task. Rather than overwrite them, the branch merged `main` and adopted **main's datasets as the
new canonical base**, so their verified findings (Sushi Sho's Tock price, Per Se's deposit-only
pages, the Wollman/Bryant Park/Lunar New Year rows, the official activity socials, flags F18–F20)
are all in this build. The merge is recorded on `pages/repo-audit.html` and in `COORDINATION.md`.

## Licence

MIT for code; CC BY 4.0 for data and prose. Restaurant and hotel facts belong to their sources.
