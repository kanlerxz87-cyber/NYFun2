#!/usr/bin/env python3
"""Static verification for the NYFun2 dashboard.

Checks local HTML links, JSON validity, HTTPS source URLs on factual data rows,
optional source URL shapes in decisions, and explanatory flags for blank fields.
This is a local structural check only; it does not fetch URLs or determine whether
a page is official, current, or still available.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []
warnings = []

for html in sorted(ROOT.glob('*.html')) + sorted((ROOT / 'pages').glob('*.html')):
    text = html.read_text(encoding='utf-8')
    for href in re.findall(r'href="([^"#]+)', text):
        if href.startswith(('http://', 'https://', 'mailto:', 'tel:', 'javascript:')):
            continue
        target = (html.parent / href.split('?')[0]).resolve()
        if not target.exists():
            errors.append(f'{html.relative_to(ROOT)}: missing local link {href}')

row_files = {
    'data/restaurants.json': ('items',),
    'data/activities.json': ('items',),
    'data/hotels.json': ('items',),
    'data/decisions.json': ('questions', 'suggestions', 'flags'),
}
row_count = 0
for rel, keys in row_files.items():
    doc = json.loads((ROOT / rel).read_text(encoding='utf-8'))
    rows = [row for key in keys for row in doc.get(key, [])]
    row_count += len(rows)
    for i, row in enumerate(rows, 1):
        label = f'{rel} row {i} ({row.get("name") or row.get("title") or row.get("question") or row.get("id")})'
        is_decision_prompt = rel == 'data/decisions.json' and row in doc.get('questions', []) + doc.get('suggestions', [])
        source = row.get('sourceUrl') or row.get('source') or row.get('rateSourceUrl')
        sources = row.get('sources')
        if not is_decision_prompt and (not source or not source.startswith('https://')):
            errors.append(f'{label}: no https official source URL')
        if sources is not None:
            if not isinstance(sources, list) or any(not isinstance(url, str) or not url.startswith('https://') for url in sources):
                errors.append(f'{label}: sources must be a list of https URLs')
        if rel == 'data/restaurants.json':
            blankable = ['address', 'hours', 'priceTwoAdults', 'officialUrl']
        elif rel == 'data/hotels.json':
            blankable = ['room', 'privateBathroom', 'sevenNightTotal', 'cheapestWindow', 'publishedRate']
        elif rel == 'data/activities.json':
            blankable = ['hours', 'costTwoAdults']
        else:
            blankable = []
        if any(not row.get(field) for field in blankable) and not row.get('flags'):
            warnings.append(f'{label}: blank field with no flag')

print(f'Checked HTML local links and {row_count} JSON rows (including all decision rows).')
for warning in warnings:
    print('WARN ', warning)
for error in errors:
    print('ERROR', error)
print(f'Result: {len(errors)} errors, {len(warnings)} warnings')
sys.exit(1 if errors else 0)
