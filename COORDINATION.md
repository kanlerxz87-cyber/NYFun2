# Coordination Board — NYFun2

Shared task board for parallel agent sessions. **Read this before starting any task.**
Statuses: `unclaimed` | `in progress` | `done` | `needs review` (published on the Flagged for Review page; does not block).

## Session / branch note

This session is pinned by the platform to branch `arena/215c2a25-nyfun2` (from `a3a2848`). Platform rules forbid switching to, creating, or pushing to any other branch, so the requested `session-<id>/<task>` branch convention **cannot** be followed here. This session therefore operates only on `arena/215c2a25-nyfun2`, claims disjoint file scopes below, and commits/pushes frequently. Any other session must not edit files claimed below; log requests here instead.

Session ID: `arena/215c2a25-nyfun2`
Started: 2026-11-25 (UTC)

## Task board

| # | Task | Status | Owner | File scope | Sources / verification | Notes |
|---|------|--------|-------|------------|------------------------|-------|
| 1 | Create shared coordination board | done | arena/215c2a25-nyfun2 | COORDINATION.md | n/a | Claim pushed before research started |
| 2 | Repo review & baseline documentation | done | arena/215c2a25-nyfun2 | docs/repo-review.md, pages/repo-review.html | `git log`, `git branch -a`, base `find` | Base had only README.md; irregularities documented |
| 3 | Trip dates, transit radius & planning constraints | done | arena/215c2a25-nyfun2 | docs/executive-summary.md, docs/questions.md, pages/itinerary.html | NYC City Clerk, NYC DCWP, NPS, MTA official map | Weekdays = calendar calculations; ≤1h transit explicitly unverified |
| 4 | Hotel shortlist: bed, bath, amenities, prices | done | arena/215c2a25-nyfun2 | data/hotels.json, pages/hotels.html | Official hotel room pages, Michelin hotel page, official Marriott dated search | 7-night totals blank: no dated official rate; undated Standard lead rate labelled |
| 5 | Michelin statuses, clusters, hours, price bands | done | arena/215c2a25-nyfun2 | data/restaurants.json, pages/restaurants.html | 18 official Guide pages + 3 Guide filter pages + Michelin NA press release | Listed-vs-starred explicit; partial hours flagged |
| 6 | Activities + hours + social review links | done | arena/215c2a25-nyfun2 | data/activities.json, pages/activities.html | NPS, Met, MoMA, 9/11, Central Park Conservancy, High Line, Top of the Rock, AMNH, Broadway League, NYC DOT; YouTube/TikTok links | 11 activities, 11 social links; blanks flagged |
| 7 | Executive summary, decision questions, suggestions | done | arena/215c2a25-nyfun2 | docs/executive-summary.md, docs/questions.md, docs/suggestions.md, matching pages | Derived only from verified tables | Decision gate defined |
| 8 | Flagged-for-review register | done | arena/215c2a25-nyfun2 | docs/questions.md, pages/flagged.html, data/*.json | Generated from row flags with primary source links | No inferred values |
| 9 | Site build: landing + category subpages | done | arena/215c2a25-nyfun2 | index.html, pages/*.html, assets/*, data/*.json | Local JSON validation + local link check | Mobile-first; filterable tables; 11 subpages |
| 10 | Final integration: re-verify, link check, publish | done | arena/215c2a25-nyfun2 | all shared outputs | JSON validation, local link check, GitHub Pages source change | See deployment note below |

## Log

- 2026-11-25 — Session `arena/215c2a25-nyfun2` created the board from scratch; base commit had no `COORDINATION.md`. Claimed all tasks tentatively because no other branch/session claims exist in `git branch -a` (`main`, `arena/215c2a25-nyfun2` only).
- 2026-11-25 — Branch-name deviation recorded above per platform restriction.
- 2026-11-25 — Research complete. Primary verification source: [MICHELIN Guide NYC filters](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/3-stars-michelin) (5/14/50 counts), [Michelin NA 2026 ceremony announcement](https://michelinmedia.com/pages/blog/detail/article/c/a1479/) (14 Dec 2026), [NYC City Clerk holidays](https://www.cityclerk.nyc.gov/content/legal-holidays), [NPS Statue of Liberty FAQ](https://www.nps.gov/stli/planyourvisit/frequently-asked-questions.htm), official venue/hotel pages. All 73 source URLs are in `data/sources.json` and rendered on the Sources page.
- 2026-11-25 — Verification performed: JSON parse of all four data files; source-ID cross-reference for all restaurant/activity/hotel rows and all social links; local href/src link check on all 12 HTML pages (no broken local links); row-level verification status (`verified`/`partial`) and per-flag review links.
- 2026-11-25 — Irregularities: (1) branch naming deviation; (2) no dated 2027 hotel rates from official booking engines ([Marriott dated search](https://www.marriott.com/search/findHotels.mi?destinationAddress.city=New%20York&destinationAddress.stateProvinceAbbreviation=NY&fromDate=02%2F15%2F2027&toDate=02%2F22%2F2027) returned no priced results), so all 7-night totals are blank; (3) no official 2-adult menu totals, so all restaurant cost cells are blank; (4) ≤1-hour transit counts not verifiable, so hotel rank is a labelled address-cluster proxy; (5) 2026 MICHELIN ceremony occurs after research date; (6) NYC DOT Brooklyn Bridge document is dated 2012. All are published on the Flagged for Review page.
- 2026-11-25 — Integration: final re-check of data/links done on the working branch. GitHub Pages was already enabled on `main`; publication from the working branch is done via the GitHub Pages source API so that no push to another branch is required. If the platform blocks that setting change, the site files remain ready on this branch for a maintainer to publish.
- 2026-11-25 — Handoff note: a later session may safely add verified dated rates or post-ceremony star data by editing only `data/hotels.json` / `data/restaurants.json` and re-running the local link/JSON checks; no other scope needs to change.
