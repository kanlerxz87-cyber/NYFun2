#!/usr/bin/env python3
"""Static verification for the NYFun2 dashboard.

Checks: local links resolve, JSON parses, every data row carries an official
source URL, and blank fields have an explanatory flag. No network calls are made.
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
    'data/restaurants.json': 'items',
    'data/activities.json': 'items',
    'data/hotels.json': 'items',
    'data/decisions.json': 'flags',
}
for rel, key in row_files.items():
    doc = json.loads((ROOT / rel).read_text(encoding='utf-8'))
    rows = doc[key] if key in doc else sum((doc[k] for k in ('questions', 'suggestions', 'flags')), [])
    for i, row in enumerate(rows, 1):
        label = f'{rel} row {i} ({row.get("name") or row.get("title") or row.get("id")})'
        source = row.get('sourceUrl') or row.get('source') or row.get('rateSourceUrl')
        if not source or not source.startswith('https://'):
            errors.append(f'{label}: no https official source URL')
        if rel == 'data/restaurants.json':
            blankable = ['address', 'hours', 'priceTwoAdults', 'officialUrl']
        elif rel == 'data/hotels.json':
            blankable = ['room', 'privateBathroom', 'sevenNightTotal', 'cheapestWindow', 'publishedRate']
        elif rel == 'data/activities.json':
            blankable = ['hours', 'costTwoAdults']
        else:
            blankable = []
        if any(not row.get(f) for f in blankable) and not row.get('flags'):
            warnings.append(f'{label}: blank field with no flag')

print(f'Checked HTML local links and {sum(len(json.loads((ROOT / f).read_text())[k]) for f, k in row_files.items() if k in json.loads((ROOT / f).read_text()))} data rows.')
for w in warnings:
    print('WARN ', w)
for e in errors:
    print('ERROR', e)
print(f'Result: {len(errors)} errors, {len(warnings)} warnings')
sys.exit(1 if errors else 0)
