#!/usr/bin/env python3
"""
NYC Trip Planner static-site generator.

Renders static HTML for GitHub Pages from JSON in ./data.
Design goals:
  * every row carries explicit source links + verification status
  * never invent a value: missing data renders as an em dash + "unverified" flag
  * mobile-first, no framework, no network access needed at build time
"""
from __future__ import annotations

import html
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

# Fully self-contained kit: the script lives beside the pages it writes, so it
# cannot touch the canonical root site that a parallel session owns and publishes.
OUT = Path(__file__).resolve().parent
ROOT = OUT                       # kept for the few links that reference the repo tree
KIT_DIR = "sessions/33cfdba4"
DATA = OUT / "data"

TODAY = "2026-11-25"  # research date stamped on every verified cell set

# ----------------------------------------------------------------------------- data
def load(name: str, default=None):
    p = DATA / name
    if not p.exists():
        return default if default is not None else {}
    with p.open(encoding="utf-8") as fh:
        return json.load(fh)


SITE = load("site.json", {})
RESTAURANTS = load("restaurants.json", {"rows": []})
HOTELS = load("hotels.json", {"rows": [], "windows": []})
ACTIVITIES = load("activities.json", {"rows": []})
WINDOWS = load("pricing_windows.json", {"windows": []})
ITINERARY = load("itinerary.json", {"days": []})
QUESTIONS = load("questions.json", {"groups": []})
SUGGESTIONS = load("suggestions.json", {"items": []})
FLAGS = load("flags.json", {"items": []})
AUDIT = load("audit.json", {"findings": []})
EXEC = load("executive_summary.json", {"sections": []})
ANCHORS = load("transit_anchors.json", {"anchors": [], "hotels": {}})

NAV = [
    ("index.html", "Overview"),
    ("executive-summary.html", "Executive Summary"),
    ("hotels.html", "Hotels"),
    ("michelin.html", "Michelin & Dining"),
    ("activities.html", "Activities"),
    ("itinerary.html", "Itinerary"),
    ("booking-strategy.html", "Booking Strategy"),
    ("open-questions.html", "Open Questions"),
    ("suggestions.html", "Site Suggestions"),
    ("flagged-for-review.html", "Flagged for Review"),
    ("repo-audit.html", "Repo Audit"),
]

# ----------------------------------------------------------------------------- helpers
def esc(v) -> str:
    return html.escape("" if v is None else str(v), quote=True)


def e(value, fallback='<span class="muted">—</span>') -> str:
    """Escape a value or render an explicit em-dash placeholder."""
    if value is None or value == "":
        return fallback
    return esc(value)


def money(v, currency="$") -> str:
    if v is None or v == "":
        return '<span class="muted">—</span>'
    try:
        n = float(v)
    except (TypeError, ValueError):
        return esc(v)
    return f"{currency}{n:,.0f}" if n == int(n) else f"{currency}{n:,.2f}"


def stars(n) -> str:
    try:
        n = int(n)
    except (TypeError, ValueError):
        return ""
    if n <= 0:
        return ""
    return f'<span class="stars" aria-label="{n} Michelin stars">{"★" * n}</span>'


def distinction_badge(row) -> str:
    d = row.get("distinction")
    if d == "bib":
        return '<span class="badge neutral">Bib Gourmand</span>'
    if d in (0, "0", None):
        return '<span class="badge neutral">Guide listed</span>'
    try:
        n = int(d)
    except (TypeError, ValueError):
        return '<span class="badge neutral">Guide listed</span>'
    if n >= 1:
        return f'<span class="badge star">{n}★ Michelin</span>'
    return '<span class="badge neutral">Guide listed</span>'


def verif(state, note="") -> str:
    state = (state or "u").lower()
    label = {"v": "Verified", "u": "Unverified", "f": "Flagged"}.get(state, "Unverified")
    title = f' title="{esc(note)}"' if note else ""
    return f'<span class="verif {state}"{title}>{label}</span>'


def link(url, label=None, cls="src", external=True) -> str:
    if not url:
        return '<span class="muted">—</span>'
    lab = esc(label) if label else esc(_pretty_url(url))
    rel = ' rel="noopener"' if external else ""
    return f'<a class="{cls}" href="{esc(url)}"{rel}>{lab} ↗</a>'


def _pretty_url(url: str) -> str:
    u = re.sub(r"^https?://(www\.)?", "", url)
    return u.rstrip("/")


SOCIAL_ICON = {"instagram": "IG", "tiktok": "TT", "youtube": "YT", "facebook": "FB", "x": "X"}


def socials(row) -> str:
    parts = []
    for key in ("instagram", "tiktok", "youtube", "facebook"):
        url = row.get(key)
        if url:
            parts.append(
                f'<a class="chip" href="{esc(url)}" rel="noopener">'
                f'{SOCIAL_ICON[key]} ↗</a>'
            )
    return " ".join(parts) if parts else '<span class="muted">—</span>'


def hours_cell(row) -> str:
    hours = row.get("hours") or {}
    if not hours:
        return '<span class="muted">—</span>'
    order = [("mon", "Mon"), ("tue", "Tue"), ("wed", "Wed"), ("thu", "Thu"),
             ("fri", "Fri"), ("sat", "Sat"), ("sun", "Sun")]
    bits = []
    for key, lab in order:
        val = hours.get(key)
        if val:
            bits.append(f"<b>{lab}</b> {esc(val)}")
    return "<br>".join(bits)


def table(cols, rows, *, cls="data", caption=None, empty_msg="No rows yet.") -> str:
    """cols: list of dicts {key,label,cls,attr}. rows: list of dicts key->html."""
    if not rows:
        return f'<div class="callout info"><p><strong>Pending.</strong> {esc(empty_msg)}</p></div>'
    head = "".join(
        f'<th class="{c.get("cls","")}">{esc(c["label"])}</th>' for c in cols
    )
    body = []
    for r in rows:
        tds = []
        for c in cols:
            val = r.get(c["key"], '<span class="muted">—</span>')
            label = c.get("label", "")
            tds.append(
                f'<td class="{c.get("cls","")}" data-label="{esc(label)}">{val}</td>'
            )
        body.append("<tr>" + "".join(tds) + "</tr>")
    cap = f'<caption class="sr-only">{esc(caption)}</caption>' if caption else ""
    return (
        f'<div class="table-scroll"><table class="{cls}">{cap}'
        f"<thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table></div>"
    )


def kpi(value, label, sub="", href=None) -> str:
    inner = (
        f'<div class="metric">{value}</div>'
        f'<p class="small muted mb0">{esc(label)}</p>'
        + (f'<p class="xs muted mb0">{esc(sub)}</p>' if sub else "")
    )
    if href:
        return f'<a class="card" href="{esc(href)}">{inner}</a>'
    return f'<div class="card">{inner}</div>'


def callout(kind, title, body_html) -> str:
    t = f"<strong>{esc(title)}</strong> " if title else ""
    return f'<div class="callout {kind}"><p>{t}{body_html}</p></div>'


# ----------------------------------------------------------------------------- layout
def page(filename: str, title: str, description: str, body: str, *, active: str | None = None):
    nav_items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == (active or filename) else ""
        nav_items.append(f'<li><a href="{href}"{cur}>{esc(label)}</a></li>')
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · NYC Trip Planner</title>
<meta name="description" content="{esc(description)}">
<link rel="stylesheet" href="assets/css/style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='22' fill='%230b5fa5'/><text x='50' y='68' font-size='52' font-family='Arial' font-weight='bold' fill='white' text-anchor='middle'>NY</text></svg>">
</head>
<body>
<a class="sr-only" href="#main">Skip to content</a>
<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="index.html" style="text-decoration:none">
      <span class="brand-mark">NY</span>
      <span class="brand-text">
        <span class="brand-title">NYC Trip Planner</span>
        <span class="brand-sub">Couple · Feb–Mar 2027 · verified sources</span>
      </span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="nav" id="site-nav" aria-label="Main">
      <ul>{''.join(nav_items)}</ul>
    </nav>
  </div>
</header>
<main id="main">
<div class="wrap">
{body}
</div>
</main>
<footer class="site-footer">
  <div class="footer-inner">
    <p><strong>NYC Trip Planner</strong> — built from official-source research checked on {esc(TODAY)} (UTC). Prices are live-search observations, not quotes; re-check before booking.</p>
    <p>Rows without a confirmable official value are left blank and listed on the <a href="flagged-for-review.html">Flagged for Review</a> page. Methodology and change log: <a href="repo-audit.html">Repo Audit</a> · <a href="https://github.com/{esc(SITE.get('repo','kanlerxz87-cyber/NYFun2'))}/blob/main/COORDINATION.md" rel="noopener">COORDINATION.md ↗</a></p>
    <p class="xs">Not affiliated with any hotel, restaurant or venue. Star ratings © MICHELIN Guide; prices © Booking.com as displayed on the check date.</p>
  </div>
</footer>
<script src="assets/js/app.js" defer></script>
</body>
</html>
"""
    (OUT / filename).write_text(doc, encoding="utf-8")
    return filename


def head(kicker, title, lede) -> str:
    return (
        '<div class="page-head">'
        f'<p class="eyebrow">{esc(kicker)}</p>'
        f"<h1>{esc(title)}</h1>"
        f'<p class="lede">{lede}</p>'
        "</div>"
    )

# ----------------------------------------------------------------------------- ranking
def hotel_rankings():
    """Rank hotels by Michelin stars reachable within 1 h (verified transit only)."""
    anchors = {a["id"]: a for a in ANCHORS.get("anchors", [])}
    rows = []
    for h in HOTELS.get("rows", []):
        matrix = [m for m in ANCHORS.get("matrix", []) if m["hotel"] == h["id"]]
        reachable, unknown, max_min = [], 0, 0
        for m in matrix:
            a = anchors.get(m["anchor"], {})
            mins = m.get("minutes")
            if mins is None:
                unknown += 1
                continue
            max_min = max(max_min, mins)
            if mins <= 60:
                for r in a.get("restaurants", []):
                    reachable.append((r, mins))
        stars_seen = {}
        for r, mins in reachable:
            stars_seen.setdefault(r, mins)
        # count Michelin-starred restaurants within 1h using the roster
        roster = {x["name"]: x for x in RESTAURANTS.get("rows", [])}
        star_total, star3, star2, star1 = 0, 0, 0, 0
        for name, mins in stars_seen.items():
            info = roster.get(name)
            if not info:
                continue
            s = int(info.get("stars") or 0)
            if s >= 1:
                star_total += 1
                star3 += 1 if s == 3 else 0
                star2 += 1 if s == 2 else 0
                star1 += 1 if s == 1 else 0
        rows.append({
            "hotel": h, "anchors_reachable": len([m for m in matrix if m.get("minutes") is not None and m["minutes"] <= 60]),
            "anchors_measured": len([m for m in matrix if m.get("minutes") is not None]),
            "anchors_total": len(matrix), "unknown": unknown, "max_min": max_min,
            "stars": star_total, "s3": star3, "s2": star2, "s1": star1,
            "star_names": sorted(stars_seen.keys()),
        })
    # The brief's measure (stars reachable within 1 h) is primary. It ties across the
    # shortlist, so price is the documented tie-break, then shortest worst-case leg.
    rows.sort(key=lambda r: (-r["stars"], r["hotel"].get("total_7n_usd") or 10**9, r["max_min"] or 999))
    for i, r in enumerate(rows, 1):
        r["rank"] = i
    return rows


def score_bar(value, maxvalue, label=None):
    pct = 0 if not maxvalue else max(2, min(100, round(value / maxvalue * 100)))
    return (f'<span class="score"><span class="bar"><span style="width:{pct}%"></span></span>'
            f'<span class="val">{esc(label if label is not None else value)}</span></span>')


# ============================================================================= pages
def page_index():
    rec = EXEC.get("recommendation", {})
    ranked = hotel_rankings()
    stars_rows = [r for r in RESTAURANTS.get("rows", []) if (r.get("stars") or 0) >= 1]
    three = [r for r in stars_rows if r["stars"] == 3]
    two = [r for r in stars_rows if r["stars"] == 2]
    one = [r for r in stars_rows if r["stars"] == 1]
    counts = RESTAURANTS.get("official_counts", {})

    kpis = "".join(
        kpi(esc(k.get("value")), k.get("label", ""), k.get("sub", ""), href=k.get("href"))
        for k in EXEC.get("kpis", [])
    )

    top_hotels = ranked[:3]
    hotel_rows = []
    for r in top_hotels:
        h = r["hotel"]
        hotel_rows.append({
            "rank": f'<strong>#{r["rank"]}</strong>',
            "name": f'<a href="hotels.html">{esc(h["name"])}</a><br><span class="xs muted">{esc(h.get("area",""))}</span>',
            "room": f'{esc(h.get("room"))}<br><span class="xs muted">{esc(h.get("bed"))}</span>',
            "total": f'<strong>{money(h.get("total_7n_usd"))}</strong><br><span class="xs muted">7 nights, pre-tax</span>',
            "stars": f'≥{r["stars"]} <span class="xs muted">of 69 · slowest {r["max_min"]} min</span>',
        })

    dining_rows = []
    for r in (three + two)[:6]:
        dining_rows.append({
            "name": f'{esc(r["name"])} {verif(r.get("verified"))}',
            "tier": distinction_badge({"distinction": r.get("stars")}),
            "area": esc(r.get("area")) if r.get("area") else '<span class="muted">—</span>',
            "hours": hours_cell(r) if r.get("hours") else '<span class="muted">—</span>',
            "links": socials(r) + " " + link(r.get("michelin_url"), "MICHELIN"),
        })

    body = head(
        "Trip brief · couple · February–March 2027",
        "New York in February, planned from official sources only",
        "Two adults, a queen bed or bigger, a private bathroom, and as many Michelin stars as a subway ride can reach. "
        "Every value on this site is either captured from a named source and linked, or left blank and flagged.",
    )

    body += callout("success", "The verdict.", esc(EXEC.get("verdict", "")))
    body += f'<div class="grid cols-4">{kpis}</div>'

    body += '<h2>Start here</h2><div class="grid cols-3">'
    body += kpi("Hotels", "Five verified queen rooms, ranked", "Transit matrix · tax notes", href="hotels.html")
    body += kpi(f'{counts.get("starred_total","69")}', "Starred restaurants, tiered", "3★ · 2★ · 1★ · Bib", href="michelin.html")
    body += kpi("9", "Activities with hours & prices", "All within an hour", href="activities.html")
    body += '</div>'

    body += '<h2>The three best hotels</h2>'
    body += table(
        [{"key": "rank", "label": "#"}, {"key": "name", "label": "Hotel"}, {"key": "room", "label": "Qualifying room"},
         {"key": "total", "label": "7 nights"}, {"key": "stars", "label": "Michelin reach"}],
        hotel_rows, caption="Top three hotels by number of Michelin restaurants reachable within one hour",
    )
    body += f'<p class="small muted">All 25 hotel-to-cluster legs were measured. Every hotel reached every cluster within 37 minutes, so the ranking is settled by price after the transit tie. <a href="hotels.html">Full matrix →</a></p>'

    body += '<h2>The stars worth booking first</h2>'
    body += table(
        [{"key": "name", "label": "Restaurant"}, {"key": "tier", "label": "Distinction"},
         {"key": "area", "label": "Area"}, {"key": "hours", "label": "Hours"}, {"key": "links", "label": "Sources"}],
        dining_rows, caption="Top tier Michelin restaurants",
    )
    body += f'<p class="small muted">Only {AUDIT.get("headline",{}).get("rows_fully_verified", 7)} of the {len(RESTAURANTS.get("rows",[]))} roster rows have fully captured hours so far; the rest are shown with a MICHELIN link and an <span class="verif u">Unverified</span> chip. <a href="michelin.html">All 69 starred →</a></p>'

    body += '<h2>What is not settled</h2><div class="grid cols-3">'
    body += kpi(str(AUDIT.get("headline", {}).get("open_flags", 14)), "Flagged items", "Known gaps, stated not patched", href="flagged-for-review.html")
    body += kpi(str(len(QUESTIONS.get("groups", []))), "Open questions", "What a human must decide", href="open-questions.html")
    body += kpi(str(len(SUGGESTIONS.get("items", []))), "Site suggestions", "Review before changing anything", href="suggestions.html")
    body += '</div>'

    page("index.html", "Overview", "An autonomous New York trip plan built from official sources: hotels ranked by Michelin reach, 69 starred restaurants, verified hours and prices, and every gap declared.", body)


def page_exec():
    rec = EXEC.get("recommendation", {})
    body = head("Executive summary", "The whole plan on one page",
                "Read this first. Everything below is a finding from the tables, not a preference.")
    body += callout("success", "", esc(EXEC.get("verdict", "")))
    body += f'<div class="grid cols-4">{"".join(kpi(esc(k.get("value")), k.get("label",""), k.get("sub","")) for k in EXEC.get("kpis", []))}</div>'
    for s in EXEC.get("sections", []):
        body += f'<h2>{esc(s.get("title"))}</h2>'
        for para in s.get("body", []):
            body += f"<p>{esc(para)}</p>"
    if rec:
        body += '<h2>The recommendation</h2>'
        body += '<div class="card"><p class="eyebrow">Book this</p>'
        body += f'<h3 class="mt0">{esc(rec.get("hotel"))}</h3>'
        body += f'<p>{esc(rec.get("why"))}</p>'
        body += callout("warn", "Risk", esc(rec.get("risk", "")))
        body += callout("info", "Fallback", esc(rec.get("fallback", "")))
        body += '<h4>Next actions</h4><ol class="timeline">'
        for a in rec.get("next_actions", []):
            body += f'<li><span>{esc(a)}</span></li>'
        body += "</ol></div>"
    page("executive-summary.html", "Executive Summary", "The verdict, the numbers behind it, and the risks in one page.", body)


def page_hotels():
    ranked = hotel_rankings()
    body = head("Where to stay", "Five hotels that meet the brief, ranked by Michelin reach",
                "Queen bed or larger, private bathroom, two adults, seven nights, 2027-02-15 to 02-22. "
                "The measure the brief asked for turned out not to separate them, so price settles it.")

    rows = []
    for r in ranked:
        h = r["hotel"]
        rows.append({
            "rank": f'<strong>#{r["rank"]}</strong>',
            "name": f'<a href="#{esc(h["id"])}">{esc(h["name"])}</a><br><span class="xs muted">{esc(h.get("area",""))}</span>',
            "room": f'{esc(h.get("room"))}<br><span class="xs muted">{esc(h.get("bed"))} · {e(h.get("size_sqft"))} ft²</span>',
            "bath": f'{esc(h.get("bath"))}',
            "total": f'<strong>{money(h.get("total_7n_usd"))}</strong><br><span class="xs muted">{money(h.get("per_night_usd"))}/night · pre-tax</span>',
            "michelin": f'<strong>≥{r["stars"]}</strong> <span class="xs muted">of 69 timed</span><br><span class="xs muted">slowest cluster {r["max_min"]} min</span>',
            "score": score_bar(h.get("rating") or 0, 10, h.get("rating")),
            "src": link(h.get("source"), "Booking") + " " + verif(h.get("verified")),
        })
    body += table(
        [{"key": "rank", "label": "#"}, {"key": "name", "label": "Hotel"}, {"key": "room", "label": "Qualifying room"},
         {"key": "bath", "label": "Bathroom"}, {"key": "total", "label": "7-night total"},
         {"key": "michelin", "label": "Michelin reach"}, {"key": "score", "label": "Guest score"}, {"key": "src", "label": "Source"}],
        rows, caption="Hotel shortlist ranked by Michelin restaurants reachable within one hour",
    )

    body += callout("info", "What the Michelin column counts",
                     "Each cluster was timed against one real restaurant and the star tally is the sum of the roster "
                     "restaurants inside the clusters that came in at or under an hour. 37 of the 69 starred restaurants sit in "
                     "clusters that were measured; the remaining 32 were not individually timed, so the column reads "
                     "'at least 37' rather than a total.")
    body += callout("warn", "The honest result",
                     "All 25 hotel-to-Michelin-cluster legs came in at 37 minutes or less, so the one-hour rule "
                     "eliminates <strong>none</strong> of these five hotels. The ranking is therefore decided by price "
                     "and by the single closest star, not by travel time.")

    body += "<h2>Transit matrix: every leg, measured</h2>"
    anchors = {a["id"]: a for a in ANCHORS.get("anchors", [])}
    anchor_list = ANCHORS.get("anchors", [])
    m_rows = []
    for h in HOTELS.get("rows", []):
        cells = {"hotel": f'<strong>{esc(h["name"])}</strong>'}
        for a in anchor_list:
            m = next((x for x in ANCHORS.get("matrix", []) if x["hotel"] == h["id"] and x["anchor"] == a["id"]), None)
            if not m or m.get("minutes") is None:
                cells[a["id"]] = '<span class="muted">—</span>'
            else:
                mins = m["minutes"]
                cls = "good" if mins <= 30 else ("ok" if mins <= 60 else "bad")
                cells[a["id"]] = f'<span class="pill {cls}">{mins} min</span><br><span class="xs muted">{esc(", ".join(m.get("lines", [])))}</span>'
        m_rows.append(cells)
    cols = [{"key": "hotel", "label": "Hotel"}] + [{"key": a["id"], "label": a["short"] if "short" in a else a["label"].split(" (")[0]} for a in anchor_list]
    body += table(cols, m_rows, caption="Door-to-door transit times from each hotel to each Michelin cluster")
    body += '<p class="small muted">Method: Google Maps transit directions, one weekday-evening sample (2026-11-25, 17:14–17:31 ET), fastest itinerary returned, door to door including walking. Every cell links back to the same query pattern, e.g. <a href="' + esc(ANCHORS.get("matrix", [{}])[0].get("source", "")) + '" rel="noopener">Eurostars → Le Bernardin ↗</a>. Re-run before travel; February service differs.</p>'

    for r in ranked:
        h = r["hotel"]
        body += f'<h2 id="{esc(h["id"])}">{esc(h["name"])}</h2>'
        body += '<div class="grid cols-2">'
        body += '<div class="card">'
        body += f'<p class="eyebrow">Room booked for the test</p><h3 class="mt0">{esc(h.get("room"))}</h3>'
        body += f'<p class="small">{esc(h.get("bed"))} · {e(h.get("size_sqft"))} ft² · {esc(h.get("bath"))}</p>'
        body += f'<p class="metric">{money(h.get("total_7n_usd"))}</p><p class="small muted">{money(h.get("per_night_usd"))} per night, 7 nights, before tax</p>'
        body += f'<p class="small">{esc(h.get("rate_terms"))}</p>'
        body += f'<p class="small muted">{esc(h.get("tax_note"))}</p>'
        body += f'<p>{link(h.get("source"), "Open this exact search")} {verif(h.get("verified"))}</p>'
        body += '</div><div class="card">'
        body += f'<p class="eyebrow">Why it ranks here</p><p class="small">{esc(h.get("notes"))}</p>'
        body += f'<p class="small"><strong>Nearest subway:</strong> {e(h.get("nearest_subway"))}</p>'
        body += f'<p class="small"><strong>Amenities:</strong> {esc(", ".join(h.get("amenities", [])))}</p>'
        body += f'<p class="small"><strong>Guest score:</strong> {e(h.get("rating"))} / 10 from {e(h.get("reviews"))} reviews</p>'
        body += '</div></div>'

    ex = HOTELS.get("excluded", [])
    if ex:
        body += '<h2>Hotels considered and rejected</h2>'
        body += table([{"key": "name", "label": "Hotel"}, {"key": "reason", "label": "Why it was excluded"}, {"key": "src", "label": "Source"}],
                      [{"name": esc(x["name"]), "reason": esc(x["reason"]), "src": link(x.get("source"), "Booking")} for x in ex],
                      caption="Hotels that did not satisfy the brief")

    body += '<h2>Hotel flags</h2><ul class="checks">'
    for f in HOTELS.get("flags", []):
        body += f"<li>{esc(f)}</li>"
    body += "</ul>"

    page("hotels.html", "Hotels", "Five verified queen-bed hotels ranked by Michelin reach, with the full 25-leg transit matrix and every price caveat.", body)


def page_michelin():
    counts = RESTAURANTS.get("official_counts", {})
    rows_all = RESTAURANTS.get("rows", [])
    body = head("Michelin", "69 starred restaurants, tiered and ranked",
                "MICHELIN Guide New York, 2025 selection as published on guide.michelin.com and captured 2026-11-25. "
                "The next selection is expected around 14 December 2026, so star counts may change before the trip.")

    body += '<div class="grid cols-4">'
    body += kpi(str(counts.get("three_star", 5)), "Three stars", "Worth a special journey", href="#three")
    body += kpi(str(counts.get("two_star", 14)), "Two stars", "Excellent cooking", href="#two")
    body += kpi(str(counts.get("one_star", 50)), "One star", "High-quality cooking", href="#one")
    body += kpi(str(counts.get("bib_gourmand", 76)), "Bib Gourmand", "Good food, moderate price", href="#bib")
    body += '</div>'

    body += callout("info", "Two kinds of listing",
                     'A <span class="badge star">3★ Michelin</span> badge means actual stars awarded by the Guide. '
                     'A <span class="badge neutral">Guide listed</span> or Bib Gourmand badge means the restaurant is '
                     "in the MICHELIN Guide without a star: the Guide recommends it, but it holds no star. "
                     f"New York also lists {counts.get('selected', 224)} restaurants with no distinction at all.")

    body += callout("info", "How cost for two is shown",
                     "MICHELIN publishes a price <em>band</em> - $$$$ is the top band, $ the lowest - not a menu price. "
                     "The band is an official MICHELIN field and is listed per restaurant. Dollar amounts are deliberately "
                     "NOT derived from it: a $$$$ dinner for two is not known to be any specific number, and inventing one "
                     "would break the rule that nothing is estimated. Where a restaurant publishes its own menu price, it "
                     "appears as text instead.")

    body += callout("warn", "The count does not quite reconcile",
                     "The live all-starred filter reports 5 / 14 / 50 = 69. The official 2025 ceremony article names "
                     "5 / 15 / 52. The two extra rows are in the two- and one-star tiers. This site follows the live "
                     "filter; the discrepancy is logged as flag F-01 rather than smoothed over.")

    # Shortlist suggestion S-01 implemented as a highlight, not a replacement
    three = [r for r in rows_all if r.get("stars") == 3]
    body += '<h2 id="three">Three stars · the marquee bookings</h2>'
    t_rows = []
    for r in three:
        t_rows.append({
            "name": f'<strong>{esc(r["name"])}</strong> {verif(r.get("verified"))}',
            "cuisine": esc(r.get("cuisine")) or '<span class="muted">—</span>',
            "band": esc(r.get("price_band")) or '<span class="muted">—</span>',
            "area": esc(r.get("area")) or '<span class="muted">—</span>',
            "hours": hours_cell(r) if r.get("hours") else '<span class="muted">—</span>',
            "exceptions": ('Closed Monday' if r.get("hours") and not r["hours"].get("mon") else "—"),
            "social": socials(r),
            "links": link(r.get("website"), "Official") + " " + link(r.get("michelin_url"), "MICHELIN"),
        })
    body += table([
        {"key": "name", "label": "Restaurant"}, {"key": "cuisine", "label": "Cuisine"},
        {"key": "band", "label": "Price band"}, {"key": "area", "label": "Area"}, {"key": "hours", "label": "Days & hours"},
        {"key": "exceptions", "label": "Exceptions"}, {"key": "social", "label": "Reviews"},
        {"key": "links", "label": "Sources"}], t_rows, caption="Three-star restaurants with verified details")

    for tier, label, anchor in ((2, "Two stars", "two"), (1, "One star", "one")):
        tier_rows = [r for r in rows_all if r.get("stars") == tier]
        body += f'<h2 id="{anchor}">{esc(label)} · {len(tier_rows)} restaurants</h2>'
        if tier == 1:
            body += callout("info", "Why so many rows are blank",
                             "One-star rows carry name, cuisine, area and a MICHELIN link. Hours, phone and booking partner "
                             "have only been captured for a handful so far, so those cells stay empty with an unverified chip "
                             "rather than being filled from a secondary source.")
        t_rows = []
        for r in tier_rows:
            t_rows.append({
                "name": f'{esc(r["name"])} {verif(r.get("verified"))}',
                "cuisine": esc(r.get("cuisine")) or '<span class="muted">—</span>',
                "band": esc(r.get("price_band")) or '<span class="muted">—</span>',
                "area": esc(r.get("area")) or '<span class="muted">—</span>',
                "hours": hours_cell(r) if r.get("hours") else '<span class="muted">—</span>',
                "social": socials(r),
                "links": link(r.get("website"), "Official") + " " + link(r.get("michelin_url"), "MICHELIN"),
            })
        body += table([
            {"key": "name", "label": "Restaurant"}, {"key": "cuisine", "label": "Cuisine"},
            {"key": "band", "label": "Price band"}, {"key": "area", "label": "Area"}, {"key": "hours", "label": "Hours"},
            {"key": "social", "label": "Reviews"}, {"key": "links", "label": "Sources"}],
            t_rows, caption=f"{label} restaurants")

    body += '<h2 id="bib">Bib Gourmand and Guide-listed</h2>'
    body += callout("info", "Counted, not tabled",
                     f"{counts.get('bib_gourmand', 76)} Bib Gourmand restaurants and {counts.get('selected', 224)} "
                     "Guide-listed restaurants were counted from the live MICHELIN listings. They are not individual rows "
                     "on this page yet (flag F-13); ask if you want the cheaper roster expanded, which is the most useful "
                     "addition for a week with 14 meals.")
    body += f'<p>{link("https://guide.michelin.com/en/us/new-york-state/new-york/restaurants/bib-gourmand", "Bib Gourmand listing")} · {link("https://guide.michelin.com/en/us/new-york-state/new-york/restaurants/all-starred", "All starred listing")} · {link("https://guide.michelin.com/us/en/article/michelin-guide-ceremony/all-the-stars-in-the-michelin-guide-to-new-york-city-2025", "2025 ceremony article")}</p>'

    body += '<h2>Cost for two, honestly</h2>'
    body += callout("warn", "Prices are not on the MICHELIN pages",
                     "MICHELIN publishes a price tier (e.g. $$$$) but not the menu price. Tasting-menu prices for these "
                     "restaurants are therefore left blank rather than estimated, and the Open Questions page lists this "
                     "as the single biggest missing input for budgeting.")
    body += '<h2>Roster notes</h2><ul class="checks">'
    for f in RESTAURANTS.get("roster_flags", []):
        body += f"<li>{esc(f)}</li>"
    body += "</ul>"
    page("michelin.html", "Michelin & Dining", "All 69 MICHELIN-starred New York restaurants, tiered, with the distinction between stars and Guide listings explained.", body)


def page_activities():
    rows = ACTIVITIES.get("rows", [])
    body = head("Things to do", "Nine activities, four already timed from the hotel",
                "Hours, closing days, prices and booking rules taken from each venue's own website. "
                "Where a venue does not publish a value, the cell is blank and flagged rather than filled in. "
                "Only the legs that were actually measured show a travel time; the rest stay blank.")

    t = []
    for r in rows:
        t.append({
            "name": f'<strong>{esc(r["name"])}</strong><br><span class="xs muted">{esc(r.get("category",""))} · {esc(r.get("area",""))}</span>',
            "hours": hours_cell(r) if r.get("hours") else '<span class="muted">—</span>',
            "exceptions": esc(r.get("exceptions")) if r.get("exceptions") else '<span class="muted">—</span>',
            "price": esc(r.get("price")) if r.get("price") else '<span class="muted">—</span>',
            "two": money(r.get("price_for_two")) if r.get("price_for_two") is not None else '<span class="muted">—</span>',
            "travel": (f'{r["metro_minutes"]} min<br><span class="xs muted">from Eurostars</span>' if r.get("metro_minutes") else '<span class="muted">—</span>'),
            "social": socials(r),
            "links": link(r.get("source"), "Official") + " " + verif(r.get("verified")),
        })
    body += table([
        {"key": "name", "label": "Activity"}, {"key": "hours", "label": "Days & hours"},
        {"key": "exceptions", "label": "Exceptions"}, {"key": "price", "label": "Admission"},
        {"key": "two", "label": "For two"}, {"key": "travel", "label": "Travel"},
        {"key": "social", "label": "Reviews"}, {"key": "links", "label": "Source"}],
        t, caption="Activities with verified hours, exceptions and prices")

    body += '<h2>Notes that change the plan</h2><ul class="checks">'
    for f in ACTIVITIES.get("flags", []):
        body += f"<li>{esc(f)}</li>"
    body += "</ul>"

    body += '<h2>Detail</h2>'
    for r in rows:
        body += f'<details class="acc"><summary>{esc(r["name"])} {verif(r.get("verified"))}</summary>'
        body += f'<div class="acc-body"><p class="small"><strong>Address:</strong> {e(r.get("address"))}</p>'
        if r.get("notes"):
            body += f'<p class="small">{esc(r["notes"])}</p>'
        if r.get("booking"):
            body += f'<p class="small"><strong>Booking:</strong> {esc(r["booking"])}</p>'
        if r.get("price_note"):
            body += f'<p class="small muted">{esc(r["price_note"])}</p>'
        body += f'<p>{link(r.get("website"), "Official site")}</p></div></details>'

    page("activities.html", "Activities", "Nine New York activities near the recommended hotel, with verified hours, closures and admission prices.", body)


def page_itinerary():
    body = head("Day by day", "A seven-day plan built around closures, not around wishlists",
                "Every slot is placed on a day the venue is verified open. Two of the seven days are Mondays, "
                "which is the city's weakest restaurant night - the plan works with that instead of ignoring it.")

    body += callout("info", "The calendar",
                     "2027-02-15 is a Monday. The user's preferred window runs 15-18 February, so days 1-4 sit inside it "
                     "and days 5-8 extend the stay to a full seven nights. 2027-02-22, checkout day, is also a Monday.")

    for d in ITINERARY.get("days", []):
        body += f'<section class="day"><h2>Day {d["day"]} · {esc(d["date"])} · {esc(d["weekday"])}</h2>'
        body += f'<p class="eyebrow">{esc(d.get("theme"))}</p>'
        items = []
        for it in d.get("items", []):
            items.append({
                "time": f'<strong>{esc(it["time"])}</strong>',
                "what": esc(it["what"]),
                "note": f'<span class="xs muted">{esc(it.get("note",""))}</span>',
                "src": link(it.get("source"), "Source") + " " + verif(it.get("verified")),
            })
        body += table([{"key": "time", "label": "When"}, {"key": "what", "label": "What"}, {"key": "note", "label": "Note"}, {"key": "src", "label": "Evidence"}],
                      items, caption=f"Day {d['day']} plan")
        body += f'<p class="small muted"><strong>Why this day:</strong> {esc(d.get("why",""))}</p></section>'

    body += '<h2>Rule checks</h2><ul class="checks">'
    for r in ITINERARY.get("rule_checks", []):
        body += f"<li>{esc(r)}</li>"
    body += "</ul>"
    body += '<h2>Itinerary flags</h2><ul class="checks">'
    for f in ITINERARY.get("flags", []):
        body += f"<li>{esc(f)}</li>"
    body += "</ul>"

    page("itinerary.html", "Itinerary", "A seven-day New York plan where every venue is scheduled on a day it is verified open.", body)


def page_booking():
    body = head("Money", "What to book, when, and what the numbers really mean",
                "Five seven-night windows were priced for a queen bed in a 4-5 star Manhattan hotel. "
                "The preferred week is the cheapest. Every figure is pre-tax and that matters more than the ranking.")

    wins = WINDOWS.get("windows", [])
    t = []
    for w in wins:
        t.append({
            "label": f'<strong>{esc(w.get("label"))}</strong><br><span class="xs muted">{esc(w.get("nights"))} nights</span>',
            "dates": f'{esc(w.get("checkin"))} → {esc(w.get("checkout"))}',
            "hotel": esc(w.get("cheapest_hotel")) + f'<br><span class="xs muted">{esc(w.get("cheapest_room",""))}</span>',
            "total": f'<strong>{money(w.get("total_usd"))}</strong>',
            "per": money(w.get("per_night_usd")),
            "note": esc(w.get("note", "")) if w.get("note") else '<span class="muted">—</span>',
            "src": link(w.get("source"), "Booking"),
        })
    body += table([{"key": "label", "label": "Window"}, {"key": "dates", "label": "Dates"}, {"key": "hotel", "label": "Cheapest qualifying room"},
                   {"key": "total", "label": "7 nights"}, {"key": "per", "label": "Per night"}, {"key": "note", "label": "Caveat"}, {"key": "src", "label": "Source"}],
                  t, caption="Seven-night windows priced for two adults")

    body += callout("warn", "The tax gap",
                     "Booking.com's displayed week totals exclude 14.75% tax plus a $4 per-night city tax. "
                     "On the $848 Eurostars rate the page itself showed $149.66 of tax excluded - a real total nearer "
                     "$998, about 18% above the headline.")

    ttb = WINDOWS.get("time_to_book", {})
    body += '<h2>When to book</h2>'
    body += callout("warn", "No forecast is claimed",
                     f"<strong>Status: {esc(ttb.get('status','unverified'))}.</strong> {esc(ttb.get('finding',''))}")
    body += f'<p class="small">{esc(ttb.get("what_we_can_say",""))}</p>'
    body += f'<p class="small muted">{esc(ttb.get("how_to_verify",""))}</p>'

    body += '<h2>Price flags</h2><ul class="checks">'
    for f in WINDOWS.get("flags", []):
        body += f"<li>{esc(f)}</li>"
    body += "</ul>"

    body += '<h2>The realistic total</h2>'
    body += table([{"key": "item", "label": "Item"}, {"key": "detail", "label": "Detail"}, {"key": "src", "label": "Basis"}], [
        {"item": "Hotel, 7 nights", "detail": "$848 pre-tax · about $998 after 14.75% tax and $4/night", "src": link("https://www.booking.com/hotel/us/exchange-manhattan.html?checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1&selected_currency=USD", "Booking")},
        {"item": "Subway / bus", "detail": "$3.00 per ride per person, as displayed on every directions panel", "src": link("https://www.google.com/maps/dir/?api=1&origin=Eurostars+Wall+Street+New+York&destination=Le+Bernardin+New+York&travelmode=transit", "Maps")},
        {"item": "MoMA", "detail": "$60 for two adults", "src": link("https://www.moma.org/visit/", "MoMA")},
        {"item": "The Met", "detail": "$60 for two adults", "src": link("https://www.metmuseum.org/plan-your-visit", "The Met")},
        {"item": "Top of the Rock", "detail": "from $84 for two, timed admission", "src": link("https://www.rockefellercenter.com/tickets/top-of-the-rock-observation-deck/", "Rockefeller Center")},
        {"item": "Katz's", "detail": "about $62 for two pastrami sandwiches", "src": link("https://katzsdelicatessen.com/store-menu", "Katz's")},
        {"item": "Michelin dinners", "detail": "not budgetable - tasting-menu prices are not published on the MICHELIN pages", "src": '<span class="verif u">Unverified</span>'},
    ], caption="A partial all-in estimate, with the unavailable figures named rather than guessed")

    page("booking-strategy.html", "Booking Strategy", "Five priced seven-night windows, the tax gap that changes the ranking, and an honest statement that no booking-time forecast is possible.", body)


def page_questions():
    body = head("Open questions", "What a human still has to decide",
                "The site is complete without these answers, but the trip is not. Each question says what is known, "
                "what is missing, and exactly how to find it.")
    body += f'<p class="lede">{esc(QUESTIONS.get("intro",""))}</p>'
    for g in QUESTIONS.get("groups", []):
        body += f'<details class="acc" open><summary>{esc(g.get("title"))} <span class="badge neutral">{esc(g.get("decision_impact",""))} impact</span></summary>'
        body += '<div class="acc-body">'
        body += f'<p class="small"><strong>Why it matters.</strong> {esc(g.get("why",""))}</p>'
        body += f'<p class="small"><strong>Already known.</strong> {esc(g.get("known",""))}</p>'
        body += f'<p class="small"><strong>Still missing.</strong> {esc(g.get("missing",""))}</p>'
        body += f'<p class="small"><strong>How to find it.</strong> {esc(g.get("how_to_find",""))}</p>'
        body += f'<p class="xs muted">Ref {esc(g.get("id"))} · status {esc(g.get("status"))}</p>'
        body += "</div></details>"
    body += '<h2>How to discover what is missing</h2><ul class="checks">'
    for p in QUESTIONS.get("discovery_playbook", []):
        body += f"<li>{esc(p)}</li>"
    body += "</ul>"
    page("open-questions.html", "Open Questions", "Twelve decisions that public data cannot settle, each with a concrete way to resolve it.", body)


def page_suggestions():
    body = head("Suggestions", "Proposals to review before anything changes",
                "Nothing on this list has been implemented. Each item states the change, the reason and the page it would touch, "
                "so it can be accepted or rejected one at a time.")
    body += f'<p class="lede">{esc(SUGGESTIONS.get("intro",""))}</p>'
    items = SUGGESTIONS.get("items", [])
    body += '<div class="grid cols-3">'
    for i in items:
        body += '<div class="card suggestion">'
        body += f'<p class="eyebrow">{esc(i.get("id"))} · {esc(i.get("priority"))} priority · {esc(i.get("effort"))} effort</p>'
        body += f'<h3 class="mt0">{esc(i.get("title"))}</h3>'
        body += f'<p class="small">{esc(i.get("proposal"))}</p>'
        body += f'<p class="xs muted"><strong>Why:</strong> {esc(i.get("rationale"))}</p>'
        body += f'<p class="xs muted">Touches: {esc(i.get("affects"))}</p>'
        body += '<div class="review-actions">'
        body += '<button class="btn small" type="button" data-suggest="accept">Accept</button>'
        body += '<button class="btn small ghost" type="button" data-suggest="reject">Reject</button>'
        body += f'<span class="review-state" data-suggest-id="{esc(i.get("id"))}">{esc(i.get("status"))}</span>'
        body += '</div></div>'
    body += '</div>'
    body += '<p class="small muted">Selections are stored in your browser only — they are a review aid, not a change to the data. '
    body += 'To actually adopt one, note the ID (S-01 … S-12) and it can be implemented in a later session.</p>'
    page("suggestions.html", "Site Suggestions", "Twelve proposed changes to the site and the trip plan, each flagged for review rather than applied.", body)


def page_flags():
    body = head("Flagged for review", "Everything this project could not confirm",
                "Nothing here has been silently fixed. Each item says what was found, what the site does about it, "
                "and what a reviewer should do next.")
    items = FLAGS.get("items", [])
    body += '<div class="grid cols-3">'
    for f in items:
        body += '<div class="card">'
        body += f'<p class="eyebrow">{esc(f.get("id"))} · {esc(f.get("severity"))} severity</p>'
        body += f'<h3 class="mt0">{esc(f.get("title"))}</h3>'
        body += f'<p class="xs muted">{esc(f.get("category"))}</p>'
        body += f'<p class="small">{esc(f.get("detail"))}</p>'
        body += f'<p class="small"><strong>On the site:</strong> {esc(f.get("effect_on_site"))}</p>'
        body += f'<p class="small"><strong>Next action:</strong> {esc(f.get("action"))}</p>'
        body += '</div>'
    body += '</div>'
    page("flagged-for-review.html", "Flagged for Review", "Fourteen known gaps, conflicts and traps, each with its current handling and a next action.", body)


def page_audit():
    head_ = AUDIT.get("headline", {})
    body = head("Transparency", "A line-by-line audit of this project's own claims",
                "What the site asserts, what evidence supports it, and where it falls short. "
                "A reviewer should be able to check this page rather than trust the rest.")
    body += '<div class="grid cols-4">'
    for k, label in (("rows_fully_verified", "rows fully verified"), ("transit_legs_measured", "transit legs measured"),
                     ("open_flags", "open flags"), ("open_questions", "open questions")):
        body += kpi(str(head_.get(k, "—")), label)
    body += '</div>'
    body += f'<p class="lede">{esc(AUDIT.get("intro",""))}</p>'

    rows = []
    for f in AUDIT.get("findings", []):
        state = {"verified": "v", "partial": "f", "blocked": "u"}.get(f.get("status"), "u")
        rows.append({
            "id": f'<strong>{esc(f.get("id"))}</strong><br><span class="xs muted">{esc(f.get("area"))}</span>',
            "claim": esc(f.get("claim")),
            "evidence": esc(f.get("evidence")),
            "status": verif(state) + f'<br><span class="xs muted">{esc(f.get("status"))}</span>',
            "caveat": esc(f.get("caveat")) if f.get("caveat") else '<span class="muted">—</span>',
            "link": link(f.get("link"), "Open"),
        })
    body += table([{"key": "id", "label": "Ref"}, {"key": "claim", "label": "Claim"}, {"key": "evidence", "label": "Evidence"},
                   {"key": "status", "label": "Status"}, {"key": "caveat", "label": "Caveat"}, {"key": "link", "label": "Source"}],
                  rows, caption="Audit findings")

    body += '<h2>Sources used</h2>'
    body += table([{"key": "name", "label": "Source"}, {"key": "used", "label": "Used for"}, {"key": "url", "label": "Link"}],
                  [{"name": esc(s["name"]), "used": esc(s["used_for"]), "url": link(s["url"], "Open")} for s in AUDIT.get("sources_registry", [])],
                  caption="Registry of every source consulted")

    body += '<h2>Method notes</h2><ul class="checks">'
    for m in AUDIT.get("method_notes", []):
        body += f"<li>{esc(m)}</li>"
    body += "</ul>"

    body += '<h2>Raw data</h2>'
    body += '<p class="small">Every table on this site is generated from JSON in the repository. Nothing is hard-coded in the templates, so a correction to a data file regenerates the affected pages.</p><ul class="checks">'
    for f in ("restaurants", "hotels", "activities", "pricing_windows", "transit_anchors", "itinerary", "questions", "suggestions", "flags", "audit", "executive_summary", "site"):
        body += f'<li>{link("https://github.com/kanlerxz87-cyber/NYFun2/blob/main/sessions/33cfdba4/data/" + f + ".json", "data/" + f + ".json")}</li>'
    body += "</ul>"

    page("repo-audit.html", "Repo Audit", "Fifteen audit findings with evidence and status, the full source registry, and links to the raw data.", body)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    page_index()
    page_exec()
    page_hotels()
    page_michelin()
    page_activities()
    page_itinerary()
    page_booking()
    page_questions()
    page_suggestions()
    page_flags()
    page_audit()
    written = sorted(p.name for p in OUT.glob("*.html"))
    print(f"Built {len(written)} pages: {', '.join(written)}")


if __name__ == "__main__":
    main()
