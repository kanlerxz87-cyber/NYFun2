# Local consistency audit — 2026-11-27

Session: `arena/7095f8e7-nyfun2` · Task T27.

## Scope and important limit

This is a **repository/data consistency check**, not a new round of live source verification. No restaurant, hotel, activity, transit, availability, price, or MICHELIN value was re-quoted or re-read from an external site during this update. The latest recorded official-source reads remain dated **2026-11-26** (with older carried captures identified separately in `data/verification.json`). Factual values and their source URLs were left unchanged. Do not interpret “checked 2026-11-26” as “checked today.”

The existing dated source register remains [`../data/verification.json`](../data/verification.json); its rows retain the official-source URL and the previous session's read/carry status. A machine URL check does not establish that a page remains live or that its content is unchanged.

## Local checks performed

| Check | Result | Method |
|---|---|---|
| Canonical JSON and documented coverage counts | Pass | Recomputed row, price, hours, social, address, hotel-rate and transit counts from `data/*.json`; checked them against `data/verification.json`. |
| Overview counters | Pass | Compared the static fallbacks in `index.html` to the canonical dataset totals. |
| README and page headline counts | Pass | Checked restaurant prices (25), hotels (16 total / 8 with dated rates), activities (18), questions (13), suggestions (17), and flags (29) against their datasets. |
| Relative-date wording | Pass after correction | Searched maintained UI/docs for “checked today”, “re-read today”, and “re-quoted today”; historical check badges now show an explicit date. |
| Data merge + site generation | Pass | `python3 scripts/build_data.py` completed with 72 restaurants, 16 hotels, 18 activities, 13 questions, 17 suggestions and 29 flags; `python3 scripts/build_site.py` generated the overview and 12 pages from the current JSON inputs. |
| Structural site verification | Pass | `python3 scripts/verify.py` — 13 HTML pages, 185 data/check rows, 0 errors, 0 warnings. |
| JavaScript syntax | Pass | `node --check assets/app.js`. |
| Whitespace/conflict check | Pass | `git diff --check`; verifier also scans maintained source files for unresolved merge markers. |

## Irregularities found and corrected

The public documentation had drifted from the merged canonical data: README stated 24 priced restaurants and 28 flags, while the data contains 25 priced restaurants and 29 flags; the overview tile said 16 suggestions while the list has 17; verification badges used “checked today” even when the last source reads were on the prior date; and README incorrectly said Atomix was blank despite its November Tock price being included. These labels, counts and claims were corrected, and automated checks now fail if the README, overview fallback counters, verification coverage counters, or review-page headlines drift from the data.

## Not re-verified in this audit

All external facts remain subject to the dated-source caveats already on [`pages/flagged.html`](../pages/flagged.html) and the existing verification log. In particular, stored hotel booking-engine prices, stored Google Maps minutes, current menus, operating hours and future seasonal/event schedules should be re-opened from each row's linked source before a purchase or reservation. No new claim is made that these links or values were live on 2026-11-27.
