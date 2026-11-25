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
| T1 | Research: Michelin Guide listed/starred restaurants, hours, official links, social media | done | arena/4a10e962-nyfun2 | `data/michelin-restaurants.json`, `research/michelin.md` | Must distinguish Guide-listed vs starred; cost for 2; official source per row. |
| T2 | Research: hotels (price/location/amenities, 7-night totals, cheapest window) | done | arena/4a10e962-nyfun2 | `data/hotels.json`, `research/hotels.md` | Private bath + queen+ bed, 2 adults; official booking-source pricing only. |
| T3 | Research: activities + attractions, hours/exceptions, social media links | done | arena/4a10e962-nyfun2 | `data/activities.json`, `research/activities.md` | ≤1 hour travel clustering; official source per row. |
| T4 | Research: transit/rough travel-time methodology + questions/answers/gaps | done | arena/4a10e962-nyfun2 | `research/methodology.md`, `data/questions.json` | Document limits, no inferred values. |
| T5 | Final integration: build GitHub Pages site, line-by-line verification, publish | in progress | arena/4a10e962-nyfun2 | `index.html`, `assets/**`, `pages/**`, `.github/**` | Only after T1–T4 done; owns shared nav/index. |

## Log

### 2026-11-25 — session `arena/4a10e962-nyfun2` (continued)
- T0 done: repo audit found no pre-existing content; no irregularities in repository history.
- T1–T4 claimed by this session (sole active session visible on the branch); non-overlapping file scopes declared above. T5 remains unclaimed until research is integrated.
- Michelin timing irregularity logged for review: Michelin Northeast Cities 2026 ceremony is scheduled for **14 Dec 2026** (official Michelin North America announcement, https://michelinmedia.com/pages/blog/detail/article/c/a1479/), i.e. between this research (25 Nov 2026) and the preferred trip (15–22 Feb 2027). Current Michelin distinctions may change before travel.

### 2026-11-25 — session `arena/4a10e962-nyfun2`
- Created board. Repo audited: single initial commit `a3a2848`, README only, no site/CI/data. No other working branches present locally.
- Claimed T0. No pre-existing work was overwritten.
- Platform constraint: this session is fixed to branch `arena/4a10e962-nyfun2`; cannot create the `session-<id>/<task>` branches requested in the general coordination instructions. Coordination and non-overlapping file scopes are still being used.

### 2026-11-25 — session `arena/4a10e962-nyfun2` (research completion)
- T1 done. Files: `data/restaurants.json`. Sources verified line-by-line against 19 official Michelin pages/articles: official star list (5/14/50), 2025 star announcement, July 2026 Guide additions, and individual restaurant pages for address, hours, cuisine, price band and official website. Third-party YouTube review links are labelled as such; official account ownership was not asserted where not confirmed. Irregularities: upcoming 14 Dec 2026 ceremony; Sushi Sho search results referred to a different city; The Modern and Semma hours not confirmed in the checked section; couple prices unavailable from official pages.
- T2 done. Files: `data/hotels.json`. Sources: Michelin NYC hotel listing/hotel pages, Michelin FiDi guide, Marriott citizenM brand page, citizenM official page. Verified room facts only for citizenM Times Square (XL king, up to two adults, power shower; undated from $395/night). Michelin booking widget states a 31-day maximum advance booking window; no dated February 2027 rate was found. 7-night totals and cheapest window left blank. Irregularity: 11 Howard guest score differs between Michelin hotel page (18) and restaurant page (18.1).
- T3 done. Files: `data/activities.json`. Sources: NPS Statue of Liberty hours, NYC Parks Central Park page/press release, The Met, MoMA, AMNH, 9/11 Memorial & Museum, The High Line, Whitney, Guggenheim, ESB hours page, NYC DOT Staten Island Ferry facts, NYPL. Hours/exceptions transcribed from those pages; couple costs only where an official adult price was published. Irregularities: conflicting Met hours in official snippets, NYPL page-version differences, ESB date-specific February hours unavailable.
- T4 done. Files: `data/decisions.json` and `pages/itinerary.html`. Eight questions with known/missing/provisional answers and discovery paths; eight improvement suggestions; nine review flags. No travel duration was inferred; routing is deferred to live map links plus a documented verification step.
- T5 in progress: site built from these data files, `scripts/verify.py` reports 0 errors / 0 warnings over 51 rows plus all local links, `node --check assets/app.js` passes. GitHub Pages was still configured to `main` at this point; source change to the session branch is the remaining publish step.

### 2026-11-25 — session `arena/4a10e962-nyfun2` (publish)
- T5 verification: live site confirmed at https://kanlerxz87-cyber.github.io/NYFun2/ and JS-rendered tables confirmed on published pages. Pages source is `main`; PR #1 merged from the session branch to trigger the published build. Count inconsistencies (19 vs 20 Michelin rows) corrected in a follow-up commit.
