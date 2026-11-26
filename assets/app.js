(function () {
  'use strict';
  const BASE = location.pathname.includes('/pages/') ? '../data/' : 'data/';
  const DEFAULT_ORIGIN = 'citizenM New York Times Square, 218 West 50th Street, New York, NY 10019';
  const storeKey = 'nyfun2_origin';

  const esc = (v) => String(v == null ? '' : v).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const link = (url, label) => url ? `<a href="${esc(url)}" target="_blank" rel="noopener noreferrer">${esc(label || 'Open')} ↗</a>` : '<span class="blank">—</span>';
  const val = (v) => v ? esc(v) : '<span class="blank">blank — unverified</span>';
  const flags = (arr) => (arr && arr.length) ? `<ul class="flag-list">${arr.map(f => `<li>${esc(f)}</li>`).join('')}</ul>` : '<span class="pill green">none</span>';
  const socials = (arr) => (arr && arr.length) ? `<div class="socials">${arr.map(s => `<a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer" title="${esc(s.note || '')}">${esc(s.platform)} ↗</a>`).join('')}</div>` : '<span class="blank">—</span>';
  const origin = () => { try { return localStorage.getItem(storeKey) || DEFAULT_ORIGIN; } catch (e) { return DEFAULT_ORIGIN; } };
  const route = (dest) => `https://www.google.com/maps/dir/?api=1&origin=${encodeURIComponent(origin())}&destination=${encodeURIComponent(dest)}&travelmode=transit`;
  const routeLink = (dest) => `<a href="${esc(route(dest))}" target="_blank" rel="noopener noreferrer">Route ↗</a>`;

  const config = {
    restaurants: {
      cols: ['Name','Guide status','Cuisine','Address / area','Days & hours','Exceptions','Total for 2','Guide band','Links','Social / review','Official source','Flags / review'],
      row: (r) => [
        `<strong>${esc(r.name)}</strong><span class="sub">${routeLink(r.address || r.name)}</span>`,
        `<span class="pill ${r.distinction.includes('3') ? 'green' : r.distinction.includes('2') ? '' : r.distinction.includes('1') ? '' : 'gray'}">${esc(r.distinction)}</span>`,
        val(r.cuisine),
        `${val(r.address)}${r.area ? `<span class="sub">${esc(r.area)}</span>` : ''}`,
        val(r.hours),
        val(r.exceptions),
        `${val(r.priceTwoAdults)}${r.priceSourceUrl ? `<span class="sub">${link(r.priceSourceUrl, 'Menu price source')}</span>` : ''}`,
        val(r.guidePriceBand),
        `${link(r.officialUrl, 'Official site')}${r.officialUrl && r.sourceUrl ? '<br>' : ''}${link(r.sourceUrl, 'MICHELIN page')}`,
        socials(r.social),
        `<a class="src" href="${esc(r.sourceUrl)}" target="_blank" rel="noopener noreferrer">Verify source ↗</a>`,
        flags(r.flags)
      ]
    },
    activities: {
      cols: ['Activity','Type','Where','Days & hours','Exceptions','Cost for 2','Links','Social / review','Official source','Flags / review'],
      row: (a) => [
        `<strong>${esc(a.name)}</strong><span class="sub">${routeLink(a.address || a.name)}</span>`,
        val(a.category),
        `${val(a.address)}${a.area ? `<span class="sub">${esc(a.area)}</span>` : ''}`,
        val(a.hours),
        val(a.exceptions),
        val(a.costTwoAdults),
        link(a.officialUrl, 'Official site'),
        socials(a.social),
        `<a class="src" href="${esc(a.sourceUrl)}" target="_blank" rel="noopener noreferrer">Verify source ↗</a>`,
        flags(a.flags)
      ]
    },
    hotels: {
      cols: ['Hotel','Area / address','Room & bath','Guide key / score','Published rate','7-night total','Cheapest window','Links','Source','Flags / review'],
      row: (h) => [
        `<strong>${esc(h.name)}</strong><span class="sub"><button class="origin-btn" data-origin="${esc(h.address || h.name)}" type="button">Use as route origin</button></span>`,
        `${val(h.address)}${h.area ? `<span class="sub">${esc(h.area)}</span>` : ''}`,
        `${val(h.room)}${h.privateBathroom ? `<span class="sub">Bath: ${esc(h.privateBathroom)}</span>` : ''}`,
        `${val(h.keyStatus)}${h.guestScore ? `<span class="sub">${esc(h.guestScore)}</span>` : ''}`,
        val(h.publishedRate),
        (h.sevenNightTotal
          ? `${esc(h.sevenNightTotal)}${h.allInSevenNights ? `<span class="sub"><strong>All-in: ${esc(h.allInSevenNights)}</strong></span>` : ''}${h.taxBasis ? `<span class="sub">${esc(h.taxBasis)}</span>` : ''}${h.rateCapturedOn ? `<span class="sub">Captured ${esc(h.rateCapturedOn)}</span>` : ''}`
          : val(h.sevenNightTotal)),
        val(h.cheapestWindow),
        `${link(h.officialUrl, 'Official site')}${h.rateSourceUrl ? `<br>${link(h.rateSourceUrl, 'Rate source')}` : ''}`,
        `<a class="src" href="${esc(h.sourceUrl)}" target="_blank" rel="noopener noreferrer">Verify source ↗</a>`,
        flags(h.flags)
      ]
    },
    questions: {
      cols: ['ID','Question','What we know','What is missing','Provisional answer','Blocks decision?','How to find out','Sources'],
      row: (q) => [
        `<strong>${esc(q.id)}</strong>`, `<strong>${esc(q.question)}</strong>`, val(q.whatWeKnow), val(q.whatWeDoNotKnow),
        val(q.provisionalAnswer), q.blocking ? '<span class="pill red">Yes</span>' : '<span class="pill amber">No</span>',
        val(q.howToDiscover),
        (q.sources || []).length ? q.sources.map(s => link(s, 'Source')).join('<br>') : '<span class="blank">blank — unverified</span>'
      ]
    },
    suggestions: {
      cols: ['ID','Suggestion','Detail','Effort','Blocked by','Status','Relevant official source'],
      row: (s) => [`<strong>${esc(s.id)}</strong>`, `<strong>${esc(s.title)}</strong>`, val(s.detail), val(s.effort), val((s.blockedBy||[]).join(', ')), val(s.status), link(s.source, 'Source')]
    },
    flags: {
      cols: ['ID','Severity','Issue','Detail','Source'],
      row: (f) => [`<strong>${esc(f.id)}</strong>`, `<span class="pill ${f.severity === 'High' ? 'red' : f.severity === 'Medium' ? 'amber' : 'gray'}">${esc(f.severity)}</span>`, `<strong>${esc(f.title)}</strong>`, val(f.detail), `${link(f.source, 'Source')}${f.secondSource ? `<br>${link(f.secondSource, 'Compare source')}` : ''}`]
    }
  };

  async function load(name) {
    const res = await fetch(BASE + name + '.json', {cache: 'no-store'});
    if (!res.ok) throw new Error('Could not load ' + name + ': ' + res.status);
    return res.json();
  }

  function renderTable(el, rows, cfg) {
    const head = `<thead><tr>${cfg.cols.map(c => `<th scope="col">${esc(c)}</th>`).join('')}</tr></thead>`;
    const body = `<tbody>${rows.map(r => `<tr>${cfg.row(r).map((cell, i) => `<td data-label="${esc(cfg.cols[i])}">${cell}</td>`).join('')}</tr>`).join('')}</tbody>`;
    el.innerHTML = `<div class="table-wrap"><table>${head}${body}</table></div>`;
  }

  function addSearch(input, tableWrap) {
    if (!input || !tableWrap) return;
    input.addEventListener('input', () => {
      const q = input.value.trim().toLowerCase();
      let shown = 0;
      tableWrap.querySelectorAll('tbody tr').forEach(tr => {
        const hit = !q || tr.textContent.toLowerCase().includes(q);
        tr.style.display = hit ? '' : 'none';
        if (hit) shown++;
      });
      const counter = input.parentElement.querySelector('.count');
      if (counter) counter.textContent = `${shown} of ${tableWrap.querySelectorAll('tbody tr').length} rows shown`;
    });
  }

  function setCounts(data) {
    const d = (data.restaurants?.items || []).length;
    const a = (data.activities?.items || []).length;
    const h = (data.hotels?.items || []).length;
    const f = (data.decisions?.flags || []).length;
    const q = (data.decisions?.questions || []).length;
    document.querySelectorAll('[data-count]').forEach(el => {
      const map = {restaurants:d, activities:a, hotels:h, flags:f, questions:q};
      if (map[el.dataset.count] != null) el.textContent = map[el.dataset.count];
    });
    document.querySelectorAll('[data-checked]').forEach(el => el.textContent = data.restaurants?.meta?.checkedOn || '');
  }

  async function init() {
    const specs = [...document.querySelectorAll('[data-table]')];
    try {
      const needed = [...new Set(specs.map(s => s.dataset.table.split(':')[0]))];
      const names = [...new Set([...needed, ...(document.querySelector('[data-count]') ? ['restaurants','activities','hotels','decisions'] : [])])];
      const data = {};
      await Promise.all(names.map(async n => { data[n] = await load(n); }));
      setCounts(data);
      specs.forEach(el => {
        const [kind, key] = el.dataset.table.split(':');
        let rows;
        if (kind === 'decisions') rows = data.decisions[key] || [];
        else rows = (data[kind]?.items) || [];
        renderTable(el, rows, config[kind] || config[key]);
        addSearch(el.parentElement.querySelector('input[type=search]'), el.querySelector('.table-wrap'));
      });
      document.querySelectorAll('.origin-btn').forEach(btn => btn.addEventListener('click', () => {
        try { localStorage.setItem(storeKey, btn.dataset.origin); } catch (e) {}
        document.querySelectorAll('.origin-btn').forEach(b => b.textContent = 'Use as route origin');
        btn.textContent = '✓ Route origin set';
        const note = document.getElementById('origin-note');
        if (note) note.textContent = 'Route origin: ' + btn.dataset.origin;
      }));
      document.querySelectorAll('[data-origin-now]').forEach(el => el.textContent = origin());
    } catch (err) {
      document.querySelectorAll('[data-table]').forEach(el => { el.innerHTML = `<p class="notice danger">Data could not be loaded: ${esc(err.message)}</p>`; });
      console.error(err);
    }
  }
  document.addEventListener('DOMContentLoaded', init);
})();
