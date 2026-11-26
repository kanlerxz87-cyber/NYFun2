# Verification log — 2026-11-26

Session `arena/9bc6abed-nyfun2` (integration task T18). This file is the human-readable record of
what was re-checked against official sources in this session, what was only corroborated, and what
remains a carried capture from 2026-11-25. The machine-readable version is `data/verification.json`.

## Method and its limits

- The session's sandbox reaches GitHub directly; external pages arrive through a proxied
  fetch/search channel. Pages that block that channel are recorded as **unreachable**, not assumed.
- A value is marked **Verified** only when the official page itself was read again today.
- **Corroborated** means the official page could not be read, but at least three independent
  listings published the same value; the official link stays on the row for a manual check.
- **Carried** means nothing was re-read; the 2026-11-25 capture with its source link stands.

## Re-read today (Verified)

| # | Fact | Value confirmed | Source |
|---|---|---|---|
| 1 | MICHELIN NYC census | 5 three-star · 14 two-star · 50 one-star · 76 Bib Gourmand · 224 Selected; "1–48 of 69" starred | https://guide.michelin.com/en/us/new-york-state/new-york/restaurants/all-starred |
| 2 | Star level spot-check (15 rows) | Le Coucou 1★, Sushi Sho 3★, Jungsik 3★, Eleven Madison Park 3★, Atera 2★, Saga 2★, Joo Ok 2★, César 2★, Noda 1★, Jeju Noodle Bar 1★, Semma 1★, Yoshino 1★, Cote 1★, Crown Shy 1★, Shmoné 1★ | same list page |
| 3 | Eleven Madison Park menus | Full Tasting $385/guest ⇒ $770 for two; Bar Tasting $255 ⇒ $510; lounge bar tasting "begins at $225" ⇒ $450 | https://www.elevenmadisonpark.com/faq |
| 4 | Jungsik | Signature Menu $335 ⇒ $670 | https://www.jungsik.com/menu/ |
| 5 | Masa | Lunch from $495; Table $750; Hinoki $950 ⇒ $990 / $1,500 / $1,900 | https://www.masanyc.com/menus |
| 6 | Cote | Butcher's Feast $84 ⇒ $168; Steak Omakase $225 ⇒ $450 | https://www.cotekoreansteakhouse.com/nycdinnermenu |
| 7 | Gramercy Tavern | Seasonal Menu $178 ⇒ $356; three-course $78 ⇒ $156 | https://www.gramercytavern.com/dining-room-menu/ |
| 8 | The Met | Adults $30 ⇒ $60; address 1000 Fifth Avenue | https://www.metmuseum.org/plan-your-visit |
| 9 | The Met hours | Sun/Mon/Tue/Thu 10–17, Fri–Sat 10–21, closed Wednesday | corroborated by four independent 2026 guides (hours block not in the captured section) |
| 10 | MoMA | Adults $30 ⇒ $60; daily 10:30–17:30, Friday to 20:30; closed Thanksgiving and 25 Dec | https://www.moma.org/visit/ |
| 11 | Lunar New Year parade | 29th parade Sun 21 Feb 2027, 13:00, Chinatown; firecracker ceremony Sat 6 Feb 2027 | http://betterchinatown.com/ + two 2027 listings |
| 12 | Hyatt Place NY/Chelsea | King-bed rooms with "a bathroom with shower"; 180 sq ft; 140 West 24th Street | https://www.hyatt.com/hyatt-place/en-US/lgazc-hyatt-place-new-york-chelsea/rooms |

## Corroborated, official page not readable today

| Fact | Value | Official link (unreadable today) | Corroboration |
|---|---|---|---|
| Bryant Park Winter Village 2026-27 | 28 Oct 2026 – 28 Feb 2027; rink 08:00–22:00; shops end 3 Jan 2027 | https://bryantpark.org/activities/winter-village | four independent 2026 guides |
| Wollman Rink 2026-27 | 28 Oct 2026 – 16 Mar 2027; adults $16 off-peak / $28 peak / $40 prime; rental $12 | https://wollmanrinknyc.com/plan/ | three independent 2026-27 price round-ups |

## Re-read by the parallel sessions the same day (2026-11-26)

These checks were performed by `arena/45972379-nyfun2` / `arena/547ee3a3-nyfun2` and are now part of
the canonical data this build starts from; each row keeps its official link.

| Fact | Value confirmed | Source |
|---|---|---|
| Sushi Sho price | Tock "Shorter Omakase at Hinoki Counter" $495/person incl. administrative fee ⇒ $990 for two; booking through 28 Feb 2027 | https://www.exploretock.com/sushi-sho-nyc/experience/474458/shorter-omakase-hinoki-counter |
| Per Se | Main Dining Room tasting "starting at $200/person" deposit; Salon Lounge now a four-course menu at $150/person deposit — earlier $185/$370 capture could not be re-confirmed, so the row stays blank | https://www.exploretock.com/perse/experience/7768/salon-lounge-seating |
| Wollman Rink 2026-27 calendar | 15 Feb Community Day (public-sector employees/families), 16–21 Feb peak $28, 22 Feb–13 Mar off-peak $16, 14–16 Mar community days; season ends 16 Mar 2027 | https://wollmanrinknyc.com/plan/ |
| Bryant Park Winter Village | Rink and Lodge to 28 Feb 2027; holiday shops closed 3 Jan 2027; free admission | https://bryantpark.org/activities/winter-village |
| Lunar New Year parade | 29th parade Sun 21 Feb 2027, 13:00 | http://betterchinatown.com/ |
| Activity official socials | MoMA, Met, AMNH, 9/11, High Line, Whitney, Guggenheim, ESB, NYPL, Wollman | each venue's own social page |

## Not re-read (carried capture, 2026-11-25)

| Fact | Why | Where it lives |
|---|---|---|
| Dated hotel totals for 15–22 Feb 2027 | Booking.com property pages returned an error to the fetcher; the Manhattan window search page did load, confirming availability | `data/hotels.json`; flags F10/F25 |
| 25 hotel→cluster and 10 hotel→activity transit legs | Google Maps cannot be queried programmatically from this session | `sessions/33cfdba4/data/transit_anchors.json`; each row links a live directions query |
| MICHELIN ceremony date (14 Dec 2026) | not re-fetched | https://michelinmedia.com/pages/blog/detail/article/c/a1479/ ; flag F1 |
| Remaining 57 restaurant rows' star levels | spot-check + census rather than 72 individual page reads | `data/restaurants.json` with a MICHELIN link per row |
| 15 activity pages (all but the Met and MoMA) | time-boxed; each row keeps its official hours link | `data/activities.json` |

## Problems found while verifying

1. **Stale counts on the previous site (F22).** The old front page said 20 restaurant rows, 12
   activities and 10 hotels; its own data held 72, 12 and 12, and README said 21. Counts are now
   rendered from JSON at load and the static HTML matches.
2. **Kit rosters ≠ official census (F23).** 14 kit venues are outside the 69-star roster; one kit
   carried three starred names absent from today's live list. None were merged into the census.
3. **Contested prices (F24).** Atomix ($424 vs $495/person), Atera ($298 vs $325) and Per Se
   ($185 vs $295) stay blank. Le Bernardin keeps $218 with the $225 alternative shown.
4. **Organiser typo (F19).** betterchinatown.com's English line says 21 Feb 2027; the Chinese line
   beside it still says 2026. Two independent 2027 listings agree with the English date.
5. **Duplicate rows after merging kits.** Frederick, NYPL, the Met and 9/11 appeared twice; the
   merge now keys them and the verifier fails on duplicates.
6. **Mis-traced transit risk.** A fuzzy name match initially attached Eurostars' legs to The Wall
   Street Hotel. Matching is now key-based and unmeasured hotels stay blank.
7. **One hotel dropped for lack of a source.** The Benjamin had measured transit but no official
   page for its room, so it was removed from the published list rather than shown unsourced.
8. **Flag ID collision.** The parallel sessions used F18–F20, so this session's new flags were
   renumbered F21–F28; the organiser-typo flag was dropped because their F19 already records it.

## Reproduce

```bash
python3 scripts/build_data.py   # merge (idempotent)
python3 scripts/build_site.py   # render
python3 scripts/verify.py       # 0 errors, 0 warnings
```

## Render and deploy checks (2026-11-26, post-merge)

- `python3 scripts/verify.py` → 0 errors, 0 warnings over 13 HTML pages and 150 data rows.
- `node --check assets/app.js` → pass.
- **jsdom render test** with `fetch` served from the local files: every page's tables populate from
  JSON and no console errors are raised — Michelin 101 rows, hotels 21, activities 18, questions 13,
  suggestions 17, flags 28, verification 16, compare 5, repo-audit 8, itinerary 5, sources 11;
  landing counters render 72 / 24 / 16 / 8 / 18 / 28.
- **Deploy:** PR #23 merged to `main` as `a78f15e`; GitHub Pages build for that commit reports
  `built`, and the live `pages/verification.html` shows this log.

Two wording defects caught in the live page and fixed in the follow-up commit: the Met hours cell
read "Sat-Mon/Tue/Thu" (now "Sun/Mon/Tue/Thu") and the transit note said "35 stored transit minutes"
(now "35 stored transit legs: 25 hotel→cluster, 10 hotel→activity").
