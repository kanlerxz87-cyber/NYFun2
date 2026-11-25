#!/usr/bin/env python3
"""Assemble canonical data/restaurants.json for session fc6d5f66 (2026-11-25).
Roster: live MICHELIN all-starred list (69 = 5x3, 14x2, 50x1) re-verified this session,
plus 3 Guide-listed new-addition rows carried from the prior canonical file.
Every row carries an official source link. Prices/socials only where read from an
official page; blanks are flagged, never inferred. Reproducible: python3 research/build_restaurants.py
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
kit = json.loads((ROOT/'sessions/33cfdba4/data/restaurants.json').read_text())
kitrows = {r['name']: r for r in kit['rows']}
canon = json.loads((ROOT/'research/canonical-restaurants-original.json').read_text())
canonrows = {r['name']: r for r in canon['items']}

# Stale canonical flags that this session re-verifies and replaces; substantive
# irregularity notes (e.g. "Located inside 11 Howard hotel") are carried forward.
STALE = ("Couple price unverified","Hours unverified","Detail page not yet checked",
         "No social link verified from an official source",
         "Social link is third-party; no official account link confirmed",
         "No verified NYC social/review link found","Added by the second session")
def carry_flags(c):
    return [f for f in (c.get('flags') or []) if not any(f.startswith(s) or s in f for s in STALE)]

LIVE = {
 3: ["Sushi Sho","Jungsik New York","Eleven Madison Park","Le Bernardin","Per Se"],
 2: ["Atera","Saga","Joo Ok","César","Odo","Chef's Table at Brooklyn Fare","Atomix","Aska","Aquavit","Jean-Georges","Gabriel Kreuther","Masa","Sushi Noz","The Modern"],
}
ONE = ["Le Coucou","Muku","Huso","Yamada","Bridges","Corima","Jua","Frevo","Torien","Tempura Matsui","Estela","Sushi Nakazawa New York","Noda","Jeju Noodle Bar","Semma","Yoshino","Cote","Crown Shy","Shmoné","Gramercy Tavern","Oiji Mi","Family Meal at Blue Hill","Dirt Candy","Tuome","Bar Miller","bōm","Noz 17","Torrisi","Casa Mono","Kosaka","Sixty Three Clinton","Nōksu","Icca","L'Abeille","Tsukimi","Rezdôra","Francie","Oxomoco","The Four Horsemen","Shota Omakase","Restaurant Yuu","Le Pavillon","Kochi","Café Boulud at Maison Barnes","Jōji","YingTao","Daniel","Essential by Christophe","Mari","Meju"]
# NOTE: kit spells odo as "Odo"; live list shows "odo". Normalize below.

KIT_LOWER = {k.lower(): v for k, v in kitrows.items()}
CANON_LOWER = {k.lower(): v for k, v in canonrows.items()}
ALIAS = {"sixty three clinton": "63 clinton"}
def kitrow(name):
    return kitrows.get(name) or KIT_LOWER.get(name.lower()) or kitrows.get(ALIAS.get(name.lower(),''), {})
def canonrow(name):
    return canonrows.get(name) or CANON_LOWER.get(name.lower()) or {}

def murl(name):
    k = kitrow(name)
    if k and k.get('michelin_url'): return k['michelin_url']
    return ""

def base(name, stars):
    k = kitrow(name)
    c = canonrow(name)
    distinction = f"{stars} MICHELIN Star{'s' if stars>1 else ''}"
    return {
        "name": name, "distinction": distinction,
        "cuisine": c.get('cuisine') or k.get('cuisine') or "",
        "address": c.get('address') or k.get('address') or "",
        "area": c.get('area') or (k.get('area','')+" (address-based grouping)" if k.get('area') else ""),
        "hours": c.get('hours') or "",
        "exceptions": c.get('exceptions') or "",
        "guidePriceBand": k.get('price_band',''),
        "priceTwoAdults": "", "priceNote": "", "priceSourceUrl": "",
        "officialUrl": c.get('officialUrl') or k.get('website') or "",
        "sourceUrl": c.get('sourceUrl') or murl(name),
        "social": list(c.get('social') or []),
        "flags": carry_flags(c),
    }

rows=[]
for stars,names in LIVE.items():
    for n in names: rows.append(base(n,stars))
for n in ONE: rows.append(base(n,1))
R={r['name']:r for r in rows}

def setp(name, total, note, src):
    R[name]['priceTwoAdults']=total; R[name]['priceNote']=note; R[name]['priceSourceUrl']=src
def addsocial(name, platform, url, note):
    R[name]['social'].append({"platform":platform,"url":url,"note":note})
def detail(name, **kw):
    R[name].update(kw)

# ---------------- 3-star ----------------
setp("Eleven Madison Park","$770 (Full Tasting, 2 x $385); $510 (Bar Tasting, 2 x $255)",
     "Official FAQ: Full Tasting $385/guest, Bar Tasting $255/guest; wine pairing from $125/guest; gratuity not included; all sales final/non-refundable; reservations open 1st of month for following month.",
     "https://www.elevenmadisonpark.com/faq")
R["Eleven Madison Park"]['exceptions']="No dress code. Reservations open on the 1st of each month for the following month; all sales final and non-refundable. Gratuity not included."
R["Eleven Madison Park"]['social']=[s for s in R["Eleven Madison Park"]['social'] if 'jalexanders' not in s.get('url','')]
R["Eleven Madison Park"]['flags'].append("Corrected 2026-11-25: canonical data listed facebook.com/jalexandersrestaurantscollection (a different restaurant group) as EMP's Facebook; removed as unverified. Official Instagram retained (handle printed on the Resy venue page MICHELIN links).")

setp("Jungsik New York","$670 (Signature Menu, 2 x $335)",
     "Official menu page: SIGNATURE MENU 335; wine pairings 225/600, mixed 175, NA 145. Entire table must participate.",
     "https://www.jungsik.com/menu/")
setp("Le Bernardin","$700 (Chef's Tasting, 2 x $350); $436 (Dinner prix fixe, 2 x $218); $284 (Lunch prix fixe, 2 x $142)",
     "Official dinner menu PDF (dinner-1.2.pdf): dinner 4-course $218/person. Chef's Tasting $350 ($530 w/ wine pairing); Lunch 3-course $142. Supplements extra (caviar $145/oz). Reconciled with session 6f217cce: an earlier accessible-page capture showed $225 dinner, but the current official PDF states $218 and is used.",
     "https://www.le-bernardin.com/content/pdfs/dinner-1.2.pdf")
# Per Se: price NOT confirmed on any reachable official page -> blank + flag
R["Per Se"]['priceNote']="Official Tock channel shows a $200/person deposit (Main Dining Room) and $150/person deposit (Salon); the tasting-menu price itself is not printed on the reachable Tock/Thomas Keller pages. A $425 figure appears only in a search snippet and is NOT used."
R["Per Se"]['flags'].append("Couple price unverified: official pages show only the $200/person deposit, not the menu price; $425 search-snippet figure not used. Confirm by phone or at booking.")
addsocial("Per Se","Instagram (official)","https://www.instagram.com/perseny/","Printed on the restaurant's official Tock booking page")
addsocial("Per Se","Facebook (official)","https://www.facebook.com/perse","Printed on the restaurant's official Tock booking page")
addsocial("Per Se","X/Twitter (official)","https://www.twitter.com/PerSeNY","Printed on the restaurant's official Tock booking page")
R["Sushi Sho"]['flags'] += ["Official website not listed by Michelin (phone only)","Couple price unverified: no official menu price published","No verified NYC social/review link found; similar-name YouTube results refer to a different city"]

# ---------------- 2-star ----------------
detail("Aska", address="47 S. 5th St., Brooklyn, NY 11249", area="Williamsburg, Brooklyn (address-based grouping)",
  hours="Mon closed; Tue-Sun 17:00-23:00", officialUrl="https://askanyc.com/",
  sourceUrl="https://guide.michelin.com/en/new-york-state/brooklyn/restaurant/aska",
  exceptions="This establishment manages its own bookings; contact the restaurant directly (MICHELIN).")
addsocial("Aska","Instagram (official)","https://instagram.com/askanyc","Printed in the footer of askanyc.com")
addsocial("Aska","Facebook (official)","https://www.facebook.com/askanyc/","Printed in the footer of askanyc.com")
addsocial("Aska","X/Twitter (official)","https://twitter.com/askanyc","Printed in the footer of askanyc.com")
R["Aska"]['flags'].append("Couple price unverified: official menu price not published on reachable page")

detail("César", address="333 Hudson St., New York, NY 10013", area="Hudson Square / West Village (address-based grouping)",
  hours="Mon-Fri 18:00-23:00; Sat-Sun 17:30-23:00", officialUrl="https://www.cesar.restaurant/",
  sourceUrl="https://guide.michelin.com/en/new-york-state/new-york/restaurant/cesar")
R["César"]['flags'].append("Couple price unverified: Chef's Tasting offered but no price printed on reachable official page")

detail("Chef's Table at Brooklyn Fare", address="431 W. 37th St., New York, NY 10018", area="Hell's Kitchen / Midtown West (address-based grouping)",
  hours="Mon closed; Tue-Thu 18:00-23:00, Fri-Sun 17:00-23:00 (MICHELIN). Seatings (official site): Tue-Thu 18:00/18:30/19:00/19:30; Fri-Sat 17:00/17:30/20:30/20:45; Sun 17:00/17:30/18:00/18:30.",
  officialUrl="https://www.brooklynfare.com/chefs-table/",
  sourceUrl="https://guide.michelin.com/en/new-york-state/new-york/restaurant/chef-s-table-at-brooklyn-fare")
setp("Chef's Table at Brooklyn Fare","$770 (tasting, 2 x $385)",
     "Official site: tasting $385 USD plus tax; service and wine not included; $200 deposit. NA pairing $215; corkage $175 (750mL, max 2).",
     "https://www.brooklynfare.com/chefs-table/")
R["Chef's Table at Brooklyn Fare"]['exceptions']="Seafood-focused; cannot accommodate vegan/vegetarian/celiac/kosher/no-seafood or soy/mushroom/lemon/lime allergies. $200 deposit; parties 15+ min late may miss courses."

setp("Gabriel Kreuther","$650 (Chef's Tasting, 2 x $325); $400 (3-course, 2 x $200); $470 (4-course, 2 x $235)",
     "Official dinner menu PDF (11.17.26): Chef's Tasting 325; 3-course 200; 4-course 235. Wine pairings Classic 255 / Reserve 595.",
     "https://cdn.prod.website-files.com/69f8cb7ff67007b4842004ce/6afddf36f7cde3e50d030e4c_RGK_DinnerMenu%2011.17.26.pdf")

detail("Joo Ok", address="22 W. 32nd St., 16th Fl., New York, NY 10001", area="Koreatown / Midtown (address-based grouping)",
  hours="Mon-Sat 17:30-23:30; Sun closed", officialUrl="https://www.joo-ok.com/",
  sourceUrl="https://guide.michelin.com/en/new-york-state/new-york/restaurant/joo-ok-1214822")
R["Joo Ok"]['flags'].append("Couple price unverified: no official menu price published on reachable page")

detail("Masa", address="10 Columbus Circle, Ste. 401, New York, NY 10019", area="Columbus Circle (address-based grouping)",
  hours="Mon & Sun closed; Tue-Sat 12:00-14:30 and 17:30-22:00", officialUrl="https://www.masanyc.com/",
  sourceUrl="https://guide.michelin.com/en/new-york-state/new-york/restaurant/masa")
setp("Masa","$990 (Lunch Omakase, 2 x $495); $1,500 (Table Omakase, 2 x $750); $1,900 (Hinoki Counter, 2 x $950)",
     "Official menus page: Lunch from 495, Table 750, Hinoki Counter 950 per person; excluding beverages, tax, optional gratuity. Corkage $300/bottle (max 2).",
     "https://www.masanyc.com/menus")
R["Masa"]['exceptions']="Casually elegant attire encouraged; no strong fragrances. Gratuity not included, never required. ~2 hours."

detail("Odo", address="17 W. 20th St., New York, NY 10011", area="Flatiron (address-based grouping)",
  hours="Mon closed; Tue-Sun 12:00-13:45 and 18:00-20:30", officialUrl="https://www.odo.nyc/",
  sourceUrl="https://guide.michelin.com/en/new-york-state/new-york/restaurant/odo",
  exceptions="Cannot accommodate vegan/vegetarian/gluten-free or guests who cannot consume seafood/seaweed; contact the restaurant directly.")
setp("Odo","$300 (Lunch Kaiseki, 2 x $150); $540 (Dinner Kaiseki, 2 x $270)",
     "Official menu page (odo.nyc/menu): Lunch 6-course 150/guest (seatings 12:00/13:45); Dinner 8-9 course 270/guest (seatings 18:00/20:30). Re-verified 2026-11-25; corroborates session 6f217cce's capture.",
     "https://www.odo.nyc/menu")

detail("Saga", address="70 Pine St., New York, NY 10005", area="Financial District (address-based grouping)",
  hours="Daily 17:00-21:30", officialUrl="https://www.saga-nyc.com/",
  sourceUrl="https://guide.michelin.com/en/new-york-state/new-york/restaurant/saga")
R["Saga"]['flags'].append("Couple price unverified")

detail("Sushi Noz", address="181 E. 78th St., New York, NY 10075", area="Upper East Side (address-based grouping)",
  hours="Mon-Sat 17:45-23:00; Sun closed", officialUrl="https://www.sushinoz.com/",
  sourceUrl="https://guide.michelin.com/en/new-york-state/new-york/restaurant/sushi-noz")
R["Sushi Noz"]['flags'].append("Couple price unverified")

detail("The Modern", address="9 W. 53rd St., New York, NY 10019", area="Midtown / MoMA (address-based grouping)",
  hours="Mon-Thu & Sun 12:00-14:30 and 17:00-21:00; Fri-Sat 12:00-14:30 and 17:00-21:30",
  officialUrl="https://www.themodernnyc.com/the-modern/",
  sourceUrl="https://guide.michelin.com/en/new-york-state/new-york/restaurant/the-modern")
setp("The Modern","$230 (Lunch prix fixe, 2 x $115); $510 (Lunch Tasting, 2 x $255); $370 (Impressions, 2 x $185); $570 (Abstractions, 2 x $285)",
     "Official menu page: Lunch 3-course 115, Lunch Tasting 255; dinner Impressions 185, Abstractions 285; Kitchen Table 345. Beverages, tax, gratuity extra.",
     "https://www.themodernnyc.com/the-modern/")
R["The Modern"]['flags']=[f for f in R["The Modern"]['flags'] if 'Hours unverified' not in f]

R["Aquavit"]['officialUrl']="https://www.aquavit.org/"
setp("Aquavit","$390 (dinner tasting, 2 x $195)",
     "Official dinner menu PDF (DR 11.20.26, linked from aquavit.org): tasting 195/person; wine pairing 145, reserve 295, NA 75. Re-verified 2026-11-25; corroborates session 6f217cce's capture.",
     "https://www.aquavit.org/s/DR-112026.pdf")
R["Atera"]['flags'].append("Couple price unverified: official site unreachable; third-party reports conflict ($195/$235/$298) - not used")
R["Atomix"]['officialUrl']="https://www.atomixnyc.com/"
R["Atomix"]['flags'].append("Couple price unverified: third-party reports conflict ($295/$375) - not used; official menu page client-rendered")
R["Jean-Georges"]['officialUrl']="https://www.jean-georgesrestaurant.com/"
R["Jean-Georges"]['flags'].append("Couple price unverified: official menu price not captured")

# ---------------- 1-star ----------------
detail("Jua", address="36 E. 22nd St., New York, NY 10010", area="Flatiron (address-based grouping)",
  hours="Mon closed; Tue-Sun 18:00-23:00", officialUrl="https://juanyc.com/",
  sourceUrl="https://guide.michelin.com/en/new-york-state/new-york/restaurant/jua")
setp("Jua","$300 (seven-course tasting, 2 x $150)",
     "Official menu page (Nov 2026): seven-course tasting 150; wine pairing (6) 110; NA pairing 85. Supplements: uni kim +32, abalone +20.",
     "https://juanyc.com/menu")

detail("Cote", address="16 W. 22nd St., New York, NY 10010", area="Flatiron (address-based grouping)",
  hours="Open 7 days: Sun-Wed 17:00-23:00; Thu-Sat 17:00-24:00 (official location-page FAQ, agrees with MICHELIN)",
  officialUrl="https://www.cotekoreansteakhouse.com/",
  exceptions="$50/person late-cancellation/no-show fee within 24h; standard reservations for 2-6 via Resy; seat completed parties only.",
  sourceUrl="https://guide.michelin.com/en/new-york-state/new-york/restaurant/cote")
setp("Cote","$168 (Butcher's Feast, 2 x $84); $450 (Steak Omakase, 2 x $225)",
     "Official NYC dinner menu: Butcher's Feast 84/person (A5 wagyu +32); Steak Omakase 225/person (wine pairing 110). A la carte steaks also available.",
     "https://www.cotekoreansteakhouse.com/nycdinnermenu")

setp("Gramercy Tavern","$356 (Dining Room Seasonal Menu, 2 x $178); $156 (Tavern 3-course, 2 x $78)",
     "Official dining-room menu: Seasonal Menu 178/person, wine pairing 118; Tavern a la carte 3-course 78. Tavern total varies by dishes chosen.",
     "https://www.gramercytavern.com/dining-room-menu/")

detail("Kochi", address="652 10th Ave., New York, NY 10036", area="Hell's Kitchen (address-based grouping)",
  hours="Mon-Thu 17:00-21:30; Fri-Sat 17:00-22:00; Sun 17:00-21:30", officialUrl="https://www.kochinyc.com/",
  sourceUrl="https://guide.michelin.com/en/new-york-state/new-york/restaurant/kochi")
setp("Kochi","$290 (tasting, 2 x $145)",
     "Official menu page: TASTING MENU 145; beverage pairing 110. Cannot accommodate vegan/celiac or allium/sesame/soy/gluten/alcohol allergies.",
     "https://www.kochinyc.com/menu/")

detail("Mari", address="679 Ninth Ave., New York, NY 10036", area="Hell's Kitchen (address-based grouping)",
  hours="Mon-Thu 17:00-21:30; Fri-Sat 17:00-22:00; Sun 17:00-21:30", officialUrl="https://marinyc.com/",
  sourceUrl="https://guide.michelin.com/en/new-york-state/new-york/restaurant/mari")
setp("Mari","$290 (tasting, 2 x $145)",
     "Official homepage menu: MARI TASTING MENU 145; WINE PAIRING 110.",
     "https://marinyc.com/")

detail("Dirt Candy", address="86 Allen St., New York, NY 10002", area="Lower East Side (address-based grouping)",
  hours="Mon & Sun closed; Tue-Sat 17:30-22:30", officialUrl="https://www.dirtcandynyc.com/",
  sourceUrl="https://guide.michelin.com/en/new-york-state/new-york/restaurant/dirt-candy")
R["Dirt Candy"]['flags'].append("Couple price unverified: official menu page not reachable; single tasting menu offered")

detail("Sushi Nakazawa New York", address="23 Commerce St., New York, NY 10014", area="Greenwich Village (address-based grouping)",
  hours="Daily 11:30-14:00 and 17:00-22:00", officialUrl="https://www.sushinakazawa.com/new-york",
  sourceUrl="https://guide.michelin.com/en/new-york-state/new-york/restaurant/sushi-nakazawa")
R["Sushi Nakazawa New York"]['flags'].append("Couple price unverified: official site is client-rendered")

detail("Semma", address="60 Greenwich Ave., New York, NY 10011", area="West Village (address-based grouping)",
  hours="Mon-Sat 17:00-22:00; Sun closed", officialUrl="https://www.semma.nyc/", guidePriceBand="$$$",
  sourceUrl="https://guide.michelin.com/en/new-york-state/new-york/restaurant/semma")
R["Semma"]['flags']=[f for f in R["Semma"]['flags'] if 'Hours unverified' not in f]
R["Semma"]['priceNote']="MICHELIN best-of guide (updated 27 Jul 2026) lists Semma among five starred restaurants at roughly $75/person (~$150 for two) - an indicative Guide estimate, not a menu quote. A la carte; exact couple total not published."
R["Semma"]['priceSourceUrl']="https://guide.michelin.com/en/best-of/least-expensive-one-michelin-star-restaurants-in-new-york"
R["Semma"]['flags'].append("Exact couple price unverified (a la carte); MICHELIN estimates ~$75/person in its least-expensive starred list")

detail("Sixty Three Clinton", address="63 Clinton St., New York, NY 10002", area="Lower East Side (address-based grouping)",
  hours="Mon & Sun closed; Tue-Sat 18:00-23:00", officialUrl="https://www.63clinton.com/", cuisine="Contemporary", guidePriceBand="$$$$",
  sourceUrl="https://guide.michelin.com/en/new-york-state/new-york/restaurant/63-clinton")
R["Sixty Three Clinton"]['flags'].append("Couple price unverified: tasting menu offered but no price captured")

# Michelin least-expensive best-of (official Guide estimate ~$75/person, Jul 2026)
BESTOF="https://guide.michelin.com/en/best-of/least-expensive-one-michelin-star-restaurants-in-new-york"
for n,addr,band in [("Casa Mono","52 Irving Pl., New York, NY 10003","$$$"),
                    ("Crown Shy","70 Pine St., New York, NY 10005","$$$"),
                    ("Jeju Noodle Bar","679 Greenwich St., New York, NY 10014","$$$"),
                    ("Tuome","536 E. 5th St., New York, NY 10009","$$$")]:
    detail(n, address=addr, guidePriceBand=band)
    R[n]['priceNote']="MICHELIN best-of guide (updated 27 Jul 2026) lists this restaurant among five starred spots at roughly $75/person (~$150 for two) - an indicative Guide estimate, not a menu quote. A la carte; exact couple total not published."
    R[n]['priceSourceUrl']=BESTOF
    R[n]['flags'].append("Exact couple price unverified (a la carte); MICHELIN estimates ~$75/person in its least-expensive starred list")

detail("Le Coucou", officialUrl="https://lecoucou.com/")
setp("Le Coucou","$440 (A Very Coucou Dinner, 2 x $220)",
     "Official menu (lecoucou.com/#menus): A Very Coucou Dinner 220/person; wine accompaniment 145/345, NA pairing 115; tax & gratuity not included. Lunch 2-course 81 / 3-course 125 / A Very Coucou Lunch 150. Re-verified 2026-11-25; corroborates session 6f217cce's capture.",
     "https://lecoucou.com/#menus")

# ---------------- verified Michelin price bands (detail pages captured this session) ----------------
BANDS = {n:"$$$$" for n in ["Cote","Aska","César","Chef's Table at Brooklyn Fare","Joo Ok","Masa","Odo","Saga","Sushi Noz","The Modern","Jua","Mari","Dirt Candy","Sushi Nakazawa New York","Sixty Three Clinton"]}
for n,b in BANDS.items():
    R[n]['guidePriceBand']=b

# ---------------- generic flags ----------------
for r in rows:
    if not r['hours']:
        r['flags'].append("Hours not transcribed this session - open the linked MICHELIN page for the live schedule")
    if not r['address']:
        r['flags'].append("Address not transcribed this session - see MICHELIN page")
    if not r['priceTwoAdults'] and not any('price' in f.lower() for f in r['flags']):
        r['flags'].append("Couple price unverified: no official menu price captured this session (a la carte or menu not reachable)")
    if not r['social']:
        r['flags'].append("No official social account verified this session; see MICHELIN/official site")
    r['flags']=list(dict.fromkeys(r['flags']))

# keep the three guide-listed new-addition rows from canonical (clearly marked, no star)
for n in ["Odo East Village","Cynthia","Len Len"]:
    if n in canonrows:
        r=dict(canonrows[n]); r['flags']=list(dict.fromkeys(r.get('flags',[])))
        rows.append(r)

meta={
 "checkedOn":"2026-11-25",
 "session":"arena/fc6d5f66-nyfun2",
 "sourceOfTruth":"Live MICHELIN Guide all-starred list (pages 1-2) + individual MICHELIN restaurant pages + official restaurant websites/menu pages",
 "starListSource":"https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred",
 "starCounts":"5 three-star, 14 two-star, 50 one-star = 69 starred (live filter counters, re-verified 2026-11-25). Plus 3 Guide-listed new-addition rows (no star) = 72 total rows.",
 "rosterReconciliation":"The namespaced kit sessions/33cfdba4 carried 72 rows but 3 (Blue Hill at Stone Barns, Shion 69 Leonard Street, La Bastide by Andrea Calstier) are NOT in the live all-starred selection; excluded here and flagged. This canonical roster is the live 69 starred + 3 guide-listed.",
 "importantTiming":"Michelin's 2026 Northeast Cities ceremony is scheduled for 2026-12-14 (https://michelinmedia.com/pages/blog/detail/article/c/a1479/), after this research and before the trip. Distinctions may change.",
 "priceNote":"priceTwoAdults = 2 x a per-person price printed on an official restaurant page (menu/FAQ/booking channel); food only, before tax, tip and beverages unless noted. Arithmetic and the exact source URL are in priceNote/priceSourceUrl and on the Michelin page's price-verification table. A-la-carte restaurants and unreachable prices stay blank and flagged. Michelin's $ band is shown separately as guidePriceBand. Menus were captured Nov 2026; re-confirm for the Feb-Mar 2027 trip.",
 "hoursNote":"Hours transcribed from MICHELIN detail pages or the restaurant's own site. Rows not yet transcribed are blank and flagged; the linked MICHELIN page shows the live schedule.",
 "socialNote":"Social links labelled (official) were read from the restaurant's own site or its official booking channel. Third-party review links are labelled as such and are not official endorsements.",
 "hoursCrossCheck":canon.get('meta',{}).get('hoursCrossCheck','')
}
out={"meta":meta,"items":rows}
(ROOT/'data/restaurants.json').write_text(json.dumps(out,indent=2,ensure_ascii=False))
print("rows:",len(rows))
from collections import Counter
print(Counter(r['distinction'] for r in rows))
print("with price:",sum(1 for r in rows if r['priceTwoAdults']))
print("with hours:",sum(1 for r in rows if r['hours']))
print("with social:",sum(1 for r in rows if r['social']))
print("with address:",sum(1 for r in rows if r['address']))
