/* NYC 2027 dashboard — renders every table from the JSON datasets. No dependencies. */
(function () {
  'use strict';
  const BASE = location.pathname.includes('/pages/') ? '../data/' : 'data/';
  const ROOT = location.pathname.includes('/pages/') ? '../' : './';
  const DEFAULT_ORIGIN = 'DoubleTree by Hilton Hotel New York City - Chelsea, 128 West 29th Street, New York, NY 10001';
  const storeKey = 'nyfun2_origin';
  let verifiedDate = 'date not recorded';

  const esc = (v) => String(v == null ? '' : v).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const val = (v) => (v !== undefined && v !== null && String(v).trim() !== '') ? esc(v) : '<span class="blank">blank — unverified</span>';
  const link = (url, label) => (url && /^https?:/.test(url))
    ? `<a href="${esc(url)}" target="_blank" rel="noopener noreferrer">${esc(label || 'Open')} ↗</a>` : '';
  const flagList = (arr) => (arr && arr.length)
    ? `<ul class="flag-list">${arr.map(f => `<li>${esc(typeof f === 'string' ? f : JSON.stringify(f))}</li>`).join('')}</ul>`
    : '<span class="pill green">none</span>';
  const socialLinks = (arr) => (arr && arr.length)
    ? `<div class="socials">${arr.map(s => `<a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer" title="${esc(s.note || '')}">${esc(s.platform)}</a>`).join('')}</div>`
    : '<span class="blank">none found</span>';
  const badge = (row) => {
    if (!row.verifiedToday) return '<span class="pill gray">carried capture</span>';
    const rowDate = String(row.verifyStatus || '').match(/\b\d{4}-\d{2}-\d{2}\b/);
    return `<span class="pill green">checked ${esc(rowDate ? rowDate[0] : verifiedDate)}</span>`;
  };
  const origin = () => { try { return localStorage.getItem(storeKey) || DEFAULT_ORIGIN; } catch (e) { return DEFAULT_ORIGIN; } };
  const route = (dest) => `https://www.google.com/maps/dir/?api=1&origin=${encodeURIComponent(origin())}&destination=${encodeURIComponent(dest)}&travelmode=transit`;
  const routeLink = (dest, label) => `<a href="${esc(route(dest))}" target="_blank" rel="noopener noreferrer">${esc(label || 'Route')} ↗</a>`;

  const starPill = (d) => {
    const s = String(d || '');
    if (/Guide-listed|Selected/i.test(s)) return `<span class="pill gray">${esc(s)}</span>`;
    if (/3/.test(s)) return `<span class="pill green">${esc(s)}</span>`;
    if (/2/.test(s)) return `<span class="pill">${esc(s)}</span>`;
    return `<span class="pill amber">${esc(s)}</span>`;
  };

  const transitCell = (h) => {
    const t = h.transit || {};
    if (!t.measured) return '<span class="blank">not measured — blank</span>';
    return `<strong>${t.clustersWithin60}/${t.clustersMeasured} clusters ≤60 min</strong>` +
      `<span class="sub">avg ${t.avgMinutes} min · longest ${t.maxMinutes} min · ${t.starsCoveredWithin60} starred venues in the sampled clusters</span>` +
      `<span class="sub">${esc(t.capturedOn || '')} snapshot</span>`;
  };

  const config = {
    restaurants: {
      cols: ['Status', 'Restaurant', 'Cuisine / area', 'Price for 2', 'Days open', 'Hours & exceptions', 'Social / video', 'Official links', 'Source', 'Review'],
      row: (r) => [
        starPill(r.distinction),
        `<strong>${esc(r.name)}</strong><span class="sub">${routeLink(r.address || r.name + ', New York')} ${badge(r)}</span>`,
        `${val(r.cuisine)}${r.area ? `<span class="sub">${esc(r.area)}</span>` : ''}`,
        `${val(r.priceTwoAdults)}${r.priceSourceUrl ? `<span class="sub">${link(r.priceSourceUrl, 'menu source')}</span>` : ''}`,
        val(r.daysOpen),
        `${val(r.hours)}${r.exceptions ? `<span class="sub">${esc(r.exceptions)}</span>` : ''}`,
        socialLinks(r.social),
        `${link(r.officialUrl, 'Official site')}${r.officialUrl && r.sourceUrl ? ' · ' : ''}${link(r.sourceUrl, 'MICHELIN page')}`,
        link(r.sourceUrl, 'Verify'),
        flagList(r.flags)
      ],
      group: (r) => /3 MICHELIN/.test(r.distinction) ? '3' : /2 MICHELIN/.test(r.distinction) ? '2' : /1 MICHELIN/.test(r.distinction) ? '1' : 'guide'
    },
    hotels: {
      cols: ['#', 'Hotel', 'Area / address', 'Room & bathroom', 'MICHELIN reach (≤60 min)', '7-night pre-tax', '7-night all-in', 'Rate source', 'Links', 'Review'],
      row: (h) => [
        `<strong>${h.rank}</strong>`,
        `<strong>${esc(h.name)}</strong><span class="sub">${h.qualifies ? '<span class="pill green">bed + bath verified</span>' : '<span class="pill amber">spec unverified</span>'} ${badge(h)}</span>`,
        `${val(h.area)}${h.address ? `<span class="sub">${esc(h.address)}</span>` : ''}<span class="sub">${routeLink(h.address || h.name, 'Route from here')} <button class="origin-btn" type="button" data-origin="${esc(h.address ? h.name + ', ' + h.address : h.name)}">Use as origin</button></span>`,
        `${val(h.room)}${h.privateBathroom ? `<span class="sub">Bath: ${esc(h.privateBathroom)}</span>` : ''}${h.eligibilityNote ? `<span class="sub">${esc(h.eligibilityNote)}</span>` : ''}`,
        transitCell(h),
        `${val(h.sevenNightPreTax)}${h.taxBasis ? `<span class="sub">${esc(h.taxBasis)}</span>` : ''}`,
        `${val(h.sevenNightAllIn)}${h.rateCapturedOn ? `<span class="sub">captured ${esc(h.rateCapturedOn)}</span>` : ''}${h.cancellation ? `<span class="sub">${esc(h.cancellation)}</span>` : ''}`,
        link(h.rateSourceUrl, 'Rate URL'),
        `${link(h.officialUrl, 'Official site')}${h.officialUrl && h.sourceUrl ? ' · ' : ''}${link(h.sourceUrl, 'Source')}`,
        flagList(h.flags)
      ],
      group: (h) => h.qualifies ? 'qualified' : 'unverified'
    },
    activities: {
      cols: ['Activity', 'Category / area', 'Days open', 'Hours & exceptions', 'Cost for 2', 'Travel note', 'Social / video', 'Official links', 'Source', 'Review'],
      row: (a) => [
        `<strong>${esc(a.name)}</strong><span class="sub">${routeLink(a.address || a.name + ', New York', 'Route')} ${badge(a)}</span>`,
        `${val(a.category)}${a.area ? `<span class="sub">${esc(a.area)}</span>` : ''}${a.address ? `<span class="sub">${esc(a.address)}</span>` : ''}`,
        val(a.daysOpen),
        `${val(a.hours)}${a.exceptions ? `<span class="sub">${esc(a.exceptions)}</span>` : ''}`,
        val(a.costTwoAdults),
        val(a.transitNote),
        socialLinks(a.social),
        link(a.officialUrl, 'Official site'),
        link(a.sourceUrl, 'Verify'),
        flagList(a.flags)
      ],
      group: () => 'all'
    },
    windows: {
      cols: ['#', 'Dates', 'Nights', 'Cheapest qualifying hotel', 'Pre-tax total', 'Est. all-in', 'Per night', 'Notes', 'Source'],
      row: (w) => [
        `<strong>${esc(w.windowId)}</strong>`,
        `<strong>${esc(w.dates)}</strong>`,
        val(w.nights),
        val(w.cheapestQualifyingHotel),
        val(w.preTaxTotalUsd),
        val(w.estimatedAllInUsd),
        val(w.perNightPreTaxUsd),
        val(w.notes),
        link(w.sourceUrl, 'Booking search')
      ],
      group: () => 'all'
    },
    questions: {
      cols: ['ID', 'Question', 'What we know', 'What is missing', 'Provisional answer', 'Blocks a decision?', 'How to find out', 'Sources'],
      row: (q) => [
        `<strong>${esc(q.id)}</strong>`,
        `<strong>${esc(q.question)}</strong>`,
        val(q.whatWeKnow),
        val(q.whatWeDoNotKnow),
        val(q.provisionalAnswer),
        q.blocking ? '<span class="pill red">Yes</span>' : '<span class="pill green">No</span>',
        val(q.howToDiscover),
        (q.sources || []).map(s => link(s, 'Source')).join('<br>') || '<span class="blank">none</span>'
      ],
      group: () => 'all'
    },
    suggestions: {
      cols: ['ID', 'Suggestion', 'Detail', 'Effort', 'Blocked by', 'Status'],
      row: (s) => [
        `<strong>${esc(s.id)}</strong>`,
        `<strong>${esc(s.title)}</strong>`,
        val(s.detail),
        val(s.effort),
        val((s.blockedBy || []).join(', ')),
        val(s.status)
      ],
      group: (s) => /^Implemented/.test(s.status || '') ? 'done' : /Partial/.test(s.status || '') ? 'partial' : 'proposed'
    },
    flags: {
      cols: ['ID', 'Severity', 'Issue', 'Detail', 'Source'],
      row: (f) => [
        `<strong>${esc(f.id)}</strong>`,
        `<span class="pill ${f.severity === 'High' ? 'red' : f.severity === 'Medium' ? 'amber' : 'gray'}">${esc(f.severity)}</span>`,
        `<strong>${esc(f.title)}</strong>`,
        val(f.detail),
        link(f.source, 'Source')
      ],
      group: (f) => (f.severity || '').toLowerCase()
    },
    verification: {
      cols: ['Fact checked', 'Value found', 'Official source', 'How it was checked', 'Result'],
      row: (c) => [
        `<strong>${esc(c.fact)}</strong>`,
        val(c.value),
        link(c.source, 'Open source'),
        val(c.note),
        `<span class="pill ${/^Verified/.test(c.result) ? 'green' : /Corroborated/.test(c.result) ? 'amber' : 'gray'}">${esc(c.result)}</span>`
      ],
      group: () => 'all'
    }
  };

  async function load(name) {
    const res = await fetch(BASE + name + '.json', { cache: 'no-store' });
    if (!res.ok) throw new Error('Could not load ' + name + '.json (' + res.status + ')');
    return res.json();
  }

  function renderTable(el, rows, cfg) {
    const head = `<thead><tr>${cfg.cols.map(c => `<th scope="col">${esc(c)}</th>`).join('')}</tr></thead>`;
    const body = rows.map(r => {
      const group = cfg.group ? cfg.group(r) : 'all';
      const verify = r.verifiedToday ? 'today' : 'carried';
      return `<tr data-group="${esc(group)}" data-verify="${esc(verify)}">` +
        cfg.row(r).map((cell, i) => `<td data-label="${esc(cfg.cols[i])}">${cell}</td>`).join('') + '</tr>';
    }).join('');
    el.innerHTML = `<div class="table-wrap"><table>${head}<tbody>${body}</tbody></table></div>`;
  }

  function applyFilters(wrap, input, selects) {
    const rows = [...wrap.querySelectorAll('tbody tr')];
    const q = (input && input.value || '').trim().toLowerCase();
    const active = selects.map(s => [s.dataset.filter, s.value]).filter(([, v]) => v);
    let shown = 0;
    rows.forEach(tr => {
      let ok = !q || tr.textContent.toLowerCase().includes(q);
      active.forEach(([key, v]) => {
        if (key === 'verify') ok = ok && tr.dataset.verify === v;
        else ok = ok && tr.dataset.group === v;
      });
      tr.style.display = ok ? '' : 'none';
      if (ok) shown++;
    });
    const counter = wrap.parentElement.querySelector('.count');
    if (counter) counter.textContent = `${shown} of ${rows.length} rows shown`;
  }

  function wireFilters(el, wrap) {
    const bar = el.parentElement.querySelector('.toolbar');
    if (!bar) return;
    const input = bar.querySelector('input[type=search]');
    const selects = [...bar.querySelectorAll('select[data-filter]')];
    const run = () => applyFilters(wrap, input, selects);
    if (input) input.addEventListener('input', run);
    selects.forEach(s => s.addEventListener('change', run));
    run();
  }

  function setCounts(data) {
    verifiedDate = data.verification?.checkedOn || data.restaurants?.meta?.integrationCheckedOn || 'date not recorded';
    const map = {
      restaurants: (data.restaurants?.items || []).length,
      activities: (data.activities?.items || []).length,
      hotels: (data.hotels?.items || []).length,
      questions: (data.decisions?.questions || []).length,
      suggestions: (data.decisions?.suggestions || []).length,
      flags: (data.decisions?.flags || []).length,
      priced: (data.restaurants?.items || []).filter(r => r.priceTwoAdults).length,
      hotelPriced: (data.hotels?.items || []).filter(h => h.sevenNightPreTax || h.sevenNightAllIn).length
    };
    document.querySelectorAll('[data-count]').forEach(el => {
      const v = map[el.dataset.count];
      if (v != null) el.textContent = v;
    });
    document.querySelectorAll('[data-checked]').forEach(el => {
      el.textContent = data.verification?.checkedOn || data.restaurants?.meta?.integrationCheckedOn || '';
    });
  }

  async function init() {
    const specs = [...document.querySelectorAll('[data-table]')];
    try {
      const needed = new Set(specs.map(s => s.dataset.table.split(':')[0]));
      if (document.querySelector('[data-count]')) ['restaurants', 'activities', 'hotels', 'decisions', 'verification'].forEach(n => needed.add(n));
      const data = {};
      await Promise.all([...needed].map(async n => { data[n] = await load(n); }));
      setCounts(data);

      specs.forEach(el => {
        const [kind, key] = el.dataset.table.split(':');
        let rows, cfg;
        if (kind === 'decisions') { rows = data.decisions?.[key] || []; cfg = config[key]; }
        else if (kind === 'hotels' && key === 'windows') { rows = data.hotels?.windows || []; cfg = config.windows; }
        else if (kind === 'verification') { rows = data.verification?.checks || []; cfg = config.verification; }
        else { rows = data[kind]?.items || []; cfg = config[kind === 'restaurants' ? 'restaurants' : kind]; }
        if (!cfg) { el.innerHTML = '<p class="notice warn">No renderer configured for ' + esc(kind) + '.</p>'; return; }
        renderTable(el, rows, cfg);
        wireFilters(el, el.querySelector('.table-wrap'));
      });

      document.querySelectorAll('.origin-btn').forEach(btn => btn.addEventListener('click', () => {
        try { localStorage.setItem(storeKey, btn.dataset.origin); } catch (e) {}
        document.querySelectorAll('.origin-btn').forEach(b => b.textContent = 'Use as origin');
        btn.textContent = '✓ origin set';
        document.querySelectorAll('[data-origin-now]').forEach(el => el.textContent = btn.dataset.origin);
      }));
      document.querySelectorAll('[data-origin-now]').forEach(el => el.textContent = origin());
    } catch (err) {
      document.querySelectorAll('[data-table]').forEach(el => {
        el.innerHTML = `<p class="notice danger">Data could not be loaded: ${esc(err.message)}. If you opened this file directly, serve the folder over HTTP (python3 -m http.server).</p>`;
      });
      console.error(err);
    }
  }
  document.addEventListener('DOMContentLoaded', init);
})();
