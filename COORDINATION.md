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
| 1 | Create shared coordination board (this file) | in progress | arena/215c2a25-nyfun2 | COORDINATION.md | n/a | Claim pushed before research starts |
| 2 | Repo review & baseline documentation | in progress | arena/215c2a25-nyfun2 | docs/repo-review.md | git history, README.md | Repo contains only `README.md` at base commit |
| 3 | Trip dates, transit radius & planning constraints research | unclaimed | — | data/trip.md, data/transit.md | official MTA / calendar sources | Feb–Mar 2027 window |
| 4 | Hotel shortlist: price, location, amenities, 7-night totals | unclaimed | — | data/hotels.md | official hotel sites / booking sources | Private bath, queen+ |
| 5 | Michelin Guide listed/starred restaurants + clusters | unclaimed | — | data/michelin.md | guide.michelin.com official pages | Listed vs starred must be distinguished |
| 6 | Activities + official hours + social review links | unclaimed | — | data/activities.md, data/social.md | official venue sites + platform pages | Blank + flag when unverified |
| 7 | Executive summary, decision questions, suggestions | unclaimed | — | docs/executive-summary.md, docs/questions.md, docs/suggestions.md | derived from verified tables | No invented numbers |
| 8 | Flagged-for-review register (unverified values / irregularities) | unclaimed | — | docs/flagged-for-review.md | cross-check log | Every blank must be flagged |
| 9 | Site build: landing page + category subpages, mobile-first | unclaimed | — | index.html, pages/*, assets/* | line-by-line re-check | Final integration only |
| 10 | Final integration: re-verify, link check, publish GitHub Pages | unclaimed | — | all shared outputs (index.html, assets/site.js, pages/nav) | build + link check | Runs after tasks 2–8 are done |

## Log

- 2026-11-25 — Session `arena/215c2a25-nyfun2` created the file board from scratch; base commit had no `COORDINATION.md`. Claimed all tasks tentatively because no other branch/session claims exist in `git branch -a` (`main`, `arena/215c2a25-nyfun2` only).
- 2026-11-25 — Branch-name deviation recorded above per platform restriction.
