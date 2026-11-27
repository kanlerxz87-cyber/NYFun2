# Official-source verification addendum — 2026-11-27 (session `arena/dbf0d1f0-nyfun2`, task T29; originally claimed as T27)

Scope: fresh official-source re-read of the points that were carried, blank or stale on the live
site after the 2026-11-26 integration. Every value below was read from the named page during this
session; anything not re-read is listed under "Not re-read / still open". Nothing was inferred.

## 1. Values re-read and confirmed (official source)

| Item | Value confirmed | Official source |
|---|---|---|
| MICHELIN NYC starred census | 5 three-star / 14 two-star / 50 one-star = 69 starred; 76 Bib Gourmand; 224 Selected | https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred |
| MICHELIN 2026 Northeast Cities ceremony | 14 Dec 2026, The Glasshouse, New York | https://michelinmedia.com/pages/blog/detail/article/c/a1479/ |
| Chinatown Lunar New Year Parade 2027 | Sunday 21 Feb 2027, 13:00; firecracker ceremony 6 Feb 2027 | https://betterchinatown.com/new-york-city-2027-lunar-new-year-parade-dates-announced/ |
| Bryant Park Winter Village | 28 Oct 2026 – 28 Feb 2027; Rink 8am–10pm; admission free; rentals $18.72–$64.48 incl. admin | https://bryantpark.org/activities/bank-of-america-winter-village-at-bryant-park |
| Wollman Rink | 28 Oct 2026 – 16 Mar 2027; Mon–Tue 10:00–14:30; Wed–Thu 10:00–21:00; **Fri–Sat 09:00–22:00; Sun 09:00–21:00**; $16 / $28 / $40 adult; $12 rental; tax included; 15 Feb Community Day, 16–21 Feb Peak, 22–25 Feb Off-Peak | https://wollmanrinknyc.com/plan/ |
| MTA fares | Subway / local bus $3; express bus $7.25 | https://www.mta.info/fares-tolls |
| MoMA | Adult $30 ($60 for two); Mon–Thu/Sat/Sun 10:30–17:30; Fri 10:30–20:30 | https://www.moma.org/visit/ |
| The Met | Adult $30 ($60 for two); NY residents pay-what-you-wish. Museum hours NOT re-read this session | https://www.metmuseum.org/plan-your-visit |
| Eleven Madison Park | Full Tasting $385/guest ($770 for two); Bar Tasting $255/guest ($510). FAQ also says lounge bar tasting "begins at $225" — inconsistency kept visible | https://www.elevenmadisonpark.com/faq |
| Atomix (Tock) | Nov Chef's Counter $424/guest ($848) and Bar $314 ($628); Dec $495 and from $352 | https://www.exploretock.com/atomixnyc/help |
| Sushi Sho (Tock) | Shorter Omakase at Hinoki Counter $495/guest ($990); booking through 28 Feb 2027; new releases 1 Dec 2026 11:00 AM EST | https://www.exploretock.com/sushi-sho-nyc/experience/474458/shorter-omakase-at-hinoki-counter |
| Per Se (Tock) | Deposit only: Salon $150/guest, Main Dining Room from $200/guest. No full menu price printed → row stays blank (F18/F24) | https://www.exploretock.com/perse/experience/7768/salon-lounge-seating-four-course-tasting-menu |
| Jungsik | Signature Menu $335/guest ($670 for two) | https://www.jungsik.com/menu/ |
| Gramercy Tavern | Dining Room Seasonal $178/guest ($356); Tavern three-course $78 ($156) | https://www.gramercytavern.com/dining-room-menu/ |
| COTE | Butcher's Feast $84/guest ($168); Steak Omakase $225/guest ($450) | https://www.cotekoreansteakhouse.com/nycdinnermenu |
| Masa | Lunch from $495; Table $750; Hinoki Counter $950 per guest | https://www.masanyc.com/menus |
| Saga | 6-course $215; 10-course $315; Kitchen Table $365 per guest | https://www.saga-nyc.com/menus |
| Kochi | Tasting Menu $145 / Beverage pairing $110 ($290 for two with pairing) | https://www.kochinyc.com/menu/ |
| Torrisi | 1 MICHELIN Star; $$$$; 275 Mulberry St.; Mon 17:00–23:00; Tue–Wed 11:30–14:00; Thu–Sat 11:30–14:00 and 17:00–23:00; Sun closed | https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/torrisi |

## 2. Corrections made

- **Wollman Rink opening time.** The carried value said Fri/Sat/Sun open 10:00. The official
  page says Fri/Sat open 09:00 and Sun 09:00–21:00. Corrected in `research/canonical/activities.json`
  and the published `data/activities.json`.
- **Stale counts**: landing "16 options" tile → 17 suggestions; README flag count 28 → 29.
- **Hotel fields**: `The Fifth Avenue Hotel` address line is still blank (street number not
  captured on the official page); its bed/bath line was added from the official page.

## 3. Hotels: room and bathroom lines verified against each hotel's own official site

| Hotel | Bed | Bathroom | Official URL |
|---|---|---|---|
| The Marlton Hotel | One queen bed per room (Queen Deluxe, Petite Queen, Queen) | Private marble bathrooms | https://marltonhotel.com/ |
| MADE Hotel (44 W 29th St, NoMad) | 1 king (Standard/Studio/Superior/Deluxe/Balcony Deluxe); Double 2 full; Accessible queen | Every room has a private bathroom (FAQ) | https://madehotels.com/rooms/ · https://madehotels.com/faqs/ |
| Soho Grand Hotel (310 W Broadway) | Soho King: king bed | In-room bathroom with walk-in rain shower | https://www.sohogrand.com/accommodations/soho-king/ |
| Arlo SoHo | City Queen: queen bed, 150 sq ft, sleeps 2 | In-room bathroom with glass rain shower | https://arlohotels.com/soho/rooms/city-queen/ |
| The Wall Street Hotel | Pearl Street King: king bed, 290 sq ft | In-room bathroom with heated flooring | https://www.thewallsthotel.com/rooms-and-suites/rooms/pearl-street-king |
| The Fifth Avenue Hotel | Mansion Double Queen: two queen beds (575 sq ft); Mansion Suite: king; Fifth Avenue Suite: king | Bath with separate shower and double vanity (in-suite) | https://www.thefifthavenuehotel.com/accommodations/the-mansion/ |

**Not verified:** The Maritime Hotel. `themaritimehotel.com` homepage was image-only, `/rooms/` and
`/accommodations/` failed, and `www.themaritimehotel.com/rooms-and-suites/` failed. Third-party
pages conflict (queen vs king). It stays blank and flagged (F26).

**Not verified (rates):** no dated official 7-night total was read for these five hotels or for
The Fifth Avenue Hotel, so their price cells stay blank. The 2026-11-25 dated totals are unchanged.

## 4. Not re-read / still open

- The Met's museum hours (Wednesday closure is carried from earlier, not re-read today).
- Per Se and Atera full menu prices (deposit-only Tock pages).
- Torrisi couple price: no official menu price captured.
- Restaurant and activity social-link samples: no new handles were verified today, so none were added.
- The Chinese-language Lunar New Year line still prints 2026 (flag F19; reported to the organiser, not edited).
- EMP bar wording: $255 headline vs "from $225" on the lounge FAQ (both shown; not reconciled).

## 5. Irregularities for review

1. Wollman Rink: the carried 10:00 Fri/Sat/Sun opening was wrong per the official page (corrected above).
2. Eleven Madison Park FAQ: bar tasting listed at $255 on one line and "begins at $225" on another.
3. Chinese-language LNY parade announcement prints 2026 (F19).
4. The Maritime Hotel official site unreadable to the fetcher; the hotel remains excluded from the recommendation until a readable official room page is published.

---

## Local consistency audit — session `arena/7095f8e7-nyfun2` (task T31)

## Scope and important limit

This is a **repository/data consistency check**, not a new round of live source verification. No restaurant, hotel, activity, transit, availability, price, or MICHELIN value was re-quoted or re-read from an external site during this update. The broad verification register remains dated **2026-11-26** (with older carried captures identified separately in `data/verification.json`). A separate session later re-read 12 activity-related rows on 2026-11-27; its official-source evidence and corrections are in [`research/review-2026-11-27.md`](review-2026-11-27.md). After integrating the T28 and T29 official-source work, the current register contains **33 flags**, 46 dated verification records, and bed/bath evidence for 15 of 16 hotels (the local count reconciliation initially saw 29 flags before F30–F33 were merged). Row badges show the date reported for that row; they are not claims that other rows were rechecked.

The existing dated source register remains [`../data/verification.json`](../data/verification.json); its rows retain the official-source URL and the previous session's read/carry status. A machine URL check does not establish that a page remains live or that its content is unchanged.

## Local checks performed

| Check | Result | Method |
|---|---|---|
| Canonical JSON and documented coverage counts | Pass | Recomputed row, price, hours, social, address, hotel-rate and transit counts from `data/*.json`; checked them against `data/verification.json`. |
| Overview counters | Pass | Compared the static fallbacks in `index.html` to the canonical dataset totals. |
| README and page headline counts | Pass | Checked restaurant prices (25), hotels (16 total / 8 with dated rates / 15 with published queen/king + private-bath evidence), activities (18), questions (13), suggestions (17), and flags (33) against their datasets. |
| Relative-date wording | Pass after correction | Searched maintained UI/docs for “checked today”, “re-read today”, and “re-quoted today”; row badges now display explicit per-row dates. |
| Data merge + site generation | Pass | `python3 scripts/build_data.py` completed with 72 restaurants, 16 hotels, 18 activities, 13 questions, 17 suggestions and 33 flags; `python3 scripts/build_site.py` generated the overview and 12 pages from the current JSON inputs. The verification dataset contains 25 base checks plus 21 official-source addendum checks. |
| Structural site verification | Pass | `python3 scripts/verify.py` — 13 HTML pages, 210 data/check rows, 0 errors, 0 warnings (46 verification records, 33 flags). |
| JavaScript syntax | Pass | `node --check assets/app.js`. |
| Whitespace/conflict check | Pass | `git diff --check`; verifier also scans maintained source files for unresolved merge markers. |

## Irregularities found and corrected

At the start of this maintenance pass, public docs were stale against canonical data: README said 24 priced restaurants and 28 flags, the overview showed 16 suggestions rather than 17, badges said “checked today” for prior-day reads, and README described Atomix as blank despite its November Tock price. Those discrepancies were corrected. The current merged build has 25 priced restaurants, 33 flags, 17 suggestions, and 46 verification records (including 21 T29 addendum checks); automated consistency gates check counts against the canonical datasets.

## Not re-verified in this audit

All external facts remain subject to the dated-source caveats already on [`pages/flagged.html`](../pages/flagged.html) and the existing verification log. In particular, stored hotel booking-engine prices, stored Google Maps minutes, current menus, operating hours and future seasonal/event schedules should be re-opened from each row's linked source before a purchase or reservation. No new claim is made that these links or values were live on 2026-11-27.