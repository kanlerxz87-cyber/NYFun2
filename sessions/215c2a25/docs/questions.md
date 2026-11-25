# Questions, information and answers to address before a decision

Each item states what is known, what is missing, and the concrete way to discover the missing information. Nothing below is filled with an estimate.

## A. Dates and trip length

| # | Question | Known from sources | Missing | How to discover |
|---|---|---|---|---|
| A1 | Which exact dates should be booked? | 15 Feb 2027 is Presidents' Day; user preference 15–18 Feb; window runs to 23 Mar 2027. | Whether the couple prefers a long weekend (3 nights), 7 nights, 14 nights or 28 nights. | Choose one of the dated options on the Itinerary page. No booking until chosen. |
| A2 | Do holidays affect opening hours? | NYC holiday list confirms 15 Feb 2027; NPS says Liberty/Ellis closed Thanksgiving and Christmas only. | 2027 Presidents' Day hours for restaurants/museums not published. | Check each official page again in Dec 2026/Jan 2027. |
| A3 | Is the Michelin list stable for the trip? | Guide pages currently reflect 2025 stars; 2026 ceremony is 14 Dec 2026. | Post-ceremony 2026 star list. | Re-fetch the three MICHELIN filter pages after 14 Dec 2026. |

## B. Hotels and money

| # | Question | Known from sources | Missing | How to discover |
|---|---|---|---|---|
| B1 | What is the total price for 7 nights? | Official room types/bed/bath descriptions for 5 hotels; one undated lead rate ($340/night, The Standard). | Dated, refundable 2-adult rate for 15–22 Feb 2027 and all-in total incl. taxes/fees. | Run each hotel's own booking engine with exact dates; capture confirmation screenshot/URL; repeat for alternative date windows. |
| B2 | Which dates are cheapest? | Not determinable — dated rates were not returned. | A dated price series across candidate windows. | Query official booking engines for each window and record results in a new dated-rate table. |
| B3 | Does the room truly have a private bathroom and queen+ bed? | Official pages describe queen/XL-king beds and in-room showers/baths. | Explicit 'private bathroom' statement for most rooms; Fifth Avenue Hotel room details. | Request written confirmation from hotel or inspect the official room page's amenities field. |
| B4 | How many Michelin restaurants are within 1 hour by subway/bus? | Official addresses exist for all 18 restaurants and 6 hotels; MTA map is official. | Door-to-door travel times for each hotel/restaurant pair at the chosen dates/times. | Use an authorised transit-routing API (e.g., MTA/GTFS-based) with departure-time assumptions; publish the method and raw results. |
| B5 | Are there hidden costs? | Not captured. | Resort/destination fees, parking, cancellations, taxes. | Read the rate rules on each official booking page before booking. |

## C. Restaurants and dining cost

| # | Question | Known from sources | Missing | How to discover |
|---|---|---|---|---|
| C1 | What will dinner for two cost? | MICHELIN price bands ($$$ / $$$$) for every listed restaurant. A few third-party videos mention menu prices, but those are not official. | Official current menu/tasting-menu prices and mandatory charges. | Fetch each restaurant's own menu page in Dec 2026; record price per person and service/tax treatment. |
| C2 | Which nights are they open? | Days/hours transcribed from MICHELIN pages, with partial coverage flagged per row. | Complete 7-day hours and holiday exceptions for several rows. | Check the official restaurant site or call; update the row. |
| C3 | Which restaurants are actually starred? | Explicit on each Guide page; 2 entries are Guide-listed without a star. | Whether 2026 ceremony changes status. | Re-check after 14 Dec 2026 (official Guide). |
| C4 | Are reservations available? | The Guide offers booking links for some restaurants. | Real availability for the chosen dates. | Check the official booking partner at the time of booking. |

## D. Activities and social reviews

| # | Question | Known from sources | Missing | How to discover |
|---|---|---|---|---|
| D1 | What are the exact February 2027 hours? | Official current hours for 11 activities; High Line publishes a Dec–Mar season. | 2027 holiday/seasonal changes and Broadway titles/times. | Re-fetch official pages within 60 days of travel. |
| D2 | Are the social links genuine reviews? | Links point to YouTube/TikTok pages returned by search with review-style titles/descriptions. | Independent verification of each creator's relationship with the venue (some may be sponsored). | Open each link and check disclosure; treat as opinion, not official information. |
| D3 | Are there social review links for every row? | No — several rows are blank and flagged. | Additional YouTube/TikTok/Instagram reviews. | Search each venue name plus "review" on-platform and record direct URLs. |

## Decision gate

A booking decision is defensible only when A1, B1, B3, B4, C1 and D1 have answers from official sources. Until then the site is a research dashboard, not a booking recommendation.
