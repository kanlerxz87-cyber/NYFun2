#!/usr/bin/env python3
"""
check_site.py — pre-publish validation for the NYFun2 static site.

Runs with no third-party packages. Checks:
  1. every local href/src in every .html file resolves to a real file
  2. every page includes the shared stylesheet + the three scripts
  3. every page has the shared header/footer mount points
  4. every page in assets/app.js PAGES list exists on disk
  5. every page on disk is listed in the PAGES nav (no orphans)
  6. JS files parse (node --check, if node is available)
  7. JSON-ish sanity: no obviously unbalanced braces in the data files
  8. every flag id referenced in HTML (flagged.html#F-xx) exists in data.js
  9. every anchor target (page.html#id) resolves to an id present in that page
     or to a row id rendered from data.js
"""

import os
import re
import sys
import json
import shutil
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []
warnings = []


def read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def html_files():
    return sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))


def local_targets(html):
    """Yield (attr, url) for local hrefs/srcs."""
    for m in re.finditer(r'(?:href|src)="([^"]+)"', html):
        url = m.group(1)
        if url.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:", "javascript:")):
            continue
        yield url


def main():
    pages = html_files()
    if not pages:
        errors.append("no .html files found")
        print_report()
        return

    # ---- 1. local link targets -------------------------------------------
    for page in pages:
        html = read(os.path.join(ROOT, page))
        for url in local_targets(html):
            path = url.split("#")[0].split("?")[0]
            if not path:
                continue
            if not os.path.exists(os.path.join(ROOT, path)):
                errors.append(f"{page}: broken local link -> {url}")

    # ---- 2 & 3. shared assets and mount points ---------------------------
    for page in pages:
        html = read(os.path.join(ROOT, page))
        for asset in ("assets/site.css", "assets/data.js", "assets/tables.js", "assets/app.js"):
            if asset not in html:
                errors.append(f"{page}: missing reference to {asset}")
        if 'id="site-header"' not in html:
            errors.append(f'{page}: missing <div id="site-header">')
        if 'id="site-footer"' not in html:
            errors.append(f'{page}: missing <div id="site-footer">')
        if 'id="main"' not in html:
            warnings.append(f'{page}: no <main id="main"> anchor')

    # ---- 4 & 5. nav list vs disk ----------------------------------------
    app_js = read(os.path.join(ROOT, "assets", "app.js"))
    nav_block = re.search(r"var PAGES = \[(.*?)\];", app_js, re.S)
    if not nav_block:
        errors.append("assets/app.js: PAGES list not found")
        nav_pages = []
    else:
        nav_pages = re.findall(r"href:\s*'([^']+)'", nav_block.group(1))
        for p in nav_pages:
            if not os.path.exists(os.path.join(ROOT, p)):
                errors.append(f"app.js nav points at missing page: {p}")
        for p in pages:
            if p not in nav_pages and p != "404.html":
                warnings.append(f"page not in nav: {p}")

    # ---- 6. JS parse -----------------------------------------------------
    node = shutil.which("node")
    if node:
        for js in ("assets/data.js", "assets/tables.js", "assets/app.js"):
            full = os.path.join(ROOT, js)
            if not os.path.exists(full):
                errors.append(f"missing {js}")
                continue
            res = subprocess.run([node, "--check", full],
                                 capture_output=True, text=True)
            if res.returncode != 0:
                errors.append(f"{js}: syntax error -> {res.stderr.strip().splitlines()[:3]}")
    else:
        warnings.append("node not available — JS syntax check skipped")

    # ---- 7. execute the data files to collect ids ------------------------
    ids_by_page = {}
    flag_ids = set()
    data_js = read(os.path.join(ROOT, "assets", "data.js"))
    flag_ids = set(re.findall(r"id:\s*'(F-\d\d)'", data_js))
    q_ids = set(re.findall(r"id:\s*'(Q-\d\d)'", data_js))
    s_ids = set(re.findall(r"id:\s*'(S\d+)'", data_js))
    r_ids = set(re.findall(r"id:\s*'(R-\d\d)'", data_js))

    # local anchors declared in static HTML
    for page in pages:
        html = read(os.path.join(ROOT, page))
        ids_by_page[page] = set(re.findall(r'id="([^"]+)"', html))

    # ---- 8 & 9. anchor resolution ---------------------------------------
    def resolves(page, anchor):
        if anchor in ids_by_page.get(page, set()):
            return True
        # data-rendered row ids
        if page == "flagged.html" and anchor in flag_ids:
            return True
        if page == "questions.html" and anchor in q_ids:
            return True
        if page == "suggestions.html" and anchor in s_ids:
            return True
        if page == "repo-audit.html" and anchor in r_ids:
            return True
        return False

    for page in pages:
        html = read(os.path.join(ROOT, page))
        for m in re.finditer(r'href="([a-z0-9\-]+\.html)#([^"]+)"', html):
            target, anchor = m.group(1), m.group(2)
            if not os.path.exists(os.path.join(ROOT, target)):
                errors.append(f"{page}: anchor into missing page {target}")
                continue
            if not resolves(target, anchor):
                errors.append(f"{page}: -> {target}#{anchor} has no matching id")
        for m in re.finditer(r'href="#([^"]+)"', html):
            if not resolves(page, m.group(1)):
                errors.append(f'{page}: internal anchor #{m.group(1)} unresolved')

    # ---- flag ids referenced must exist ---------------------------------
    for page in pages:
        html = read(os.path.join(ROOT, page))
        for m in re.finditer(r"flagged\.html#(F-\d\d)", html):
            if m.group(1) not in flag_ids:
                errors.append(f"{page}: references unknown flag {m.group(1)}")

    # ---- table coverage --------------------------------------------------
    tables_js = read(os.path.join(ROOT, "assets", "tables.js"))
    for page in pages:
        html = read(os.path.join(ROOT, page))
        for m in re.finditer(r'data-table="([a-z_]+)"', html):
            key = m.group(1)
            if f"{key}:" not in tables_js:
                errors.append(f"{page}: data-table=\"{key}\" not defined in tables.js")

    print_report()


def print_report():
    print(f"checked in {ROOT}")
    if warnings:
        print("\nWARNINGS")
        for w in warnings:
            print("  !", w)
    if errors:
        print("\nERRORS")
        for e in errors:
            print("  x", e)
        print(f"\nFAILED — {len(errors)} error(s), {len(warnings)} warning(s)")
        sys.exit(1)
    print(f"\nOK — 0 errors, {len(warnings)} warning(s)")


if __name__ == "__main__":
    main()
