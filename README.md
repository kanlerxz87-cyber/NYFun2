# NYFun2 — New York trip planning dashboard

A static, mobile-friendly research dashboard for two adults planning a trip within 15 February–23 March 2027. [GitHub Pages site](https://kanlerxz87-cyber.github.io/NYFun2/).

## Decision status

- Preferred dates 15–18 February cover three nights; the requested seven-night comparison uses 15–22 February as a provisional case.
- No comparable **hotel-direct** seven-night total, cheapest week, or verified one-hour transit ranking has been established. Prior third-party rate snapshots and tax calculations have been excluded from the main hotel table.
- Historical restaurant and activity research is source-linked but has **not** been independently reverified in full. Distinctions, hours, prices and availability may change. The official [Michelin ceremony announcement](https://michelinmedia.com/pages/blog/detail/article/c/a1479/) schedules the 2026 selection for 14 December 2026.
- The [review register](pages/flagged.html) records gaps and conflicts, including inconsistent Eleven Madison Park bar-tasting prices in its official FAQ. Historical alternate dashboards under `alt/` and `sessions/` are preserved but are not the audited main dataset.

## Files

`index.html` and `pages/` provide the dashboard and categories; `data/` contains its JSON; `assets/` contains styling and rendering; `COORDINATION.md` records ownership, sources and session history. The static site has no build dependencies.

## Checks

```sh
python3 scripts/verify.py
node --check assets/app.js
python3 -m http.server 8000
```

The script checks local structure and links, not whether external sources support the facts or are current. The site requires HTTP to load JSON; opening HTML directly as a file is not supported. GitHub Pages serves the root of `main` with `.nojekyll`.
