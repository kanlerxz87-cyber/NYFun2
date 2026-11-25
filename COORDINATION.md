# COORDINATION.md — Shared Task Board

Repo: `kanlerxz87-cyber/NYFun2` · Live site: https://kanlerxz87-cyber.github.io/NYFun2/
Board protocol: claim = write session ID + file scope here, commit & push immediately. Never edit files outside your scope.
Statuses: `unclaimed` · `in progress` · `needs review` (published on Flagged for Review page; does not block) · `done`.

## Sessions

| Session ID | Branch | Started (UTC) | Notes |
|---|---|---|---|
| `arena-33cfdba4` | `arena/33cfdba4-nyfun2` | 2026-11-25 | Sole active session at time of writing. All tasks below are owned by this session unless a later session re-claims a stale task. |

## Task board

| ID | Task | Status | Owner | File scope | Sources / verification | Notes |
|---|---|---|---|---|---|---|
| CORE-00 | Create coordination board + project skeleton (README, Pages config, CSS/JS shell) | done | arena-33cfdba4 | `COORDINATION.md`, `README.md`, `.nojekyll`, `.gitignore`, `assets/**` | n/a | Committed before any data work. |
| CORE-01 | Repo audit (line-by-line review of pre-existing content, irregularities) | in progress | arena-33cfdba4 | `repo-audit.html`, `data/audit.json` | GitHub API + `git log` | Repo contained only a 8-byte README stub at commit `a3a2848`; findings published with links. |
| CORE-02 | Hotels: candidate list, 7-night Feb 2027 pricing, amenities, bed/bath constraints | in progress | arena-33cfdba4 | `data/hotels.json`, `hotels.html` | Booking.com live search (retrieved dates logged per row), hotel official sites | Private bathroom + bed ≥ queen is enforced as a booking filter, not assumed. |
| CORE-03 | Michelin restaurants: starred + guide-listed table, hours, price for 2, official links, socials | in progress | arena-33cfdba4 | `data/restaurants_starred.json`, `data/restaurants_listed.json`, `michelin.html` | `guide.michelin.com` (official), restaurant official sites, social profile pages | Unconfirmed cells left blank + flagged. |
| CORE-04 | Activities: hours, exceptions, official links, socials, transit from hotels | unclaimed | — | `data/activities.json`, `activities.html` | Official venue sites | To be claimed after CORE-03 research pass. |
| CORE-05 | Booking strategy: real Feb–Mar 2027 price windows, cheapest time-to-book analysis | unclaimed | — | `data/pricing_windows.json`, `booking-strategy.html` | Booking.com saved searches (dated) | No price extrapolation; each figure is a dated observation. |
| CORE-06 | Itinerary: 7-night plan + 2-week and 2–4 week extensions, transit ≤ 1 h rule | unclaimed | — | `data/itinerary.json`, `itinerary.html` | Built on CORE-02/03/04 outputs | |
| CORE-07 | Open questions & answers (what we know / don't know / how to find out) | unclaimed | — | `data/questions.json`, `open-questions.html` | n/a | |
| CORE-08 | Site improvement suggestions with review workflow | unclaimed | — | `data/suggestions.json`, `suggestions.html` | n/a | Decision status per suggestion: proposed / accepted / rejected / deferred. |
| CORE-09 | Site build + design system (mobile-first dashboard, generators, link checker) | in progress | arena-33cfdba4 | `scripts/**`, root `*.html`, `assets/**` | Build script output | Shared index/nav changed only at integration (CORE-11). |
| CORE-10 | Final verification pass: every row has official source or explicit "unverified" flag; internal link check | unclaimed | — | `flagged-for-review.html`, `docs/VERIFICATION.md` | Re-check against official pages | |
| CORE-11 | Integration & publish: merge branches, re-verify, publish GitHub Pages | unclaimed | — | — | `gh` Pages build status | Only this session at present; can be claimed by a later integration session. |

## Change requests between sessions
(none yet)

## Log
- 2026-11-25 — `arena-33cfdba4` created board, claimed CORE-01/02/03/09. Repo audit: repository had only README stub; no prior site content to preserve.
