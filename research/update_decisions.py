import json, pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
p=ROOT/'data/decisions.json'
d=json.loads(p.read_text())
def find(k,i): return next(x for x in d[k] if x['id']==i)

q6=find('questions','Q6')
q6['whatWeKnow']="15 restaurants now have a couple total verified from an official menu/FAQ/booking page (food only, pre-tax/tip/beverages), reconciled across sessions fc6d5f66 and 6f217cce: EMP $770/$510; Le Bernardin $700/$436/$284; Jungsik $670; Masa $990/$1,500/$1,900; Gabriel Kreuther $650/$400/$470; The Modern $230/$510/$370/$570; Chef's Table BF $770; Aquavit $390; odo $300/$540; Cote $168/$450; Kochi $290; Mari $290; Jua $300; Gramercy Tavern $356/$156; Le Coucou $440. Michelin's least-expensive list groups Casa Mono, Crown Shy, Jeju Noodle Bar, Semma, Tuome at ~$75/person (indicative)."
q6['whatWeDoNotKnow']="2027 menu prices (menus captured Nov 2026), beverage pairings, service charge, tax and cancellation policies for the trip dates; exact prices for Per Se, Sushi Sho, Atera, Atomix, Jean-Georges, César, Joo Ok, Saga, Sushi Noz and most a-la-carte one-stars."
q6['provisionalAnswer']="Use the verified couple totals on the Michelin page as a planning floor; re-confirm at booking. Per Se shows only a $200/person deposit officially, so its menu price stays blank."
q6['sources']=[
 "https://www.elevenmadisonpark.com/faq",
 "https://www.le-bernardin.com/accessible/menus/dining-room/chef-s-tasting/",
 "https://www.masanyc.com/menus",
 "https://www.themodernnyc.com/the-modern/",
 "https://www.brooklynfare.com/chefs-table/",
 "https://guide.michelin.com/en/best-of/least-expensive-one-michelin-star-restaurants-in-new-york"
]

q8=find('questions','Q8')
q8['whatWeKnow']="Official accounts confirmed from the venues' own pages: MoMA @themuseumofmodernart; The Met @metmuseum; AMNH @amnh; Empire State Building @empirestatebldg (incl. verified TikTok); Whitney @whitneymuseum; Guggenheim; 9/11 Memorial @911Memorial; High Line @highlinenyc; NYPL @nypl. Restaurants: Per Se (Tock), Aska (site footer), Eleven Madison Park and Le Bernardin (Resy venue pages). NYC Parks and NPS link their own accounts."
q8['whatWeDoNotKnow']="Official account ownership for the remaining restaurants/venues; whether linked third-party reviews still represent current menus/hours."
q8['sources']=[
 "https://www.moma.org/about/about-this-site",
 "https://www.metmuseum.org/press/news/2014/webby-awards",
 "https://www.esbnyc.com/press/visit-empire-state-building-observatory-holiday-season",
 "https://www.thehighline.org/",
 "https://www.nypl.org/blog/2019/08/20/nypl-insta-novels",
 "https://www.exploretock.com/perse/faq",
 "https://www.askanyc.com/"
]

f11=find('flags','F11')
f11['severity']="Low"
f11['title']="RESOLVED 2026-11-25: starred catalogue now covers the full live roster (69 of 69)"
f11['detail']="The canonical restaurants.json now holds all 69 live starred restaurants (5 three-star, 14 two-star, 50 one-star) plus 3 Guide-listed new additions (72 rows). Three kit-only names (Blue Hill at Stone Barns, Shion 69 Leonard Street, La Bastide by Andrea Calstier) are not in the live all-starred selection and were excluded/flagged. Cluster statements can now use the full census; travel times still require real routing."

f13=find('flags','F13')
f13['title']="Airfare and theatre remain unpriced; restaurant menu prices PARTIALLY resolved"
f13['detail']="12 restaurants now have verified couple totals from official pages (see Q6 / Michelin page), so the largest dining line items are no longer wholly unpriced. Still unpriced: flights, theatre tickets, and exact menu prices for Per Se, Sushi Sho, Aquavit, Atera, Atomix, Jean-Georges and most a-la-carte one-stars. Menus were captured Nov 2026 and must be re-confirmed for Feb-Mar 2027. No grand total is claimed."

find('suggestions','S3')['status']="Partially implemented 2026-11-25 - 12 official-menu couple totals captured with sources and capture date; remainder blank/flagged"
find('suggestions','S10')['status']="Implemented 2026-11-25 - full live roster of 69 starred + 3 Guide-listed rows catalogued"

newflags=[
 {"id":"F14","severity":"Medium","title":"Per Se menu price not published on official pages",
  "detail":"Per Se's official Tock channel and Thomas Keller site print only a $200/person deposit (Main Dining Room) and $150/person deposit (Salon), not the tasting-menu price. A $425 figure appears only in a search snippet and was NOT used. priceTwoAdults left blank and flagged; confirm by phone or at booking.",
  "source":"https://www.exploretock.com/perse/faq"},
 {"id":"F15","severity":"Medium","title":"Atomix and Atera third-party price reports conflict - not used",
  "detail":"Official sites for Atomix (client-rendered) and Atera (unreachable) yielded no price. Third-party blogs report Atomix $295/$375 and Atera $195/$235/$298. These conflict and are not official, so both couple totals stay blank and flagged rather than guessed.",
  "source":"https://guide.michelin.com/en/new-york-state/new-york/restaurant/atomix"},
 {"id":"F16","severity":"Low","title":"Corrected wrong Facebook link for Eleven Madison Park",
  "detail":"Canonical data listed facebook.com/jalexandersrestaurantscollection (a different restaurant group) as EMP's Facebook. Removed as unverified on 2026-11-25. EMP's official Instagram (elevenmadisonpark, printed on the Resy venue page MICHELIN links) is retained.",
  "source":"https://www.elevenmadisonpark.com/faq"},
 {"id":"F17","severity":"Medium","title":"Menu prices captured Nov 2026 vs Feb-Mar 2027 trip",
  "detail":"All verified restaurant menu prices were captured 2026-11-25 (Nov 2026 menus). The trip is Feb 15-Mar 23 2027, so prices may change. Every couple total must be re-confirmed on the official page at booking; the Michelin 14 Dec 2026 ceremony may also change distinctions.",
  "source":"https://michelinmedia.com/pages/blog/detail/article/c/a1479/"}
]
have={f['id'] for f in d['flags']}
for f in newflags:
    if f['id'] not in have: d['flags'].append(f)

d['checkedOn']="2026-11-25"
p.write_text(json.dumps(d,indent=2,ensure_ascii=False))
print("questions",len(d['questions']),"suggestions",len(d['suggestions']),"flags",len(d['flags']))
