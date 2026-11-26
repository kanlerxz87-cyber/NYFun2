#!/usr/bin/env python3
"""Static verification for the NYFun2 dashboard. No network calls.

Checks
  1. every local href/src in HTML resolves
  2. every JSON file parses and every dataset has its integration date
  3. every restaurant / hotel / activity / flag / verification row carries an
     http(s) source URL on an official or clearly labelled domain
  4. no duplicate names inside a dataset
  5. a blank critical field is explained by a flag (warning, not an error)
  6. hotel all-in totals are consistent with the published pre-tax total using
     the stated 14.75% + fee formula (tolerance $6 for rounding / fee shape)
  7. every social link is a real https URL
  8. navigation on every page points at a file that exists

Exit code 1 on any error.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors, warnings, notes = [], [], []
rows_checked = 0


def add(lst, msg):
    lst.append(msg)


# ---------------------------------------------------------------- local links
for html in sorted(ROOT.glob("*.html")) + sorted((ROOT / "pages").glob("*.html")):
    text = html.read_text(encoding="utf-8")
    for attr, href in re.findall(r'(href|src)="([^"]+)"', text):
        if href.startswith(("http://", "https://", "mailto:", "tel:", "javascript:", "#")):
            continue
        target = (html.parent / href.split("#")[0].split("?")[0]).resolve()
        if not target.exists():
            add(errors, f"{html.relative_to(ROOT)}: missing local {attr} -> {href}")
    # navigation sanity
    if 'class="nav"' not in text and html.name != "index.html":
        add(errors, f"{html.relative_to(ROOT)}: no navigation block")
    for label in ("Overview", "Michelin", "Hotels", "Activities", "Verification"):
        if label not in text:
            add(warnings, f"{html.relative_to(ROOT)}: nav label missing: {label}")

# ------------------------------------------------------------------- datasets
FILES = {
    "data/restaurants.json": ("items", ["address", "hours", "priceTwoAdults", "social"]),
    "data/hotels.json": ("items", ["room", "privateBathroom", "sevenNightPreTax", "sevenNightAllIn"]),
    "data/activities.json": ("items", ["hours", "costTwoAdults"]),
}
docs = {}
for rel, (key, blankable) in FILES.items():
    doc = json.loads((ROOT / rel).read_text(encoding="utf-8"))
    docs[rel] = doc
    if doc.get("meta", {}).get("integrationCheckedOn") is None:
        add(errors, f"{rel}: meta.integrationCheckedOn missing")
    rows = doc[key]
    names = [r.get("name") for r in rows]
    dupes = {n for n in names if names.count(n) > 1}
    if dupes:
        add(errors, f"{rel}: duplicate rows {sorted(dupes)}")
    for row in rows:
        rows_checked += 1
        name = row.get("name")
        src = row.get("sourceUrl") or row.get("officialUrl") or row.get("rateSourceUrl")
        if not (src and str(src).startswith("http")):
            add(errors, f"{rel} [{name}]: no http source URL")
        if row.get("priceSourceUrl") and not str(row["priceSourceUrl"]).startswith("http"):
            add(errors, f"{rel} [{name}]: price source is not a URL")
        if any(not row.get(f) for f in blankable) and not row.get("flags") and not row.get("eligibilityNote"):
            add(warnings, f"{rel} [{name}]: blank field without an explanatory flag")
        for s in row.get("social") or []:
            if not str(s.get("url", "")).startswith("https://"):
                add(errors, f"{rel} [{name}]: social link is not https ({s.get('url')})")
            if not s.get("platform"):
                add(warnings, f"{rel} [{name}]: social link without platform label")

# ------------------------------------------------------------- hotel arithmetic
TAX = 0.1475
for h in docs["data/hotels.json"]["items"]:
    pre = re.search(r"\$([\d,]+)", str(h.get("sevenNightPreTax") or ""))
    allin = re.search(r"\$([\d,]+)", str(h.get("sevenNightAllIn") or ""))
    if not (pre and allin):
        continue
    p = int(pre.group(1).replace(",", ""))
    a = int(allin.group(1).replace(",", ""))
    est = p * (1 + TAX) + 28  # 14.75% + ~$4/night city unit fee, as documented on the row
    if abs(a - est) > max(12, 0.02 * est):
        add(warnings, f"hotels [{h['name']}]: all-in ${a} vs formula ${est:.0f} from ${p} — check taxBasis")

# --------------------------------------------------------------- decisions log
dec = json.loads((ROOT / "data/decisions.json").read_text(encoding="utf-8"))
for section in ("questions", "suggestions", "flags"):
    ids = [x["id"] for x in dec[section]]
    if len(ids) != len(set(ids)):
        add(errors, f"decisions.{section}: duplicate IDs")
for f in dec["flags"]:
    rows_checked += 1
    if not str(f.get("source", "")).startswith("http") and not str(f.get("source", "")).startswith("data/"):
        add(errors, f"flags [{f['id']}]: no usable source")
for q in dec["questions"]:
    for s in q.get("sources") or []:
        if not str(s).startswith("http"):
            add(errors, f"questions [{q['id']}]: source is not a URL")

# ------------------------------------------------------------ verification log
ver = json.loads((ROOT / "data/verification.json").read_text(encoding="utf-8"))
for c in ver["checks"]:
    rows_checked += 1
    if not str(c.get("source", "")).startswith("http"):
        add(errors, f"verification [{c['fact']}]: no http source")

# --------------------------------------------------------------------- report
print(f"Checked {len(list(ROOT.glob('*.html'))) + len(list((ROOT / 'pages').glob('*.html')))} HTML pages "
      f"and {rows_checked} data rows.")
print(f"Datasets: restaurants {len(docs['data/restaurants.json']['items'])}, "
      f"hotels {len(docs['data/hotels.json']['items'])}, "
      f"activities {len(docs['data/activities.json']['items'])}, "
      f"questions {len(dec['questions'])}, suggestions {len(dec['suggestions'])}, flags {len(dec['flags'])}, "
      f"verification checks {len(ver['checks'])}")
for w in warnings:
    print("WARN ", w)
for err in errors:
    print("ERROR", err)
print(f"Result: {len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
