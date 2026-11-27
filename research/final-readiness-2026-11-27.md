# Final readiness audit — 2026-11-27

## Scope and result

This was a readiness audit of the integrated dashboard already present on `main`, not a new round of restaurant, hotel, or attraction research. No factual dataset values were changed. The current branch began at `a4f205d` (`main`); the canonical source-linked content and the outstanding uncertainty register remain on the site for review.

## Reproducible local checks

- `python3 scripts/verify.py` — passed: 13 HTML pages, 185 data rows, 0 errors, 0 warnings. Dataset counts: 72 restaurants, 16 hotels, 18 activities, 13 questions, 17 suggestions, 29 flags, 25 verification checks, and 25 transit legs.
- `python3 scripts/build_site.py` — completed and reported writing the overview and 12 pages. It produced no working-tree changes.
- `node --check assets/app.js` — passed.
- `git diff --check` — passed.

The verifier establishes repository structure and link-field constraints; it does **not** prove that external source URLs remain reachable, that prices are bookable at this moment, or that live schedules have not changed. The repository's dated verification notes and per-row source links are the evidence to use for those claims. No live hotel availability/quote or restaurant booking quote was fabricated in this audit.

## Publication status observed

GitHub Pages API reports the site as `built`, public, HTTPS-enforced, with source `main` at `/`: <https://kanlerxz87-cyber.github.io/NYFun2/>. The latest successful Pages deployment observed in `gh run list` is run `45834063858`, for the main-branch merge from PR #30. A verification-workflow run (`46041857073`) started for this audit branch after its coordination claim; deployment is correctly main-only and is not triggered by this feature branch.

## Irregularities / limitations

- Prices and opening hours are time-sensitive. Existing rows and flags explicitly distinguish confirmed, blank, and unverified values; this audit did not renew third-party availability quotes.
- The repository contains parallel-session historical workspaces and older variants. The root `scripts/verify.py` checks the canonical dashboard (not every historical session kit), so those archives should not be mistaken for the canonical tables.
- Existing board entries contain historical counts and deployment records from earlier integrations. This note records the current audit's canonical counts and current Pages status without rewriting history.

## Sources for manual review

- Published overview: https://kanlerxz87-cyber.github.io/NYFun2/
- Published verification page: https://kanlerxz87-cyber.github.io/NYFun2/pages/verification.html
- Published flagged-for-review page: https://kanlerxz87-cyber.github.io/NYFun2/pages/flagged.html
- MICHELIN NYC official starred roster: https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred
- GitHub Pages deployment workflow and result: https://github.com/kanlerxz87-cyber/NYFun2/actions/workflows/pages/pages-build-deployment
