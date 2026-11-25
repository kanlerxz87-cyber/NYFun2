# COORDINATION — Shared Task Board

> Shared board for all agent sessions working on this repo. Read this first.
> **Rules:** claim a task by writing your session ID + file scope here, commit & push immediately.
> Never start a task another session has claimed. Keep scopes non-overlapping.
> Log cross-scope change requests here instead of editing another session's files.

**Last updated:** 2026-11-25 (session `arena-1a7ae497`)

---

## Session registry

| Session ID | Branch | Status | Notes |
|---|---|---|---|
| `arena-1a7ae497` | `arena/1a7ae497-nyfun2` | active | Sole session on 2026-11-25. Owns and completed T1–T12. |

---

## Task board

| # | Task | Status | Owner | File scope |
|---|---|---|---|---|
| T1 | Repo audit + audit log | done | `arena-1a7ae497` | `repo-audit.html`, `assets/data.js` (`REPO_FINDINGS`) |
| T2 | Michelin restaurant dataset (distinction, price, hours, links, social) | needs review | `arena-1a7ae497` | `michelin.html`, `assets/data.js` (`RESTAURANTS`, `MICHELIN_COVERAGE`) |
| T3 | Hotel dataset (price/7nt, amenities, location) + Michelin-cluster analysis | needs review | `arena-1a7ae497` | `hotels.html`, `assets/data.js` (`HOTELS`, `HOTEL_CLUSTERS`) |
| T4 | Activities dataset (hours, exceptions, links, social) | needs review | `arena-1a7ae497` | `activities.html`, `assets/data.js` (`ACTIVITIES`, `ACTIVITY_BACKLOG`) |
| T5 | Itinerary + budget model (Feb 2027 dates) | done | `arena-1a7ae497` | `itinerary.html`, `assets/data.js` (`ITINERARY`, `BUDGET`, `PRICE_WINDOWS`) |
| T6 | Executive summary | done | `arena-1a7ae497` | `executive-summary.html` |
| T7 | Suggestions register | done | `arena-1a7ae497` | `suggestions.html`, `assets/data.js` (`SUGGESTIONS`) |
| T8 | Open questions register | done | `arena-1a7ae497` | `questions.html`, `assets/data.js` (`QUESTIONS`) |
| T9 | Flagged for review register | done | `arena-1a7ae497` | `flagged.html`, `assets/data.js` (`FLAGGED`) |
| T10 | Site shell: landing dashboard, nav, CSS, mobile layout | done | `arena-1a7ae497` | `index.html`, `assets/site.css`, `assets/app.js`, `assets/tables.js` |
| T11 | Source register | done | `arena-1a7ae497` | `sources.html`, `assets/data.js` (`SOURCES`) |
| T12 | Verification pass (line-by-line, link check) + Pages publish | done | `arena-1a7ae497` | `tools/check_site.py`, `tools/check_render.js`, all pages |

Status values: `unclaimed` · `in progress` · `needs review` · `done`.
`needs review` = published, with gaps documented on Flagged for Review; does not block anything.

---

## Verification performed (session `arena-1a7ae497`)

**Automated, run before every push:**

```bash
python3 tools/check_site.py     # 0 errors, 0 warnings
node tools/check_render.js      # all 14 tables render cleanly
```

`check_site.py` asserts: every local href/src resolves; every page loads the shared CSS + 3 JS files
and the header/footer mounts; every page in the `PAGES` nav exists and no page is orphaned; JS parses via
`node --check`; every `page.html#anchor` cross-link resolves to a real id, including ids rendered from data;
every referenced flag id exists in the dataset.

`check_render.js` asserts: each table produces balanced `<tr>`/`<td>`; no `undefined`/`NaN`/`[object Object]`
leaks into a cell; the expected figures ($1,305 hotel total, Le Bernardin Instagram, F-06 badge) survive
rendering; anchors F-01…F-15 and Q-05 exist as row ids.

### Sources (all read 2026-11-25 — full list on `sources.html`)

| What | Source |
|---|---|
| MICHELIN distinction counts 5 / 14 / 50 / 76 / 224 | guide.michelin.com NYC filtered list pages |
| 3-star names, cuisine, price band | guide.michelin.com 3-star list |
| Le Bernardin / EMP / Per Se / Atera records (address, hours, phone) | guide.michelin.com restaurant records |
| Le Bernardin + EMP Instagram/Facebook handles, cancellation policy | resy.com venue pages (MICHELIN's booking partner) |
| Hotel rates for 15–22 Feb 2027, bed type, bathroom, taxes | booking.com rate pages, exact URLs published per row |
| Arlo NoMad room types | arlohotels.com/nomad/rooms |
| Hyatt Place NY/Chelsea address | hyatt.com hotel-info |
| Subway/local bus fare $3, express $7.25 | mta.info/fares-tolls |
| The Met address, adult $30, pay-what-you-wish rules | metmuseum.org/plan-your-visit |
| 9/11 Memorial + Museum hours and rules | 911memorial.org/visit |
| Top of the Rock 8 AM–12 AM, from $42 | rockefellercenter.com ticket page |

### Irregularities recorded

15 items on `flagged.html`. The five High-severity ones are missing-by-construction, not errors:

1. **F-01** — no transit-routing source was reachable, so the “within 1 hour” rule is never asserted;
   only same-ZIP proximity is claimed, with per-pair Google Maps transit links supplied.
2. **F-02** — the MICHELIN index is incomplete (11 of 69 starred named) because the list pages serve
   48 rows at a time.
3. **F-05** — social handles exist only where an official/booking-partner page printed them.
4. **F-06** — no per-person restaurant prices; MICHELIN publishes only a `$$$$` band and the
   restaurants’ menu pages are client-rendered.
5. **F-12** — airfare not researched.

Notable corrections made during verification:

- **MTA fare is $3, not $2.90.** Cached guides still quote $2.90; the official fares page says $3.
- **Two activity addresses were removed** (9/11 Memorial, Top of the Rock) after review: neither official
  page printed a street address in the captured text, so asserting one would have been recall, not
  verification. Logged as F-15.
- **The Le Coucou ↔ 11 Howard relationship was reworded** to describe what MICHELIN actually shows
  (a cross-link between the two records), not an inference about the physical room layout.

---

## Change requests (cross-scope)

| Request | Files needed | Owner of those files | Status |
|---|---|---|---|
| Complete the MICHELIN index to all 69 starred + 76 Bib Gourmand | `assets/data.js` (`RESTAURANTS`) | `arena-1a7ae497` | open — tracked as suggestion S3 |
| Wire a transit-routing source for the 1-hour rule | `assets/data.js` (`HOTEL_CLUSTERS`) | `arena-1a7ae497` | open — tracked as suggestion S1 |
| Capture per-person menu prices | `assets/data.js` (`RESTAURANTS.cost2`) | `arena-1a7ae497` | open — tracked as suggestion S2 |

## Handoff log

| When | Task | From → To | Reason |
|---|---|---|---|
| 2026-11-25 | board created | — | Repo arrived with a single 8-byte README; no board existed. |
| 2026-11-25 | T1–T12 | `arena-1a7ae497` → unclaimed | Session ended; all scopes released back to the board. |

## Notes for the next session

- Never write a value into `assets/data.js` that you did not read from the cited page. If you cannot read
  it, leave the field as `{ v: '', flag: 'F-xx' }` and add the flag.
- Data files are the single source of truth; pages contain prose only. Table columns live in
  `assets/tables.js`, rendering in `assets/app.js`.
- Run both checkers before pushing. A JS error in `data.js` blanks every table on every page at once.
- GitHub Pages serves `main` at the repository root; a merge to `main` is the deploy.
