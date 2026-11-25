# NYFun2 — New York trip planning dashboard

A source-checked, mobile-friendly GitHub Pages dashboard for a two-adult New York City trip in February 2027. It collects Michelin distinctions, restaurants, activities, hotel candidates, social-review links, opening hours, open decisions and review flags.

**Live site:** https://kanlerxz87-cyber.github.io/NYFun2/

## What is in here

- `index.html` — landing page / overview.
- `pages/` — subpages by category: executive summary, Michelin restaurants, hotels, activities, itinerary logic, questions, suggestions, flagged items, sources.
- `data/` — source-linked JSON used by the tables.
- `assets/styles.css`, `assets/app.js` — mobile-first layout and table rendering (search, route origin selection).
- `scripts/verify.py` — offline link/row verification.
- `COORDINATION.md` — shared task board for parallel sessions.

## Verification policy

Every table row carries a link to an official/primary source: Michelin Guide, a government site (NPS, NYC DOT, NYC Parks), or the venue's own site. If an official source did not state a value, the cell is blank and an explanation appears on the *Flagged for review* page. Third-party YouTube links are explicitly labelled and are never used as evidence for hours, prices or account ownership.

Research was checked on **25 November 2026**. Two material limits are recorded prominently on the site:

1. Michelin's 2026 Northeast Cities ceremony is scheduled for 14 December 2026, after the research date; star levels may change before travel.
2. No official booking source published dated February 2027 hotel rates, so seven-night totals and a cheapest booking window are blank rather than estimated.

## Run locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Verify

```bash
python3 scripts/verify.py
node --check assets/app.js
```

## Coordination

See `COORDINATION.md` for task claims, file scopes, source records and irregularities. Work on this repository's active session branch only.
