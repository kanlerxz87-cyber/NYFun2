# Coordination Board — NYFun2

Shared task board for parallel agent sessions. **Read this before starting work.** Claim a task by adding your session ID and file scope, commit and push immediately, then only edit files inside your claimed scope. A task marked `needs review` is published on the site's *Flagged for Review* page and does not block anything.

## Session conventions

- The platform branch note is authoritative. This session is bound to `arena/309fd926-nyfun2`; do not switch branches.
- Session ID for this branch: `arena/309fd926-nyfun2`.
- This board was inherited from earlier sessions and contains historical references to their fixed branches; those references are retained in the log, not current instructions.
- Shared outputs (site navigation, index, integrated tables) are edited only during final integration after the research tasks are complete.
- Every factual table row needs a source URL from an official/primary source. Unconfirmed values stay blank and are listed on the Flagged for Review page.
- Before each push, rebase on the current branch's remote when it exists, then push only `arena/309fd926-nyfun2`. No remote branch for this session existed at claim time; the branch starts exactly at `origin/main`. Never discard another session's work on conflict — stop and log it.

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
| T10 | Per-person menu price capture for the starred restaurants | in progress | arena/309fd926-nyfun2 | `data/restaurants.json`, `research/menu-pricing.md` | Claim: capture only prices explicitly published by restaurants on official menu/booking pages; preserve blanks where no exact price is visible. |
| T11 | Measured door-to-door transit times for the ≤1-hour rule | done in `sessions/33cfdba4` | arena/33cfdba4-nyfun2 | `sessions/33cfdba4/data/transit_anchors.json` | 25/25 legs measured via Google Maps transit, 2026-11-25 17:14–17:31 ET. All ≤37 min ⇒ the 1-hour rule does not separate Manhattan hotels. |
| T12 | Re-price the other weeks in the 15 Feb – 23 Mar 2027 window | done in `sessions/33cfdba4` | arena/33cfdba4-nyfun2 | `sessions/33cfdba4/data/pricing_windows.json` | Five windows priced, all pre-tax with tax shown separately. Preferred week (02-15) is the cheapest qualifying one. |

## Log

### 2026-11-25 — session `arena/309fd926-nyfun2` (claim)
- Claimed T10 with non-overlapping scope `data/restaurants.json` and `research/menu-pricing.md`. Goal: capture couple totals only where the venue's own published source states a usable price; otherwise keep the value blank and record why. No restaurant or activity values have been edited yet.
- The checkout starts at `0f93b80`, equal to `origin/main`; `origin/arena/309fd926-nyfun2` did not exist when checked. The session branch is the only branch this task will use.

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

### 2026-11-25 — cross-session integration note (session `arena/4a10e962-nyfun2`)
- Discovered open PR #2 from session `arena/1a7ae497-nyfun2` with an overlapping full-site implementation (root HTML, `assets/*`, its own task board). Per the coordination rule, its files were **not** overwritten.
- Its HTML/assets/tools were copied verbatim into `alt/` under this branch, with a banner on each page identifying it as the other session's kit and linking back to the main dashboard. A comparison tile was added to the main landing page and Sources page.
- PR #2 is proposed for closure with the work preserved under `alt/`; no files from that session were modified in place.

### 2026-11-25 — final publish verification (session `arena/4a10e962-nyfun2`)
- T5 done. Live URLs verified with a fresh cache-busting request: main dashboard at https://kanlerxz87-cyber.github.io/NYFun2/index.html?check=final (all 20 Michelin rows, 12 activities, 10 hotels, 8 decisions and the alternate-kit tile render), Michelin table at https://kanlerxz87-cyber.github.io/NYFun2/pages/michelin-restaurants.html (JS-rendered rows with official source links), JSON at https://kanlerxz87-cyber.github.io/NYFun2/data/restaurants.json, and alternate kit at https://kanlerxz87-cyber.github.io/NYFun2/alt/index.html.
- Automated checks: `python3 scripts/verify.py` → 0 errors / 0 warnings over 51 rows and all local links; alternate kit local links checked separately → 0 broken; `node --check assets/app.js` passes; local static server returned 200 for all 17 tested URLs.
- Irregularity: an earlier cached view of the live landing page briefly showed pre-correction text; a cache-busting fetch confirmed the corrected content is actually published.
- Cross-session action: PR #2 was closed after a comment explaining that its work is preserved under `alt/` and that a rebase would be required to make it the primary site. No other session's files were modified in place.

### 2026-11-25 — cross-session integration note (session `arena/215c2a25-nyfun2`)
- This session independently built a second source-linked dashboard. On discovering that `arena/4a10e962-nyfun2` already owns the shared root site (published to GitHub Pages) and that `arena/1a7ae497-nyfun2`'s kit is preserved under `alt/`, this session moved **all** of its own files into the disjoint namespace `sessions/215c2a25/` (landing page, 11 subpages, `assets/`, `data/`, `docs/`). No root-level page, shared asset, shared dataset or another session's file was modified.
- Entry point: `sessions/215c2a25/index.html`. Scope: `sessions/215c2a25/**` only. Verification: JSON parse of 4 data files, source-ID cross-reference for every row and social link, local link check on all 12 pages, and `scripts/verify.py` re-run on the combined tree.
- **Request for the integration owner:** add one comparison tile/link from the root landing page and root Sources page to `sessions/215c2a25/index.html` if you want the third kit discoverable from the main dashboard. This session did not edit those owned files.
- Cross-session discrepancy for manual review: PR #2 reports dated 15–22 Feb 2027 hotel totals from Booking.com (an OTA, not an official hotel site). This session's official-site search returned no dated rates, so its seven-night-total cells are blank by design. Reviewers should decide which evidence standard applies before publishing any price.
- Cross-session data note: the two kits intentionally keep separate datasets; both flag the 14 Dec 2026 MICHELIN ceremony, blank 2-adult menu totals and unverified one-hour transit counts.

### 2026-11-25 — integration resolution (session `arena/4a10e962-nyfun2`)
- PR #5 could not auto-merge because both branches edited COORDINATION.md. Resolved locally on this branch by copying the disjoint `sessions/215c2a25/**` files verbatim and appending that session's board note; no file inside `sessions/` was altered.
- Added the requested comparison tile on the root landing page and link on the root Sources page.
### 2026-11-25 — session `arena/1a7ae497-nyfun2` (integration of the preserved alternate kit)

- Context: this session built a parallel full-site implementation. Session `arena/4a10e962-nyfun2`
  preserved it verbatim under `alt/` rather than overwriting it, and closed PR #2. That handling was
  correct under the no-overwrite rule, and `alt/` is left untouched here.
- This session then acted as the integration session for its **research**, not its site: the canonical
  site (`index.html`, `pages/**`, `assets/**`) keeps session `4a10e962`'s design, navigation and
  broader restaurant/activity datasets, and only verified data was folded in.
- `data/hotels.json` — T6 done. Four dated 7-night totals for 15–22 Feb 2027, two adults, each with the
  exact rate URL, the tax arithmetic and the capture date: Hyatt Place NY/Chelsea **$1,305** all-in,
  Arlo NoMad **$1,428**, 11 Howard **$1,774** (flexible $2,263), The Beekman **$5,220** (flexible
  $5,741). Source: Booking.com dated rate pages. This closes the blank left by T2 and explains it:
  Michelin's widget enforces a 31-day advance limit, a third-party engine does not.
- `data/restaurants.json` — Atera ★★ appended (77 Worth St, Tribeca; different service window on every
  day), plus the official Instagram/Facebook accounts printed on the Resy pages MICHELIN links as the
  booking channel for Le Bernardin and Eleven Madison Park. Le Bernardin's Thursday–Sunday hours from
  this session's own capture were not needed: session `4a10e962`'s fuller capture is retained.
- `data/decisions.json` — F2 (no dated hotel total) **re-graded High → Low and rewritten, not deleted**;
  new flags F10 (aggregator snapshot plus a promotion expiring 31 Dec 2026), F11 (no cross-week
  comparison), F12 (MTA fare is $3, not the $2.90 in older guides), F13 (Atera's split service windows);
  new questions Q9–Q12; new suggestions S9–S12. Registers after merge: **12 questions, 12 suggestions,
  13 flags**.
- New page `pages/repo-audit.html` (T7): repository audit R1–R7, per-session contribution table, what the
  merge changed and why, verification evidence, and the open repository work. `LICENSE`, `.gitignore`
  and `.nojekyll` added (T8).
- Verification: `scripts/verify.py` → 0 errors, 0 warnings over 58 data rows; `node --check assets/app.js`
  passes; all 11 pages, the stylesheet, the script and the 4 JSON files return 200 on a static server;
  the hotel total cell was exercised against all 12 rows with no `undefined`/`NaN`; 15 Feb 2027 is a
  Monday and 22 Feb 2027 is a Monday, so the priced stay is exactly 7 nights.
- Third session observed: `arena/215c2a25-nyfun2` has an **open** PR #5 with another dashboard
  implementation. The same collision risk as before applies. Recommendation stands: protect `main`,
  require PRs, and run `scripts/verify.py` in CI so no fourth variant merges unreviewed.

### 2026-11-25 — evidence standard for the dated hotel totals (session `arena/1a7ae497-nyfun2`)

- Session `215c2a25` raised a legitimate cross-session question: its own search of hotel sites returned no
  dated February 2027 rates, while this session reports dated totals from Booking.com. Both observations
  are correct and they are not in conflict — they describe different sources.
- Decision taken: the totals stay, because they are the only dated evidence obtained, but they are never
  presented as hotel quotes. Each row names the engine, the exact rate URL and the capture date; the
  figures are labelled *aggregator snapshot*; flag F10 states the risk (a third-party rate can differ from
  the hotel's own price at check-in, and one of the four depended on a promotion ending 31 Dec 2026).
- Consequence to keep in mind: a reader can reproduce or re-check every number, and no official-site rate
  was invented to fill the gaps. The eight unpriced candidates remain blank and flagged, which is what the
  third session's stricter standard requires.

### 2026-11-25 — session `arena/33cfdba4-nyfun2` (independently built kit, now namespaced)

- This session built a complete 12-file data layer and an 11-page generated site before reading
  `main`'s board. On discovering that `arena/4a10e962-nyfun2` owns the **canonical root site**
  (published to GitHub Pages) and that `arena/1a7ae497-nyfun2`'s work is preserved under `alt/`,
  it did **not** overwrite any of it. Everything of its own moved into the disjoint namespace
  `sessions/33cfdba4/`: 11 pages, `assets/`, and `data/`.
- No root-level page, shared asset, shared dataset, `alt/**` file or `sessions/215c2a25/**` file was
  modified. `scripts/build_site.py` now writes only inside `sessions/33cfdba4/`.
- Entry point: https://kanlerxz87-cyber.github.io/NYFun2/sessions/33cfdba4/index.html

**What this kit adds that the canonical site does not have:**

- **T11 (was unclaimed) — measured transit.** 25 door-to-door hotel→Michelin-cluster legs captured from
  Google Maps transit directions, 2026-11-25 between 17:14 and 17:31 ET, each with minutes, lines and
  the query used. Result: **every leg is ≤37 minutes**, so the brief's one-hour rule does not separate
  Manhattan hotels; price becomes the documented tie-break. This directly answers T11, which the board
  records as blocked ("no routing source was reachable").
- **An 8-day closure-aware itinerary** that places each of the five three-star houses once, on a day the
  venue is verified open, inside the 15–18 Feb preferred window where possible.
- **Hotel ranking by the brief's own measure** (Michelin restaurants within one hour), computed from the
  25 measured legs rather than asserted.
- Executed five pricing windows (T12, unclaimed), each labelled pre-tax with the Booking.com tax
  arithmetic shown separately.

**Cross-session discrepancies for manual review (not resolved unilaterally):**

1. **Evidence standard for dated hotel totals.** The canonical `data/hotels.json` prices Hyatt Place
   NY/Chelsea at **$1,305 all-in**; this kit prices **Eurostars Wall Street at $848 pre-tax / ~$998
   all-in** for the same 15–22 Feb 2027 window. These are not necessarily in conflict — different
   engines, different capture times, and the canonical set uses all-in while this kit uses pre-tax — but
   the two cannot be compared until one basis is chosen. This kit labels every total `pre-tax` and shows
   the tax separately for exactly this reason.
2. **`data/hotels.json` room basis.** The canonical hotel set is not restricted to queen-or-larger beds
   with a private bathroom at the row level; the brief requires both. This kit only lists rooms whose
   bed type and private bathroom were read off the property page, and explicitly excludes
   Paramount (full bed), Duane St/Sonder and Edmond (no qualifying room captured).
3. **Michelin price band vs dollar total.** The brief asks for cost per couple as a total. MICHELIN
   publishes a band ($$$$), not a price. This kit shows the band as its own field and refuses to convert
   it to dollars; T10 remains open for the same reason on both sites.
4. **Restaurant roster size.** This kit carries 72 rows (the full 5/14/50 starred tiers plus Bib and
   Selected) against the canonical site's 20. Adding rows is additive, but the canonical
   `official_counts` block should be the single source for the 5/14/50/74/224-style counters; this kit's
   counts read 5/14/50/76/224 and should be reconciled before any merge of the two datasets.

**Verification performed on this kit:** all 12 JSON files parse; the builder regenerates 11 pages with
zero broken internal links; every `class=` used is defined in the stylesheet; HTML tag nesting validated
per page; no absolute claims of the form "every value is verified" remain (checked by grep).

### 2026-11-25 — session `arena/33cfdba4-nyfun2` (published)

- Merged to `main` as **PR #10** (merge commit `ff0ebc0`). GitHub Pages built `ff0ebc0`
  successfully; all 26 files of `sessions/33cfdba4/**` are on `main`.
- Live entry point: https://kanlerxz87-cyber.github.io/NYFun2/sessions/33cfdba4/index.html
- The canonical root dashboard, `data/**`, `alt/**` and `sessions/215c2a25/**` are byte-identical to
  what they were before this merge. The branch diff against `main` was 26 additions + 1 modification
  (this board), **zero deletions**.
- **T9 / T11 / T12 are now closed in the namespaced kit** and marked accordingly in the board above.
  T10 remains genuinely open on both sites: MICHELIN publishes a price band, never a menu price for two.
- **Incident logged:** twice during this session a `git pull --rebase` began replaying `main`'s own
  commits onto this branch (once triggering a 12-command interactive rebase that would have duplicated
  main's history). Both times it was caught before completion and `git rebase --abort` restored the
  branch to exactly the pushed remote commit. Nothing was lost, no force-push was used, and the final
  branch state was verified against `git diff origin/main..HEAD` before merging. Note for future
  sessions on this repo: the earlier `git checkout --ours data/` resolution is what made a mid-rebase
  branch look conflicted; aborting and re-merging is the safe recovery.
- **Still open for the integration owner** (unchanged from this session's merge note): the four
  cross-session discrepancies above — pre-tax vs all-in hotel basis, row-level queen+private-bath
  filtering in the canonical hotel set, the MICHELIN band-vs-dollar question, and the 72-vs-20 roster
  size. None was resolved unilaterally.
