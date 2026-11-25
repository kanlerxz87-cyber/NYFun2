# T10 — Michelin restaurant price verification (session arena/fc6d5f66-nyfun2)

Checked **2026-11-25** against official restaurant websites, official menu PDFs, and the
restaurants' own booking channels (Tock / Resy / OpenTable). All amounts are **USD, food
only, for 2 adults**, before tax, tip and beverages unless a row says otherwise.
`priceTwoAdults = 2 × a per-person price printed on an official page`. Menus were captured
**Nov 2026**; the trip is **Feb–Mar 2027**, so every figure must be re-confirmed at booking.
Michelin's `$`–`$$$$` band is a separate, non-dollar indicator (`guidePriceBand`).

## Verified couple totals (official source printed the per-person price)

| Restaurant | Stars | Menu | Per person | Couple total | Official source | Captured |
|---|---|---|---|---|---|---|
| Eleven Madison Park | 3★ | Full Tasting | $385 | **$770** | elevenmadisonpark.com/faq | 2026-11-25 |
| Eleven Madison Park | 3★ | Bar Tasting | $255 | **$510** | elevenmadisonpark.com/faq | 2026-11-25 |
| Le Bernardin | 3★ | Chef's Tasting | $350 | **$700** | le-bernardin.com/accessible/menus/dining-room/chef-s-tasting/ | 2026-11-25 |
| Le Bernardin | 3★ | Dinner prix fixe (4-course) | $218 | **$436** | le-bernardin.com/content/pdfs/dinner-1.2.pdf | 2026-11-25 |
| Le Bernardin | 3★ | Lunch prix fixe (3-course) | $142 | **$284** | le-bernardin.com/accessible/menus/lunch/ | 2026-11-25 |
| Jungsik New York | 3★ | Signature Menu | $335 | **$670** | jungsik.com/menu/ | 2026-11-25 |
| Masa | 2★ | Lunch Omakase (from) | $495 | **$990** | masanyc.com/menus | 2026-11-25 |
| Masa | 2★ | Table Omakase | $750 | **$1,500** | masanyc.com/menus | 2026-11-25 |
| Masa | 2★ | Hinoki Counter | $950 | **$1,900** | masanyc.com/menus | 2026-11-25 |
| Gabriel Kreuther | 2★ | Chef's Tasting | $325 | **$650** | RGK_DinnerMenu 11.17.26.pdf (gknyc.com/menus) | 2026-11-25 |
| Gabriel Kreuther | 2★ | 3-course | $200 | **$400** | RGK_DinnerMenu 11.17.26.pdf | 2026-11-25 |
| Gabriel Kreuther | 2★ | 4-course | $235 | **$470** | RGK_DinnerMenu 11.17.26.pdf | 2026-11-25 |
| The Modern | 2★ | Lunch prix fixe (3-course) | $115 | **$230** | themodernnyc.com/the-modern/ | 2026-11-25 |
| The Modern | 2★ | Lunch Tasting | $255 | **$510** | themodernnyc.com/the-modern/ | 2026-11-25 |
| The Modern | 2★ | Impressions (dinner) | $185 | **$370** | themodernnyc.com/the-modern/ | 2026-11-25 |
| The Modern | 2★ | Abstractions (dinner) | $285 | **$570** | themodernnyc.com/the-modern/ | 2026-11-25 |
| The Modern | 2★ | Kitchen Table | $345 | **$690** | themodernnyc.com/the-modern/ | 2026-11-25 |
| Chef's Table at Brooklyn Fare | 2★ | Tasting | $385 | **$770** | brooklynfare.com/chefs-table/ | 2026-11-25 |
| Cote | 1★ | Butcher's Feast | $84 | **$168** | cotekoreansteakhouse.com/nycdinnermenu | 2026-11-25 |
| Cote | 1★ | Steak Omakase | $225 | **$450** | cotekoreansteakhouse.com/nycdinnermenu | 2026-11-25 |
| Kochi | 1★ | Tasting (8-course) | $145 | **$290** | kochinyc.com/menu/ | 2026-11-25 |
| Mari | 1★ | Tasting | $145 | **$290** | marinyc.com/ | 2026-11-25 |
| Jua | 1★ | Seven-course tasting | $150 | **$300** | juanyc.com/menu | 2026-11-25 |
| Gramercy Tavern | 1★ | Dining Room Seasonal Menu | $178 | **$356** | gramercytavern.com/dining-room-menu/ | 2026-11-25 |
| Gramercy Tavern | 1★ | Tavern 3-course (à la carte) | $78 | **$156** | gramercytavern.com/dining-room-menu/ | 2026-11-25 |
| Aquavit | 2★ | Dinner tasting | $195 | **$390** | aquavit.org/s/DR-112026.pdf (DR 11.20.26) | 2026-11-25 |
| odo | 2★ | Lunch Kaiseki (6-course) | $150 | **$300** | odo.nyc/menu | 2026-11-25 |
| odo | 2★ | Dinner Kaiseki (8–9 course) | $270 | **$540** | odo.nyc/menu | 2026-11-25 |
| Le Coucou | 1★ | A Very Coucou Dinner | $220 | **$440** | lecoucou.com/#menus | 2026-11-25 |

**Reconciliation with session `arena/6f217cce-nyfun2` (PR #13, merged to main):** that session
independently captured Aquavit ($390), odo ($300/$540) and Le Coucou ($440), which this session had
left blank; those official sources were re-opened and re-verified here on 2026-11-25 and adopted.
It also read Le Bernardin's dinner prix fixe as **$218** from the official PDF `dinner-1.2.pdf`;
this session's earlier accessible-page capture of $225 was superseded by the PDF ($436 for two).
All other overlapping totals (EMP, Jungsik, Gabriel Kreuther, The Modern, Masa, Gramercy Tavern)
agree between the two sessions. No verified figure from either session was discarded.

### Wine / beverage pairings (per person, official pages)
EMP from $125 · Le Bernardin $180 (tasting $530 w/ pairing) · Gabriel Kreuther Classic $255 /
Reserve $595 · The Modern $85 / $135 / $295 · Jungsik $145–$600 · Cote $110 · Kochi $110 ·
Mari $110 · Jua $85–$215 · Chef's Table BF NA pairing $215 · Gramercy Tavern $118.

### Notable policies captured (official)
- **EMP**: gratuity not included; all sales final/non-refundable; reservations open the 1st of
  each month for the following month (Feb 2027 ⇒ ~Jan 1 2027); corkage $75, max 4 bottles.
- **Masa**: gratuity never required (pooled); corkage $300/bottle, max 2; ~2 hours.
- **Chef's Table BF**: $200 deposit; seafood-focused; cannot accommodate vegan/vegetarian/
  celiac/kosher/no-seafood or soy/mushroom/lemon/lime allergies; corkage $175.
- **Per Se**: business casual dress code; corkage $200/bottle (max 3); bookings released the
  1st of each month for the following month (official Tock FAQ).
- **Kochi**: cannot accommodate vegan/celiac or allium/sesame/soy/gluten/alcohol allergies.

## Indicative Guide estimate (NOT a menu quote) — exact couple total left blank
MICHELIN's own best-of list "The Least Expensive MICHELIN-Starred Restaurants in New York"
(updated 27 Jul 2026) groups **Casa Mono, Crown Shy, Jeju Noodle Bar, Semma, Tuome** at
**roughly $75 per person (~$150 for two)**. This is an indicative Guide estimate, not a
published menu price, so `priceTwoAdults` stays blank and the estimate is recorded in
`priceNote` with the source. All five are à la carte.
Source: guide.michelin.com/en/best-of/least-expensive-one-michelin-star-restaurants-in-new-york

## Left blank + flagged (no official price confirmed this session)
- **Per Se (3★)** — official Tock/Thomas Keller pages print only the **$200/person deposit**
  (Main Dining Room) and $150/person deposit (Salon), not the menu price. A **$425** figure
  appears only in a search snippet and is **not used**. Confirm by phone / at booking.
- **Sushi Sho (3★)** — no official website listed by Michelin (phone only); no price published.
- **Atera, Atomix, Jean-Georges, César, Joo Ok, Saga, Sushi Noz (2★)** — official menu price not
  reachable/published. Atera's own page content conflicts ($325 visible menu text vs $298 embedded
  structured data, per session 6f217cce; third-party reports also vary $195/$235/$298) and Atomix
  third-party reports conflict ($295/$375); none were used.
- **Dirt Candy, Sushi Nakazawa, Sixty Three Clinton, and most other 1★** — à la carte or menu
  not reachable; no fixed couple total published.

## Method / irregularities
- Only official restaurant pages, official menu PDFs, or the restaurant's own booking channel
  were accepted as price sources. Third-party blogs (TableTurn, myreservetable, kevinEats,
  Tripadvisor) were rejected; their conflicting Atomix/Atera figures are flagged, not used.
- Image-only / client-rendered official pages (Atomix, Aquavit menu, Sushi Nakazawa, Dirt Candy,
  Jua homepage) yielded no text price; the reachable subpage (e.g. juanyc.com/menu) was used.
- **Capture-date risk:** all menus are Nov 2026; the Feb–Mar 2027 trip may see price changes.
- **Ceremony risk:** Michelin's 14 Dec 2026 Northeast Cities ceremony may change distinctions.

### Cote hours cross-check (resolved)
The Cote homepage search snippet showed a stale "Mon–Sat 5PM–2AM, closed Sundays" block, but the
official Flatiron location-page FAQ (cotekoreansteakhouse.com/locations/cotenycflatiron) states
"open for dinner service 7 days a week ... 5:00-11:00 PM Sunday to Wednesday, and 5:00-12:00 AM
Thursday to Saturday" — which agrees with the MICHELIN detail page. The location-page FAQ is used.
Also captured: $50/person late-cancellation/no-show fee within 24h; reservations for 2–6 via Resy.
