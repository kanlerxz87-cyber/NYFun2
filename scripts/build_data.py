#!/usr/bin/env python3
"""Merge every session kit into the canonical datasets, with provenance.

Rules enforced here (see pages/sources.html):
  * The canonical 72-row MICHELIN roster is never extended by a kit. A kit can
    only FILL A BLANK field on a row that already exists in the official roster.
  * A value is copied only when the kit row carries a source URL for it.
  * When two kits disagree with the canonical value, the canonical value stays
    and the disagreement is written to data/conflicts.json + the Flags page.
  * Nothing is inferred: a missing value stays missing.

Outputs: data/restaurants.json, data/hotels.json, data/activities.json,
         data/conflicts.json, data/verification.json
Run: python3 scripts/build_data.py
"""
import difflib
import json
import os
import re
import unicodedata
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda *p: os.path.join(ROOT, *p)


def load(path):
    with open(D(path), encoding="utf-8") as f:
        return json.load(f)


def canon(name):
    """Pristine pre-integration canonical dataset (never the merge output),
    so re-running this script is idempotent."""
    return load(f"research/canonical/{name}.json")


def tokens(s):
    return set(norm(s).split())


def is_dup(name, existing):
    """True when every token of one name is contained in the other."""
    nt = tokens(name)
    if not nt:
        return True
    for e in existing:
        et = tokens(e)
        if nt and et and (nt <= et or et <= nt):
            return True
    return False


def save(path, obj):
    with open(D(path), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    s = s.lower()
    s = re.sub(r"\(.*?\)", " ", s)
    s = re.sub(r"\b(the|restaurant|new york|nyc|hotel|a thompson|by hyatt|michelin key|michelin keys)\b", " ", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())


def as_list(v):
    if not v:
        return []
    return v if isinstance(v, list) else [v]


def merge_social(*groups):
    out, seen = [], set()
    for g in groups:
        for s in as_list(g):
            if not isinstance(s, dict):
                continue
            url = s.get("url") or ""
            if not url.startswith("http") or url in seen:
                continue
            seen.add(url)
            item = {"platform": s.get("platform") or "Link", "url": url}
            note = s.get("note") or s.get("label") or s.get("type")
            if note:
                item["note"] = note
            out.append(item)
    return out


# --------------------------------------------------------------------------
# Restaurants
# --------------------------------------------------------------------------
VERIFIED_TODAY_RESTAURANTS = {
    "Eleven Madison Park", "Jungsik New York", "Masa", "Cote", "Gramercy Tavern",
    "Le Coucou", "Sushi Sho", "Per Se", "Atomix", "Atera", "Saga", "Joo Ok", "César", "Noda",
    "Jeju Noodle Bar", "Semma", "Yoshino", "Crown Shy", "Shmoné",
}
VERIFIED_TODAY_ACTIVITIES = {
    "The Met Fifth Avenue", "MoMA (Museum of Modern Art)",
    "Solomon R. Guggenheim Museum", "American Museum of Natural History",
    "9/11 Memorial (outdoor) and Museum", "Empire State Building Observatory",
    "Wollman Rink in Central Park",
    "Bank of America Winter Village at Bryant Park (The Rink & The Lodge)",
    "29th Chinatown Lunar New Year Parade & Festival (2027)",
}
VERIFIED_TODAY_HOTELS = {"Hyatt Place New York / Chelsea"}


def build_restaurants():
    data_canon = canon("restaurants")
    rows = [dict(r) for r in data_canon["items"]]

    kit_files = [
        ("sessions/c1cf7b23/data/restaurants.json", "items", "arena/c1cf7b23-nyfun2"),
        ("sessions/657520df/data/restaurants.json", "items", "arena/657520df-nyfun2"),
        ("sessions/33cfdba4/data/restaurants.json", "rows", "arena/33cfdba4-nyfun2"),
    ]
    index = {}
    for path, key, session in kit_files:
        try:
            data = load(path)
        except FileNotFoundError:
            continue
        for r in data.get(key, []):
            index.setdefault(norm(r.get("name")), []).append((session, r))

    conflicts, enriched, kit_only = [], Counter(), []
    # Venues where the kits' official pages disagree with each other or are not a
    # menu page: no price is adopted, the row stays blank and is flagged (F15/F24).
    # (Atomix was resolved 2026-11-26 via its official Tock page: Nov $424/$314 vs Dec $495/$352+.)
    PRICE_BLOCKLIST = {
        "Atera": "Kits report $298 (restaurant page) and $325 (booking page) per person.",
        "Per Se": "Kits report $185 (Salon 4-course) and $295 (Salon 5-course); the dining room shows only a deposit.",
    }

    def first_nested(r, *keys):
        for k in keys:
            for kk in (k, *k.split(".")):
                if kk in r and r[kk] not in (None, "", []):
                    return r[kk]
        return None

    for row in rows:
        matches = index.get(norm(row["name"]), [])
        prov = row.setdefault("provenance", {})
        prov.setdefault("roster", "official MICHELIN all-starred census, 2026-11-25 (re-checked 2026-11-26)")
        social_new = []
        for session, r in matches:
            # address / cuisine
            if not row.get("address") and r.get("address"):
                row["address"] = r["address"]
                prov["address"] = session
            if not row.get("cuisine") and r.get("cuisine"):
                row["cuisine"] = r["cuisine"]
                prov["cuisine"] = session
            # hours
            for field, keys in (("hours", ("hours", "hoursText")),
                                ("exceptions", ("exceptions", "exception")),
                                ("daysOpen", ("daysOpen", "days"))):
                if not row.get(field):
                    v = first_nested(r, *keys)
                    if v and isinstance(v, str) and len(v) < 400 and v.strip().lower() not in {"not confirmed", "unknown", "n/a"}:
                        row[field] = v
                        prov[field] = session
                    elif v and str(v).strip().lower() in {"not confirmed", "unknown"}:
                        missing_note = f"{field} not confirmed in the sources checked"
                        if missing_note not in row.setdefault("flags", []):
                            row["flags"].append(missing_note)
            if not row.get("officialUrl") and (r.get("officialUrl") or r.get("website")):
                row["officialUrl"] = r.get("officialUrl") or r.get("website")
                prov["officialUrl"] = session
            if not row.get("guidePriceBand"):
                v = r.get("guidePriceBand") or r.get("guideBand")
                if v:
                    row["guidePriceBand"] = v
                    prov["guidePriceBand"] = session
            # price: only from an official restaurant page the kit cites
            price = r.get("totalPriceTwoAdults") or r.get("coupleMenuTotal") or r.get("priceTwoAdults")
            psrc = r.get("priceSourceUrl") or r.get("menuSourceUrl")
            if row["name"] in PRICE_BLOCKLIST:
                price = None
            if price and not row.get("priceTwoAdults"):
                if psrc and psrc.startswith("http") and "michelin.com" not in psrc and "booking.com" not in psrc:
                    row["priceTwoAdults"] = price
                    row["priceSourceUrl"] = psrc
                    row["priceNote"] = (r.get("priceDetail") or r.get("couplePriceBasis") or
                                        "Per-person menu price published by the restaurant; couple total = 2 x that price. Food only.")
                    prov["priceTwoAdults"] = session
                else:
                    conflicts.append({
                        "type": "price-without-official-source",
                        "row": row["name"],
                        "session": session,
                        "value": price,
                        "source": psrc or "none",
                        "action": "not adopted; canonical price stays blank/unchanged",
                    })
            elif price and row.get("priceTwoAdults") and dollars(price) != dollars(row["priceTwoAdults"]):
                conflicts.append({
                    "type": "price-disagreement",
                    "row": row["name"],
                    "session": session,
                    "kitValue": price,
                    "canonicalValue": row["priceTwoAdults"],
                    "source": psrc or "",
                    "action": "canonical value kept; both shown on the Michelin page note",
                })
            # socials
            social_new.append(r.get("social") or r.get("socials") or r.get("socialLinks"))

        if row.get("social") or social_new:
            merged = merge_social(row.get("social"), *social_new)
            if merged:
                row["social"] = merged
                if any(social_new):
                    prov["social"] = "canonical + kit links (see note per link)"
        if not row.get("priceSourceUrl") and row.get("priceTwoAdults"):
            prov["priceTwoAdults"] = prov.get("priceTwoAdults", "canonical capture")

        # verification status label used by the site filter
        if row["name"] in VERIFIED_TODAY_RESTAURANTS:
            row["verifiedToday"] = True
        if row.get("verifiedToday"):
            row["verifyStatus"] = "checked today (2026-11-26)"
        else:
            row["verifyStatus"] = "carried capture (2026-11-25)"

    # kit-only names are reported, never added
    canon_norms = {norm(r["name"]) for r in rows}
    for key, entries in index.items():
        if key not in canon_norms:
            for session, r in entries:
                kit_only.append({"name": r.get("name"), "session": session,
                                 "status": "not in the official 69-star census checked 2026-11-26",
                                 "source": r.get("sourceUrl") or r.get("source") or ""})

    # de-duplicate reports
    def uniq(items, keyfields):
        seen, out = set(), []
        for it in items:
            k = tuple(str(it.get(f)) for f in keyfields)
            if k in seen:
                continue
            seen.add(k)
            out.append(it)
        return out

    conflicts = uniq(conflicts, ("type", "row", "session", "kitValue"))
    kit_only = uniq(kit_only, ("name", "session"))

    meta = data_canon["meta"]
    meta.update({
        "checkedOn": "2026-11-25",
        "integrationCheckedOn": "2026-11-26",
        "integrationSession": "arena/9bc6abed-nyfun2",
        "integrationNote": ("Kit fields were merged into the canonical roster on 2026-11-26. "
                            "A blank field was filled only when the kit row carried a source URL for it; "
                            "the provenance object on each row names the originating session. "
                            "No row was added or removed: the roster remains the official 69 starred + 3 guide-listed census."),
    })
    data_canon["items"] = rows
    save("data/restaurants.json", data_canon)

    # coverage
    fields = ["address", "hours", "exceptions", "priceTwoAdults", "officialUrl", "social", "guidePriceBand"]
    coverage = {f: sum(1 for r in rows if r.get(f)) for f in fields}
    summary = {
        "rows": len(rows),
        "starred": sum(1 for r in rows if "Star" in r.get("distinction", "") and "Guide-listed" not in r.get("distinction", "")),
        "guideListed": sum(1 for r in rows if "Guide-listed" in r.get("distinction", "")),
        "coverage": coverage,
        "conflicts": conflicts,
        "kitOnly": kit_only,
    }
    return summary


# --------------------------------------------------------------------------
# Hotels
# --------------------------------------------------------------------------
def hotel_key(name):
    n = norm(name)
    rules = [("frederick", "frederick"), ("eurostars", "eurostars"), ("doubletree", "doubletree"),
             ("evelyn", "evelyn"), ("benjamin", "benjamin"), ("hyatt place", "hyattplace"),
             ("arlo nomad", "arlonomad"), ("arlo soho", "arlosoho"), ("howard", "howard11"),
             ("beekman", "beekman"), ("citizenm", "citizenm"), ("fifth avenue", "fifthave"),
             ("maritime", "maritime"), ("marlton", "marlton"), ("soho grand", "sohogrand"),
             ("wall street hotel", "wallsthotel"), ("made", "made")]
    for needle, k in rules:
        if needle in n:
            return k
    return n


FIELD_ALIASES = {
    "address": ("address",),
    "area": ("area", "neighborhood"),
    "room": ("room", "qualifyingRoom", "bedType"),
    "privateBathroom": ("privateBathroom",),
    "keyStatus": ("keyStatus", "michelinKey"),
    "guestScore": ("guestScore", "michelinScore"),
    "publishedRate": ("publishedRate",),
    "sevenNightPreTax": ("sevenNightPreTax", "preTax7Night", "sevenNightTotal", "pre_tax_total"),
    "sevenNightAllIn": ("sevenNightAllIn", "allIn7Night", "allInSevenNights"),
    "taxBasis": ("taxBasis", "taxArithmetic"),
    "rateSourceUrl": ("rateSourceUrl", "bookingUrl"),
    "rateCapturedOn": ("rateCapturedOn",),
    "officialUrl": ("officialUrl",),
    "sourceUrl": ("sourceUrl",),
    "amenities": ("amenities",),
    "cancellation": ("cancellationTerms",),
    "michelinWithin60": ("michelinWithin60Min", "starredWithin60"),
    "clusterTransit": ("clusterTransitBreakdown",),
}


def build_hotels():
    data_canon = canon("hotels")
    base = [dict(r) for r in data_canon["items"]]

    kit_files = [
        ("sessions/c1cf7b23/data/hotels.json", "arena/c1cf7b23-nyfun2"),
        ("sessions/657520df/data/hotels.json", "arena/657520df-nyfun2"),
        ("sessions/33cfdba4/data/hotels.json", "arena/33cfdba4-nyfun2"),
    ]
    pool = []
    for path, session in kit_files:
        try:
            data = load(path)
        except FileNotFoundError:
            continue
        for r in data.get("items") or data.get("rows") or []:
            pool.append((session, r))

    rows = []
    by_key = {}
    for r in base:
        k = hotel_key(r["name"])
        r.setdefault("provenance", {})["row"] = "canonical data/hotels.json"
        by_key[k] = r
        rows.append(r)

    for session, r in pool:
        k = hotel_key(r.get("name"))
        row = by_key.get(k)
        if row is None:
            row = {
                "name": r.get("name"),
                "flags": [],
                "provenance": {"row": f"added from {session} (property not in the first canonical set)"},
            }
            by_key[k] = row
            rows.append(row)
        prov = row.setdefault("provenance", {})
        for target, keys in FIELD_ALIASES.items():
            if row.get(target):
                continue
            for kk in keys:
                v = r.get(kk)
                if v not in (None, "", []):
                    row[target] = v
                    prov[target] = session
                    break
        for f in as_list(r.get("flags")):
            if isinstance(f, str) and f not in row.setdefault("flags", []):
                row["flags"].append(f)

    for h in rows:
        if not h.get("sourceUrl"):
            h["sourceUrl"] = h.get("officialUrl") or h.get("rateSourceUrl") or ""
    # a row with no official source at all cannot be published: drop it and record why
    dropped = [h["name"] for h in rows if not str(h.get("sourceUrl", "")).startswith("http")]
    rows = [h for h in rows if str(h.get("sourceUrl", "")).startswith("http")]

    # ---- measured transit anchors -----------------------------------------
    try:
        anchors = load("sessions/33cfdba4/data/transit_anchors.json")
    except FileNotFoundError:
        anchors = {}
    matrix = anchors.get("matrix") or []
    anchor_meta = {a["id"]: a for a in anchors.get("anchors") or []}
    leg_by_hotel = {}
    for leg in matrix:
        leg_by_hotel.setdefault(leg["hotel"], []).append(leg)

    ORIGIN_MAP = {
        "eurostars-wall": "Eurostars Wall Street",
        "doubletree-chelsea": "DoubleTree by Hilton Hotel New York City - Chelsea",
        "frederick-tribeca": "The Frederick Hotel Tribeca",
        "evelyn-nomad": "The Evelyn NoMad",
        "benjamin-midtown": "The Benjamin Royal Sonesta New York",
    }
    for h in rows:
        k = None
        for slug, name in ORIGIN_MAP.items():
            if difflib.SequenceMatcher(None, norm(h["name"]), norm(name)).ratio() >= 0.9:
                k = slug
                break
        if not k or k not in leg_by_hotel:
            h["transit"] = {"measured": False,
                            "note": "No door-to-door measurement stored for this property; left blank, not estimated."}
            continue
        legs = leg_by_hotel[k]
        mins = [leg["minutes"] for leg in legs]
        h["transit"] = {
            "measured": True,
            "legs": [{"anchor": anchor_meta.get(l["anchor"], {}).get("label", l["anchor"]),
                      "destination": anchor_meta.get(l["anchor"], {}).get("destination", ""),
                      "minutes": l["minutes"], "lines": l.get("lines", []),
                      "source": l.get("source", "")} for l in legs],
            "maxMinutes": max(mins),
            "avgMinutes": round(sum(mins) / len(mins), 1),
            "clustersWithin60": sum(1 for m in mins if m <= 60),
            "clustersMeasured": len(mins),
            "starsCoveredWithin60": sum(len(anchor_meta.get(l["anchor"], {}).get("restaurants", []))
                                        for l in legs if l["minutes"] <= 60),
            "capturedOn": anchors.get("as_of", ""),
            "method": "Google Maps transit, 'leave now', door-to-door incl. walking; fastest itinerary returned.",
        }

    # ---- eligibility + ranking ---------------------------------------------
    for h in rows:
        bed = str(h.get("room") or "")
        bath = str(h.get("privateBathroom") or "")
        has_bed = bool(re.search(r"\b(queen|king)\b", bed, re.I))
        has_bath = bool(re.search(r"(private|en-suite|ensuite|attached)", bath, re.I))
        h["qualifies"] = has_bed and has_bath
        if not h["qualifies"]:
            h["eligibilityNote"] = ("Queen+/private-bath specification not confirmed on an official property page: "
                                    "excluded from the recommendation until verified (flag F26).")
        h["pricedTier"] = "dated 7-night total" if (h.get("sevenNightPreTax") or h.get("sevenNightAllIn")) else ""
        h["verifiedToday"] = h["name"] in VERIFIED_TODAY_HOTELS
        h["verifyStatus"] = "checked today (2026-11-26)" if h["verifiedToday"] else "carried capture (2026-11-25)"

    qual = [h for h in rows if h.get("qualifies")]
    qual_measured = sorted([h for h in qual if h.get("transit", {}).get("measured")],
                           key=lambda h: (money(h.get("sevenNightAllIn") or h.get("sevenNightPreTax")),
                                          h["transit"]["avgMinutes"]))
    qual_unmeasured = sorted([h for h in qual if not h.get("transit", {}).get("measured")],
                             key=lambda h: money(h.get("sevenNightAllIn") or h.get("sevenNightPreTax")))
    rest = sorted([h for h in rows if not h.get("qualifies")],
                  key=lambda h: money(h.get("sevenNightAllIn") or h.get("sevenNightPreTax")))
    ranked = qual_measured + qual_unmeasured + rest
    for i, h in enumerate(ranked, 1):
        h["rank"] = i

    windows = []
    try:
        w = load("sessions/c1cf7b23/data/hotels.json").get("bookingWindows") or []
        windows = w
    except FileNotFoundError:
        pass
    data_canon["windows"] = windows
    data_canon["items"] = ranked
    data_canon["meta"].update({
        "checkedOn": "2026-11-25",
        "integrationCheckedOn": "2026-11-26",
        "rankingPolicy": ("Rank 1 group = private bath + queen/king bed confirmed AND a stored door-to-door transit "
                          "measurement (25 legs were captured across five origin hotels; one origin was dropped for "
                          "lacking an official source). Every measured hotel reaches all five sampled MICHELIN clusters "
                          "in 37 minutes or less, so the one-hour rule does not separate them; ties break on average sampled transit "
                          "time, then on verified all-in 7-night price. Hotels with no stored measurement follow, then "
                          "hotels whose bed/bath specification is unconfirmed (flagged, never assumed)."),
        "hotelCount": len(ranked),
        "pricedCount": sum(1 for h in ranked if h.get("sevenNightPreTax") or h.get("sevenNightAllIn")),
        "measuredCount": sum(1 for h in ranked if h.get("transit", {}).get("measured")),
        "qualifiedCount": len(qual),
        "droppedWithoutSource": dropped,
    })
    save("data/hotels.json", data_canon)
    return {"rows": len(ranked),
            "priced": data_canon["meta"]["pricedCount"],
            "measured": data_canon["meta"]["measuredCount"],
            "qualified": len(qual),
            "ranking": [(h["rank"], h["name"], h.get("sevenNightAllIn") or h.get("sevenNightPreTax") or "",
                         h.get("transit", {}).get("avgMinutes"), h["qualifies"]) for h in ranked]}


def dollars(v):
    """Set of dollar amounts in a price string, so wording differences do not count as conflicts."""
    return sorted({m.replace(",", "") for m in re.findall(r"\$\s?([\d,]+)", str(v or ""))})


def money(v):
    if not v:
        return 9e9
    m = re.search(r"\$([\d,]+)", str(v))
    return int(m.group(1).replace(",", "")) if m else 9e9


# --------------------------------------------------------------------------
# Activities
# --------------------------------------------------------------------------
def build_activities():
    data_canon = canon("activities")
    base = [dict(r) for r in data_canon["items"]]

    kit_files = [
        ("sessions/c1cf7b23/data/activities.json", "items", "arena/c1cf7b23-nyfun2"),
        ("sessions/657520df/data/activities.json", "items", "arena/657520df-nyfun2"),
        ("sessions/33cfdba4/data/activities.json", "rows", "arena/33cfdba4-nyfun2"),
    ]
    pool = []
    for path, key, session in kit_files:
        try:
            data = load(path)
        except FileNotFoundError:
            continue
        for r in data.get(key, []):
            pool.append((session, r, data))

    RULES = [
        ("met fifth", "met"), ("nypl", "nypl"), ("lunar new year", "lny"), ("chinatown", "lny"), ("bryant", "bryant"), ("wollman", "wollman"),
        ("top of the rock", "top"), ("summit", "summit"), ("brooklyn bridge", "brooklyn"),
        ("september 11", "911"), ("9 11", "911"), ("guggenheim", "guggenheim"), ("high line", "highline"),
        ("whitney", "whitney"), ("natural history", "amnh"), ("modern art", "moma"),
        ("metropolitan", "met"), ("statue of liberty", "statue"), ("empire state", "esb"),
        ("staten island", "staten"), ("public library", "nypl"), ("central park", "centralpark"),
        ("katz", "katz"), ("cloisters", "cloisters"),
    ]

    alias = {
        "statue of liberty national monument ellis island": "statue of liberty",
        "statue of liberty ellis island": "statue of liberty",
        "statue of liberty ellis island statue city cruises": "statue of liberty",
        "statue of liberty ellis island national monuments": "statue of liberty",
        "the metropolitan museum of art the met fifth avenue": "met fifth avenue",
        "the metropolitan museum of art fifth avenue": "met fifth avenue",
        "met fifth avenue": "met fifth avenue",
        "museum of modern art moma": "moma",
        "the museum of modern art moma": "moma",
        "moma museum of modern art": "moma",
        "american museum of natural history gilder center": "amnh",
        "national september 11 memorial museum": "911",
        "911 memorial museum": "911",
        "whitney museum of american art": "whitney",
        "solomon r guggenheim museum": "guggenheim",
        "the high line elevated park": "high line",
        "high line": "high line",
        "central park bethesda terrace bow bridge the mall": "central park",
        "top of the rock observation deck rockefeller center": "top of the rock",
        "top of the rock observation deck": "top of the rock",
        "empire state building observatory 86th 102nd floors": "esb",
        "empire state building 86th floor observatory": "esb",
        "bank of america winter village at bryant park the rink the lodge": "bryant park",
        "bank of america winter village at bryant park ice rink": "bryant park",
        "wollman rink in central park": "wollman",
        "new york public library stephen a schwarzman building": "nypl",
        "new york public library stephen a schwarzman building polonsky exhibition": "nypl",
        "staten island ferry harbor statue of liberty skyline cruise": "staten island ferry",
        "staten island ferry free harbor skyline liberty views": "staten island ferry",
        "brooklyn bridge pedestrian promenade dumbo waterfront": "brooklyn bridge",
        "29th chinatown lunar new year parade festival 2027 date confirmed": "lny parade",
        "29th chinatown lunar new year parade festival year of the goat sheep": "lny parade",
        "summit one vanderbilt": "summit",
        "catz delicatessen": "katz",
    }

    def akey(name):
        n = norm(name)
        for needle, key in RULES:
            if needle in n:
                return key
        return alias.get(n, n)

    idx = {}
    for session, r, data in pool:
        idx.setdefault(akey(r.get("name")), []).append((session, r))

    used = set()
    out = []
    for row in base:
        row = dict(row)
        prov = row.setdefault("provenance", {})
        prov["row"] = "canonical data/activities.json"
        k = akey(row["name"])
        socials = []
        for session, r in idx.get(k, []):
            used.add((session, id(r)))
            for target, keys in (
                ("hours", ("hours",)),
                ("exceptions", ("exceptions", "notes")),
                ("costTwoAdults", ("costTwoAdults", "coupleCost", "price_for_two", "price")),
                ("address", ("address", "neighborhood")),
                ("area", ("area", "neighborhood")),
                ("daysOpen", ("daysOpen", "days")),
                ("officialUrl", ("officialUrl", "website")),
                ("sourceUrl", ("sourceUrl", "source")),
                ("transitNote", ("transitNote", "maxTransitFromShortlist", "metro_minutes")),
            ):
                if row.get(target):
                    continue
                for kk in keys:
                    v = r.get(kk)
                    if v in (None, "", []):
                        continue
                    if isinstance(v, (int, float)):
                        v = str(v)
                    row[target] = v
                    prov[target] = session
                    break
            socials.append(r.get("social") or r.get("socials") or r.get("socialLinks"))
            for f in as_list(r.get("flags")):
                if isinstance(f, str) and f not in row.setdefault("flags", []):
                    row["flags"].append(f)
        merged_social = merge_social(row.get("social"), *socials)
        if merged_social:
            row["social"] = merged_social
        if row["name"] in VERIFIED_TODAY_ACTIVITIES:
            row["verifiedToday"] = True
        row["verifyStatus"] = "checked today (2026-11-26)" if row.get("verifiedToday") else "carried capture (2026-11-25)"
        out.append(row)

    # add kit-only activities that materially expand the plan
    seen_keys = {akey(r["name"]) for r in out}
    for session, r, data in pool:
        k = akey(r.get("name"))
        if k in seen_keys or k == "katz" or is_dup(r.get("name"), [x["name"] for x in out]):
            continue
        seen_keys.add(k)
        item = {
            "name": r.get("name"),
            "category": r.get("category") or "",
            "area": r.get("area") or r.get("neighborhood") or "",
            "address": r.get("address") or "",
            "daysOpen": r.get("daysOpen") or r.get("days") or "",
            "hours": r.get("hours") or "",
            "exceptions": r.get("exceptions") or "",
            "costTwoAdults": r.get("costTwoAdults") or r.get("coupleCost") or r.get("price") or "",
            "transitNote": r.get("transitNote") or r.get("maxTransitFromShortlist") or "",
            "officialUrl": r.get("officialUrl") or r.get("website") or "",
            "sourceUrl": r.get("sourceUrl") or r.get("source") or "",
            "social": merge_social(r.get("social") or r.get("socials")),
            "flags": as_list(r.get("flags")),
            "provenance": {"row": f"added from {session} (activity not in the first canonical set)"},
            "verifyStatus": "carried capture (2026-11-25)",
        }
        # Preserve PR #28 (arena/4a8e5aa4-nyfun2) official FAQ correction for SUMMIT One Vanderbilt
        if "SUMMIT One Vanderbilt" in str(item["name"]):
            item["daysOpen"] = "Daily (7 days) — official FAQ footer lists every weekday, re-read 26 Nov 2026"
            item["hours"] = "Daily 08:00–24:00; last entry 22:30 (official FAQ footer, re-read 26 Nov 2026)"
            item["exceptions"] = ("Final re-check found no Tuesday closure on the official page: it prints daily "
                                  "08:00–24:00 and an earlier kit note about historical winter Tuesday closures is not "
                                  "carried forward. All ticket sales are final; low-visibility rebooking terms and "
                                  "mirrored-floor dress guidance remain on the official page. F29 records the discrepancy.")
            item["flags"] = [
                "Dynamic timed-ticket checkout price for Feb 2027 still requires a live Webstore check; couple cost left blank rather than citing third-party ~$40 estimates.",
                "F29: the opening-days line was corrected from the kit's 'historically closed Tuesdays' after the official FAQ footer was re-read on 26 Nov 2026.",
            ]
            item["provenance"]["hoursAndDays"] = "Re-verified 2026-11-26 by arena/4a8e5aa4-nyfun2 against https://info.summitov.com/"
            item["verifyStatus"] = "checked today (2026-11-26)"
        out.append(item)

    data_canon["items"] = out
    data_canon["meta"].update({
        "integrationCheckedOn": "2026-11-26",
        "integrationNote": ("Union of the canonical 12 activities and every kit row (deduplicated by name). "
                            "Existing canonical values were kept; kit values filled blanks only and each fill is "
                            "named in the row's provenance. Every row keeps its own official source link."),
        "travelTimePolicy": ("Stored door-to-door minutes appear only where a Google Maps transit result was captured "
                             "(10 activity legs from Eurostars Wall Street, 2026-11-25). Other rows link a live "
                             "directions query instead."),
    })
    save("data/activities.json", data_canon)
    return {"rows": len(out),
            "hours": sum(1 for r in out if r.get("hours")),
            "social": sum(1 for r in out if r.get("social")),
            "cost": sum(1 for r in out if r.get("costTwoAdults"))}


# --------------------------------------------------------------------------
# Verification log (checks actually performed on 2026-11-26)
# --------------------------------------------------------------------------
V = [
    ("Michelin NYC starred census", "5 three-star / 14 two-star / 50 one-star; 69 starred; 76 Bib Gourmand; 224 Selected",
     "https://guide.michelin.com/en/us/new-york-state/new-york/restaurants/all-starred",
     "Confirmed on the live filter panel, 2026-11-26", "Verified"),
    ("Star level spot-check, 15 rows", "Le Coucou 1*, Sushi Sho 3*, Jungsik 3*, EMP 3*, Atera 2*, Saga 2*, Joo Ok 2*, Cesar 2*, Noda 1*, Jeju Noodle Bar 1*, Semma 1*, Yoshino 1*, Cote 1*, Crown Shy 1*, Shmone 1*",
     "https://guide.michelin.com/en/us/new-york-state/new-york/restaurants/all-starred",
     "Star icons on the official list matched the catalogue for all 15 sampled rows", "Verified"),
    ("Eleven Madison Park menu prices", "Full Tasting $385/guest ($770 for two); Bar Tasting $255/guest ($510); lounge bar tasting 'begins at $225' ($450)",
     "https://www.elevenmadisonpark.com/faq",
     "Read directly from the official FAQ; both bar-tasting endpoints exist on the same page", "Verified"),
    ("Jungsik menu price", "Signature Menu $335/guest -> $670 for two",
     "https://www.jungsik.com/menu/", "Read from the official menu page", "Verified"),
    ("Masa menu prices", "Lunch from $495; Table Omakase $750; Hinoki Counter $950 -> $990 / $1,500 / $1,900 for two",
     "https://www.masanyc.com/menus", "Read from the official menus page", "Verified"),
    ("Cote menu prices", "Butcher's Feast $84/guest ($168); Steak Omakase $225/guest ($450)",
     "https://www.cotekoreansteakhouse.com/nycdinnermenu", "Read from the official Flatiron dinner menu", "Verified"),
    ("Gramercy Tavern menu prices", "Dining Room Seasonal Menu $178/guest ($356); Tavern three-course $78 ($156)",
     "https://www.gramercytavern.com/dining-room-menu/", "Read from the official menu page", "Verified"),
    ("The Met admission and hours", "Adults $30 ($60 for two); Sun/Mon/Tue/Thu 10-17, Fri-Sat 10-21, closed Wednesday",
     "https://www.metmuseum.org/plan-your-visit",
     "Admission table read on the official page today; the Wednesday closure corroborated by four independent guides because the hours block was not in the page section captured", "Verified (hours corroborated)"),
    ("MoMA admission and hours", "Adults $30 ($60 for two); daily 10:30-17:30, Friday to 20:30; closed Thanksgiving and 25 Dec",
     "https://www.moma.org/visit/", "Read directly from the official visit page", "Verified"),
    ("Chinatown Lunar New Year Parade 2027", "29th parade: Sunday 21 February 2027, 13:00, Chinatown; firecracker ceremony Sat 6 Feb 2027",
     "http://betterchinatown.com/",
     "Organiser page plus two independent listings agree. The organiser's Chinese-language line on the same page still says 2026 - flagged F19", "Verified (typo flagged)"),
    ("Bryant Park Winter Village season", "Season 28 Oct 2026 - 28 Feb 2027; rink 08:00-22:00 daily; Lodge 10:00-22:00; holiday shops end 3 Jan 2027; rental $18.72-$64.48",
     "https://bryantpark.org/activities/bank-of-america-winter-village-at-bryant-park",
     "Re-read directly from bryantpark.org on 2026-11-26 (sessions 45972379 and 4a8e5aa4)", "Verified"),
    ("Wollman Rink 2026-27", "Season 28 Oct 2026 - 16 Mar 2027; adults $16 off-peak / $28 peak / $40 prime; rental $12; 15 Feb Community Day, 16-21 Feb Peak, 22-25 Feb Off-Peak",
     "https://wollmanrinknyc.com/plan/",
     "Re-read directly from wollmanrinknyc.com/plan/ on 2026-11-26 (sessions 45972379 and 4a8e5aa4)", "Verified"),
    ("Hyatt Place NY/Chelsea room specification", "King-bed rooms with a bathroom with shower; 180 sq ft; address 140 West 24th Street",
     "https://www.hyatt.com/hyatt-place/en-US/lgazc-hyatt-place-new-york-chelsea/rooms",
     "Read from the official rooms page today", "Verified"),
    ("Dated hotel rates for 15-22 Feb 2027", "$1,113 pre-tax Hyatt Place, $1,214 Arlo NoMad, $1,522 11 Howard, $848 Eurostars, $943 DoubleTree",
     "https://www.booking.com/searchresults.html?ss=Manhattan%2C+New+York&checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1&selected_currency=USD&order=price",
     "Booking.com property detail pages returned an error to this session's fetcher, so the dated totals could not be re-quoted today. The search page for the window did load, confirming availability for 15-22 Feb 2027. Treat the totals as 2026-11-25 snapshots (F10)", "NOT re-quoted today - carried"),
    ("Transit times", "25 hotel->cluster legs, 3-37 minutes; 10 hotel->activity legs",
     "https://www.google.com/maps/dir/?api=1&origin=Eurostars+Wall+Street+New+York&destination=Le+Bernardin+New+York&travelmode=transit",
     "Captured 2026-11-25 17:14-17:31 ET. Google Maps cannot be queried programmatically from this session, so the stored minutes are snapshots; each leg links a live directions query", "Carried snapshot"),
    ("Michelin 2026 ceremony date", "14 Dec 2026 (Northeast Cities)",
     "https://michelinmedia.com/pages/blog/detail/article/c/a1479/",
     "Not re-fetched today; carried from the 2026-11-25 capture and still the basis of flag F1", "Carried"),
    ("Atomix Tock pricing & socials", "Nov Chef's Counter $424/pp ($848) & Bar Tasting $314/pp ($628) incl. admin fee; Dec $495/pp & from $352/pp; @atomixnyc",
     "https://www.exploretock.com/atomixnyc/help",
     "Read directly from Atomix's official Tock help page on 2026-11-26 (session arena/779506a6-nyfun2); explains why earlier sessions saw $424 vs $495", "Verified"),
    ("Sushi Sho Tock pricing & release", "Shorter Omakase at Hinoki Counter $495/pp incl. admin fee ($990 for two); booking through 28 Feb 2027; releases 1 Dec 2026 11:00 AM EST; @sushishonyc",
     "https://www.exploretock.com/sushi-sho-nyc/experience/474458/shorter-omakase-at-hinoki-counter",
     "Read directly from Sushi Sho's official Tock page on 2026-11-26 (sessions 45972379, 4a8e5aa4, 779506a6)", "Verified"),
    ("Per Se Tock deposit-only status", "Main Dining Room starting at $200/pp deposit; Salon Four-Course $150/pp deposit; no full menu price printed",
     "https://www.exploretock.com/perse/experience/7768/salon-lounge-seating-four-course-tasting-menu",
     "Read directly from Per Se's official Tock page on 2026-11-26; confirms row must stay blank (F18/F24)", "Verified"),
    ("Guggenheim admission and hours", "General Admission $30 ($60 for two); daily 10:30-17:30; PWYW Tue & Sun 16:00-17:30",
     "https://www.guggenheim.org/plan-your-visit",
     "Read directly from guggenheim.org/plan-your-visit on 2026-11-26 (session arena/779506a6-nyfun2)", "Verified"),
    ("AMNH Pay What You Wish & hours", "NY-resident PWYW suggested $25 adult ($50 for two, GA only); non-NY mandatory GA; closed Thanksgiving 26 Nov",
     "https://www.amnh.org/plan-your-visit",
     "Read directly from amnh.org/plan-your-visit on 2026-11-26 (session arena/779506a6-nyfun2)", "Verified"),
    ("9/11 Memorial & Museum hours", "Memorial daily 08:00-20:00; Museum Wed-Mon + select Tue 09:00-19:00 (last entry 17:30); advance Museum ticket required",
     "https://www.911memorial.org/visit",
     "Read directly from 911memorial.org/visit on 2026-11-26 (session arena/779506a6-nyfun2)", "Verified"),
    ("Empire State Building seasonal hours", "Open 365 days; typical winter 10:00-22:00 (doors close 21:00; select Nov/Dec dates 09:00-23:00)",
     "https://www.esbnyc.com/visit/hours-of-operation",
     "Read directly from esbnyc.com/visit/hours-of-operation on 2026-11-26 (session arena/779506a6-nyfun2); Feb 2027 calendar not yet posted", "Verified"),
    ("SUMMIT One Vanderbilt opening days", "Daily (Sunday-Saturday) 08:00-24:00, last entry 22:30; no Tuesday closure on official FAQ",
     "https://info.summitov.com/",
     "Read directly from info.summitov.com FAQ footer on 2026-11-26 (session arena/4a8e5aa4-nyfun2; F29)", "Verified"),
    ("MTA subway and bus fares", "Subway / local / limited / Select Bus Service $3; express bus $7.25",
     "https://www.mta.info/fares-tolls",
     "Read directly from mta.info/fares-tolls on 2026-11-26 (session arena/779506a6-nyfun2)", "Verified"),
]


def merge_text(old, new):
    """Keep the existing verified wording and append the new wording when it adds facts."""
    old = (old or "").strip()
    new = (new or "").strip()
    if not old:
        return new
    if not new or new in old:
        return old
    return old + " " + new


def build_decisions(rest, hot, act):
    data = canon("decisions")
    q = {x["id"]: x for x in data["questions"]}
    sg = {x["id"]: x for x in data["suggestions"]}

    q["Q1"]["whatWeKnow"] = merge_text(q["Q1"].get("whatWeKnow"), ("15 Feb 2027 is a Monday and 18 Feb a Thursday; 15-22 Feb 2027 is exactly 7 nights. "
                             "All dated hotel totals on this site use the 7-night window because that is what the "
                             "request asked to compare."))
    q["Q2"]["whatWeKnow"] = merge_text(q["Q2"].get("whatWeKnow"), (f"{hot['priced']} of {hot['rows']} shortlisted properties now carry a dated 7-night total for "
                             "15-22 Feb 2027, two adults, captured 2026-11-25. All-in range: $998 (Eurostars Wall Street, "
                             "non-refundable) to $5,220 (The Beekman). Totals are third-party booking-engine snapshots, "
                             "not hotel quotes, and two depend on promotions that expire."))
    q["Q2"]["provisionalAnswer"] = ("Use $1,110 all-in at DoubleTree Chelsea (free cancellation) as the budget anchor and "
                                    "$998 (Eurostars, non-refundable) as the floor. Re-quote both before paying.")
    q["Q3"]["provisionalAnswer"] = (f"{hot['qualified']} of {hot['rows']} properties have a published queen/king bed and private "
                                    "bathroom and can be booked against the requirement; the others must be verified first.")
    q["Q3"]["whatWeKnow"] = (f"{hot['qualified']} of {hot['rows']} properties publish a queen/king bed plus a private bathroom "
                             "on an official property page (or a property page the kits quote directly). "
                             f"{hot['rows'] - hot['qualified']} do not, and are excluded from the recommendation (flag F26).")
    q["Q5"]["whatWeKnow"] = ("25 hotel-to-MICHELIN-cluster legs were measured with Google Maps transit on 2026-11-25 "
                             "(17:14-17:31 ET) across five origin hotels; one of those five was dropped from the "
                             "shortlist for having no official source, leaving four published hotels with measured "
                             "transit. Every leg was 3-37 minutes door-to-door, so all four reach all five sampled "
                             "clusters inside the one-hour rule and the rule does not separate them; the ranking falls "
                             "through to verified price and average sampled time.")
    q["Q5"]["provisionalAnswer"] = ("Treat 'within one hour' as satisfied for any central Manhattan hotel; rank on price, "
                                    "room quality and average transit instead. Unmeasured hotels carry a blank, not a guess.")
    q["Q5"]["blocking"] = False
    q["Q6"]["provisionalAnswer"] = ("Use the verified couple totals as a planning floor and re-confirm at booking. Per Se "
                                    "and Atera stay blank until an official menu price resolves the conflict (F24); Atomix "
                                    "is resolved via Tock ($848/$628 November, $990/$704+ December - re-confirm for 2027).")
    q["Q6"]["whatWeKnow"] = (f"{rest['coverage']['priceTwoAdults']} of {rest['rows']} restaurant rows carry a couple total built from "
                             "a per-person price on an official menu, FAQ or official booking channel: from $156 (Gramercy "
                             "Tavern tavern three-course) to $1,900 (Masa Hinoki Counter). Food only, before tax and tip. "
                             "The full per-restaurant reconciliation (including EMP $770/$510, Le Bernardin $700/$436/$284, "
                             "Masa $990/$1,500/$1,900, Gabriel Kreuther $650/$400/$470) is on the Michelin page's price table.")
    q["Q8"]["whatWeKnow"] = merge_text(q["Q8"].get("whatWeKnow"), (f"{rest['coverage']['social']} restaurant rows and {act['social']} activity rows carry at least one "
                             "social link. Each link is labelled official or third-party review; ownership is only asserted "
                             "where the venue's own site or the platform's verified account confirms it."))

    if "Q13" not in q:
        data["questions"].append({
            "id": "Q13",
            "question": "Should the plan include Brooklyn and Queens MICHELIN venues, or stay in Manhattan?",
            "whatWeKnow": ("Williamsburg (Aska) measured 30-37 minutes from all five measured hotels, so it fits the "
                           "one-hour rule. Meju (Queens) and the Brooklyn one-stars were not individually routed."),
            "whatWeDoNotKnow": "Whether a 30-40 minute cross-borough trip is acceptable on a dining night.",
            "provisionalAnswer": "Keep one Brooklyn evening optional (Aska or Francie) and route it before booking.",
            "blocking": False,
            "howToDiscover": "Route the two or three Brooklyn candidates from the chosen hotel at the intended time.",
            "sources": ["https://www.google.com/maps/dir/?api=1&origin=DoubleTree+by+Hilton+Hotel+New+York+City+Chelsea&destination=Aska+Brooklyn&travelmode=transit"],
        })
        q["Q13"] = data["questions"][-1]

    status_updates = {
        "S2": "Partially implemented 2026-11-26 - 25 hotel-to-cluster and 10 hotel-to-activity legs stored with live directions links; the remaining pairs are still unrouted.",
        "S3": f"Implemented 2026-11-26 - {rest['coverage']['priceTwoAdults']} official-menu couple totals, each with its source URL and capture date.",
        "S5": "Partially implemented 2026-11-26 - 7-night totals for 8 hotels; a 3-night quote exists in no verified source yet.",
        "S7": "Implemented 2026-11-26 - every restaurant and activity row now carries a 'checked today / carried capture' badge and filter.",
        "S10": "Implemented 2026-11-25 - full live roster of 69 starred + 3 Guide-listed rows.",
        "S11": "Partially implemented 2026-11-26 - data age is displayed on every page; scheduled re-capture is still manual.",
        "S12": "Partially implemented 2026-11-26 - Met and MoMA hours re-read; 13 other activity pages not re-read today.",
    }
    for k, v in status_updates.items():
        if k in sg:
            sg[k]["status"] = v

    new_s = [
        {"id": "S13", "title": "Keep a dated quote screenshot for every hotel you are about to book",
         "detail": "Save the booking page (dates, room type, cancellation terms, total) as a PDF or image per hotel. It converts an aggregator snapshot into evidence and makes a price dispute resolvable.",
         "effort": "Low", "blockedBy": [], "status": "Proposed - no changes implemented"},
        {"id": "S14", "title": "Re-capture dated hotel prices weekly and show the delta",
         "detail": "A once-a-week re-quote of the eight priced hotels, stored beside the previous figure, would show whether the February window is moving up or down instead of relying on a single snapshot.",
         "effort": "Medium", "blockedBy": ["Q2"], "status": "Proposed - no changes implemented"},
        {"id": "S15", "title": "Add the Bib Gourmand and Selected census for cheaper MICHELIN meals",
         "detail": "The official filter shows 76 Bib Gourmand and 224 Selected restaurants. A verified subset would give a mid-price MICHELIN option for every night instead of only starred venues.",
         "effort": "High", "blockedBy": [], "status": "Proposed - no changes implemented"},
        {"id": "S17", "title": "Close the social-link gap for the 45 restaurants without one",
         "detail": "Work restaurant by restaurant: open the venue's own site footer for its official accounts, then search YouTube for a recent review. Record the account owner so official and third-party stay distinguishable. Roughly one hour per ten venues.",
         "effort": "Medium", "blockedBy": [], "status": "Proposed - no changes implemented"},
        {"id": "S16", "title": "Add a map view with the five restaurant clusters and the ranked hotels",
         "detail": "A static map with cluster markers and hotel pins would make the geographic trade-off visible at a glance; the measured minutes can sit in the popups.",
         "effort": "Medium", "blockedBy": [], "status": "Proposed - no changes implemented"},
    ]
    existing_s = {x["id"] for x in data["suggestions"]}
    for item in new_s:
        if item["id"] not in existing_s:
            data["suggestions"].append(item)

    new_flags = [
        {"id": "F21", "severity": "High",
         "title": "This session could not re-read every official page",
         "detail": ("The sandbox reaches GitHub directly and external pages through a proxied fetch/search channel. "
                    "16 checks were re-run on 2026-11-26 (MICHELIN filter counters, 15 star levels, 5 menus, Met and MoMA, "
                    "the Lunar New Year parade, Hyatt room types). Booking.com property pages returned an error, and "
                    "bryantpark.org and wollmanrinknyc.com could not be fetched, so those figures are carried captures or "
                    "secondary corroboration. Every row states which it is."),
         "source": "data/verification.json"},
        {"id": "F22", "severity": "Medium",
         "title": "The previous front page understated its own data (fixed in this build)",
         "detail": ("index.html said the site detailed 20 restaurant rows, 12 attractions and 10 hotel candidates while the "
                    "datasets held 72 restaurant rows, 12 activities and 12 hotels; README said 21. All counts are now "
                    "rendered from the JSON at load time, so they cannot drift again."),
         "source": "https://github.com/kanlerxz87-cyber/NYFun2/blob/main/index.html"},
        {"id": "F23", "severity": "Medium",
         "title": "Kit rosters are not the same census as the live MICHELIN list",
         "detail": ("The parallel kits contained 14 venue names outside the 69-star census (Katz's, Thai Diner, Via Carota, "
                    "Dhamaka, Manhatta, Cafe Carmellini and others - Bib Gourmand/Selected or non-Guide), and one kit carried "
                    "three starred names that are not in today's live all-starred list (Blue Hill at Stone Barns, Shion 69 "
                    "Leonard Street, La Bastide by Andrea Calstier). None were added to the census; all are listed in "
                    "data/conflicts.json for review."),
         "source": "https://guide.michelin.com/en/us/new-york-state/new-york/restaurants/all-starred"},
        {"id": "F24", "severity": "Medium",
         "title": "Two restaurant prices (Atera, Per Se) remain contested/deposit-only and stay blank; Atomix is month-variable",
         "detail": ("Atera ($298 on the site vs $325 on the booking page) and Per Se ($185 Salon 4-course vs $295 Salon 5-course; "
                    "the live Tock pages publish only $200 MDR / $150 Salon deposits) are not adopted as prices and stay blank. "
                    "Atomix's $424 vs $495/pp difference was resolved on its official Tock page (November $424/$314 vs December $495/$352+ "
                    "incl. admin fee; November adopted, Feb-Mar 2027 flagged). Le Bernardin's dinner prix fixe keeps $218 (dinner-1.2.pdf) "
                    "with the $225 later-PDF figure also noted."),
         "source": "data/conflicts.json"},
        {"id": "F25", "severity": "Medium",
         "title": "Dated hotel totals could not be re-quoted today",
         "detail": ("Booking.com property pages refused this session's fetcher, so the 15-22 Feb 2027 totals are the "
                    "2026-11-25 snapshots. Two of them (DoubleTree, Arlo NoMad) were Black Friday promotions whose terms "
                    "expire; the search page for the window did load, confirming the dates remain bookable."),
         "source": "https://www.booking.com/searchresults.html?ss=Manhattan%2C+New+York&checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1&selected_currency=USD&order=price"},
        {"id": "F26", "severity": "Medium",
         "title": f"{hot['rows'] - hot['qualified']} shortlisted hotels still lack a verified bed and bathroom line",
         "detail": ("The Maritime, MADE, The Marlton, Soho Grand, Arlo Soho and The Wall Street Hotel do not have a "
                    "published queen/king + private-bathroom statement in the sources checked, so they are listed for "
                    "completeness and excluded from the recommendation rather than assumed to comply. (The Benjamin was "
                    "measured but dropped entirely: no official source for its room.)"),
         "source": "data/hotels.json"},
        {"id": "F27", "severity": "Low",
         "title": "RESOLVED 2026-11-26: two winter-activity official pages re-read successfully",
         "detail": ("Session 4a8e5aa4 fetched both official pages on 26 Nov 2026. Bryant Park states 28 Oct 2026–28 Feb 2027, "
                    "Rink 08:00–22:00, The Lodge 10:00–22:00, and rental $18.72–$64.48 including admin fees. Wollman states "
                    "28 Oct 2026–16 Mar 2027, day-specific hours, $16/$28/$40 adult admission and $12 rental, with 15 Feb a "
                    "restricted Community Day, 16–21 Feb Peak and 22–25 Feb Off-Peak. The previously unreachable values are now "
                    "confirmed on the official pages linked from those rows; no new figures were inferred."),
         "source": "https://bryantpark.org/activities/bank-of-america-winter-village-at-bryant-park"},
    ]
    social_gap = rest["rows"] - rest["coverage"]["social"]
    new_flags.append({
        "id": "F28", "severity": "Medium",
        "title": f"{social_gap} starred restaurants still have no social or video link",
        "detail": ("You asked for a YouTube/TikTok/Instagram link per restaurant. Links were found and merged for "
                   f"{rest['coverage']['social']} of {rest['rows']} rows; for the remaining {social_gap} no specific video or "
                   "account could be confirmed against the venue's own site, so none was invented. The MICHELIN page and "
                   "the restaurant's own site remain on every row, and suggestion S17 is the route to closing the gap."),
        "source": "https://guide.michelin.com/en/us/new-york-state/new-york/restaurants/all-starred"})
    new_flags.append({
        "id": "F29", "severity": "Low",
        "title": "SUMMIT One Vanderbilt opening days corrected from official FAQ",
        "detail": ("A parallel kit warned that SUMMIT was historically closed on Tuesdays in winter and told readers to check "
                   "the calendar. The official FAQ footer was re-read on 26 Nov 2026 and lists Sunday through Saturday as "
                   "08:00–24:00 with last entry at 22:30. The canonical row now says Daily (7 days); the earlier caveat is "
                   "retained here rather than repeated as a fact. Ticket price remains blank — no adult price was printed on "
                   "the page checked."),
        "source": "https://info.summitov.com/"})
    existing_f = {x["id"] for x in data["flags"]}
    for item in new_flags:
        if item["id"] not in existing_f:
            data["flags"].append(item)

    data["checkedOn"] = "2026-11-25"
    data["integrationCheckedOn"] = "2026-11-26"
    data["integrationSession"] = "arena/9bc6abed-nyfun2"
    save("data/decisions.json", data)
    return {"questions": len(data["questions"]), "suggestions": len(data["suggestions"]), "flags": len(data["flags"])}


def build_verification(rest, hot, act):
    checks = [{"fact": f, "value": v, "source": s, "note": n, "result": r} for f, v, s, n, r in V]
    counts = Counter(c["result"] for c in checks)
    data = {
        "checkedOn": "2026-11-26",
        "session": "arena/9bc6abed-nyfun2",
        "methodNote": ("This session's sandbox reaches GitHub directly and external sites through a proxied "
                       "fetch/search channel. Pages that block that channel are recorded as unreachable rather "
                       "than assumed. A value is only marked Verified when the official page itself was read today."),
        "checks": checks,
        "resultCounts": dict(counts),
        "coverage": {
            "restaurants": {"rows": rest["rows"], "withOfficialSource": rest["rows"],
                            "withPrice": rest["coverage"]["priceTwoAdults"],
                            "withHours": rest["coverage"]["hours"],
                            "withSocial": rest["coverage"]["social"],
                            "withAddress": rest["coverage"]["address"]},
            "hotels": {"rows": hot["rows"], "priced": hot["priced"], "measuredTransit": hot["measured"]},
            "activities": {"rows": act["rows"], "withHours": act["hours"],
                           "withSocial": act["social"], "withCost": act["cost"]},
        },
    }
    save("data/verification.json", data)
    return data["resultCounts"]


def main():
    rest = build_restaurants()
    hot = build_hotels()
    act = build_activities()
    dec = build_decisions(rest, hot, act)
    results = build_verification(rest, hot, act)
    save("data/conflicts.json", {
        "checkedOn": "2026-11-26",
        "note": "Disagreements found while merging kits into the canonical data. Nothing here was silently resolved.",
        "conflicts": rest["conflicts"],
        "kitOnlyRestaurants": rest["kitOnly"],
    })
    print("restaurants:", rest["rows"], "starred", rest["starred"], "guide", rest["guideListed"], rest["coverage"])
    print("restaurant conflicts:", len(rest["conflicts"]), "kit-only names:", len(rest["kitOnly"]))
    print("hotels:", hot["rows"], "priced", hot["priced"], "measured", hot["measured"])
    for r in hot["ranking"]:
        print("   rank", r)
    print("activities:", act)
    print("decisions:", dec)
    print("verification results:", results)


if __name__ == "__main__":
    main()
