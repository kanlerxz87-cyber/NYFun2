#!/usr/bin/env python3
"""Check local dashboard structure only; this does not verify external facts."""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
errors = []

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ('href', 'src'):
            if key in attrs:
                self.urls.append(attrs[key])

pages = sorted(ROOT.glob('*.html')) + sorted((ROOT / 'pages').glob('*.html'))
for html in pages:
    parser = Links()
    parser.feed(html.read_text(encoding='utf-8'))
    for url in parser.urls:
        parts = urlsplit(url)
        if parts.scheme or parts.netloc or not parts.path:
            continue
        target = (html.parent / unquote(parts.path)).resolve()
        if not target.is_relative_to(ROOT) or not target.exists():
            errors.append(f'{html.relative_to(ROOT)}: missing local target {url}')

docs = {}
for name in ('restaurants', 'activities', 'hotels', 'decisions'):
    try:
        docs[name] = json.loads((ROOT / 'data' / f'{name}.json').read_text(encoding='utf-8'))
    except (ValueError, OSError) as e:
        errors.append(f'{name}: {e}')

count = 0
for name in ('restaurants', 'activities', 'hotels'):
    for row in docs.get(name, {}).get('items', []):
        count += 1
        label = f'{name}: {row.get("name", "unnamed")}'
        if not row.get('sourceUrl', '').startswith('https://'):
            errors.append(f'{label}: missing source URL')
        if name == 'restaurants' and row.get('priceTwoAdults') and not row.get('priceSourceUrl'):
            errors.append(f'{label}: menu price missing source URL')
        if name == 'hotels' and row.get('sevenNightTotal') and not row.get('rateSourceUrl'):
            errors.append(f'{label}: hotel total missing rate source URL')
for group in ('questions', 'suggestions', 'flags'):
    for row in docs.get('decisions', {}).get(group, []):
        count += 1
        sources = row.get('sources', []) or [row.get('source', '')]
        if not any(s.startswith('https://') for s in sources):
            errors.append(f'{group}: {row.get("id")} missing contextual source URL')

for error in errors:
    print('ERROR', error)
print(f'Checked {len(pages)} main HTML files and {count} data rows: {len(errors)} errors.')
print('External URLs, source accuracy and current availability are NOT checked.')
sys.exit(bool(errors))
