# Michelin restaurant menu-price capture

**Checked:** 2026-11-25  
**Scope:** the restaurant rows in `data/restaurants.json` (18 starred rows plus three Guide-listed/no-star rows).  
**Important:** these are current published menu snapshots, not February 2027 quotations. Restaurants may change menus and prices before the trip. A blank means this check did not establish a defensible couple total from an official source.

## Method and price semantics

- A displayed total for two is arithmetic from a venue-published per-person menu price (`2 × per-person price`) or a published table price. The per-person source amounts and arithmetic are stated below.
- These are **menu subtotals**, not guaranteed final bills. Taxes, gratuity, beverages, supplements, booking deposits, or administrative charges are included/excluded only where the linked source says so. No tax, tip, or beverage allowance has been estimated.
- For à-la-carte restaurants, no meal total is inferred from a guessed number of dishes or portions.
- MICHELIN's `$` price band is not a menu price and was not converted to dollars.
- `priceSources` and `priceCheckedOn` in each row identify the evidence and capture date. Table values with no authoritative published couple basis remain blank and carry a flag.

## Row-by-row evidence

| Restaurant | Menu total for two (USD) | Basis and review note | Primary price / review source |
|---|---:|---|---|
| Eleven Madison Park | $510–$770 | Official FAQ lists Bar Tasting at $255/guest and Full Tasting at $385/guest; `2 ×` each. The FAQ says gratuity is not included; wine pairings are extra. | [Official FAQ](https://www.elevenmadisonpark.com/faq) |
| Jungsik New York | $670 | Official menu lists the Signature Menu at $335; `2 × $335`. The menu asks for full-table participation; supplements and beverage pairings are separate choices. | [Official menu](https://www.jungsik.com/menu/) |
| Le Bernardin | $274 lunch / $436 dinner | Official lunch PDF lists the three-course prix fixe at $137/guest; dinner PDF lists the four-course prix fixe at $218/guest. Each total is `2 ×` the published per-person price; supplements may apply. | [Official lunch menu PDF](https://www.le-bernardin.com/content/pdfs/lunch-2.191.pdf) · [official dinner menu PDF](https://www.le-bernardin.com/content/pdfs/dinner-1.2.pdf) |
| Per Se | $370–$850 | Official Tock venue pages publish the Salon four-course menu at $185/guest and Main Dining Room tasting menus at $425/guest; `2 ×` each. Tock says the $200/guest booking deposit is applied to the bill. The February 2027 menu is not yet a date-specific quote. | [Main Dining Room on Tock](https://www.exploretock.com/perse/experience/288603/main-dining-room-tasting-menu) · [Salon on Tock](https://www.exploretock.com/perse/experience/7768/salon-lounge-seating-four-course-tasting-menu) |
| Sushi Sho |  | No NYC couple price confirmed. The Tock page that publishes $400/guest is explicitly for Sushi Sho at 383 Kalaimoku Street, Honolulu, Hawaii; it was not transferred to the New York restaurant. | [NYC MICHELIN listing](https://guide.michelin.com/en/new-york-state/new-york/restaurant/sushi-sho-1213976) · [Honolulu Tock page (wrong location for this row)](https://www.exploretock.com/sushisho/) |
| Aquavit | $160–$610 | Official menus dated 20 Nov 2026 list lunch two-course $80/guest, three-course $95/guest, lunch tasting $185/guest, dinner tasting $195/guest and Chef's Tasting $305/guest; `2 ×` each. Beverage pairings and listed supplements are extra. | [Official lunch PDF](https://www.aquavit.org/s/DR-Lunch-112026.pdf) · [dinner tasting PDF](https://www.aquavit.org/s/DR-112026.pdf) · [Chef's Tasting PDF](https://www.aquavit.org/s/DR-112026-Chefs.pdf) |
| Atomix | $704–$990 | The latest regular bookable menus found were for December 2026: Bar Tasting starts at $352/guest and Chef's Counter is $495/guest; `2 ×` each. Tock states the price includes its administrative fee. The February 2027 menu price was not posted in this capture. Holiday event prices are excluded. | [Official Tock Chef's Counter, Dec 2026](https://www.exploretock.com/atomixnyc/experience/629195/chefs-counter-december-2026) · [official Tock Bar Tasting, Dec 2026](https://www.exploretock.com/atomixnyc/experience/629197/bar-tasting-menu-december-2026) |
| Gabriel Kreuther | $150–$650 | Current official PDFs dated 17 Nov 2026 list lunch two-course $75, three-course $95 and Le Grand Dégustation $155/guest; dinner three-course $200, four-course $235 and Chef's Tasting $325/guest. Totals are `2 ×` those amounts; beverage pairings are separate. | [Official lunch PDF](https://cdn.prod.website-files.com/69f8cb7ff67007b4842004ce/6afddf473ff2ad124ea3845e_RGK_FallLunch%20Menu%2011.17.26%20Wine.pdf) · [official dinner PDF](https://cdn.prod.website-files.com/69f8cb7ff67007b4842004ce/6afddf36f7cde3e50d030e4c_RGK_DinnerMenu%2011.17.26.pdf) |
| The Modern | $230–$570 | Official standard menus list lunch three-course prix fixe $115/guest, lunch tasting $255/guest, dinner Impressions $185/guest and dinner Abstractions $285/guest; `2 ×` each. These menus are seasonal. Special-event menus are not included. | [Official menus](https://www.themodernnyc.com/the-modern/) |
| Masa | $990 lunch starting price / $1,500 table / $1,900 Hinoki Counter | Official menus say lunch starts at $495/guest, table omakase is $750/guest and Hinoki Counter is $950/guest; `2 ×` each. The page explicitly excludes beverages, tax and optional gratuity. | [Official menus](https://www.masanyc.com/menus) |
| odo | $300 lunch / $540 dinner | Official menu lists lunch Kaiseki at $150/guest and dinner Kaiseki at $270/guest; `2 ×` each. This is the starred `odo` row, not the separate Guide-listed `Odo East Village` row. | [Official menu](https://www.odo.nyc/menu) |
| Sushi Noz | $990 | Official Tock venue listing publishes its omakase at $495/guest; `2 × $495`. The February 2027 rate was not posted in this capture. | [Official Tock omakase booking](https://www.exploretock.com/sushinoz/experience/335003/omakase) |
| César |  | The official site describes a tasting menu but no full menu amount was confirmed. The official booking page shows a $200/guest deposit, not the menu price, so the deposit was not treated as the couple's meal cost. | [Official restaurant](https://www.cesar.restaurant/) · [official Tock venue page](https://www.exploretock.com/cesarrestaurant) |
| Le Coucou | $162–$440 | Official standard menus list lunch at $81 for two courses, $125 for three courses or $150 for A Very Coucou Lunch, and dinner at $220/guest; totals are `2 ×` each. The page says tax and gratuity are not included. Event menus are excluded. | [Official menus](https://lecoucou.com/) |
| Gramercy Tavern | $356 | Official Dining Room seasonal menu lists $178/guest; `2 × $178`. The optional wine pairing is $118/guest and is not included in the food subtotal. | [Official Dining Room menu](https://www.gramercytavern.com/menu/the-dining-room/) |
| Casa Mono |  | The official menu checked is à la carte and did not publish a fixed couple total; no number or portion size was assumed. | [Official menu](https://www.casamononyc.com/menus/) |
| Semma |  | The official menu lists à-la-carte dishes, but no fixed two-person menu or meal total. The total depends on choices and quantities, so it remains blank. | [Official menu](https://www.semma.nyc/) |
| Odo East Village |  | Kept separate from `odo`. No official menu page was tied to this Guide-listed entry in the price check. | [Official MICHELIN July 2026 additions](https://guide.michelin.com/en/article/travel/new-restaurants-new-york) |
| Cynthia |  | Guide-listed/no-star row; no official menu source with a couple total confirmed in this task. | [Official MICHELIN July 2026 additions](https://guide.michelin.com/en/article/travel/new-restaurants-new-york) |
| Len Len |  | Guide-listed/no-star row; no official menu source with a couple total confirmed in this task. | [Official MICHELIN July 2026 additions](https://guide.michelin.com/en/article/travel/new-restaurants-new-york) |
| Atera |  | Withheld due to a conflict inside the official site's extracted price data: visible page text shows $325/guest while its structured menu metadata reports $298. Tock pages checked exposed deposits or older booking periods, not a reconciled February 2027 total. | [Official Atera site](https://ateranyc.com/) · [official Tock venue](https://www.exploretock.com/atera/) |

## Verification performed

- Opened the official menu, official venue site, or venue-linked reservation page for each nonblank price; the direct source URL is stored with that restaurant row.
- Checked every multiplication against the displayed per-person figure and party size of two.
- Kept menu subtotals separate from MICHELIN's price band and from the hotel's/restaurant's booking deposit.
- Kept the NYC Sushi Sho price blank after identifying the $400/guest Tock result as the Honolulu venue, not the New York venue.
- Kept Atera blank because its official page extraction conflicts ($325 visible text versus $298 structured data); recorded the conflict rather than selecting one.
- Kept Per Se, Atomix and Sushi Noz price notes explicitly non-date-specific: the captured menu/booking price is not a promise for February 2027.
- Re-validated `data/restaurants.json` with `python3 -m json.tool`; the general repository verifier is run again after the site's price-source display is integrated.
