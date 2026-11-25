#!/usr/bin/env python3
"""Static verification suite for sessions/657520df NYC 2027 Couple Planner."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

BASE = Path(__file__).resolve().parents[1]
DATA_DIR = BASE / "data"

errors: list[str] = []


def check_https(url: str, ctx: str) -> None:
    if not url:
        errors.append(f"{ctx}: empty URL where official URL is required")
        return
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        errors.append(f"{ctx}: invalid https URL '{url}'")


def verify_json_files() -> dict[str, dict]:
    loaded: dict[str, dict] = {}
    for name in ("restaurants.json", "hotels.json", "activities.json", "decisions_and_audit.json"):
        p = DATA_DIR / name
        if not p.exists():
            errors.append(f"Missing data file: {p}")
            continue
        loaded[name] = json.loads(p.read_text(encoding="utf-8"))
    return loaded


def verify_restaurants(data: dict) -> None:
    items = data.get("items", [])
    if len(items) < 20:
        errors.append(f"Expected >=20 Michelin rows, found {len(items)}")
    seen_ids = set()
    for r in items:
        rid = r.get("id", "<missing>")
        if rid in seen_ids:
            errors.append(f"Duplicate restaurant id: {rid}")
        seen_ids.add(rid)
        check_https(r.get("sourceUrl", ""), f"restaurant[{rid}].sourceUrl")
        if r.get("officialUrl"):
            check_https(r["officialUrl"], f"restaurant[{rid}].officialUrl")
        else:
            if not r.get("flags"):
                errors.append(f"restaurant[{rid}] has blank officialUrl without a flag")
        if not r.get("coupleMenuTotal"):
            if not r.get("flags"):
                errors.append(f"restaurant[{rid}] has blank coupleMenuTotal without a flag")
        if not r.get("socials"):
            if not r.get("flags"):
                errors.append(f"restaurant[{rid}] has empty socials without a flag")
        for s in r.get("socials", []):
            check_https(s.get("url", ""), f"restaurant[{rid}].social")


def verify_hotels(data: dict) -> None:
    items = data.get("items", [])
    if len(items) < 8:
        errors.append(f"Expected >=8 hotels, found {len(items)}")
    for h in items:
        hid = h.get("id", "<missing>")
        check_https(h.get("officialUrl", ""), f"hotel[{hid}].officialUrl")
        check_https(h.get("roomSourceUrl", ""), f"hotel[{hid}].roomSourceUrl")
        check_https(h.get("rateSourceUrl", ""), f"hotel[{hid}].rateSourceUrl")
        check_https(h.get("transitSourceUrl", ""), f"hotel[{hid}].transitSourceUrl")
        room = h.get("qualifyingRoom", "").lower()
        if "queen" not in room and "king" not in room:
            errors.append(f"hotel[{hid}] qualifyingRoom '{h.get('qualifyingRoom')}' lacks Queen/King verification")
        bath = h.get("privateBathroom", "").lower()
        if "private" not in bath and "en-suite" not in bath:
            errors.append(f"hotel[{hid}] privateBathroom '{h.get('privateBathroom')}' not verified")
        if not h.get("allIn7Night"):
            if not h.get("flags"):
                errors.append(f"hotel[{hid}] has blank allIn7Night without a flag")
    for w in data.get("crossWeekWindows", []):
        check_https(w.get("sourceUrl", ""), f"window[{w.get('windowId')}].sourceUrl")


def verify_activities(data: dict) -> None:
    items = data.get("items", [])
    if len(items) < 14:
        errors.append(f"Expected >=14 activities, found {len(items)}")
    for a in items:
        aid = a.get("id", "<missing>")
        check_https(a.get("officialUrl", ""), f"activity[{aid}].officialUrl")
        check_https(a.get("sourceUrl", ""), f"activity[{aid}].sourceUrl")
        if not a.get("socials"):
            errors.append(f"activity[{aid}] missing social links")
        for s in a.get("socials", []):
            check_https(s.get("url", ""), f"activity[{aid}].social")


def verify_html_links() -> int:
    html_files = [BASE / "index.html"] + sorted((BASE / "pages").glob("*.html"))
    attr_re = re.compile(r'(?:href|src)="([^"]+)"')
    checked = 0
    for hf in html_files:
        text = hf.read_text(encoding="utf-8")
        for target in attr_re.findall(text):
            checked += 1
            if target.startswith(("https://", "mailto:", "#")):
                continue
            if target.startswith("http://"):
                errors.append(f"{hf.name}: insecure http:// link '{target}'")
                continue
            clean = target.split("#")[0].split("?")[0]
            resolved = (hf.parent / clean).resolve()
            if not resolved.exists():
                errors.append(f"{hf.relative_to(BASE)}: broken local link '{target}' -> {resolved}")
    return checked


def main() -> int:
    loaded = verify_json_files()
    if "restaurants.json" in loaded:
        verify_restaurants(loaded["restaurants.json"])
    if "hotels.json" in loaded:
        verify_hotels(loaded["hotels.json"])
    if "activities.json" in loaded:
        verify_activities(loaded["activities.json"])
    link_count = verify_html_links()

    if errors:
        print("VERIFICATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1

    r_cnt = len(loaded["restaurants.json"]["items"])
    h_cnt = len(loaded["hotels.json"]["items"])
    a_cnt = len(loaded["activities.json"]["items"])
    s_cnt = sum(len(x["socials"]) for x in loaded["restaurants.json"]["items"]) + sum(
        len(x["socials"]) for x in loaded["activities.json"]["items"]
    )
    print(
        f"OK: Verified {r_cnt} Michelin venues, {h_cnt} Queen+/private-bath hotels, "
        f"{a_cnt} activities, {s_cnt} social review links, and {link_count} HTML asset/nav links with 0 errors."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
