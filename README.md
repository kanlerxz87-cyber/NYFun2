# NYFun2 — New York City trip plan, February 2027

A static, source-audited planning dashboard for two adults in New York City, built around
MICHELIN-starred dining and hotels that meet a private-bathroom / queen-or-larger-bed requirement.

**Live site:** https://kanlerxz87-cyber.github.io/NYFun2/

**Travel window:** preferred 15–18 Feb 2027; priced case 15–22 Feb 2027 (Monday → Monday, 7 nights).

---

## The rule this project runs on

> Every table row carries an official source. Values that cannot be confirmed are left blank and
> flagged — never estimated.

Where the site performs arithmetic itself (adding a published tax rate to a published pre-tax total),
the formula is printed next to the result. A review video is labelled third-party; it is never presented
as an official endorsement.

## What is here

| Path | Purpose |
|---|---|
| `index.html` | Dashboard / overview |
| `pages/executive-summary.html` | Decision-ready summary |
| `pages/michelin-restaurants.html` | 21 restaurant rows — star level, hours, guide band, review links, source |
| `pages/hotels.html` | 12 hotel candidates, 4 with dated 7-night totals |
| `pages/activities.html` | 12 activities with official hours, exceptions and couple costs |
| `pages/itinerary.html` | Day plan and how the ≤1-hour travel goal is handled |
| `pages/questions.html` | 12 open questions: known / missing / how to discover |
| `pages/suggestions.html` | 12 improvement options, none implemented |
| `pages/flagged.html` | 13 flags: every unverified value and irregularity |
| `pages/sources.html` | Primary-source register and verification rules |
| `pages/repo-audit.html` | Repository audit and the two-session integration log |
| `data/restaurants.json` | Restaurant dataset |
| `data/hotels.json` | Hotel dataset |
| `data/activities.json` | Activities dataset |
| `data/decisions.json` | Questions, suggestions and flags |
| `assets/styles.css` · `assets/app.js` | Styling and table rendering (no dependencies) |
| `scripts/verify.py` | Pre-push verification |
| `COORDINATION.md` | Shared task board and session log |

## Headline findings

- **MICHELIN counts (official filter panel, 25 Nov 2026):** 5 three-star, 14 two-star, 50 one-star,
  76 Bib Gourmand, 224 guide-listed with no star.
- **Dated hotel totals now exist** for 15–22 Feb 2027, all-in for two adults:
  **Hyatt Place NY/Chelsea $1,305** · Arlo NoMad $1,428 · 11 Howard $1,774 · The Beekman $5,220.
  A 4× spread for identical dates. They are dated aggregator snapshots, not hotel quotes (flag F10).
- **11 Howard** is the only shortlisted hotel sharing a ZIP code (10013) with a verified starred
  restaurant — Atera ★★, 77 Worth St.
- **MTA fare is $3** per subway / local-bus ride ($7.25 express), not the $2.90 still quoted in older guides.
- **Michelin's 2026 Northeast Cities ceremony is scheduled for 14 Dec 2026** — after this research,
  before the trip. Star levels may change (flag F1).

## Deliberately blank

No measured transit times (no routing source was reachable, so only same-ZIP proximity is claimed and
each pair links a live directions query), no per-person restaurant prices (client-rendered menu pages),
no airfare, no theatre tickets. Every gap is on `pages/flagged.html` with its cause and its remedy.

## Verify locally

```bash
python3 scripts/verify.py     # local links, JSON validity, source-per-row, blank-implies-flag
node --check assets/app.js    # JS syntax
python3 -m http.server 8000   # then open http://localhost:8000/
```

No build step and no third-party dependencies: the site is HTML, one stylesheet, one script and JSON.

## Publishing

GitHub Pages is configured to serve `main` at the repository root, so a merge to `main` deploys.
`.nojekyll` is present so Jekyll does not process the folder.

## Sessions and coordination

Two agent sessions worked this repository on 2026-11-25 on separate branches and were merged rather
than overwritten. See `COORDINATION.md` for the task board and `pages/repo-audit.html` for the
integration log: what each session contributed, which flag was resolved (F2), and which new risk the
merged data introduced (F10).

## Licence

Code: MIT. Data and prose: CC BY 4.0. Third-party marks, quotations and source pages remain the
property of their owners. See `LICENSE`.
