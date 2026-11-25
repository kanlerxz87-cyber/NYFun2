# Coordination Board — NYFun2

Shared task board for parallel agent sessions. **Read this before starting work.** Claim a task by adding your session ID and file scope, commit and push immediately, then only edit files inside your claimed scope. A task marked `needs review` is published on the site's *Flagged for Review* page and does not block anything.

## Session conventions

- This repository session is bound to branch `arena/4a10e962-nyfun2` (fixed by the platform). Do not switch branches.
- Session ID for this branch: `arena/4a10e962-nyfun2`.
- Shared outputs (site navigation, index, integrated tables) are edited only during final integration after the research tasks are complete.
- Every factual table row needs a source URL from an official/primary source. Unconfirmed values stay blank and are listed on the Flagged for Review page.
- Before each push: `git pull --rebase origin arena/4a10e962-nyfun2`, then push to that same branch. Never discard another session's work on conflict — stop and log it.

## Task board

| ID | Task | Status | Owner session | File scope | Notes |
|---|---|---|---|---|---|
| T0 | Repo audit + create coordination board | done | arena/4a10e962-nyfun2 | `COORDINATION.md`, `README.md` | Repo contained only an 8-byte README at start; no prior findings to preserve. |
| T1 | Research: Michelin Guide listed/starred restaurants, hours, official links, social media | in progress | arena/4a10e962-nyfun2 | `data/michelin-restaurants.json`, `research/michelin.md` | Must distinguish Guide-listed vs starred; cost for 2; official source per row. |
| T2 | Research: hotels (price/location/amenities, 7-night totals, cheapest window) | in progress | arena/4a10e962-nyfun2 | `data/hotels.json`, `research/hotels.md` | Private bath + queen+ bed, 2 adults; official booking-source pricing only. |
| T3 | Research: activities + attractions, hours/exceptions, social media links | in progress | arena/4a10e962-nyfun2 | `data/activities.json`, `research/activities.md` | ≤1 hour travel clustering; official source per row. |
| T4 | Research: transit/rough travel-time methodology + questions/answers/gaps | in progress | arena/4a10e962-nyfun2 | `research/methodology.md`, `data/questions.json` | Document limits, no inferred values. |
| T5 | Final integration: build GitHub Pages site, line-by-line verification, publish | unclaimed | — | `index.html`, `assets/**`, `pages/**`, `.github/**` | Only after T1–T4 done; owns shared nav/index. |

## Log

### 2026-11-25 — session `arena/4a10e962-nyfun2` (continued)
- T0 done: repo audit found no pre-existing content; no irregularities in repository history.
- T1–T4 claimed by this session (sole active session visible on the branch); non-overlapping file scopes declared above. T5 remains unclaimed until research is integrated.
- Michelin timing irregularity logged for review: Michelin Northeast Cities 2026 ceremony is scheduled for **14 Dec 2026** (official Michelin North America announcement, https://michelinmedia.com/pages/blog/detail/article/c/a1479/), i.e. between this research (25 Nov 2026) and the preferred trip (15–22 Feb 2027). Current Michelin distinctions may change before travel.

### 2026-11-25 — session `arena/4a10e962-nyfun2`
- Created board. Repo audited: single initial commit `a3a2848`, README only, no site/CI/data. No other working branches present locally.
- Claimed T0. No pre-existing work was overwritten.
- Platform constraint: this session is fixed to branch `arena/4a10e962-nyfun2`; cannot create the `session-<id>/<task>` branches requested in the general coordination instructions. Coordination and non-overlapping file scopes are still being used.
