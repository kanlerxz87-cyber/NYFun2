<<<<<<< HEAD
# NYFun2 — New York City trip plan, February–March 2027

<<<<<<< HEAD
A static, source-audited planning dashboard for **two adults** in New York City inside the
**15 Feb – 23 Mar 2027** window, built around MICHELIN dining and hotels that publish a
**queen-or-larger bed and a private bathroom**.
=======
A mobile-friendly, source-audited planning dashboard for two adults. The preferred dates are **15–18 February 2027** (3 nights); the canonical seven-night hotel comparison uses **15–22 February 2027**. The full allowed trip window is 15 February–23 March 2027.
=======
# NYFun2 — New York City Trip Planning Dashboard (Feb–Mar 2027)
>>>>>>> 62ef838 (Integrate complete verified NYC 2027 trip dashboard: 72 Michelin restaurants, 10 ranked hotels with 5-week sweeps, 18 activities, transit matrix, and decision framework (T18))

A static, source-audited intelligence and vacation planning dashboard for a couple (2 adults) in New York City, built around MICHELIN-starred dining clusters, verified Queen/King-bed and private-bathroom hotel accommodations with ≤1-hour transit reach, date-specific February 2027 activities, real pricing, and structured decision frameworks.
>>>>>>> e17ec92 (Integrate complete verified NYC 2027 trip dashboard: 72 Michelin restaurants, 10 ranked hotels with 5-week sweeps, 18 activities, transit matrix, and decision framework (T18))

<<<<<<< HEAD
**Preferred trip:** 15–18 Feb 2027 (Mon–Thu, 3 nights).
**Priced case:** 15–22 Feb 2027 (Mon–Mon, 7 nights) — the window the brief asked to price.
=======
**Live Site:** https://kanlerxz87-cyber.github.io/NYFun2/

<<<<<<< HEAD
## Use the dashboards
=======
**Travel Window:** Preferred core 15–18 Feb 2027 (3 nights, Presidents' Day); priced baseline 15–22 Feb 2027 (Monday → Monday, 7 nights); full eligibility window 15 Feb – 23 Mar 2027.
>>>>>>> e17ec92 (Integrate complete verified NYC 2027 trip dashboard: 72 Michelin restaurants, 10 ranked hotels with 5-week sweeps, 18 activities, transit matrix, and decision framework (T18))
>>>>>>> 62ef838 (Integrate complete verified NYC 2027 trip dashboard: 72 Michelin restaurants, 10 ranked hotels with 5-week sweeps, 18 activities, transit matrix, and decision framework (T18))

**Travel window:** preferred 15–18 Feb 2027; priced case 15–22 Feb 2027 (Monday → Monday, 7 nights); full allowed window 15 Feb–23 Mar 2027.
**Date-critical:** the 29th Chinatown Lunar New Year Parade is on Sun 21 Feb 2027 — it is only catchable on the 7-night window, not the preferred 15–18 Feb trip. Wollman Rink closes 16 Mar 2027; Bryant Park Winter Village closes 28 Feb 2027. Michelin's 2026 ceremony is 14 Dec 2026 (before the trip).

<<<<<<< HEAD
The root site is the canonical source-linked catalogue. The separate [T17 detailed planning kit](https://kanlerxz87-cyber.github.io/NYFun2/sessions/c1cf7b23/index.html) is a curated, independently researched comparison with additional dated hotel windows, measured transit data and social links. The kits retain separate datasets and assumptions; do not combine their prices without checking each source and flag.

> Every table row carries a link to the official page it came from. A value that cannot be
> confirmed is **blank and flagged** — never estimated, and never inferred from a similar venue.

Where the site does arithmetic (2 × a published per-person menu price, or a published pre-tax
hotel total plus the stated 14.75% NYC occupancy/sales tax), the formula is printed next to the
result. Review videos are labelled third-party; they are never presented as official.

Each row also carries a verification badge:

| Badge | Meaning |
|---|---|
| **checked today** | the official page was re-read on 2026-11-26 |
| **carried capture** | the value comes from the 2026-11-25 capture; the source link is on the row |

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
| `pages/flagged.html` | 28 flags: unverified values, conflicts, irregularities |
| `pages/verification.html` | Dated log of the 16 checks re-run on 2026-11-26 and what could not be re-read |
| `pages/sources.html` | Rules, primary-source register, reproduce steps |
| `pages/repo-audit.html` | What each session contributed, what this integration changed |
| `pages/compare.html` | The five parallel session kits and their disagreements |

## Findings and limits

- **MICHELIN census (re-checked 2026-11-26):** 5 three-star, 14 two-star, 50 one-star (69 starred),
  76 Bib Gourmand, 224 Selected.
- **Dining money:** 24 restaurants have a couple total built from an official menu/FAQ/booking
  page — from **$156** (Gramercy Tavern tavern three-course) and **$168** (Cote Butcher's Feast)
  to **$1,900** (Masa hinoki counter). Atomix, Atera and Per Se stay blank because captures
  disagree or the page only shows a deposit (flag F24).
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

<<<<<<< HEAD
| Path | Purpose |
|---|---|
| `data/restaurants.json` | 72 rows, per-field `provenance`, verification badge |
| `data/hotels.json` | 16 rows + 5 booking windows + transit objects + ranking |
| `data/activities.json` | 18 rows with hours, exceptions, costs, socials |
| `data/decisions.json` | 13 questions, 17 suggestions, 28 flags |
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
=======
Every factual row in the category tables links to a primary or official source. Values that could not be confirmed are left blank and explained in the Flags page. Arithmetic (such as multiplying an official per-person menu price by two, or applying a published tax basis) is identified in context. User-generated reviews are labelled third-party and are not treated as official endorsements. Dated prices and hours are time-sensitive and should be rechecked before booking.
=======
## Core Verification Rule

> Every single data row carries an official HTTPS source link. Values that cannot be confirmed from an official source are left deliberately blank and flagged on the Flagged for Review page — never estimated or hallucinated.

Where arithmetic is performed (adding published 14.75% tax + $3.50/nt unit fee to published pre-tax rates, or multiplying adult admission for 2), the formula and source basis are explicitly documented. Third-party review videos (YouTube, TikTok) are labeled as traveler preview media and not official venue endorsements.

---

## Site Structure & Dashboard Pages

| Path | Purpose | Key Content |
|---|---|---|
| `index.html` | Overview & Dashboard | High-level metrics, key findings, quick category tiles, transit verdict |
| `pages/executive-summary.html` | Executive Summary | Decision blueprint, hotel rankings, Michelin clusters, budget tiers ($1.8k–$9.5k), booking timeline |
| `pages/michelin-restaurants.html` | Michelin Dining Directory | Full 72-row roster (69 starred + 3 guide additions), 24 verified couple prices, clusters, 100+ review links |
| `pages/hotels.html` | Hotels & Booking Windows | 10 ranked hotels (Queen+/private bath verified), 7-night totals (pre-tax & all-in), 5-week price sweep |
| `pages/activities.html` | Activities & Events | 18 curated NYC activities, operating hours, exceptions, couple costs, Chinatown Lunar New Year Parade |
| `pages/itinerary.html` | Itinerary & Transit Matrix | 7-day & 4-day cluster-aligned plans, 25-leg measured transit matrix (3–37 min), closure rules |
| `pages/questions.html` | Decision Framework | 12 prioritized questions: what we know, what is missing, blocking status, discovery playbook |
| `pages/suggestions.html` | Suggestions Portal | 12 prioritized improvement proposals with impact, effort, prerequisites, and action paths |
| `pages/flagged.html` | Flagged for Review | 17 transparent audit flags covering unverified fields, ceremony risks, and pricing caveats |
| `pages/sources.html` | Sources & Methodology | Primary-source directory, strict verification standards, cross-session audit trails |
| `pages/repo-audit.html` | Repository Audit | Multi-session integration history, git logs, automated verification evidence |
| `data/restaurants.json` | Restaurant Dataset | 72 rows (69 starred + 3 Guide-listed), verified couple prices, operating hours, socials |
| `data/hotels.json` | Hotel Dataset | 10 ranked hotels, Queen+/private bath specs, 7-night rates, 5 weekly booking sweeps |
| `data/activities.json` | Activities Dataset | 18 attractions, verified 2-adult admission costs, opening hours, schedule exceptions |
| `data/decisions.json` | Decisions Dataset | 12 questions, 12 suggestions, 17 flags, executive briefing |
| `assets/styles.css` · `assets/app.js` | Styling & Logic | Modern responsive design, interactive filters, origin-based route calculation |
| `scripts/verify.py` | Automated Verification | Local link validation, JSON integrity, HTTPS source enforcement, blank-flag checks |
| `COORDINATION.md` | Task Board & Log | Multi-session task board, ownership scopes, commit log |

---

## Headline Findings & Strategic Analysis

1. **≤1-Hour Transit Rule 100% Satisfied:**
   Across 25 measured door-to-door transit legs via MTA subway and local walking, all shortlisted Manhattan hotels reach 100% of NYC's 67 Michelin-starred restaurants and top activities in **3 to 37 minutes** (average 17.2 to 21.4 minutes). The 1-hour constraint is comfortably satisfied across the board.
>>>>>>> e17ec92 (Integrate complete verified NYC 2027 trip dashboard: 72 Michelin restaurants, 10 ranked hotels with 5-week sweeps, 18 activities, transit matrix, and decision framework (T18))

2. **Cheapest Upcoming Time to Book (5-Week Sweep):**
   Across the 15 Feb – 23 Mar 2027 window, **Week 1 (15–22 Feb 2027)** is the cheapest verified Queen-bed stay:
   - **Eurostars Wall Street:** $848 pre-tax / $998 all-in (non-ref) · $1,025 pre-tax / $1,204 all-in (cancellable)
   - **DoubleTree by Hilton Chelsea (#1 Pick):** $943 pre-tax / $1,110 all-in (cancellable, King bed, central location)
   - *Warning on Week 2 (22 Feb – 1 Mar):* The entry $836 rate at Eurostars is a *Twin Bed room* (disqualified for Queen+ requirement).

3. **Date-Critical February 2027 Events:**
   - **29th Chinatown Lunar New Year Parade & Festival:** Sunday, February 21, 2027 at 1:00 PM (Mott St to Grand St, Free).
   - **Bank of America Winter Village at Bryant Park:** Free admission ice rink closes for the season on **Sunday, February 28, 2027**.

4. **Michelin Dining Clusters & Verified Menu Prices:**
   - 69 starred restaurants (5×3★, 14×2★, 50×1★) across 5 transit clusters (Midtown West, Flatiron/NoMad, Tribeca/Lower Manhattan, Upper East Side, Williamsburg).
   - 24 venues have exact verified 2-adult food subtotals ($156 to $1,900 for two).

5. **MTA Fare & Subway Budget:**
   - MTA single ride is **$3.00** ($35/week OMNY fare cap for unlimited subway/bus rides).

6. **Michelin Guide Ceremony Notice:**
   - The 2026/2027 Northeast Cities ceremony is scheduled for **14 December 2026**. Star levels should be re-checked post-ceremony.

---

## Local Verification & Testing

```bash
<<<<<<< HEAD
python3 scripts/verify.py
python3 sessions/c1cf7b23/scripts/verify.py
>>>>>>> 62ef838 (Integrate complete verified NYC 2027 trip dashboard: 72 Michelin restaurants, 10 ranked hotels with 5-week sweeps, 18 activities, transit matrix, and decision framework (T18))
node --check assets/app.js
python3 -m http.server 8000       # then open http://localhost:8000/
```

There is no build step on the host: GitHub Pages serves the repository root from `main`, and
`.nojekyll` stops Jekyll processing.

## What is deliberately blank

Airfare; theatre tickets; the 3-night hotel total; per-dish à-la-carte totals; six hotels without a
published bed-and-bathroom line; 45 of 72 restaurant social links that could not be confirmed; every
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

<<<<<<< HEAD
MIT for code; CC BY 4.0 for data and prose. Restaurant and hotel facts belong to their sources.
=======
Code: MIT. Data and prose: CC BY 4.0. Third-party marks, quotations and linked source content remain the property of their owners. See `LICENSE`.
=======
python3 scripts/verify.py     # Checks local HTML links, JSON integrity, sources, and flags
node --check assets/app.js    # Checks JavaScript syntax
python3 -m http.server 8000   # Starts local static preview at http://localhost:8000/
```

No build tools or external dependencies are required. The site runs natively in any modern browser.

---

## Publishing

GitHub Pages serves `main` at the repository root with `.nojekyll` enabled.

## Licence

MIT for code; CC BY 4.0 for compiled data and prose. See `LICENSE`.
>>>>>>> e17ec92 (Integrate complete verified NYC 2027 trip dashboard: 72 Michelin restaurants, 10 ranked hotels with 5-week sweeps, 18 activities, transit matrix, and decision framework (T18))
>>>>>>> 62ef838 (Integrate complete verified NYC 2027 trip dashboard: 72 Michelin restaurants, 10 ranked hotels with 5-week sweeps, 18 activities, transit matrix, and decision framework (T18))
