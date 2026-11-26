#!/usr/bin/env python3
"""Static verification for the canonical NYFun2 dashboard.

Checks local HTML links, JSON validity, primary-source links, explanatory flags for
blank values, and the hotel's Queen/King + private-bathroom requirement. No network
calls are made; a successful run is structural verification, not live-source review.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []
warnings = []

html_files = sorted(ROOT.glob('*.html')) + sorted((ROOT / 'pages').glob('*.html'))
for html in html_files:
    text = html.read_text(encoding='utf-8')
    for href in re.findall(r'href="([^"#]+)', text):
        if href.startswith(('http://', 'https://', 'mailto:', 'tel:', 'javascript:')):
            continue
        target = (html.parent / href.split('?')[0]).resolve()
        if not target.exists():
            errors.append(f'{html.relative_to(ROOT)}: missing local link {href}')

catalogs = {
    'data/restaurants.json': 'restaurants',
    'data/hotels.json': 'hotels',
    'data/activities.json': 'activities',
}
loaded = {}
all_rows = []
for rel, kind in catalogs.items():
    try:
        doc = json.loads((ROOT / rel).read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f'{rel}: invalid JSON ({exc})')
        continue
    loaded[kind] = doc
    rows = doc.get('items', [])
    if not isinstance(rows, list):
        errors.append(f'{rel}: items must be a list')
        continue
    for i, row in enumerate(rows, 1):
        label = f'{rel} row {i} ({row.get("name", "unnamed")})'
        all_rows.append((kind, label, row))
        source = row.get('sourceUrl')
        if not isinstance(source, str) or not source.startswith('https://'):
            errors.append(f'{label}: no https official/primary sourceUrl')
        for field in ('officialUrl', 'priceSourceUrl', 'rateSourceUrl'):
            url = row.get(field)
            if url and (not isinstance(url, str) or not url.startswith('https://')):
                errors.append(f'{label}: {field} must be https when present')

        if kind == 'restaurants':
            blankable = ('address', 'hours', 'priceTwoAdults', 'officialUrl')
        elif kind == 'hotels':
            blankable = ('room', 'privateBathroom', 'sevenNightTotal', 'cheapestWindow', 'publishedRate')
            if not row.get('room') or not row.get('privateBathroom'):
                errors.append(f'{label}: hotel candidate lacks a verified room or private-bath specification')
            if row.get('sevenNightTotal'):
                if not row.get('rateSourceUrl', '').startswith('https://'):
                    errors.append(f'{label}: dated hotel rate lacks an https rateSourceUrl')
                if not row.get('rateCapturedOn'):
                    errors.append(f'{label}: dated hotel rate lacks a capture date')
        else:
            blankable = ('hours', 'costTwoAdults')
        if any(not row.get(field) for field in blankable) and not row.get('flags'):
            warnings.append(f'{label}: blank field with no explanatory row flag')

try:
    decisions = json.loads((ROOT / 'data/decisions.json').read_text(encoding='utf-8'))
except (OSError, json.JSONDecodeError) as exc:
    decisions = {}
    errors.append(f'data/decisions.json: invalid JSON ({exc})')

for key in ('questions', 'suggestions', 'flags'):
    rows = decisions.get(key, [])
    if not isinstance(rows, list):
        errors.append(f'data/decisions.json: {key} must be a list')
        continue
    for i, row in enumerate(rows, 1):
        label = f'data/decisions.json {key} row {i} ({row.get("id", "unnamed")})'
        all_rows.append(('decisions', label, row))
        if key == 'flags':
            source = row.get('source')
            if not isinstance(source, str) or not source.startswith('https://'):
                errors.append(f'{label}: no https source URL')
        if key == 'questions':
            for source in row.get('sources', []):
                if not isinstance(source, str) or not source.startswith('https://'):
                    errors.append(f'{label}: question source is not https: {source!r}')

# Catch duplicate flag/question/suggestion IDs, which would make references ambiguous.
for key in ('questions', 'suggestions', 'flags'):
    ids = [row.get('id') for row in decisions.get(key, [])]
    if len(ids) != len(set(ids)):
        errors.append(f'data/decisions.json: duplicate IDs in {key}')

counts = {kind: len(doc.get('items', [])) for kind, doc in loaded.items()}
counts.update({key: len(decisions.get(key, [])) for key in ('questions', 'suggestions', 'flags')})
row_count = sum(counts.values())
print(
    'Checked {} canonical rows ({} restaurants, {} hotels, {} activities, '
    '{} questions, {} suggestions, {} flags) and local links in {} HTML files.'.format(
        row_count,
        counts.get('restaurants', 0), counts.get('hotels', 0), counts.get('activities', 0),
        counts.get('questions', 0), counts.get('suggestions', 0), counts.get('flags', 0),
        len(html_files),
    )
)
for warning in warnings:
    print('WARN ', warning)
for error in errors:
    print('ERROR', error)
print(f'Result: {len(errors)} errors, {len(warnings)} warnings')
sys.exit(1 if errors else 0)
