# Repository review (2026-11-25)

## Starting state

`git log` at branch `arena/215c2a25-nyfun2`, base commit `a3a2848`:

```
a3a2848 Initial commit
```

`find` at base showed exactly one tracked file:

```
README.md   (8 bytes: "# NYFun2")
```

There was **no** `COORDINATION.md`, site, data, workflow, or prior research in the repository. The shared task board was created this session and its claim pushed before research began.

## Irregularities / review flags

1. **Branch-name deviation.** The request asks parallel sessions to work on branches named `session-<id>/<task>`. The platform pins this session to `arena/215c2a25-nyfun2` and forbids switching/creating other branches. Work was done on the pinned branch with disjoint file scopes recorded in `COORDINATION.md`. Reviewers should confirm this is acceptable for their integration model.
2. **Parallel sessions appeared after this session started.** At the first check, only `main` and this branch existed; later, open PRs from `arena/1a7ae497-nyfun2` and `arena/4a10e962-nyfun2` were found. Per the coordination rule, this session did not overwrite their files: its entire kit now lives in the disjoint namespace `sessions/215c2a25/`. The request for a root-navigation link is logged in the shared `COORDINATION.md`.
3. **GitHub Pages source and deployment restriction.** Pages is enabled on `main` (legacy build). This token cannot change the Pages source (HTTP 403), and the `actions/deploy-pages` route is blocked because deployments are only allowed from `main`. The root site published by session `arena/4a10e962-nyfun2` remains the live dashboard; this kit is published alongside it under `sessions/215c2a25/` via PR #5, without touching root files.
4. **Verification limits.** No official booking site rendered a dated rate for February 2027 (Marriott dated search rendered "0–0 of 0 Results"). Official restaurants did not expose machine-readable menu prices. These gaps are recorded as blanks and flags, never filled with estimates. An OTA price reported in PR #2 is logged as a cross-session discrepancy for manual review.
5. **Superseded workflow file removed.** An experimental `.github/workflows/pages.yml` was tried during publication attempts; it failed because Pages deployments are restricted to `main` and was removed before integration, leaving no broken CI configuration.

## Verification method

- Primary sources: MICHELIN Guide restaurant pages, U.S. National Park Service, NYC DOT, NYC City Clerk/DCWP, MTA, official venue sites, official hotel sites, Michelin North America press release.
- Search results were cross-checked against the linked official page where the page body was retrievable. Where only a search-excerpt was retrievable, the exact excerpted values are used and partial coverage is flagged.
- Every row in the site's tables carries at least one source link; unverified fields are blank and listed on the Flagged for Review page.
- Calendar weekdays were computed deterministically from ISO dates (Python `datetime`) and are labelled as calendar calculations, not sourced events.
