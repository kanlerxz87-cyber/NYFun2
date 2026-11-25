#!/usr/bin/env python3
"""Static integrity verifier for sessions/c1cf7b23/."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

BASE = Path(__file__).resolve().parent.parent
ERRORS: list[str] = []


def err(msg: str) -> None:
    ERRORS.append(msg)


def check_url(url: str, ctx: str, allow_http_betterchinatown: bool = True) -> None:
    if not url:
        err(f"{ctx}: empty URL")
        return
    p = urlparse(url)
    if p.scheme == "http" and allow_http_betterchinatown and p.netloc == "betterchinatown.com":
        return
    if p.scheme != "https" or not p.netloc:
        err(f"{ctx}: non-HTTPS or invalid URL -> {url!r}")


def verify_json_files() -> dict[str, int]:
    counts: dict[str, int] = {}

    r_data = json.loads((BASE / "data/restaurants.json").read_text())
    counts["restaurants"] = len(r_data["items"])
    for r in r_data["items"]:
        rid = f"restaurant:{r.get('id')}"
        if r.get("officialUrl"):
            check_url(r.get("officialUrl", ""), f"{rid}.officialUrl")
        elif not r.get("flags"):
            err(f"{rid}: blank officialUrl must carry an explanatory flag")
        check_url(r.get("sourceUrl", ""), f"{rid}.sourceUrl")
        if r.get("totalPriceTwoAdults"):
            check_url(r.get("priceSourceUrl", ""), f"{rid}.priceSourceUrl")
        else:
            if not r.get("flags"):
                err(f"{rid}: blank totalPriceTwoAdults must carry an explanatory flag")
        for s in r.get("social", []):
            check_url(s.get("url", ""), f"{rid}.social")

    h_data = json.loads((BASE / "data/hotels.json").read_text())
    counts["hotels"] = len(h_data["items"])
    for w in h_data["bookingWindows"]:
        check_url(w.get("sourceUrl", ""), f"window:{w.get('windowId')}")
    for h in h_data["items"]:
        hid = f"hotel:{h.get('id')}"
        check_url(h.get("officialUrl", ""), f"{hid}.officialUrl")
        check_url(h.get("sourceUrl", ""), f"{hid}.sourceUrl")
        if not h.get("sevenNightAllIn") and not h.get("flags"):
            err(f"{hid}: blank sevenNightAllIn must carry an explanatory flag")
        for s in h.get("social", []):
            check_url(s.get("url", ""), f"{hid}.social")

    a_data = json.loads((BASE / "data/activities.json").read_text())
    counts["activities"] = len(a_data["items"])
    for a in a_data["items"]:
        aid = f"activity:{a.get('id')}"
        check_url(a.get("officialUrl", ""), f"{aid}.officialUrl")
        check_url(a.get("sourceUrl", ""), f"{aid}.sourceUrl")
        if not a.get("costTwoAdults") and not a.get("flags"):
            err(f"{aid}: blank costTwoAdults must carry an explanatory flag")
        for s in a.get("social", []):
            check_url(s.get("url", ""), f"{aid}.social")

    d_data = json.loads((BASE / "data/decisions.json").read_text())
    counts["questions"] = len(d_data["questions"])
    counts["suggestions"] = len(d_data["suggestions"])
    counts["flags"] = len(d_data["flags"])
    for q in d_data["questions"]:
        check_url(q.get("sourceUrl", ""), f"question:{q.get('id')}")
    for f in d_data["flags"]:
        check_url(f.get("sourceUrl", ""), f"flag:{f.get('id')}")

    return counts


def verify_html_links() -> int:
    html_files = [BASE / "index.html", *sorted((BASE / "pages").glob("*.html"))]
    href_re = re.compile(r'(?:href|src)="([^"]+)"')
    for hf in html_files:
        txt = hf.read_text()
        for m in href_re.finditer(txt):
            ref = m.group(1)
            if ref.startswith(("https://", "http://", "#", "mailto:")):
                continue
            target = (hf.parent / ref.split("#")[0]).resolve()
            if not target.exists():
                err(f"{hf.relative_to(BASE)}: broken local link {ref!r} -> {target}")
    return len(html_files)


def main() -> int:
    counts = verify_json_files()
    html_n = verify_html_links()
    if ERRORS:
        for e in ERRORS:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print(
        f"OK: {html_n} HTML pages and JSON datasets verified cleanly -> {counts} | 0 errors"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
