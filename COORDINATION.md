# Coordination Board — NYFun2

Shared task board for parallel agent sessions. **Read this before starting work.** Claim a task by
adding your session ID and file scope, commit, and push immediately — then only edit files inside your
claimed scope. A task marked `needs review` is published on the site's *Flagged for Review* page and
does not block anything.

---

## ⚠️ Read this first: this repository has already had a parallel-session collision

Two sessions worked the repository on **2026-11-25** from the same empty commit (`a3a2848`) without
seeing each other's claim, because the board did not exist when they started:

| Session | Branch | Produced | Merged as |
|---|---|---|---|
| `arena/4a10e962-nyfun2` | `arena/4a10e962-nyfun2` | Site shell (`index.html`, `pages/**`, `assets/**`), `data/restaurants.json` (20 rows), `data/activities.json` (12), `data/hotels.json` (10, no dated rates), `data/decisions.json` (8/8/9), `scripts/verify.py` | PR #1 |
| `arena/1a7ae497-nyfun2` | `arena/1a7ae497-nyfun2` | Parallel site shell, plus **four dated 7-night hotel totals for 15–22 Feb 2027**, Atera ★★ record, official Instagram/Facebook for two restaurants, MTA fare correction, repo audit | PR #2 |

**Resolution (PR #2, second session acting as integration session):** the merged product keeps
Session A's site shell, navigation and design system — it was already published and indexed — and
folds Session B's unique verified data into it. Nothing from either session was discarded silently.
The full reconciliation is on `pages/repo-audit.html`.

**Known structural gap:** the platform fixes each session to one branch, so the `session-<id>/<task>`
branching convention in the standing instructions cannot be honoured. Ownership therefore relies on
this board and on merge discipline. Protect `main` before the next parallel run.

---

## Session conventions

- A session is bound to the branch named in its task context. Do not switch branches.
- Shared outputs (navigation, `index.html`, integrated data files) are edited only during final
  integration, once research tasks are complete.
- Every factual table row needs a source URL from an official/primary source. Unconfirmed values stay
  blank and are listed on the Flagged page.
- Before each push: `git pull --rebase origin <your-branch>`. On conflict, **stop**, resolve without
  discarding the other session's work, and log it here.
- Run `python3 scripts/verify.py` and `node --check assets/app.js` before pushing.

## Task board

| ID | Task | Status | Owner session | File scope |
|---|---|---|---|---|
| T0 | Repo audit + coordination board | done | `4a10e962` | `COORDINATION.md`, `README.md` |
| T1 | MICHELIN restaurants: stars vs guide-listed, hours, links, social | done | `4a10e962` | `data/restaurants.json` |
| T2 | Hotels: price / location / amenities, 7-night totals | **done (completed by second session)** | `4a10e962` + `1a7ae497` | `data/hotels.json` |
| T3 | Activities + attractions: hours, exceptions, social | done | `4a10e962` | `data/activities.json` |
| T4 | Transit methodology + questions/suggestions/flags | done | `4a10e962` | `data/decisions.json` |
| T5 | Site build + publish | done | `4a10e962` | `index.html`, `assets/**`, `pages/**` |
| T6 | Dated hotel pricing for the exact travel window | done | `1a7ae497` | `data/hotels.json` |
| T7 | Repo audit page + integration log | done | `1a7ae497` | `pages/repo-audit.html` |
| T8 | Hygiene: licence, ignore rules, nojekyll | done | `1a7ae497` | `LICENSE`, `.gitignore`, `.nojekyll` |
| T9 | Complete MICHELIN index to official counters (18 of 69 starred today) | unclaimed | — | `data/restaurants.json` |
| T10 | Per-person menu price capture | unclaimed | — | `data/restaurants.json` |
| T11 | Measured door-to-door transit times (the ≤1-hour rule) | unclaimed | — | `data/hotels.json` |
| T12 | Re-price the other weeks in the 15 Feb – 23 Mar 2027 window | unclaimed | — | `data/hotels.json` |

Status values: `unclaimed` · `in progress` · `needs review` · `done`.

---

## Log

### 2026-11-25 — session `arena/4a10e962-nyfun2`

- T0 done. Repo audited: single commit `a3a2848`, 8-byte README only, no site/CI/data. No prior work
  existed to overwrite.
- T1 done — `data/restaurants.json`. Verified against 19 official MICHELIN pages/articles. Irregularities
  logged: the 14 Dec 2026 ceremony falls between research and travel; Sushi Sho search results referred
  to a different city; The Modern and Semma hours unconfirmed in the checked section; couple prices
  unavailable from official pages.
- T2 done — `data/hotels.json`. Michelin's booking widget enforces a 31-day advance limit and no hotel's
  own engine published February 2027 rates, so 7-night totals and the cheapest window were left blank.
- T3 done — `data/activities.json`. Hours transcribed from NPS, NYC Parks, The Met, MoMA, AMNH, the
  9/11 Memorial & Museum, the High Line, the Whitney, the Guggenheim, ESB, the Staten Island Ferry and
  NYPL. Irregularities: conflicting Met hours across official snippets; NYPL page-version differences;
  ESB date-specific February hours unavailable.
- T4 done — `data/decisions.json` (8 questions / 8 suggestions / 9 flags).
- T5 done — site built; `scripts/verify.py` reported 0 errors over 51 rows; `node --check` passed.

### 2026-11-25 — session `arena/1a7ae497-nyfun2`

- Board created independently (the first session's board was not visible from this branch).
- Research performed: MICHELIN counts + records, Resy venue pages for social handles and policies,
  Booking.com dated rates for 15–22 Feb 2027, MTA fares, The Met, 9/11 Memorial & Museum, Top of the Rock.
- T6 done — **four dated 7-night totals now exist**, with tax arithmetic and capture dates per row:
  $1,305 / $1,428 / $1,774 / $5,220 all-in. This directly contradicted the first session's conclusion
  that dated rates were unobtainable; the cause was found (Michelin's widget enforces 31 days; a
  third-party engine does not).
- Corrections made during verification: **MTA fare is $3, not $2.90** (F12); two activity street
  addresses were removed because neither official page printed one; the Le Coucou ↔ 11 Howard phrasing
  was narrowed to what MICHELIN actually shows (a cross-link between records).
- T7, T8 done — repo audit page, licence, ignore rules, `.nojekyll`.
- **Integration:** merged `origin/main` into this branch, kept the first session's site shell intact,
  and folded this session's data into it. Duplicate parallel pages from this session were removed
  (its own work only — nothing belonging to the other session).
- Registers after merge: **12 questions, 12 suggestions, 13 flags**. Flag F2 was re-graded from High to
  Low and rewritten rather than deleted, because the new data partially resolved it.

### Verification evidence (current head)

```
python3 scripts/verify.py   -> 0 errors, 0 warnings over 58 data rows
node --check assets/app.js  -> passes
static serve                -> all pages and assets return 200
calendar                    -> 15 Feb 2027 = Monday, 22 Feb 2027 = Monday, 7 nights
hotel arithmetic            -> 1113->1305 · 1213.96->1428 · 1522->1774 · 4488->5220
```

---

## Change requests (cross-scope)

| Request | Files needed | Status |
|---|---|---|
| Complete the MICHELIN index to the official counters | `data/restaurants.json` | open — suggestion S10 |
| Capture per-person menu prices | `data/restaurants.json` | open — suggestion S3 |
| Integrate a routing source for the ≤1-hour rule | `data/hotels.json` | open — suggestion S2 |
| Price the other weeks in the travel window | `data/hotels.json` | open — flag F2 remainder |
| Protect `main`; add CI running `scripts/verify.py` | repo settings, `.github/workflows` | open — repo audit R4/R6 |

## Handoff log

| When | Task | From → To | Reason |
|---|---|---|---|
| 2026-11-25 | board created twice | `4a10e962` ∥ `1a7ae497` | Both sessions started from the same empty commit; neither could see the other's claim. |
| 2026-11-25 | T2 (dated hotel totals) | `4a10e962` → `1a7ae497` | First session recorded it as blocked; second session completed it. |
| 2026-11-25 | T9–T12 | — → unclaimed | Released for the next session. |

## Notes for the next session

- Never write a value into `data/*.json` that you did not read from the source cited in that row. If you
  cannot read it, leave the field empty and add a flag explaining why.
- The rendering layer is `assets/app.js`, driven by the column lists inside it. Adding a JSON field is
  invisible until the corresponding column is added there.
- `data/hotels.json` keeps two different price concepts apart on purpose: `publishedRate` is an undated
  "from" figure on an official page; `sevenNightTotal` is a dated engine quote. Never mix the columns.
- Pages serves `main` at the repository root; a merge to `main` is the deploy.
