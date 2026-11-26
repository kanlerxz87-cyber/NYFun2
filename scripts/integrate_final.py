#!/usr/bin/env python3
"""Final-integration merge of the verified parallel-session datasets.

Run from the repo root. Inputs are read-only; this script writes only the
canonical data files owned by the final-integration task (T18). Every merged
value keeps the source URL of the session that captured it; values re-checked
against an official page on 2026-11-26 record that check in their note.

No value is invented: prices are added only where an official menu/booking
page was fetched and read during final verification.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANON = ROOT / "data"
C1 = ROOT / "sessions/c1cf7b23/data"
S6 = ROOT / "sessions/657520df/data"
T11 = ROOT / "sessions/33cfdba4/data"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, doc):
    Path(path).write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def norm(name):
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


# Manual aliases where two sessions used different display names for the same
# venue. Each alias is a name actually printed by one of the source datasets.
ACTIVITY_ALIASES = {
    "statueoflibertynationalmonumentellisisland": "Statue of Liberty National Monument & Ellis Island",
    "statueoflibertyellisislandstatuecitycruises": "Statue of Liberty National Monument & Ellis Island",
    "themetfifthavenue": "The Metropolitan Museum of Art (The Met Fifth Avenue)",
    "metropolitanmuseumofartthemetfifthavenue": "The Metropolitan Museum of Art (The Met Fifth Avenue)",
    "metropolitanmuseumofartfifthavenue": "The Metropolitan Museum of Art (The Met Fifth Avenue)",
    "museumofmodernartmoma": "MoMA (Museum of Modern Art)",
    "themuseumofmodernartmoma": "MoMA (Museum of Modern Art)",
    "americanmuseumofnaturalhistorygildercenter": "American Museum of Natural History",
    "nationalseptember11memorialmuseum": "9/11 Memorial (outdoor) and Museum",
    "911memorialmuseum": "9/11 Memorial (outdoor) and Museum",
    "thehighlineelevatedpark": "The High Line",
    "whitneymuseumofamericanart": "Whitney Museum of American Art",
    "solomonrguggenheimmuseum": "Solomon R. Guggenheim Museum",
    "empirestatebuildingobservatory86th102ndfloors": "Empire State Building Observatory",
    "empirestatebuilding86thfloorobservatory": "Empire State Building Observatory",
    "statenislandferryharborstatueoflibertyskylinecruise": "Staten Island Ferry",
    "statenislandferryfreeharborskylinelibertyviews": "Staten Island Ferry",
    "newyorkpubliclibrarystephenaschwarzmanbuilding": "New York Public Library, Stephen A. Schwarzman Building",
    "newyorkpubliclibrarystephenaschwarzmanbuildingpolonskyexhibition": "New York Public Library, Stephen A. Schwarzman Building",
    "centralparkbethesdaterracebowbridgethemall": "Central Park",
    "topoftherockobservationdeck": "Top of the Rock Observation Deck (Rockefeller Center)",
    "bankofamericawintervillageatbryantparkicerink": "Bank of America Winter Village at Bryant Park (The Rink & The Lodge)",
    "29thchinatownlunarnewyearparadefestivalyearofthegoatsheep": "29th Chinatown Lunar New Year Parade & Festival (2027 Date Confirmed)",
}

RESTAURANT_ALIASES = {
    "cot": "Cote",
    "odoeastvillage": "Odo",
    "chefstableatbrooklynfare": "Chef's Table at Brooklyn Fare",
}


def canonical_key(name, aliases):
    n = norm(name)
    return norm(aliases.get(n, name))


def social_merge(existing, sources, provenance_map):
    """Merge social links by URL; never drop a canonical link."""
    out = []
    seen = set()
    for s in existing or []:
        if s.get("url"):
            seen.add(s["url"].rstrip("/"))
        out.append(s)
    for s in sources or []:
        url = (s.get("url") or "").strip()
        if not url or not url.startswith(("https://", "http://")):
            continue
        key = url.rstrip("/")
        if key in seen:
            # Upgrade provenance when a second session independently found it.
            for prior in out:
                if (prior.get("url") or "").rstrip("/") == key:
                    prior["provenance"] = "cross-confirmed by sessions c1cf7b23 + 657520df"
            continue
        seen.add(key)
        label = s.get("label") or s.get("note") or s.get("platform") or "Link"
        out.append({
            "platform": s.get("platform", "Link"),
            "url": url,
            "note": label,
            "type": s.get("type", "review"),
            "provenance": provenance_map.get(url, "session-verified"),
        })
    return out


def build_social_sources():
    """Return name-keyed social lists and a URL -> provenance lookup."""
    by_name = {}
    url_votes = {}
    for ns, items, field in (
        ("c1cf7b23", load(C1 / "restaurants.json")["items"], "social"),
        ("657520df", load(S6 / "restaurants.json")["items"], "socials"),
        ("c1cf7b23", load(C1 / "activities.json")["items"], "social"),
        ("657520df", load(S6 / "activities.json")["items"], "socials"),
    ):
        for row in items:
            key = canonical_key(row["name"], {**ACTIVITY_ALIASES, **RESTAURANT_ALIASES})
            bucket = by_name.setdefault(key, [])
            for link in row.get(field, []) or []:
                if link.get("url"):
                    url_votes.setdefault(link["url"].rstrip("/"), set()).add(ns)
                    bucket.append(link)
    prov = {
        url: ("cross-confirmed by sessions c1cf7b23 + 657520df" if len(v) > 1
              else "session-verified by " + sorted(v)[0])
        for url, v in url_votes.items()
    }
    return by_name, prov


def add_days(row, other):
    if row.get("daysOpen") or not other:
        return
    days = other.get("daysOpen") or ""
    if days:
        row["daysOpen"] = days


def build_rows_by_name():
    """Name-keyed source rows so opening-day text can be carried across."""
    out = {}
    for path in (C1 / "restaurants.json", S6 / "restaurants.json",
                 C1 / "activities.json", S6 / "activities.json"):
        for row in load(path)["items"]:
            key = canonical_key(row["name"], {**ACTIVITY_ALIASES, **RESTAURANT_ALIASES})
            out.setdefault(key, []).append(row)
    return out


def main():
    restaurants = load(CANON / "restaurants.json")
    activities = load(CANON / "activities.json")
    hotels = load(CANON / "hotels.json")
    decisions = load(CANON / "decisions.json")

    social_by_name, provenance = build_social_sources()
    rows_by_name = build_rows_by_name()

    # ---- Restaurants: social links, opening days, four re-verified prices ----
    verified_prices = {
        "Sushi Sho": {
            "priceTwoAdults": "$990 for two — Shorter Omakase, $495/person prepaid including admin fee",
            "priceNote": "Official Tock experience page, fetched 26 Nov 2026: '$495 per person (including administrative fee)'. Tax, beverages and optional Okonomi extra. The earlier $450 base figure is not printed on the live page; bookings open 1 Dec 2026 at 11:00 ET and currently run through 28 Feb 2027.",
            "priceSourceUrl": "https://www.exploretock.com/sushi-sho-nyc/experience/474458/shorter-omakase-at-hinoki-counter",
        },
        "Saga": {
            "priceTwoAdults": "$430 (6-course, 2 × $215) · $630 (10-course, 2 × $315) · $730 (Kitchen Table, 2 × $365)",
            "priceNote": "saga-nyc.com/menus, fetched 26 Nov 2026; food only, pre-tax/pre-tip/pre-beverage.",
            "priceSourceUrl": "https://www.saga-nyc.com/menus",
        },
        "Aska": {
            "priceTwoAdults": "$750 (12–14 course tasting, 2 × $375)",
            "priceNote": "askanyc.com/dining, fetched 26 Nov 2026; optional wine pairing from $250/person extra.",
            "priceSourceUrl": "https://www.askanyc.com/dining",
        },
        "Daniel": {
            "priceTwoAdults": "$390 (3-course, 2 × $195) · $510 (5-course, 2 × $255)",
            "priceNote": "danielnyc.com/cuisine/prix-fixe, fetched 26 Nov 2026; supplements and wine extra.",
            "priceSourceUrl": "https://www.danielnyc.com/cuisine/prix-fixe",
        },
    }
    for row in restaurants["items"]:
        key = canonical_key(row["name"], RESTAURANT_ALIASES)
        candidates = social_by_name.get(key, [])
        row["social"] = social_merge(row.get("social"), candidates, provenance)
        for other in rows_by_name.get(key, []):
            add_days(row, other)
        if row["name"] in verified_prices and not row.get("priceTwoAdults"):
            row.update(verified_prices[row["name"]])
            row.setdefault("flags", []).append(
                "Price re-verified by final integration on 26 Nov 2026 against the official page linked in priceSourceUrl."
            )
        if row["name"] == "Per Se":
            row.setdefault("flags", []).append(
                "F18: final re-check of the live Tock page shows $150/person deposit for the four-course Salon and $200/person deposit for the Main Dining Room; an earlier session's $185/$590 Salon figures are not confirmed. No menu total is asserted."
            )

    # ---- Activities: days, cross-session socials, six additional verified rows ----
    c1act = load(C1 / "activities.json")["items"]
    for row in activities["items"]:
        key = canonical_key(row["name"], ACTIVITY_ALIASES)
        candidates = social_by_name.get(key, [])
        row["social"] = social_merge(row.get("social"), candidates, provenance)
        for other in rows_by_name.get(key, []):
            add_days(row, other)

    existing_names = {norm(a["name"]) for a in activities["items"]}
    additions = [
        "Top of the Rock Observation Deck (Rockefeller Center)",
        "SUMMIT One Vanderbilt",
        "Bank of America Winter Village at Bryant Park (The Rink & The Lodge)",
        "Wollman Rink in Central Park",
        "Brooklyn Bridge Pedestrian Promenade & DUMBO Waterfront",
        "29th Chinatown Lunar New Year Parade & Festival (2027 Date Confirmed)",
    ]
    overrides = {
        "Top of the Rock Observation Deck (Rockefeller Center)": {
            "costTwoAdults": "From $84 for two (2 × adult 'from $42' on the official timed-admission checkout)",
            "exceptions": "Checkout page redirects from the ticket URL; adult 'from $42' and 'No Hidden Fees' are printed there. Date-specific prices must be re-checked.",
        },
        "SUMMIT One Vanderbilt": {
            "hours": "Daily 08:00–24:00; last entry 22:30 (official FAQ footer, fetched 26 Nov 2026)",
            "daysOpen": "Daily (7 days)",
            "exceptions": "Final re-check contradicts an earlier kit note about winter Tuesday closures; the official footer lists all seven days as 08:00–24:00. All ticket sales final. No adult price is printed on the official page checked, so couple cost stays blank.",
            "costTwoAdults": "",
            "flags": ["No published adult price on the official FAQ page checked; cost left blank (F20)."],
        },
        "Bank of America Winter Village at Bryant Park (The Rink & The Lodge)": {
            "daysOpen": "Daily, 28 Oct 2026 – 28 Feb 2027 ONLY",
            "hours": "Rink daily 08:00–22:00 · Lodge daily 10:00–22:00; 19 Nov–3 Jan until 24:00",
            "exceptions": "Official page fetched 26 Nov 2026: season ends 28 Feb 2027, so a March trip misses it. Holiday Shops end 3 Jan 2027. Rink admission free with own skates; skate hire is paid and date-dependent.",
            "costTwoAdults": "$0 admission for two with own skates; official page lists skate rental $18.72–$64.48/person (2 × = $37.44–$128.96) before tax",
            "flags": [
                "F19: one parallel kit wrote 'through Mar 1, 2027'; the official page says 28 Feb 2027 and that date is used here."
            ],
        },
        "Wollman Rink in Central Park": {
            "daysOpen": "Daily, 28 Oct 2026 – 16 Mar 2027",
            "hours": "Mon–Tue 10:00–14:30 · Wed–Thu & Sun 10:00–21:00 · Fri–Sat 10:00–22:00",
            "exceptions": "Official 2026–27 calendar: 15 Feb 2027 is a Community Day (eligible groups only); 16–21 Feb are Peak days; 22–25 Feb are Off-Peak. All tickets final, no re-entry, waiver required.",
            "costTwoAdults": "$56 Off-Peak / $80 Peak / $104 Prime for two, including $12/person skate rental (2 × $16/$28/$40 admission + 2 × $12)",
        },
        "Brooklyn Bridge Pedestrian Promenade & DUMBO Waterfront": {
            "flags": ["F21: the NYC DOT brochure used by the source session could not be re-fetched during final verification; the free/24-hour values are retained from that session and marked unverified by the final pass."],
        },
        "29th Chinatown Lunar New Year Parade & Festival (2027 Date Confirmed)": {
            "officialUrl": "https://betterchinatown.com/new-york-city-2027-lunar-new-year-parade-dates-announced/",
            "sourceUrl": "https://betterchinatown.com/new-york-city-2027-lunar-new-year-parade-dates-announced/",
            "hours": "Sunday 21 Feb 2027, parade step-off 13:00 (festival booths from 11:30, per source session)",
            "exceptions": "Official page re-fetched 26 Nov 2026. Its Chinese line still prints '2026年2月21日' while the English headline says 'February 21, 2027 | Sunday | 1:00pm'; 21 Feb 2027 is indeed a Sunday. Date-specific: only the 7-night Feb 15–22 option catches it.",
            "flags": ["Official page contains a Chinese-text year typo (2026) beside the correct English 2027 date; see exceptions."],
        },
    }
    for src in c1act:
        if norm(src["name"]) in existing_names or src["name"] not in additions:
            continue
        row = {
            "name": src["name"],
            "category": src["category"],
            "area": src["area"],
            "address": src["address"],
            "daysOpen": src.get("daysOpen", ""),
            "hours": src.get("hours", ""),
            "exceptions": src.get("exceptions", ""),
            "costTwoAdults": src.get("costTwoAdults", ""),
            "officialUrl": (src.get("officialUrl") or src.get("sourceUrl") or "").replace("http://", "https://"),
            "sourceUrl": (src.get("sourceUrl") or "").replace("http://", "https://"),
            "social": social_merge([], src.get("social", []), provenance),
            "flags": list(src.get("flags", [])),
            "integrationNote": "Imported from sessions/c1cf7b23/data/activities.json by final integration (T18); official source linked on this row.",
        }
        row.update(overrides.get(src["name"], {}))
        activities["items"].append(row)

    activities["meta"]["travelTimePolicy"] = (
        "Measured transit legs now exist in the sidebar 'Research & integration' page "
        "(25 hotel→Michelin-cluster legs, all ≤37 min, captured 25 Nov 2026). Each row still "
        "links to a live directions query; re-check on the travel date."
    )
    activities["meta"]["socialPolicy"] = (
        "Social links were merged from two independent session audits. 'cross-confirmed' means "
        "both audits recorded the same URL; all others are labelled with the capturing session. "
        "Review links are third-party; official accounts are labelled (official)."
    )

    # ---- Hotels: verified room/bath facts and the four new qualifying hotels ----
    s6hotels = {norm(h["name"]): h for h in load(S6 / "hotels.json")["items"]}
    hotel_alias = {
        "the beekman a thompson hotel": "The Beekman, a Thompson Hotel (by Hyatt)",
        "11 howard": "11 Howard",
        "hyatt place new york / chelsea": "Hyatt Place New York / Chelsea",
    }
    for h in hotels["items"]:
        other = s6hotels.get(norm(hotel_alias.get(norm(h["name"]), h["name"])))
        if not other:
            continue
        if not h.get("room") and other.get("qualifyingRoom"):
            h["room"] = other["qualifyingRoom"]
            h.setdefault("flags", []).append("Room specification imported from sessions/657520df; official room page linked in roomSourceUrl.")
        if not h.get("privateBathroom") and other.get("privateBathroom"):
            h["privateBathroom"] = other["privateBathroom"]
        if other.get("roomSourceUrl"):
            h["roomSourceUrl"] = other["roomSourceUrl"]
        if other.get("amenities"):
            h["amenities"] = other["amenities"]
        if other.get("michelinWithin60Min"):
            h["michelinWithin60Min"] = other["michelinWithin60Min"]
        if other.get("taxArithmetic") and not h.get("taxBasis"):
            h["taxBasis"] = other["taxArithmetic"]

    new_hotels = ["DoubleTree by Hilton Hotel New York City - Chelsea", "Eurostars Wall Street",
                  "The Frederick Hotel Tribeca", "The Evelyn NoMad"]
    existing_hotels = {norm(h["name"]) for h in hotels["items"]}
    for src in load(S6 / "hotels.json")["items"]:
        if src["name"] not in new_hotels or norm(src["name"]) in existing_hotels:
            continue
        hotels["items"].append({
            "name": src["name"],
            "area": src.get("neighborhood", ""),
            "address": src.get("address", ""),
            "room": src.get("qualifyingRoom", ""),
            "privateBathroom": src.get("privateBathroom", ""),
            "keyStatus": "",
            "guestScore": "",
            "publishedRate": "",
            "sevenNightTotal": src.get("preTax7Night", ""),
            "allInSevenNights": src.get("allIn7Night", ""),
            "taxBasis": src.get("taxArithmetic", ""),
            "cheapestWindow": src.get("cheapestWindow", ""),
            "officialUrl": src.get("officialUrl", ""),
            "sourceUrl": src.get("roomSourceUrl") or src.get("officialUrl"),
            "rateSourceUrl": src.get("rateSourceUrl", ""),
            "roomSourceUrl": src.get("roomSourceUrl", ""),
            "amenities": src.get("amenities", ""),
            "michelinWithin60Min": src.get("michelinWithin60Min", ""),
            "rateCapturedOn": "2026-11-25",
            "flags": list(src.get("flags", [])) + [
                "Imported from sessions/657520df by final integration (T18); dated total is an aggregator snapshot, not a hotel quote."
            ],
        })
    hotels["meta"]["rankingPolicy"] = (
        "Measured door-to-door transit (25 legs, sessions/33cfdba4, captured 25 Nov 2026) puts every "
        "tested Manhattan hotel within 3–37 minutes of all five Michelin clusters, so the ≤1-hour "
        "rule does not separate them. Ranking falls through to verified room/bath compliance and "
        "price; see the Research & integration page for the matrix."
    )
    hotels["meta"]["crossSessionCheck"] = (
        "Four all-in totals were independently captured by two sessions and agree: Hyatt Place "
        "Chelsea $1,305, Arlo NoMad $1,428, 11 Howard $1,774, The Beekman $5,220."
    )

    # ---- Decisions: gaps discovered during final verification ----
    new_flags = [
        {
            "id": "F18", "severity": "Medium", "title": "Per Se Salon price conflict between sessions and live Tock",
            "detail": "A parallel session recorded $185/person for a four-course Salon tasting ($370/couple) and $590 for a five-course version. Final re-check of the live Tock page on 26 Nov 2026 shows $150/person deposit for the four-course Salon and $200/person deposit for the Main Dining Room; neither is a published menu total. Canonical price remains blank.",
            "source": "https://www.exploretock.com/perse/experience/7768/salon-lounge-seating-four-course-tasting-menu",
        },
        {
            "id": "F19", "severity": "Low", "title": "Bryant Park Winter Village season-end discrepancy",
            "detail": "One session wrote 'through late Feb / Mar 1, 2027'; the official page states 28 Feb 2027. The official date is used; March travel misses the rink.",
            "source": "https://bryantpark.org/activities/bank-of-america-winter-village-at-bryant-park",
        },
        {
            "id": "F20", "severity": "Low", "title": "SUMMIT One Vanderbilt opening days changed",
            "detail": "A session noted historical Tuesday winter closures; the official FAQ footer now lists daily 08:00–24:00 with last entry 22:30. The official listing is used and the older note is not repeated as fact.",
            "source": "https://info.summitov.com/",
        },
        {
            "id": "F21", "severity": "Low", "title": "Brooklyn Bridge brochure not re-fetchable in final pass",
            "detail": "The NYC DOT PDF cited by the source session returned a fetch error during final verification. The activity is retained with its original source, but the free/24-hour values are marked unverified by the final pass.",
            "source": "https://www.nyc.gov/html/dot/downloads/pdf/brooklyn_bridge_brochure.pdf",
        },
        {
            "id": "F22", "severity": "Low", "title": "Sushi Sho base price not visible on live Tock page",
            "detail": "A session recorded a $450/person base price alongside $495 prepaid. Final fetch showed only '$495 per person (including administrative fee)', so only the $990/couple prepaid total is used.",
            "source": "https://www.exploretock.com/sushi-sho-nyc/experience/474458/shorter-omakase-at-hinoki-counter",
        },
        {
            "id": "F23", "severity": "Medium", "title": "'Cheapest time to book' is not a forecast",
            "detail": "Five dated weekly snapshots identify the cheapest qualifying week (15–22 Feb 2027), but no official source names a future booking date on which prices will be lowest. The site says so rather than predicting one.",
            "source": "https://www.booking.com/searchresults.html?ss=Manhattan%2C+New+York&checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1&selected_currency=USD&order=price&nflt=class%3D4%3Bclass%3D5",
        },
    ]
    have = {f["id"] for f in decisions["flags"]}
    decisions["flags"].extend(f for f in new_flags if f["id"] not in have)

    # Idempotency: drop any earlier copies before adding (the script may be re-run).
    decisions["questions"] = [q for q in decisions["questions"] if q.get("id") != "Q13"]
    decisions["suggestions"] = [s for s in decisions["suggestions"] if s.get("id") not in ("S13", "S14")]

    decisions["questions"].append({
        "id": "Q13",
        "question": "Which booking week, and is there a future date on which the rate will be lower?",
        "whatWeKnow": "Five dated 7-night snapshots (25 Nov 2026) put the preferred 15–22 Feb 2027 week lowest among qualifying queen/king rooms: $848 pre-tax / $998 all-in at Eurostars Wall Street. The 22 Feb–1 Mar snapshot is $12 cheaper but its cheapest room has twin beds and fails the brief.",
        "whatWeDoNotKnow": "No official source forecasts the lowest future booking date. Rates and the Black Friday promotion can change.",
        "provisionalAnswer": "Treat 15–22 Feb 2027 as the cheapest verified qualifying week so far; hold a cancellable rate and re-run the saved searches weekly. No 'best future booking date' is asserted (F23).",
        "blocking": False,
        "howToDiscover": "Save the five exact Booking.com URLs, re-run weekly, and log date, total, room type and cancellation terms. Compare with the hotel's own booking engine when its 2027 window opens.",
        "sources": [
            "https://www.booking.com/searchresults.html?ss=Manhattan%2C+New+York&checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1&selected_currency=USD&order=price&nflt=class%3D4%3Bclass%3D5",
            "https://www.booking.com/searchresults.html?ss=Manhattan%2C+New+York&checkin=2027-02-22&checkout=2027-03-01&group_adults=2&no_rooms=1&selected_currency=USD&order=price&nflt=class%3D4%3Bclass%3D5",
        ],
    })

    decisions["suggestions"].extend([
        {
            "id": "S13", "title": "Adopt one canonical dataset and keep the parallel kits as evidence",
            "detail": "Copy only rows whose source URL was re-read into the canonical tables; leave the other sessions' directories untouched. This drops conflicting duplicates without discarding their evidence.",
            "effort": "Medium", "blockedBy": [], "status": "Implemented by T18 for prices, room facts, social links and six activities; the rest remains read-only.",
        },
        {
            "id": "S14", "title": "Put the six date-critical activities in the day plan",
            "detail": "The parade is one day only (21 Feb 2027), Bryant Park ends 28 Feb, Wollman runs to 16 Mar and SUMMIT/Top of the Rock have date-specific hours. Rebuild the itinerary around these cutoffs once the trip length is fixed.",
            "effort": "Low", "blockedBy": ["Q1"], "status": "Proposed — rows are on the Activities page; itinerary sequencing not yet changed.",
        },
    ])

    save(CANON / "restaurants.json", restaurants)
    save(CANON / "activities.json", activities)
    save(CANON / "hotels.json", hotels)
    save(CANON / "decisions.json", decisions)

    # ---- Cross-session findings page data ----
    transit = load(T11 / "transit_anchors.json")
    pricing = load(T11 / "pricing_windows.json")
    c1hotels = load(C1 / "hotels.json")
    integration = {
        "meta": {
            "checkedOn": "2026-11-26 (final integration re-read of the official pages listed in the flags)",
            "provenance": "Merged read-only from sessions/33cfdba4 (transit + weekly prices) and sessions/c1cf7b23 + sessions/657520df (hotel ranks, room facts, social links). No file inside sessions/ was edited.",
            "transitMethod": transit["method"],
            "fareNote": transit["fare_note"],
            "priceMethod": pricing["method"],
            "bookingCaution": pricing["time_to_book"],
            "activityTransitCaveat": "Only 4 of the 10 activity legs in the source session carried both minutes and a routing URL. The other 6 were notes without a captured route and are not presented as measured values.",
        },
        "bookingWindows": [
            {
                "id": w["label"],
                "dates": f"{w['checkin']} → {w['checkout']}",
                "nights": w["nights"],
                "hotel": w["cheapest_hotel"],
                "room": w["cheapest_room"],
                "preTax": f"${w['total_usd']:,}",
                "allIn": (next((b.get("estimatedAllInUsd", "") for b in c1hotels["bookingWindows"]
                                if b["windowId"] == w["label"]), "")),
                "qualifies": "No — twin beds" if w["label"] == "W2" else "Yes — queen/king room",
                "captured": w.get("retrieved") or w.get("bronze") or "",
                "note": w.get("note", "Cheapest qualifying room in that snapshot; aggregator total, pre-tax."),
                "sourceUrl": w["source"],
            }
            for w in pricing["windows"]
        ],
        "transit": [
            {
                "id": f"T{i:02d}",
                "hotel": transit["hotel_origins"].get(m["hotel"], m["hotel"]),
                "cluster": next((a["label"] for a in transit["anchors"] if a["id"] == m["anchor"]), m["anchor"]),
                "destination": next((a["destination"] for a in transit["anchors"] if a["id"] == m["anchor"]), ""),
                "minutes": str(m["minutes"]),
                "route": ", ".join(m.get("lines") or []),
                "verified": "Captured 25 Nov 2026" if m.get("verified") == "v" else "Unverified",
                "sourceUrl": m["source"],
            }
            for i, m in enumerate(transit["matrix"], 1)
        ],
        "activitiesTransit": [
            {
                "id": f"A{i:02d}",
                "hotel": transit["hotel_origins"].get(m["hotel"], m["hotel"]),
                "activity": m["activity"],
                "minutes": str(m["minutes"]),
                "route": ", ".join(m.get("lines") or []),
                "sourceUrl": m["source"],
            }
            for i, m in enumerate([x for x in transit["activity_legs"] if x.get("source") and x.get("minutes")], 1)
        ],
        "hotelRanking": [
            {
                "id": f"R{h['rank']:02d}",
                "rank": str(h["rank"]),
                "hotel": h["name"],
                "room": h.get("qualifyingRoom", ""),
                "bath": h.get("privateBathroom", ""),
                "michelinReach": h.get("michelinWithin60Min", ""),
                "breakdown": h.get("clusterTransitBreakdown", ""),
                "preTax": h.get("sevenNightPreTax", ""),
                "allIn": h.get("sevenNightAllIn", ""),
                "sourceUrl": h.get("sourceUrl") or h.get("officialUrl") or "",
                "rateSourceUrl": h.get("rateSourceUrl", ""),
            }
            for h in sorted(c1hotels["items"], key=lambda x: x["rank"])
        ],
        "findings": [
            {"id": "I1", "topic": "Transit rule", "finding": "All 25 measured hotel→Michelin-cluster legs are ≤37 minutes; the one-hour rule does not separate the tested hotels.", "sourceUrl": "https://www.google.com/maps/dir/?api=1&origin=Eurostars+Wall+Street+New+York&destination=Crown+Shy+New+York&travelmode=transit"},
            {"id": "I2", "topic": "Fastest leg", "finding": "Eurostars Wall Street → Crown Shy is a 3-minute walk; The Frederick → Jungsik is 5 minutes.", "sourceUrl": "https://www.google.com/maps/dir/?api=1&origin=Eurostars+Wall+Street+New+York&destination=Crown+Shy+New+York&travelmode=transit"},
            {"id": "I3", "topic": "Cheapest qualifying week", "finding": "15–22 Feb 2027: $848 pre-tax / ~$998 all-in for a Queen Room at Eurostars Wall Street. The $836 22 Feb–1 Mar option is a twin room and fails the brief.", "sourceUrl": pricing["windows"][0]["source"]},
            {"id": "I4", "topic": "Booking timing", "finding": "No official source names a future date when rates will be lowest. Hold a cancellable rate and re-run saved searches weekly (F23).", "sourceUrl": pricing["windows"][1]["source"]},
            {"id": "I5", "topic": "Cross-session price agreement", "finding": "Four all-in totals were captured independently and agree: Hyatt Place $1,305 · Arlo NoMad $1,428 · 11 Howard $1,774 · Beekman $5,220.", "sourceUrl": "https://www.booking.com/hotel/us/hyatt-place-new-york-chelsea.en-us.html?checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1"},
        ],
    }
    save(CANON / "integration.json", integration)

    print("Integration complete:",
          len(restaurants["items"]), "restaurants,",
          len(activities["items"]), "activities,",
          len(hotels["items"]), "hotels,",
          len(integration["transit"]), "transit legs,",
          len(integration["bookingWindows"]), "booking windows.")


if __name__ == "__main__":
    main()
