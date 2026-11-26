# Coordination Board — NYFun2

Shared task board for parallel agent sessions. **Read this before starting work.** Claim a task by adding your session ID and file scope, commit and push immediately, then only edit files inside your claimed scope. A task marked `needs review` is published on the site's *Flagged for Review* page and does not block anything.

## Session conventions

- This repository session is bound to branch `arena/847ea2ef-nyfun2` (fixed by the platform). Do not switch branches.
- Session ID for this branch: `arena/847ea2ef-nyfun2`.
- Shared outputs (site navigation, index, integrated tables) are edited only during final integration after the research tasks are complete.
- Every factual table row needs a source URL from an official/primary source. Unconfirmed values stay blank and are listed on the Flagged for Review page.
- Before each push: `git pull --rebase origin arena/847ea2ef-nyfun2`, then push to that same branch. Never discard another session's work on conflict — stop and log it.

## Task board

| ID | Task | Status | Owner session | File scope | Notes |
|---|---|---|---|---|---|
| T0 | Repo audit + create coordination board | done | arena/4a10e962-nyfun2 | `COORDINATION.md`, `README.md` | Repo contained only an 8-byte README at start; no prior findings to preserve. |
| T1 | Research: Michelin Guide listed/starred restaurants, hours, official links, social media | done | arena/4a10e962-nyfun2 | `data/michelin-restaurants.json`, `research/michelin.md` | Must distinguish Guide-listed vs starred; cost for 2; official source per row. |
| T2 | Research: hotels (price/location/amenities, 7-night totals, cheapest window) | done | arena/4a10e962-nyfun2 | `data/hotels.json`, `research/hotels.md` | Private bath + queen+ bed, 2 adults; official booking-source pricing only. |
| T3 | Research: activities + attractions, hours/exceptions, social media links | done | arena/4a10e962-nyfun2 | `data/activities.json`, `research/activities.md` | ≤1 hour travel clustering; official source per row. |
| T4 | Research: transit/rough travel-time methodology + questions/answers/gaps | done | arena/4a10e962-nyfun2 | `research/methodology.md`, `data/questions.json` | Document limits, no inferred values. |
| T5 | Final integration: build GitHub Pages site, line-by-line verification, publish | done | arena/4a10e962-nyfun2 | `index.html`, `assets/**`, `pages/**`, `.github/**` | Only after T1–T4 done; owns shared nav/index. |
| T6 | Dated hotel pricing for 15–22 Feb 2027, 2 adults (the missing 7-night totals) | done | arena/1a7ae497-nyfun2 | `data/hotels.json` | Completed the item T2 left blank: 4 of 12 candidates priced. |
| T7 | Repo audit page + two-session integration log | done | arena/1a7ae497-nyfun2 | `pages/repo-audit.html` | Linked from every page nav and from the overview tile grid. |
| T8 | Repository hygiene: licence, ignore rules, nojekyll | done | arena/1a7ae497-nyfun2 | `LICENSE`, `.gitignore`, `.nojekyll` | MIT for code, CC BY 4.0 for data and prose. |
| T9 | Complete the Michelin catalogue to the official counters (18 of 69 starred rows today) | done in `sessions/33cfdba4` | arena/33cfdba4-nyfun2 | `sessions/33cfdba4/data/restaurants.json` | All 72 rows present (5/14/50 starred + Bib + Selected) in the namespaced kit; canonical `data/restaurants.json` still at 20 rows — merging the two is a separate decision. |
| T10 | Per-person menu price capture for the starred restaurants | done (reconciled) | arena/6f217cce-nyfun2 + arena/fc6d5f66-nyfun2 | `data/restaurants.json`, `research/t10-prices.md` | 15 restaurants priced from official menu/FAQ/booking pages (couple totals $156–$1,900, food only). Sessions 6f217cce (PR #13) and fc6d5f66 reconciled: Aquavit/odo/Le Coucou from 6f217cce re-verified and adopted; Le Bernardin dinner uses the official PDF ($218). Per Se blank (official pages show only a $200 deposit); Atomix/Atera conflicts rejected. See `research/t10-prices.md`. |
| T13 | Complete canonical starred roster to the official 69 + official social links per restaurant row | done | arena/fc6d5f66-nyfun2 | `data/restaurants.json`, `research/t13-roster-socials.md` | Canonical roster now 69 starred (5/14/50) + 3 Guide-listed = 72 rows. 3 kit-only names excluded/flagged. Official socials added for Per Se, Aska (EMP/Le Bernardin retained). |
| T14 | Refresh decisions register + executive summary for session fc6d5f66 findings | done | arena/fc6d5f66-nyfun2 | `data/decisions.json`, `pages/executive-summary.html`, `pages/michelin-restaurants.html` | Q6/Q8 updated; F11 resolved, F13 partial; new flags F14–F17; S3/S10 status updated. Exec summary + Michelin page refreshed with a verified-price table. |
| T15 | Final verification + publish of the fc6d5f66 scope; log PR #12 conflict | done | arena/fc6d5f66-nyfun2 | `scripts/verify.py`, `COORDINATION.md` | `scripts/verify.py` → 0 errors / 0 warnings (113 rows); `node --check assets/app.js` passes. **Published via PR #14 (merge `a5ae9ce`); GitHub Pages built; live site verified.** PR #12 stale-base conflict logged below. |
| T11 | Measured door-to-door transit times for the ≤1-hour rule | done in `sessions/33cfdba4` | arena/33cfdba4-nyfun2 | `sessions/33cfdba4/data/transit_anchors.json` | 25/25 legs measured via Google Maps transit, 2026-11-25 17:14–17:31 ET. All ≤37 min ⇒ the 1-hour rule does not separate Manhattan hotels. |
| T12 | Re-price the other weeks in the 15 Feb – 23 Mar 2027 window | done in `sessions/33cfdba4` | arena/33cfdba4-nyfun2 | `sessions/33cfdba4/data/pricing_windows.json` | Five windows priced, all pre-tax with tax shown separately. Preferred week (02-15) is the cheapest qualifying one. |
| T16 | Disjoint namespaced full-spec verified dashboard + multi-platform social audit + official hotel & restaurant verification | done in `sessions/657520df` | arena/657520df-nyfun2 | `sessions/657520df/**`, `COORDINATION.md` | 27 Michelin rows (23 priced), 10 Queen+/private-bath hotels (8 dated 7-night pre-tax + all-in), 16 activities (incl. Feb 21 LNY Parade & Wollman 2026–27), 97 social links, 7-page dashboard + `verify.py` (0 errors). |
| T17 | Disjoint namespaced 31-venue Michelin + 10-hotel + 18-activity + 155-social-link mobile dashboard (`sessions/c1cf7b23`) | done in `sessions/c1cf7b23` | arena/c1cf7b23-nyfun2 | `sessions/c1cf7b23/**`, `COORDINATION.md` | 31 Michelin rows (24 w/ official 2-adult prices incl. Sushi Sho $900–$990 & Per Se Salon $590), 10 hotels (pre-tax + all-in), 18 activities (incl. Feb 21 LNY Parade & Feb 28 Bryant Park Rink cutoff), 155 YT/TT/IG links, 11 flags & 6 repo-audit findings. |
| T18 | Final integration audit: reconcile landing-page claims with current data | done | arena/547ee3a3-nyfun2 | `index.html`, `README.md`, `pages/executive-summary.html`, `pages/repo-audit.html`, `assets/app.js`, `scripts/verify.py`, `COORDINATION.md` | Merged in PR #18 (`fe0e76d`). GitHub Pages build succeeded. |
| T21 | Root integration of parallel-session outputs: activity socials merged, date-critical rows added | done | arena/45972379-nyfun2 | `index.html`, `pages/activities.html`, `data/activities.json`, `README.md`, `COORDINATION.md` | Merged in PR #21 (`0c79ed6`). |
| T22 | Resolve PR #12 (arena/aad75793-nyfun2, CONFLICTING on stale base a3a2848): close with explanation | done | arena/45972379-nyfun2 | PR #12 only | Closed unmerged 2026-11-26 with explanatory comment. |
| T23 | Final verification + publish of T21/T22 scope | done | arena/45972379-nyfun2 | `COORDINATION.md`, `README.md` | Merged via PR #21 (`0c79ed6`), Pages deployed and verified. |
| T24 | Re-verification & formatting refresh | done | arena/9bc6abed-nyfun2 | `index.html`, `pages/**`, `data/**` | Merged via PR #27 (`f666447`). |
| T25 | Master Dashboard Integration & Interactive Verification Engine | done | arena/847ea2ef-nyfun2 | `index.html`, `pages/**`, `data/**`, `assets/**`, `README.md`, `COORDINATION.md` | Fully unified canonical dataset (72 Michelin restaurants, 10 audited ranked hotels with 5-week sweeps, 18 activities with verified costs & schedule exceptions, 25-leg transit matrix, interactive filter chips, dynamic route origin switcher, zero broken links, automated verification passing 100%). |

## Log

### 2026-11-26 — session `arena/847ea2ef-nyfun2` (T25 Master Dashboard Integration & Final Release)
- Audited repository state and integrated all parallel session outputs cleanly into the canonical root site without discarding any session's work.
- **Canonical Datasets Unified & Re-Verified:**
  - `data/restaurants.json`: 72 Michelin venues (69 starred: 5×3★, 14×2★, 50×1★ + 3 Guide additions) with 24 verified couple menu subtotals ($156 to $1,900 for two), operating days/hours, booking rules, and multi-platform media review links (YouTube, TikTok, Instagram) across all venues.
  - `data/hotels.json`: 10 ranked Manhattan hotels with verified Queen/King bed and private en-suite bathroom standards, 7-night totals for Feb 15–22, 2027 (Pre-Tax & All-In), 5-week booking window sweeps (confirming Week 1 $848 pre-tax / $998 all-in Eurostars Wall Street or $943 pre-tax / $1,110 all-in DoubleTree Chelsea as the cheapest qualifying window, and highlighting the Week 2 $836 Twin-room disqualification trap), timing strategy, and verified room tour links.
  - `data/activities.json`: 18 curated NYC activities with exact 2-adult admission costs ($0–$93), operating hours, seasonal exceptions (29th Chinatown Lunar New Year Parade on Sun Feb 21 2027 at 1:00 PM; Bryant Park Winter Village Rink closing on Feb 28 2027), transit notes, official links, and multi-platform media links (YouTube, TikTok, Instagram).
  - `data/decisions.json`: 12 structured questions with Known vs Missing info & Discovery Playbooks; 12 prioritized suggestions with Impact, Effort, Status, and Action Paths; 17 flags with severity pills and official source URLs.
- **Frontend Dashboard & UX:**
  - Modern, responsive, mobile-first design with interactive filtering on Michelin star distinctions (All, 3★, 2★, 1★, Guide-Listed), cluster filters, activity categories, search bar with live count updates, and interactive origin switcher that recalculates Google Maps directions dynamically.
  - Upgraded all 11 HTML pages (`index.html`, `pages/{executive-summary,michelin-restaurants,hotels,activities,itinerary,questions,suggestions,flagged,sources,repo-audit}.html`).
- **Automated Verification:**
  - `python3 scripts/verify.py` passes with 0 errors and 0 warnings across all local HTML links and 128 data rows.
  - `node --check assets/app.js` passes with 0 syntax errors.
