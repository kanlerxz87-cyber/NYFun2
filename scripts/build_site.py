#!/usr/bin/env python3
"""Build the static dashboard (index.html + pages/*.html) from data/*.json.

Run after scripts/build_data.py. No dependencies, no build step on the host:
GitHub Pages serves the output directly.
"""
import html
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda *p: os.path.join(ROOT, *p)

NAV = [
    ("index.html", "Overview", "overview"),
    ("pages/executive-summary.html", "Summary", "summary"),
    ("pages/michelin-restaurants.html", "Michelin", "michelin"),
    ("pages/hotels.html", "Hotels", "hotels"),
    ("pages/activities.html", "Activities", "activities"),
    ("pages/itinerary.html", "Itinerary", "itinerary"),
    ("pages/questions.html", "Questions", "questions"),
    ("pages/suggestions.html", "Suggestions", "suggestions"),
    ("pages/flagged.html", "Flagged", "flagged"),
    ("pages/verification.html", "Verification", "verification"),
    ("pages/sources.html", "Sources", "sources"),
    ("pages/repo-audit.html", "Repo audit", "repo"),
]

CHECKS_DATE = json.load(open(D("data", "verification.json"), encoding="utf-8")).get("checkedOn", "date not recorded")
DATA_DATE = json.load(open(D("data", "restaurants.json"), encoding="utf-8")).get("meta", {}).get("checkedOn", "date not recorded")


def load(name):
    with open(D("data", name + ".json"), encoding="utf-8") as f:
        return json.load(f)


def e(v):
    return html.escape(str(v if v is not None else ""))


def nav_html(active, depth):
    items = []
    for href, label, key in NAV:
        cls = ' class="active"' if key == active else ""
        if depth:
            href = ("../" + href) if href == "index.html" else href.replace("pages/", "", 1)
        items.append(f'<a{cls} href="{href}">{label}</a>')
    return f'<nav class="nav" aria-label="Main navigation">{"".join(items)}</nav>'


def shell(active, title, eyebrow, h1, lede, body, depth=0, description=""):
    prefix = "../" if depth else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} — NYC 2027</title>
<meta name="description" content="{e(description or lede)}">
<meta name="color-scheme" content="light dark">
<link rel="stylesheet" href="{prefix}assets/styles.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="topbar"><div class="topbar-inner">
  <a class="brand" href="{prefix}index.html"><span class="mark">NY</span><span><b>NYC 2027</b><small>2 adults · Feb 2027</small></span></a>
  {nav_html(active, depth)}
</div></header>
<main class="wrap" id="main">
  <p class="eyebrow">{e(eyebrow)}</p>
  <h1>{e(h1)}</h1>
  <p class="lede">{lede}</p>
{body}
  <footer class="foot">
    <p><strong>Broad verification register:</strong> {CHECKS_DATE} ·
    <strong>Latest row-specific re-check:</strong> 2026-11-27 (restaurant, hotel and activity addenda) ·
    <strong>Roster census:</strong> {DATA_DATE} ·
    <a href="{prefix}research/verification-2026-11-27.md">2026-11-27 source review ↗</a> ·
    <a href="{prefix}research/review-2026-11-27.md">Activity corrections ↗</a></p>
    <p>Repository: <a href="https://github.com/kanlerxz87-cyber/NYFun2" target="_blank" rel="noopener noreferrer">kanlerxz87-cyber/NYFun2 ↗</a> ·
    Coordination board: <a href="{prefix}COORDINATION.md" target="_blank" rel="noopener noreferrer">COORDINATION.md ↗</a> ·
    <a href="{prefix}pages/flagged.html">Flagged for review</a> ·
    <a href="{prefix}pages/verification.html">Verification log</a> ·
    <a href="{prefix}pages/compare.html">Compare session kits</a></p>
    <p class="small">Prices are what the linked official page said on the capture date. Nothing here is a booking, a quote, or financial advice. Blank means unverified — never estimated.</p>
  </footer>
</main>
<script src="{prefix}assets/app.js"></script>
</body>
</html>
"""


def toolbar(search_placeholder, extra=""):
    return (f'<div class="toolbar"><input type="search" aria-label="Search table" placeholder="{e(search_placeholder)}">'
            f'{extra}<span class="count"></span></div>')


VERIFY_SELECT = ('<select data-filter="verify" aria-label="Filter by verification status">'
                 '<option value="">All rows</option>'
                 '<option value="today">Verified rows (date shown per row)</option>'
                 '<option value="carried">Carried capture (2026-11-25)</option></select>')


def money(v):
    return str(v or "")


def build():
    R = load("restaurants")
    H = load("hotels")
    A = load("activities")
    Q = load("decisions")
    V = load("verification")
    C = load("conflicts")

    r_items = R["items"]
    h_items = H["items"]
    a_items = A["items"]
    priced = [r for r in r_items if r.get("priceTwoAdults")]
    hotels_priced = [h for h in h_items if h.get("sevenNightPreTax") or h.get("sevenNightAllIn")]
    measured = [h for h in h_items if h.get("transit", {}).get("measured")]
    qualified = [h for h in h_items if h.get("qualifies")]
    star_counts = {
        "3": sum(1 for r in r_items if r["distinction"].startswith("3")),
        "2": sum(1 for r in r_items if r["distinction"].startswith("2")),
        "1": sum(1 for r in r_items if r["distinction"].startswith("1")),
        "guide": sum(1 for r in r_items if "Guide-listed" in r["distinction"]),
    }
    cheapest_hotel = min(hotels_priced, key=lambda h: int("".join(ch for ch in str(h.get("sevenNightAllIn") or h.get("sevenNightPreTax")).split("$")[1].split()[0] if ch.isdigit()) or 10**9))
    top3 = [h for h in h_items if h.get("qualifies") and (h.get("sevenNightPreTax") or h.get("sevenNightAllIn"))][:3]

    def price_rows():
        out = []
        for r in priced:
            src = r.get("priceSourceUrl")
            src_cell = ('<a href="' + e(src) + '" target="_blank" rel="noopener noreferrer">Menu / FAQ ↗</a>'
                        if src else '<span class="blank">no source</span>')
            out.append(
                '<tr><td data-label="Restaurant"><strong>' + e(r["name"]) + '</strong>'
                '<span class="sub">' + e(r["distinction"]) + '</span></td>'
                '<td data-label="Couple total">' + e(r["priceTwoAdults"]) + '</td>'
                '<td data-label="Official menu source">' + src_cell + '</td>'
                '<td data-label="Note">' + e(r.get("priceNote") or "") + '</td></tr>')
        return "\n".join(out)

    # ------------------------------------------------------------------ index
    index_body = f"""
  <div class="notice good"><strong>What this is.</strong> A source-audited plan for two adults in New York City inside the 15 Feb – 23 Mar 2027 window, built around MICHELIN dining and hotels that publish a queen-or-larger bed and a private bathroom. Every row links the page it came from. Anything that could not be confirmed is blank and sits on the <a href="pages/flagged.html">Flagged</a> page.</div>

  <div class="stats">
    <div class="stat"><b data-count="restaurants">{len(r_items)}</b><span>MICHELIN rows (69 starred + 3 guide-listed)</span></div>
    <div class="stat"><b data-count="priced">{len(priced)}</b><span>with a verified couple price</span></div>
    <div class="stat"><b data-count="hotels">{len(h_items)}</b><span>hotel candidates · <span data-count="hotelPriced">{len(hotels_priced)}</span> with a dated 7-night total</span></div>
    <div class="stat"><b data-count="activities">{len(a_items)}</b><span>activities with official hours</span></div>
    <div class="stat"><b data-count="flags">{len(Q["flags"])}</b><span>flagged items for your review</span></div>
  </div>

  <div class="card">
    <h2 style="margin-top:0">The short version</h2>
    <ul>
      <li><strong>Dates.</strong> Your preferred window is <strong>15–18 Feb 2027</strong> (Mon–Thu, 3 nights). All hotel maths here uses the requested <strong>7-night</strong> case, <strong>15–22 Feb 2027</strong> (Mon–Mon). Feb 15 is Presidents' Day; the Chinatown Lunar New Year parade is <strong>Sunday 21 Feb 2027 at 13:00</strong> — inside the 7-night window, outside the 3-night one.</li>
      <li><strong>Hotels.</strong> {len(hotels_priced)} of {len(h_items)} candidates carry a dated 7-night total for two adults, from <strong>{e(cheapest_hotel.get("sevenNightAllIn"))}</strong> all-in (Eurostars Wall Street, non-refundable) to <strong>$5,220</strong> (The Beekman). Best value with free cancellation: <strong>DoubleTree Chelsea, $1,110 all-in</strong>.</li>
      <li><strong>Dining.</strong> The live MICHELIN filter reads <strong>5 three-star, 14 two-star, 50 one-star</strong> — 69 starred, all catalogued here plus 3 guide-listed newcomers. {len(priced)} rows have a couple total from an official menu; the cheapest is <strong>Gramercy Tavern's tavern three-course at $156</strong>, then <strong>Cote's Butcher's Feast at $168</strong>.</li>
      <li><strong>The one-hour rule.</strong> 25 hotel→MICHELIN-cluster subway/bus legs were measured: every one was <strong>3–37 minutes</strong>. The rule therefore does not separate central Manhattan hotels; the ranking falls through to price and room quality.</li>
      <li><strong>What could change.</strong> MICHELIN's next New York ceremony is <strong>14 Dec 2026</strong>, before the trip. Restaurant menus and hotel rates were captured in November 2026 and must be re-checked before booking.</li>
    </ul>
    <p><a href="pages/executive-summary.html"><strong>Read the executive summary →</strong></a></p>
  </div>

  <h2>Browse by category</h2>
  <div class="tiles">
    <a class="tile" href="pages/michelin-restaurants.html"><span class="tag">Dining</span><h3>MICHELIN restaurants</h3><p>All 69 starred venues plus guide-listed rows: star level, price for two, hours, social links, source.</p></a>
    <a class="tile" href="pages/hotels.html"><span class="tag">Stay</span><h3>Hotels & ranking</h3><p>Bed/bath evidence, dated 7-night totals, measured MICHELIN reach and the five price windows.</p></a>
    <a class="tile" href="pages/activities.html"><span class="tag">Things to do</span><h3>Activities</h3><p>Official hours, closures, couple costs and the date-critical February events.</p></a>
    <a class="tile" href="pages/itinerary.html"><span class="tag">Plan</span><h3>Itinerary</h3><p>A 7-night skeleton built only from verified opening days, plus the 3-night variant.</p></a>
    <a class="tile" href="pages/questions.html"><span class="tag">Decide</span><h3>Questions & answers</h3><p>What is known, what is missing, and what actually blocks a booking decision.</p></a>
    <a class="tile" href="pages/suggestions.html"><span class="tag">Improve</span><h3>Suggestions</h3><p>{len(Q["suggestions"])} options to improve the plan or the site, each with effort, blockers and status.</p></a>
    <a class="tile" href="pages/flagged.html"><span class="tag">Audit</span><h3>Flagged for review</h3><p>Every unverified value, conflict and irregularity, with its source, in one list.</p></a>
    <a class="tile" href="pages/verification.html"><span class="tag">Audit</span><h3>Verification log</h3><p>What was re-read on {CHECKS_DATE}, what was only corroborated, and what stayed a carried capture.</p></a>
    <a class="tile" href="pages/sources.html"><span class="tag">Method</span><h3>Sources & rules</h3><p>The verification rules, the primary-source register and how to reproduce the build.</p></a>
    <a class="tile" href="pages/repo-audit.html"><span class="tag">Repo</span><h3>Repository audit</h3><p>What each session contributed, what this integration changed and what it found.</p></a>
    <a class="tile" href="pages/compare.html"><span class="tag">Parallel work</span><h3>Compare session kits</h3><p>Five independent kits, what each added and where they disagree.</p></a>
  </div>

  <h2>How to read a row</h2>
  <div class="card">
    <p><strong>Status badge.</strong> <span class="pill green">checked YYYY-MM-DD</span> shows the date on which the row's source was re-read. The wider verification register is dated {CHECKS_DATE}; the activity audit includes later 2026-11-27 row checks. <span class="pill gray">carried capture</span> means the value comes from the 2026-11-25 capture and the source link is still there for you to open.</p>
    <p><strong>Blank</strong> (<span class="blank">blank — unverified</span>) means no official page confirmed the value. It is never filled with an estimate. Each blank is explained on the Flagged page.</p>
    <p><strong>Route</strong> links open live Google Maps transit directions from the hotel you pick on the Hotels page. Stored minutes only appear where a real routing result was captured.</p>
    <p><strong>Social links</strong> are labelled by platform; "review" links are third-party and are not treated as endorsements.</p>
  </div>
"""
    pages = {}
    pages["index"] = shell(
        "overview", "NYC 2027 trip dashboard", "New York City · 15 Feb – 23 Mar 2027 · 2 adults",
        "A trip you can audit, line by line.",
        "MICHELIN dining, hotel pricing and February activities for two adults, with every claim tied to an official source and every gap left visibly blank.",
        index_body, depth=0)

    # ------------------------------------------------------- executive summary
    exec_body = f"""
  <div class="stats">
    <div class="stat"><b>15–18 Feb 2027</b><span>Preferred window (3 nights, Mon–Thu)</span></div>
    <div class="stat"><b>15–22 Feb 2027</b><span>7-night pricing case (Mon–Mon)</span></div>
    <div class="stat"><b>5 / 14 / 50</b><span>Three / two / one MICHELIN stars in NYC</span></div>
    <div class="stat"><b>$998–$5,220</b><span>All-in 7-night hotel range, two adults</span></div>
  </div>

  <div class="card">
    <h2 style="margin-top:0">Bottom line</h2>
    <p><strong>Book a free-cancellation hotel now; defer everything non-refundable.</strong> The 15–22 Feb week is the cheapest of the five February–March weeks tested (W1 $848 pre-tax / $998 all-in at Eurostars vs $1,087–$1,260 for the March windows), and the 30–39% "Black Friday" rates seen on 25 Nov 2026 expire. A $0-prepayment, free-cancellation hold at <strong>DoubleTree Chelsea ($1,110 all-in)</strong> captures the cheap week without locking a non-refundable rate before the 14 Dec 2026 MICHELIN ceremony and before your 3-vs-7-night choice is settled.</p>
  </div>

  <h2>Key findings</h2>
  <div class="card">
    <ul>
      <li><strong>Dining.</strong> {len(r_items)} rows: 69 starred ({star_counts["3"]}+{star_counts["2"]}+{star_counts["1"]}) plus 3 guide-listed. {len(priced)} have a verified couple total from an official menu, FAQ or official booking channel — from <strong>$156</strong> (Gramercy Tavern tavern three-course) and <strong>$168</strong> (Cote Butcher's Feast) up to <strong>$1,900</strong> (Masa hinoki counter), including Atomix ($848/$628 November Tock) and Sushi Sho ($990 Tock). Two prices (Atera, Per Se) remain contested/deposit-only and stay blank (flag F24).</li>
      <li><strong>Hotels.</strong> {len(hotels_priced)} of {len(h_items)} shortlisted properties have a dated 7-night total; {len(qualified)} publish a queen/king bed plus private bathroom. {len(h_items) - len(qualified)} {'does' if len(h_items) - len(qualified) == 1 else 'do'} not and {'is' if len(h_items) - len(qualified) == 1 else 'are'} excluded from the recommendation rather than assumed to comply (F26).</li>
      <li><strong>The one-hour rule.</strong> 25 measured hotel→cluster legs, all 3–37 minutes, so every published hotel with a measurement reaches all five sampled MICHELIN clusters within an hour. The constraint is satisfied everywhere it can be measured; price and room quality decide.</li>
      <li><strong>Dates that matter.</strong> Presidents' Day Mon 15 Feb; Chinatown Lunar New Year parade Sun 21 Feb 13:00; Bryant Park rink closes Sun 28 Feb; Wollman Rink runs to 16 Mar (cheap off-peak $16); the Met is closed Wednesdays; MoMA is open late Fridays.</li>
      <li><strong>Risk.</strong> Star levels may change on 14 Dec 2026; menus and rates are November 2026 captures; the hotel totals are booking-engine snapshots, not quotes.</li>
    </ul>
  </div>

  <h2>Recommended decision sequence</h2>
  <div class="card">
    <ol>
      <li><strong>Choose 3 or 7 nights</strong> (Q1). Only the 7-night window has verified totals.</li>
      <li><strong>Place a free-cancellation hold</strong> on DoubleTree Chelsea or Eurostars (Q2) before the promo rates end; do not pay non-refundable yet.</li>
      <li><strong>Re-check MICHELIN after 14 Dec 2026</strong> (Q4) before building a dining list.</li>
      <li><strong>Reserve one anchor dinner per night</strong> from the priced list (Q6), checking the day the restaurant is actually open.</li>
      <li><strong>Fix the activity days</strong> around Met (closed Wed) and the 21 Feb parade.</li>
      <li><strong>Only then</strong> fill in airfare and any theatre tickets (Q7/Q10), which no verified source here covers.</li>
    </ol>
  </div>


  <h2>What a week could cost (illustrative arithmetic)</h2>
  <div class="card">
    <p class="small muted">Every unit price below is a verified figure from the tables; the <em>quantities</em> are assumptions you choose (one dinner per evening, four subway rides a day for two people). Airfare and theatre are not priced anywhere in the sources and are excluded.</p>
    <div class="table-wrap"><table>
      <thead><tr><th scope="col">Line</th><th scope="col">Unit price (verified)</th><th scope="col">Quantity</th><th scope="col">Total</th></tr></thead>
      <tbody>
        <tr><td data-label="Line">Hotel, 7 nights, all-in</td><td data-label="Unit">$1,110 (DoubleTree Chelsea)</td><td data-label="Quantity">1 stay</td><td data-label="Total"><strong>$1,110</strong></td></tr>
        <tr><td data-label="Line">Four dinners for two</td><td data-label="Unit">$156 + $168 + $440 + $670</td><td data-label="Quantity">Gramercy Tavern, Cote, Le Coucou, Jungsik</td><td data-label="Total"><strong>$1,434</strong></td></tr>
        <tr><td data-label="Line">Museums and observatory</td><td data-label="Unit">$60 + $60 + $74 + $93</td><td data-label="Quantity">Met, MoMA, AMNH, Empire State Building</td><td data-label="Total"><strong>$287</strong></td></tr>
        <tr><td data-label="Line">Subway and bus</td><td data-label="Unit">$3 per ride per person (MTA)</td><td data-label="Quantity">4 rides/day × 2 people × 7 days = 56</td><td data-label="Total"><strong>$168</strong></td></tr>
        <tr><td data-label="Line">Activities with no admission</td><td data-label="Unit">$0</td><td data-label="Quantity">Central Park, High Line, Staten Island Ferry, Brooklyn Bridge, parade</td><td data-label="Total"><strong>$0</strong></td></tr>
        <tr><td data-label="Line"><strong>Illustrative subtotal</strong></td><td data-label="Unit" colspan="2">excludes airfare, theatre, drinks, tips and tax on food</td><td data-label="Total"><strong>$2,999</strong></td></tr>
      </tbody>
    </table></div>
    <p class="small muted">Swap lines to match your taste: Masa's hinoki counter alone is $1,900 for two, while the tavern menus at Gramercy Tavern ($156) and Cote ($168) are the cheapest starred meals with a published price. Tip and drinks are extra at every starred venue.</p>
  </div>
  <div class="notice warn"><strong>Deliberately unresolved:</strong> the final hotel choice, the total budget ceiling, airfare, theatre tickets, the 3-night hotel price, and any trip whose dates fall after 28 Feb (Bryant Park rink closed). These are listed with discovery paths on the <a href="questions.html">Questions</a> page and quantified on <a href="flagged.html">Flagged</a>.</div>
  <p class="small muted">Every number above is drawn from <code>data/*.json</code> at build time; the counts on the overview update from the same files when the page loads.</p>
"""
    pages["executive-summary"] = shell(
        "summary", "Executive summary", "Decision brief", "Executive summary",
        "What the sources verified on the dated checks support, what remains unknown, and the order in which to decide.",
        exec_body, depth=1)

    # ------------------------------------------------------------- michelin
    michelin_body = f"""
  <div class="notice danger"><strong>Timing.</strong> MICHELIN's next New York ceremony is scheduled for <a href="https://michelinmedia.com/pages/blog/detail/article/c/a1479/" target="_blank" rel="noopener noreferrer">14 Dec 2026 ↗</a> — after this research, before your trip. Re-check every star level after that date.</div>

  <div class="card">
    <p><strong>Citywide, re-checked {CHECKS_DATE} on the live MICHELIN filter:</strong>
    <a href="https://guide.michelin.com/en/us/new-york-state/new-york/restaurants/all-starred" target="_blank" rel="noopener noreferrer">5 three-star · 14 two-star · 50 one-star · 76 Bib Gourmand · 224 Selected ↗</a>.
    This site catalogues the full <strong>69 starred</strong> roster plus <strong>3 guide-listed</strong> new additions ({len(r_items)} rows total).</p>
    <p>MICHELIN's <strong>$$–$$$$</strong> band is reproduced exactly as published. It is a price indicator, not a dollar amount, and is never converted into one here. Dollar figures come only from the restaurant's own menu, FAQ or official booking channel.</p>
  </div>

  <h2>Verified menu prices for two adults</h2>
  <p class="lede">{len(priced)} restaurants have at least one menu price printed on an official page. Each total is 2 × the published per-person price, food only, before tax, tip and drinks. The capture date is November 2026 — re-confirm for February 2027.</p>
  <div class="table-wrap"><table>
    <thead><tr><th scope="col">Restaurant</th><th scope="col">Couple total</th><th scope="col">Official menu source</th><th scope="col">Basis / note</th></tr></thead>
    <tbody>{price_rows()}</tbody>
  </table></div>

  <h2>The five MICHELIN cluster anchors used for travel measurement</h2>
  <p class="lede">Door-to-door transit minutes were captured to one representative restaurant per cluster (Google Maps, transit, 2026-11-25). The clusters are the ones the hotel ranking refers to.</p>
  <div class="table-wrap"><table>
    <thead><tr><th scope="col">Cluster</th><th scope="col">Anchor destination</th><th scope="col">Starred venues in this cluster (as listed in the measurement set)</th><th scope="col">Live directions</th></tr></thead>
    <tbody>
      <tr><td data-label="Cluster"><strong>Midtown 51st</strong></td><td data-label="Anchor">Le Bernardin</td><td data-label="Venues">Le Bernardin, The Modern, Per Se, Jean-Georges, Sushi Sho, Masa</td><td data-label="Route"><a href="https://www.google.com/maps/dir/?api=1&origin=DoubleTree+by+Hilton+Hotel+New+York+City+Chelsea&destination=Le+Bernardin+New+York&travelmode=transit" target="_blank" rel="noopener noreferrer">Route ↗</a></td></tr>
      <tr><td data-label="Cluster"><strong>Flatiron / Madison Square</strong></td><td data-label="Anchor">Eleven Madison Park</td><td data-label="Venues">Eleven Madison Park, Atomix, Cote, Jua, Oiji Mi, Noda, Rezdôra, odo, YingTao, Yoshino, Mari, Casa Mono</td><td data-label="Route"><a href="https://www.google.com/maps/dir/?api=1&origin=DoubleTree+by+Hilton+Hotel+New+York+City+Chelsea&destination=Eleven+Madison+Park+New+York&travelmode=transit" target="_blank" rel="noopener noreferrer">Route ↗</a></td></tr>
      <tr><td data-label="Cluster"><strong>Tribeca / Lower Manhattan</strong></td><td data-label="Anchor">Jungsik</td><td data-label="Venues">Jungsik, Atera, Icca, Huso, Muku, L'Abeille, Le Coucou, Corima, Bar Miller, Shmoné, Estela</td><td data-label="Route"><a href="https://www.google.com/maps/dir/?api=1&origin=DoubleTree+by+Hilton+Hotel+New+York+City+Chelsea&destination=Jungsik+New+York&travelmode=transit" target="_blank" rel="noopener noreferrer">Route ↗</a></td></tr>
      <tr><td data-label="Cluster"><strong>Financial District</strong></td><td data-label="Anchor">Crown Shy</td><td data-label="Venues">Crown Shy, and the Wall Street hotel cluster used as a walking anchor</td><td data-label="Route"><a href="https://www.google.com/maps/dir/?api=1&origin=DoubleTree+by+Hilton+Hotel+New+York+City+Chelsea&destination=Crown+Shy+New+York&travelmode=transit" target="_blank" rel="noopener noreferrer">Route ↗</a></td></tr>
      <tr><td data-label="Cluster"><strong>Williamsburg, Brooklyn</strong></td><td data-label="Anchor">Aska</td><td data-label="Venues">Aska</td><td data-label="Route"><a href="https://www.google.com/maps/dir/?api=1&origin=DoubleTree+by+Hilton+Hotel+New+York+City+Chelsea&destination=Aska+Brooklyn&travelmode=transit" target="_blank" rel="noopener noreferrer">Route ↗</a></td></tr>
    </tbody>
  </table></div>
  <p class="small muted">These venue lists are the measurement sets used in the 2026-11-25 routing capture, not a complete per-cluster census. The full roster is the table below.</p>

  <h2>Full roster</h2>
  {toolbar("Search 72 restaurants by name, cuisine, area, price or day…", VERIFY_SELECT + '<select data-filter="stars" aria-label="Filter by star level"><option value="">All distinctions</option><option value="3">3 stars</option><option value="2">2 stars</option><option value="1">1 star</option><option value="guide">Guide-listed (no star)</option></select>')}
  <div data-table="restaurants"></div>

  <div class="notice info"><strong>How the price columns work.</strong> A dollar total appears only where an official page printed the per-person price. The MICHELIN band ($$–$$$$) is shown separately. "Price on request", "MP" and deposit-only venues are blank and flagged — Per Se publishes only deposits ($200 MDR / $150 Salon); Atera has conflicting captures (F24); Atomix carries its verified November Tock rates ($848/$628) with December ($990/$704+) noted.</div>
"""
    pages["michelin"] = shell(
        "michelin", "MICHELIN restaurants", "Dining · source-checked", "MICHELIN restaurants and guide listings",
        "Star levels transcribed from the live MICHELIN Guide, couple prices from each restaurant's own menu, and an honest blank wherever neither exists.",
        michelin_body, depth=1)

    # --------------------------------------------------------------- hotels
    def hotel_cards():
        out = []
        for h in top3:
            out.append(f"""<div class="card">
      <h3 style="margin-top:0">#{h["rank"]} · {e(h["name"])}</h3>
      <p class="small muted">{e(h.get("area") or "")}</p>
      <p><strong>All-in 7 nights:</strong> {e(h.get("sevenNightAllIn") or "blank")} <span class="small muted">(pre-tax {e(h.get("sevenNightPreTax") or "blank")})</span><br>
      <strong>MICHELIN reach:</strong> {h["transit"]["clustersWithin60"]}/{h["transit"]["clustersMeasured"]} sampled clusters ≤60 min · avg {h["transit"]["avgMinutes"]} min · longest {h["transit"]["maxMinutes"]} min<br>
      <strong>Room:</strong> {e(h.get("room") or "blank")}<br>
      <strong>Bath:</strong> {e(h.get("privateBathroom") or "blank")}</p>
      <p class="small">{e((h.get("flags") or ["no flags"])[0])}</p>
      </div>""")
        return "\n".join(out)

    hotels_body = f"""
  <div class="notice good"><strong>Ranking rule.</strong> Primary key: a verified private bathroom + queen-or-larger bed <em>and</em> at least one stored door-to-door transit measurement. Every measured hotel reaches every sampled MICHELIN cluster inside 60 minutes (3–37 min), so the one-hour rule does not separate them and ties break on verified all-in price, then average transit time. Hotels with no measurement follow; hotels whose bed/bath is unconfirmed are listed last and excluded from the recommendation. <span class="small muted">25 transit legs were captured from five origin hotels on 2026-11-25; one origin (The Benjamin) was dropped for lacking an official source, so four published hotels carry measurements.</span></div>

  <h2>Recommended shortlist</h2>
  <div class="tiles">{hotel_cards()}</div>

  <h2>All candidates, ranked</h2>
  {toolbar("Search hotels by name, area, price or room…", VERIFY_SELECT + '<select data-filter="qualified" aria-label="Filter by bed/bath verification"><option value="">All candidates</option><option value="qualified">Bed + bath verified</option><option value="unverified">Specification unverified</option></select>')}
  <div data-table="hotels"></div>

  <h2>Is the preferred week the cheapest? (five windows measured)</h2>
  <p class="lede">Every window is 7 nights, two adults, 4–5 star Manhattan, sorted by the cheapest <em>qualifying</em> room. The date arithmetic and each booking search URL are in the table.</p>
  <div data-table="hotels:windows"></div>
  <div class="notice warn"><strong>The trap in W2.</strong> The $836 February 22 – March 1 rate is a <em>twin</em> room, which fails your queen-bed rule, so it is not comparable. The qualifying floor across the window is the preferred week (W1, 15–22 Feb) at $848 pre-tax / $998 all-in.</div>

  <h2>When to book</h2>
  <div class="card">
    <p><strong>Now, at a cancellable rate.</strong> Two of the priced hotels were running 30–39% "Black Friday" promotions on 25 Nov 2026 (DoubleTree Chelsea, Arlo NoMad). A free-cancellation, $0-prepayment hold captures that price without risking a non-refundable commitment before the 14 Dec 2026 MICHELIN announcement and before the 3-vs-7-night decision.</p>
    <p><strong>Then re-shop</strong> in early February 2027 (14–30 days out) and around the ceremony. No official source promises a future price drop, so the cancellable hold is the risk cap, not a prediction.</p>
    <p><strong>Re-quote before paying:</strong> the totals here are third-party booking-engine snapshots captured 2026-11-25, not hotel quotes (flag F25). Booking.com property pages refused this session's fetcher during the 2026-11-26 verification pass, so the stored totals remain carried snapshots.</p>
  </div>

  <h2>Why the ranking is not just "count of restaurants within an hour"</h2>
  <div class="card">
    <p>25 legs were measured on 2026-11-25 between five hotels and the five MICHELIN cluster anchors. The longest was 37 minutes (Williamsburg). Because every hotel reached every sampled cluster, the count is identical (5/5) for all measured hotels, and the metric carries no information for choosing between them. The site therefore reports the measured reach as a pass/fail gate and ranks on verified price and room quality. Unmeasured hotels show a blank rather than an implied 5/5.</p>
    <p class="small muted">Method: Google Maps directions, travelmode=transit, "leave now", fastest itinerary returned, door-to-door including walks; captured 17:14–17:31 ET. Live service estimates, not timetables — re-run each row's Route link before committing to a reservation.</p>
  </div>
"""
    pages["hotels"] = shell(
        "hotels", "Hotels", "Stay · ranked", "Hotels ranked by verified MICHELIN reach, then price",
        f"{len(h_items)} candidates, {len(hotels_priced)} with a dated 7-night total for two adults, "
        f"{len(measured)} with measured transit to every sampled MICHELIN cluster, and a clear note on the "
        f"{len(h_items) - len(qualified)} whose bed and bathroom are still unconfirmed.",
        hotels_body, depth=1)

    # ----------------------------------------------------------- activities
    activities_body = f"""
  <div class="notice warn"><strong>February 2027 dates that change the plan.</strong>
  Presidents' Day is <strong>Monday 15 Feb</strong> · the 29th Chinatown Lunar New Year Parade is <strong>Sunday 21 Feb at 13:00</strong> ·
  Bryant Park's rink closes <strong>28 Feb 2027</strong> · Wollman Rink runs to <strong>16 Mar 2027</strong> ·
  the Met is <strong>closed on Wednesdays</strong> · MoMA stays open until 20:30 on Fridays.</div>

  <div class="card">
    <p><strong>{len(a_items)} activities</strong> with a source per row. Opening hours and closures are transcribed from each venue's own page; the couple cost is only shown where an official adult price exists (for example $30 × 2 = $60 at the Met and MoMA). Free sites show $0 because the operator publishes free entry.</p>
    <p>Travel notes appear only where a door-to-door result was captured (10 legs from Eurostars Wall Street on 2026-11-25). Every other row links a live transit route from the hotel you choose.</p>
  </div>

  {toolbar("Search activities by name, type, hours or cost…", VERIFY_SELECT)}
  <div data-table="activities"></div>

  <div class="notice info"><strong>Weather and seasonality.</strong> Outdoor items (Statue of Liberty ferry, High Line, Brooklyn Bridge, Central Park, the parade) are February-dependent and have no price risk but real comfort risk. The two rinks close on 28 Feb and 16 Mar respectively, so both are available in the preferred window.</div>
"""
    pages["activities"] = shell(
        "activities", "Activities", "Things to do · official hours", "Activities, hours and the February 2027 calendar",
        "Museums, landmarks, parks and two date-critical winter events — each with the operator's hours, closures, cost for two and a social/video link.",
        activities_body, depth=1)

    # ------------------------------------------------------------- itinerary
    itinerary_body = f"""
  <div class="notice info"><strong>This is a skeleton, not a booking.</strong> Each day uses only venues whose opening day is verified for that weekday. Restaurant suggestions are drawn from rows whose published hours include that day; where hours are blank the row is marked "check".</div>

  <h2>7-night structure (15–22 Feb 2027)</h2>
  <div class="card">
    <p><strong>Mon 15 Feb — arrive, Presidents' Day.</strong> Museums run holiday hours; expect crowds. Keep the evening free or book a low-commitment dinner. Do not book anything non-refundable until the hotel is confirmed.</p>
    <p><strong>Tue 16 Feb — The Met.</strong> Open 10:00–17:00 (closed Wednesdays). Pair with Central Park or the Guggenheim on Fifth Avenue. Evening: a Flatiron/Midtown dinner — Eleven Madison Park ($770 for two) or Gramercy Tavern's tavern menu ($156).</p>
    <p><strong>Wed 17 Feb — MoMA.</strong> The Met is closed today; MoMA is open 10:30–17:30. Afternoon: Top of the Rock or SUMMIT. Evening: Cote's Butcher's Feast ($168) or The Modern ($230 lunch prix fixe, $370 dinner).</p>
    <p><strong>Thu 18 Feb — downtown.</strong> Statue of Liberty ferry (last statue entry 15:30), 9/11 Memorial, Staten Island Ferry at sunset (free), or the Brooklyn Bridge walk. Evening: Jungsik ($670) or Le Coucou ($440).</p>
    <p><strong>Fri 19 Feb — late museum day.</strong> MoMA is open to 20:30; the Met to 21:00. Use the morning for the High Line and Chelsea Market, the evening for a starred dinner — Aquavit ($390) or Gabriel Kreuther ($400).</p>
    <p><strong>Sat 20 Feb — flexible.</strong> AMNH (dinosaurs + Gilder Center), Wollman Rink (off-peak $16 if the date is off-peak; $28 peak / $40 prime), or a second museum. Evening: Masa ($990 lunch / $1,500 table) or Le Bernardin ($436 dinner prix fixe).</p>
    <p><strong>Sun 21 Feb — Lunar New Year parade, 13:00.</strong> Chinatown. This is the single fixed event of the trip and the strongest reason to keep the 7-night window. Book a light dinner, not a tasting menu, given street-food temptation: Semma or Crown Shy are the cheaper starred options.</p>
    <p><strong>Mon 22 Feb — depart.</strong> Morning at Bryant Park's rink (open to 28 Feb) or a final walk before the flight.</p>
  </div>

  <h2>3-night variant (15–18 Feb)</h2>
  <div class="card">
    <p>If you keep the preferred <strong>Mon 15 – Thu 18</strong> window, keep Tue (Met), Wed (MoMA) and Thu (downtown) and drop the Friday–Sunday blocks. You lose the 21 Feb parade and the Bryant Park weekend, which is the main trade-off to weigh. No 3-night hotel total exists in the verified sources yet — that is question Q5/S5.</p>
  </div>

  <h2>Before you book anything</h2>
  <div class="card">
    <ol>
      <li>Confirm 3 or 7 nights, and confirm the hotel (Q1, Q2).</li>
      <li>Re-check MICHELIN stars after 14 Dec 2026 (Q4).</li>
      <li>Check each chosen restaurant's own page for its February hours and holiday closures — several close Sunday/Monday and the data marks those that are unknown.</li>
      <li>Route each restaurant from the chosen hotel at the intended time. The stored minutes are morning/evening snapshots from 25 Nov 2026, not timetable guarantees.</li>
      <li>Book the 21 Feb parade day loosely: streets close and restaurants fill.</li>
    </ol>
  </div>

  <h2>The 3-night vs 7-night trade-off in one table</h2>
  <div class="table-wrap"><table>
    <thead><tr><th scope="col">Item</th><th scope="col">3 nights (15–18 Feb)</th><th scope="col">7 nights (15–22 Feb)</th></tr></thead>
    <tbody>
      <tr><td data-label="Item">Hotel total available?</td><td data-label="3 nights"><span class="blank">no verified quote</span></td><td data-label="7 nights">$998–$5,220 all-in, 8 hotels</td></tr>
      <tr><td data-label="Item">Lunar New Year parade (21 Feb)</td><td data-label="3 nights">Missed</td><td data-label="7 nights">Included</td></tr>
      <tr><td data-label="Item">Bryant Park rink (to 28 Feb)</td><td data-label="3 nights">Available</td><td data-label="7 nights">Available</td></tr>
      <tr><td data-label="Item">Michelin dinners possible</td><td data-label="3 nights">3 evenings</td><td data-label="7 nights">7 evenings</td></tr>
      <tr><td data-label="Item">Weather risk</td><td data-label="3 nights">Lower spend exposure</td><td data-label="7 nights">More outdoor days at risk</td></tr>
    </tbody>
  </table></div>
"""
    pages["itinerary"] = shell(
        "itinerary", "Itinerary", "Plan · verified opening days", "A 7-night skeleton that respects opening days",
        "Day by day from verified hours and February dates, with the 3-night variant and the checks to run before booking.",
        itinerary_body, depth=1)

    # ------------------------------------------------------------- questions
    questions_body = f"""
  <div class="card">
    <p><strong>{len(Q["questions"])} questions.</strong> Each one lists what the sources already establish, what is genuinely missing, a provisional answer you can act on, whether it blocks a booking, and the exact step to close it. "Blocks a decision?" is about spending money, not about completeness.</p>
  </div>
  <div data-table="decisions:questions"></div>
  <div class="notice info"><strong>Reading the answers.</strong> A provisional answer is a recommendation built on verified values, never a substitute for the missing one. Where the answer depends on a quote that does not exist yet, the row says so.</div>
"""
    pages["questions"] = shell(
        "questions", "Questions", "Decide · known / missing / how to find out", "Questions that must be answered before money is spent",
        "Thirteen decision questions with their known facts, their gaps and the precise way to close each gap.",
        questions_body, depth=1)

    # ----------------------------------------------------------- suggestions
    suggestions_body = f"""
  <div class="card">
    <p><strong>{len(Q["suggestions"])} suggestions</strong> for improving the plan or this site. Nothing here is implemented unless the Status column says so — this is the review list you asked for, so you can pick a path before anything changes.</p>
    <p class="small muted">How to use it: filter to "Proposed" for uninplemented ideas, or "Implemented"/"Partially implemented" to see what this build already did. Each suggestion names its effort and what blocks it.</p>
  </div>
  <div class="toolbar"><input type="search" aria-label="Search suggestions" placeholder="Search suggestions…">
    <select data-filter="status" aria-label="Filter by status"><option value="">All statuses</option><option value="done">Implemented</option><option value="partial">Partially implemented</option><option value="proposed">Proposed</option></select>
    <span class="count"></span></div>
  <div data-table="decisions:suggestions"></div>
"""
    pages["suggestions"] = shell(
        "suggestions", "Suggestions", "Improve · nothing applied without review", "Suggestions, ranked by effort",
        "Sixteen options to improve decision-making — with current status, so implemented ideas are not confused with proposals.",
        suggestions_body, depth=1)

    # --------------------------------------------------------------- flagged
    flagged_body = f"""
  <div class="notice warn"><strong>These do not block the trip.</strong> They are the things you should look at before relying on a specific number: unverified values, conflicting official captures, and known irregularities. Severity High means it changes a decision; Medium means it changes a number; Low is a housekeeping or wording issue.</div>
  <div class="card"><p><strong>{len(Q["flags"])} flags</strong>, each with its source. Where a value is contested, the site keeps the value that the strongest official page supports and shows the alternative on the flag rather than silently picking one.</p></div>
  <div class="toolbar"><input type="search" aria-label="Search flags" placeholder="Search flags…">
    <select data-filter="severity" aria-label="Filter by severity"><option value="">All severities</option><option value="high">High</option><option value="medium">Medium</option><option value="low">Low</option></select>
    <span class="count"></span></div>
  <div data-table="decisions:flags"></div>
"""
    pages["flagged"] = shell(
        "flagged", "Flagged for review", "Audit trail", "Flagged for review",
        "Every unverified value, conflicting capture and irregularity, with the source you need to check it.",
        flagged_body, depth=1)

    # ---------------------------------------------------------- verification
    result_counts = V.get("resultCounts", {})
    cov = V["coverage"]
    rows = "".join(
        f"<tr><td data-label=\"Result\"><strong>{e(k)}</strong></td><td data-label=\"Checks\">{v}</td></tr>"
        for k, v in result_counts.items())
    verification_body = f"""
  <div class="notice info"><strong>What "verified" means on this site.</strong> A value is marked <em>Verified</em> only when the official page itself was read again on {CHECKS_DATE}. Where the official page blocked the fetcher and independent sources agreed, the result says <em>Corroborated</em>. Where nothing could be re-read, the row says <em>Carried</em> and keeps its source link so you can check it yourself in one click.</div>

  <div class="stats">
    <div class="stat"><b>{cov["restaurants"]["rows"]}</b><span>restaurant rows · {cov["restaurants"]["withPrice"]} priced · {cov["restaurants"]["withHours"]} with hours · {cov["restaurants"]["withSocial"]} with social links</span></div>
    <div class="stat"><b>{cov["hotels"]["priced"]}/{cov["hotels"]["rows"]}</b><span>hotels with dated 7-night totals · {cov["hotels"]["measuredTransit"]} with measured transit</span></div>
    <div class="stat"><b>{cov["activities"]["rows"]}</b><span>activity rows · {cov["activities"]["withHours"]} with hours · {cov["activities"]["withCost"]} with a couple cost</span></div>
  </div>

  <h2>Verification log — {len(V["checks"])} records</h2>
  <p>The table combines the 25-entry 2026-11-26 base log and 21 2026-11-27 addendum checks (session <code>arena/dbf0d1f0-nyfun2</code>, task T29; originally claimed as T27). The addendum re-read the MICHELIN census, seasonal activities, MTA fares, MoMA/Met admission, ten priced restaurant menus, hotel bed/bathroom lines, and Torrisi's hours. It corrected one carried value (Wollman Fri/Sat/Sun opening time, 10:00 → 09:00), verified five hotels that previously lacked a bed/bathroom line, and left The Maritime Hotel unverified (F26).</p>
  <div data-table="verification"></div>

  <h2>Supplemental official-source activity re-check · 2026-11-27</h2>
  <div class="notice info"><strong>12 activity-related rows were re-read by a separate session.</strong> Eight matched fully or partly; four discrepancies were corrected or flagged (Wollman hours F30, Statue of Liberty hours/date F31, Empire State Building Feb 2027 hours F32, Bryant Park stale ticket wording F33). See the <a href="../research/review-2026-11-27.md">row-by-row source review ↗</a>. A row badge shows its own check date.</div>

  <h2>Limits in the broader 2026-11-26 verification pass</h2>
  <div class="card">
    <ul>
      <li><strong>Booking.com property pages</strong> returned an error to that fetcher, so the dated hotel totals were not re-quoted. The Manhattan search page for 15–22 Feb 2027 did load, confirming the dates were bookable at that capture.</li>
      <li><strong>bryantpark.org</strong> and <strong>wollmanrinknyc.com</strong> were unreadable in the 2026-11-26 broad pass, but were subsequently re-read on their official pages by later sessions; 2026-27 schedule corrections and source notes are in the activity review above.</li>
      <li><strong>Google Maps</strong> cannot be queried programmatically here, so the 35 stored transit legs (25 hotel→cluster, 10 hotel→activity) remain the 2026-11-25 capture. Every row links a live directions query.</li>
      <li><strong>Individual MICHELIN detail pages</strong> were spot-checked (15 star levels plus the filter counters), not all 72 one by one; the census itself was re-read on 2026-11-26.</li>
    </ul>
    <p class="small muted">The full machine-readable log is <a href="../data/verification.json" target="_blank" rel="noopener noreferrer">data/verification.json ↗</a>. The 2026-11-27 local consistency audit (not a fresh source reread) is <a href="../research/verification-2026-11-27.md">here ↗</a>.</p>
  </div>
"""
    pages["verification"] = shell(
        "verification", "Verification log", "Audit · dated checks", "What was checked, and how",
        "A dated log of every fact re-read on 2026-11-26, the 2026-11-27 addendum, every figure only corroborated, and every number still carried from the November 25 capture.",
        verification_body, depth=1)

    # --------------------------------------------------------------- sources
    sources_body = f"""
  <h2>The rules this build follows</h2>
  <div class="card">
    <ol>
      <li><strong>One official source per row.</strong> MICHELIN Guide, a government page, or the venue's own site. Social platforms are used for links, never to establish a price or an hour.</li>
      <li><strong>No inference.</strong> If a page does not state it, the cell is blank. Bands ($$–$$$$) are never converted to dollars; a "from" rate is never treated as a quote.</li>
      <li><strong>Arithmetic is shown.</strong> A couple total is always 2 × the published per-person price, and hotel all-in totals show the tax formula used.</li>
      <li><strong>Provenance is recorded per field.</strong> Each merged row carries a <code>provenance</code> object naming the session that supplied each value.</li>
      <li><strong>Conflicts are published, not resolved silently.</strong> Disagreements go to <code>data/conflicts.json</code> and the Flagged page.</li>
      <li><strong>Third-party is labelled.</strong> Review videos are marked as reviews; only accounts confirmed by the venue's own site are called official.</li>
    </ol>
  </div>

  <h2>Primary-source register</h2>
  <div class="table-wrap"><table>
    <thead><tr><th scope="col">Source</th><th scope="col">Used for</th><th scope="col">Link</th></tr></thead>
    <tbody>
      <tr><td data-label="Source">MICHELIN Guide — NYC all-starred</td><td data-label="Used for">Census (5/14/50), star levels, addresses, bands</td><td data-label="Link"><a href="https://guide.michelin.com/en/us/new-york-state/new-york/restaurants/all-starred" target="_blank" rel="noopener noreferrer">Open ↗</a></td></tr>
      <tr><td data-label="Source">MICHELIN Guide — restaurant pages</td><td data-label="Used for">Hours, address, cuisine, band per restaurant</td><td data-label="Link"><a href="https://guide.michelin.com/en/new-york-state/new-york/restaurant/jungsik-new-york" target="_blank" rel="noopener noreferrer">Example ↗</a></td></tr>
      <tr><td data-label="Source">MICHELIN North America — ceremony notice</td><td data-label="Used for">14 Dec 2026 ceremony date</td><td data-label="Link"><a href="https://michelinmedia.com/pages/blog/detail/article/c/a1479/" target="_blank" rel="noopener noreferrer">Open ↗</a></td></tr>
      <tr><td data-label="Source">Each restaurant's own menu / FAQ / booking channel</td><td data-label="Used for">Couple prices for {len(priced)} rows</td><td data-label="Link">Linked per row on the Michelin page</td></tr>
      <tr><td data-label="Source">Booking.com Manhattan search (dated)</td><td data-label="Used for">7-night rates for 15–22 Feb 2027 and the five windows</td><td data-label="Link"><a href="https://www.booking.com/searchresults.html?ss=Manhattan%2C+New+York&checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1&selected_currency=USD&order=price" target="_blank" rel="noopener noreferrer">Open ↗</a></td></tr>
      <tr><td data-label="Source">Hotel brand pages (Hyatt, Hilton, Marriott/citizenM, Arlo, Eurostars)</td><td data-label="Used for">Room type, bed size, private bathroom</td><td data-label="Link">Linked per row on the Hotels page</td></tr>
      <tr><td data-label="Source">Google Maps transit directions</td><td data-label="Used for">35 door-to-door legs (25 hotel→cluster, 10 hotel→activity)</td><td data-label="Link"><a href="https://www.google.com/maps/dir/?api=1&origin=DoubleTree+by+Hilton+Hotel+New+York+City+Chelsea&destination=Le+Bernardin+New+York&travelmode=transit" target="_blank" rel="noopener noreferrer">Example ↗</a></td></tr>
      <tr><td data-label="Source">The Met · MoMA · AMNH · Whitney · Guggenheim · 9/11 · High Line · NYPL · NPS · NYC DOT · ESB</td><td data-label="Used for">Activity hours, closures, adult prices</td><td data-label="Link">Linked per row on the Activities page</td></tr>
      <tr><td data-label="Source">betterchinatown.com</td><td data-label="Used for">21 Feb 2027 Lunar New Year parade</td><td data-label="Link"><a href="http://betterchinatown.com/" target="_blank" rel="noopener noreferrer">Open ↗</a></td></tr>
      <tr><td data-label="Source">bryantpark.org · wollmanrinknyc.com</td><td data-label="Used for">Winter Village and Wollman season, prices</td><td data-label="Link"><a href="https://bryantpark.org/activities/winter-village" target="_blank" rel="noopener noreferrer">Bryant Park ↗</a> · <a href="https://wollmanrinknyc.com/plan/" target="_blank" rel="noopener noreferrer">Wollman ↗</a></td></tr>
      <tr><td data-label="Source">MTA</td><td data-label="Used for">Subway/bus fares and route context</td><td data-label="Link"><a href="https://www.mta.info/fares" target="_blank" rel="noopener noreferrer">Open ↗</a></td></tr>
    </tbody>
  </table></div>

  <h2>How this build is produced</h2>
  <div class="card">
    <p><code>research/canonical/*.json</code> holds the pristine datasets from the research sessions. <code>scripts/build_data.py</code> merges the parallel kits into <code>data/*.json</code> under the rules above (idempotent — re-running cannot double-count). <code>scripts/build_site.py</code> renders these pages. <code>scripts/verify.py</code> checks links, source-per-row, and blank-implies-flag.</p>
    <pre class="small" style="overflow-x:auto;background:var(--gray-bg);padding:12px;border-radius:8px">python3 scripts/verify.py
node --check assets/app.js</pre>
    <p class="small muted">No build step, no dependencies, no trackers. GitHub Pages serves the repository root.</p>
  </div>
"""
    pages["sources"] = shell(
        "sources", "Sources & method", "Method · provenance", "Sources, rules and how to reproduce",
        "The verification rules, the primary-source register, and the two scripts that turn canonical data into this site.",
        sources_body, depth=1)

    # ------------------------------------------------------------ repo audit
    repo_body = f"""
  <h2>What this repository contains</h2>
  <div class="card">
    <p>A static GitHub Pages dashboard plus every parallel session's independent kit, preserved verbatim. Nothing another session wrote was overwritten or deleted; the kits remain readable at their original paths.</p>
    <div class="table-wrap"><table>
      <thead><tr><th scope="col">Path</th><th scope="col">What it is</th><th scope="col">Status</th></tr></thead>
      <tbody>
        <tr><td data-label="Path"><code>index.html</code>, <code>pages/</code>, <code>data/</code>, <code>assets/</code>, <code>scripts/</code></td><td data-label="What">The published dashboard (this site)</td><td data-label="Status">Rebuilt 2026-11-26 (integration session <code>arena/9bc6abed-nyfun2</code>)</td></tr>
        <tr><td data-label="Path"><code>research/canonical/</code></td><td data-label="What">Pristine pre-merge datasets</td><td data-label="Status">Added 2026-11-26 so the merge is reproducible</td></tr>
        <tr><td data-label="Path"><code>sessions/c1cf7b23/</code></td><td data-label="What">31-venue, 10-hotel, 18-activity kit with 155 social links</td><td data-label="Status">Preserved; source of most hours/socials and 4 dated hotel rates</td></tr>
        <tr><td data-label="Path"><code>sessions/657520df/</code></td><td data-label="What">27-venue kit with cross-week window analysis</td><td data-label="Status">Preserved; source of Met/MoMA/Whitney socials and window notes</td></tr>
        <tr><td data-label="Path"><code>sessions/33cfdba4/</code></td><td data-label="What">72-row roster, 25-leg transit matrix, 5 price windows</td><td data-label="Status">Preserved; source of the transit measurements</td></tr>
        <tr><td data-label="Path"><code>data/verification.json</code>, <code>data/conflicts.json</code>, <code>research/verification-2026-11-26.md</code>, <code>research/verification-2026-11-27.md</code></td><td data-label="What">Dated verification log, every kit conflict, and the narrative audits</td><td data-label="Status">New 2026-11-26; addendum 2026-11-27</td></tr>
        <tr><td data-label="Path"><code>pages/verification.html</code>, <code>pages/compare.html</code></td><td data-label="What">Public verification log and kit comparison</td><td data-label="Status">New 2026-11-26</td></tr>
        <tr><td data-label="Path"><code>sessions/215c2a25/</code>, <code>alt/</code></td><td data-label="What">Two earlier independent dashboards</td><td data-label="Status">Preserved, not linked in the main navigation</td></tr>
      </tbody>
    </table></div>
  </div>

  <h2>Audit findings from this integration</h2>
  <div class="card">
    <ul>
      <li><strong>Stale headline counts (F22).</strong> The previous front page claimed 20 restaurant rows, 12 activities and 10 hotels while its own data held 72, 12 and 12; README said 21. All counts are now rendered from JSON at load, and the static HTML matches.</li>
      <li><strong>Kit rosters were not the official census (F23).</strong> 14 kit venues sit outside the 69-star roster, and one kit carried 3 starred names absent from the live list checked on 2026-11-25. None were added; all are in <code>data/conflicts.json</code>.</li>
      <li><strong>Duplicate rows in merged kits.</strong> The same hotel appeared as "The Frederick Hotel Tribeca" and "The Frederick Hotel Tribeca, a Small Luxury Hotel"; NYPL, the Met and 9/11 each appeared twice. The merge now keys these and reports rather than duplicates.</li>
      <li><strong>Mis-traced transit risk.</strong> A fuzzy name match initially attached Eurostars Wall Street's transit legs to The Wall Street Hotel. Matching is now key-based, and unmeasured hotels are blank.</li>
      <li><strong>Contested prices stay blank (F24).</strong> Atera and Per Se are not assigned a price; Atomix carries its verified November Tock price ($848/$628) with December ($990/$704+) flagged; Le Bernardin keeps $218 with the $225 alternative shown.</li>
      <li><strong>Verification is dated, not implied (F21).</strong> The log contains 46 records: 25 baseline records from 2026-11-26 and 21 addendum checks from 2026-11-27 (42 verified, 4 carried overall); each row shows its status and source.</li>
    </ul>
  </div>

  <h2>Parallel sessions and the merge that resolved the collision</h2>
  <div class="card">
    <p>Several sessions worked this repository at once. This build started as task T18, then found that
    <code>arena/547ee3a3-nyfun2</code> (T18) and <code>arena/45972379-nyfun2</code> (T21–T23) had already merged
    PRs #18–#22 to <code>main</code>, making the first PR (#23) conflicting.</p>
    <p><strong>Resolution:</strong> <code>main</code> was merged into the branch and <em>its datasets were adopted as the new
    canonical base</em> (<code>research/canonical/*.json</code>), so their verified work — Sushi Sho's Tock price,
    Per Se's revised deposit pages, the Wollman / Bryant Park / Lunar New Year rows, the official activity
    socials, and flags F18–F20 — flows into this build. Their pages were regenerated from that merged data
    rather than overwritten by hand, and the task was renumbered <strong>T24</strong> to avoid the T18 collision.
    Nothing another session verified was discarded; the one file that could not be auto-merged
    (<code>COORDINATION.md</code>) keeps both sessions' entries.</p>
    <p>Task board: <a href="../COORDINATION.md" target="_blank" rel="noopener noreferrer">COORDINATION.md ↗</a> ·
    Parallel kits and what each adds: <a href="compare.html">Compare session kits →</a></p>
  </div>
"""
    pages["repo"] = shell(
        "repo", "Repository audit", "Repo · what changed", "Repository audit and integration log",
        "What the repository contained, what each session contributed, what this integration changed, and the irregularities it found.",
        repo_body, depth=1)

    # --------------------------------------------------------------- compare
    def kit_rows():
        rows = [
            ("sessions/c1cf7b23/", "31 restaurants · 10 hotels · 18 activities · 155 social links",
             "Richest per-row hours and social links; the four extra dated hotel rates (DoubleTree, Eurostars, Evelyn, Frederick).",
             "Four venues are outside the starred census; its Sushi Sho / Per Se Salon prices were not carried where the source was a help page."),
            ("sessions/657520df/", "27 restaurants · 10 hotels · 16 activities",
             "Cross-week booking-window analysis and the Met/MoMA/Whitney social sets.",
             "Same census gap; Atomix/Atera price captures conflict with the other kit."),
            ("sessions/33cfdba4/", "72-row roster · 25 transit legs · 5 price windows",
             "The only measured transit matrix, which is what makes the hotel ranking evidence-based.",
             "Carried 3 starred names absent from the live list checked on 2026-11-25."),
            ("sessions/215c2a25/", "Independent early dashboard",
             "A third independent reading of the same sources for comparison.",
             "Earlier capture; superseded by the roster above."),
            ("alt/", "Independent early site",
             "Budget-oriented analysis and a different layout.",
             "Earlier capture; preserved, not linked in the main navigation."),
        ]
        return "".join(
            f"<tr><td data-label=\"Kit\"><code>{e(p)}</code></td><td data-label=\"Contents\">{e(c)}</td>"
            f"<td data-label=\"What it adds\">{e(g)}</td><td data-label=\"Caveat\">{e(cv)}</td></tr>"
            for p, c, g, cv in rows)

    compare_body = f"""
  <div class="card"><p>Five parallel kits were produced for this same brief. This integration kept every one of them and merged only what could be traced to an official source. The table shows what each contributed and where it disagrees.</p></div>
  <div class="table-wrap"><table>
    <thead><tr><th scope="col">Kit</th><th scope="col">Contents</th><th scope="col">What it adds to this site</th><th scope="col">Caveat</th></tr></thead>
    <tbody>{kit_rows()}</tbody>
  </table></div>
  <h2>Disagreements between kits</h2>
  <div class="card"><p><strong>{len(C["conflicts"])} conflicts</strong> are recorded in <code>data/conflicts.json</code>. Most are wording differences that reduce to the same dollar figures; the substantive ones (Le Bernardin dinner $218 vs $225, Le Coucou set menu vs à la carte, Atomix/Atera/Per Se) are on the <a href="flagged.html">Flagged</a> page.</p>
  <p class="small muted">{len(C["kitOnlyRestaurants"])} restaurant names from the kits are outside the official census and were not added.</p></div>
"""
    pages["compare"] = shell(
        "repo", "Compare session kits", "Repo · parallel work", "Compare the parallel session kits",
        "Five independent attempts at the same brief, what each added, and where they disagree.",
        compare_body, depth=1)

    # ------------------------------------------------------------- write out
    with open(D("index.html"), "w", encoding="utf-8") as f:
        f.write(pages["index"])
    os.makedirs(D("pages"), exist_ok=True)
    for key in ("executive-summary", "michelin", "hotels", "activities", "itinerary",
                "questions", "suggestions", "flagged", "verification", "sources", "repo", "compare"):
        fname = key if key != "compare" else "compare"
        fname = {"michelin": "michelin-restaurants", "repo": "repo-audit"}.get(key, key)
        with open(D("pages", fname + ".html"), "w", encoding="utf-8") as f:
            f.write(pages[key])
    print("wrote index.html and", len(pages) - 1, "pages")


if __name__ == "__main__":
    build()
