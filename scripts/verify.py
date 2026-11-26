#!/usr/bin/env python3
"""Static verification for the NYFun2 dashboard.

Checks: local links resolve, JSON parses, every data row carries a source URL,
social links are real URLs, IDs/names are unique, and blank fields have an
explanatory flag. No network calls are made: a link's existence is not the
same as a verified fact, and the latter is recorded in COORDINATION.md.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []
warnings = []
row_count = 0

HTML_FILES = sorted(ROOT.glob('*.html')) + sorted((ROOT / 'pages').glob('*.html'))
for html in HTML_FILES:
    text = html.read_text(encoding='utf-8')
    for href in re.findall(r'href="([^"#]+)', text):
        if href.startswith(('http://', 'https://', 'mailto:', 'tel:', 'javascript:')):
            continue
        target = (html.parent / href.split('?')[0]).resolve()
        if not target.exists():
            errors.append(f'{html.relative_to(ROOT)}: missing local link {href}')

# Every root page must expose the same navigation, including the research page.
for html in HTML_FILES:
    text = html.read_text(encoding='utf-8')
    if 'class="nav"' in text and 'research.html' not in text:
        errors.append(f'{html.relative_to(ROOT)}: nav is missing research.html')

row_files = {
    'data/restaurants.json': 'items',
    'data/activities.json': 'items',
    'data/hotels.json': 'items',
    'data/decisions.json': 'flags',
}
docs = {rel: json.loads((ROOT / rel).read_text(encoding='utf-8')) for rel in row_files}
docs['data/integration.json'] = json.loads((ROOT / 'data/integration.json').read_text(encoding='utf-8'))


def check_source(label, value, field='sourceUrl'):
    if not value or not str(value).startswith('https://'):
        errors.append(f'{label}: no https official source URL in {field}')


def check_social(label, row, field):
    for link in row.get(field, []) or []:
        url = link.get('url', '')
        if not url.startswith(('https://', 'http://')):
            errors.append(f'{label}: social link is not a URL: {url!r}')
        if not link.get('platform'):
            warnings.append(f'{label}: social link has no platform label')


for rel, key in row_files.items():
    doc = docs[rel]
    rows = doc[key] if key in doc else sum((doc[k] for k in ('questions', 'suggestions', 'flags')), [])
    row_count += len(rows)
    ids = set()
    for i, row in enumerate(rows, 1):
        label = f'{rel} row {i} ({row.get("name") or row.get("title") or row.get("id")})'
        if row.get('id'):
            if row['id'] in ids:
                errors.append(f'{label}: duplicate id {row["id"]}')
            ids.add(row['id'])
        source = row.get('sourceUrl') or row.get('source') or row.get('rateSourceUrl')
        if rel != 'data/decisions.json' or key == 'flags':
            check_source(label, source, 'source/rateSourceUrl')
        if rel == 'data/restaurants.json':
            blankable = ['address', 'hours', 'priceTwoAdults', 'officialUrl']
            check_social(label, row, 'social')
        elif rel == 'data/hotels.json':
            blankable = ['room', 'privateBathroom', 'sevenNightTotal', 'cheapestWindow', 'publishedRate']
        elif rel == 'data/activities.json':
            blankable = ['hours', 'costTwoAdults']
            check_social(label, row, 'social')
        else:
            blankable = []
        if any(not row.get(f) for f in blankable) and not row.get('flags'):
            warnings.append(f'{label}: blank field with no flag')

# Names must be unique inside the three entity tables.
for rel in ('data/restaurants.json', 'data/activities.json', 'data/hotels.json'):
    names = [r['name'] for r in docs[rel]['items']]
    seen = set()
    for name in names:
        if name in seen:
            errors.append(f'{rel}: duplicate row name {name!r}')
        seen.add(name)

# Cross-session evidence tables: each row needs its own source URL.
integ = docs['data/integration.json']
for key in ('bookingWindows', 'transit', 'activitiesTransit', 'hotelRanking', 'findings'):
    rows = integ.get(key, [])
    row_count += len(rows)
    for i, row in enumerate(rows, 1):
        label = f'data/integration.json {key} row {i} ({row.get("id")})'
        check_source(label, row.get('sourceUrl'))
        if not row.get('id'):
            errors.append(f'{label}: missing id')

for label, questions in (('questions', docs['data/decisions.json']['questions']),
                         ('suggestions', docs['data/decisions.json']['suggestions'])):
    ids = [q.get('id') for q in questions]
    if len(ids) != len(set(ids)):
        errors.append(f'data/decisions.json: duplicate {label} ids: {ids}')

print(f'Checked {len(HTML_FILES)} HTML pages and {row_count} data rows.')
for w in warnings:
    print('WARN ', w)
for e in errors:
    print('ERROR', e)
print(f'Result: {len(errors)} errors, {len(warnings)} warnings')
sys.exit(1 if errors else 0)
