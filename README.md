# NYFun2 — New York trip planning kit (15–22 February 2027)

A static, dependency-free research site for a couple's one-to-four-week New York trip, built around
MICHELIN-starred dining and hotels with a private bathroom and a queen-or-larger bed.

**Live site:** https://kanlerxz87-cyber.github.io/NYFun2/

---

## What this repository contains

| Path | Purpose |
|---|---|
| `index.html` | Dashboard / landing page |
| `executive-summary.html` | Decision-ready one-pager |
| `hotels.html` | Four hotels priced for the exact dates, plus MICHELIN proximity |
| `michelin.html` | Official distinction counts and every restaurant catalogued so far |
| `activities.html` | Verified activities plus a clearly-labelled candidate backlog |
| `itinerary.html` | Seven-night schedule and the budget model |
| `suggestions.html` | Ten reviewed suggestions with impact/effort and three ready paths |
| `questions.html` | Twelve open questions: known, missing, how to resolve |
| `flagged.html` | Fifteen unverified items and irregularities with remedies |
| `sources.html` | Source register — 22 sources, what each verified, when it was read |
| `repo-audit.html` | Audit of this repository as found |
| `assets/site.css` | Single stylesheet, mobile-first |
| `assets/data.js` | **The dataset.** Every value with its provenance or its flag id |
| `assets/tables.js` | Column definitions for each table |
| `assets/app.js` | Navigation, table rendering, helpers |
| `tools/check_site.py` | Link check + JS/HTML sanity check (run it before pushing) |
| `COORDINATION.md` | Shared task board for parallel agent sessions |

## The rule this project runs on

> Every value is either **linked to the official source that states it**, or **left blank and flagged**.

There are no estimates pretending to be facts. Where the site performs arithmetic itself — for example
adding a published tax rate to a published pre-tax hotel total — the formula is printed next to the result
and the cell is labelled as an estimate.

## Method

1. **Distinctions and counts** come from the MICHELIN Guide's own filtered list pages
   (3-star / 2-star / 1-star / Bib Gourmand / Selected). The filter counters are treated as authoritative.
2. **Restaurant hours, addresses, price bands** are copied from each restaurant's MICHELIN record.
   Social handles are recorded only where an official page — or the booking partner the guide links to —
   prints them.
3. **Hotel prices** are live Booking.com rate pages for `checkin=2027-02-15&checkout=2027-02-22`, read on
   2026-11-25, with the exact URL published per row. They are dated snapshots, not quotes.
4. **Activities** are included only when the venue's own page was read in-session.
5. **Travel times are not asserted.** No transit-routing source was reachable, so proximity claims are
   limited to matching postal codes, and Google Maps transit links are provided for manual verification.

## Run locally

No build step, no dependencies. Any static server works:

```bash
python3 -m http.server 8000
# then open http://localhost:8000/
```

## Validate before pushing

```bash
python3 tools/check_site.py
```

Checks: every internal `href`/`src` resolves to a real file, every page references the shared assets,
`node --check` parses each JS file if node is available, and every HTML file has a matching nav entry.

## Publishing

GitHub Pages is configured to serve `main` at the repository root, so a merge to `main` is the deploy.
`.nojekyll` is present so no Jekyll processing interferes.

## Licence

Code: MIT. Data and prose: CC BY 4.0. See `LICENSE`.

## Known gaps

See `flagged.html` — 15 items, 5 of them High severity. The largest three are: measured transit times,
per-person restaurant prices, and the incomplete MICHELIN index (11 of 69 starred restaurants named).
