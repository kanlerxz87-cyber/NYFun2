# Activities verification (T13) — 2026-11-25

Line-by-line verification of `data/activities.json` (12 rows). Sources are official venue or platform pages; every new link is sourced.

## Method
- Hours/exceptions transcribed from the venue's official pages (links in `data/activities.json` `sourceUrl`).
- New social links added below are official accounts confirmed on the venue's own website or a platform-linked page.

## Verified rows (social enrichment)

| Row | Added official links | Source page |
|---|---|---|
| Statue of Liberty + Ellis Island | Facebook `StatueLibrtyNPS` (https://www.facebook.com/StatueLibrtyNPS), X `StatueEllisNPS` (https://twitter.com/StatueEllisNPS), Instagram `StatueEllisNPS` (https://www.instagram.com/StatueEllisNPS) | nps.gov/stli/faqs.htm (FAQ: "Does the Statue of Liberty have a Facebook page? Yes! ... @StatueEllisNPS") |
| Empire State Building Observatory | YouTube `https://www.youtube.com/@theempirestatebldg` | esbnyc.com structured-data ("The official YouTube channel for the World's Most Famous Building", @theempirestatebldg) |
| New York Public Library, Stephen A. Schwarzman Building | Instagram `https://www.instagram.com/nypl/`, Facebook `https://www.facebook.com/nypl/`, YouTube playlist `https://www.youtube.com/playlist?list=PLL6gs3aZKBap8fArHk2EdhwoEPZoWKPAt` | NYPL press release (Insta Novels, nypl.org/press) for IG; NYPL events General Information listing (web.nypl.org/events/live-nypl/about) for FB/YT |
| MoMA (Museum of Modern Art) | Instagram `https://www.instagram.com/themuseumofmodernart/`, Facebook `https://www.facebook.com/MuseumofModernArt` | moma.org/about/about-this-site (Privacy Policy lists both accounts) |

## Flags kept as-is (verified gaps, blank per policy)
- ESB February 2027 hours not published — hours blank, flag "February 2027 hours not published; hours left blank".
- ESB ticket prices unconfirmed — flag kept.
- Other rows: confirm on the day; park hours can change seasonally (Central Park flag).

## Irregularities
- NYPL page versions differ (press release + legacy admin blog); I kept only the URLs on the official Schroedman page / NYPL pages that cite them.
