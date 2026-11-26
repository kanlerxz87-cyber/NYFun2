(function () {
  'use strict';
  const BASE = location.pathname.includes('/pages/') ? '../data/' : 'data/';
  const DEFAULT_ORIGIN = 'DoubleTree by Hilton Hotel New York City - Chelsea, 128 W 29th St, New York, NY 10001';
  const storeKey = 'nyfun2_origin';

  const esc = (v) => String(v == null ? '' : v).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const link = (url, label) => url ? `<a href="${esc(url)}" target="_blank" rel="noopener noreferrer">${esc(label || 'Open')} ↗</a>` : '<span class="blank">—</span>';
  const val = (v) => (v != null && String(v).trim() !== '') ? esc(v) : '<span class="blank">blank — unverified</span>';
  const flags = (arr) => (arr && arr.length) ? `<ul class="flag-list">${arr.map(f => `<li>${esc(f)}</li>`).join('')}</ul>` : '<span class="pill green">none</span>';
  
  const socials = (arr) => {
    if (!arr || !arr.length) return '<span class="blank">—</span>';
    return `<div class="socials">${arr.map(s => {
      let icon = '';
      if (s.platform === 'YouTube') icon = '▶ ';
      else if (s.platform === 'TikTok') icon = '♪ ';
      else if (s.platform === 'Instagram') icon = '📷 ';
      return `<a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer" title="${esc(s.note || s.label || '')}">${icon}${esc(s.platform)} ↗</a>`;
    }).join('')}</div>`;
  };

  const origin = () => {
    try { return localStorage.getItem(storeKey) || DEFAULT_ORIGIN; }
    catch (e) { return DEFAULT_ORIGIN; }
  };

  const route = (dest) => `https://www.google.com/maps/dir/?api=1&origin=${encodeURIComponent(origin())}&destination=${encodeURIComponent(dest)}`;
  const routeLink = (dest) => `<a class="route-link" href="${esc(route(dest))}" target="_blank" rel="noopener noreferrer" title="Get directions from active origin">Route ↗</a>`;

  const config = {
    restaurants: {
      cols: ['Name & Route', 'Distinction', 'Cluster', 'Cuisine', 'Address', 'Hours & Days', 'Booking & Exceptions', 'Couple Total (2 Adults)', 'Guide Band', 'Official Links', 'Social & Reviews', 'Flags / Review'],
      row: (r) => {
        let starClass = 'gray';
        if (r.distinction && r.distinction.includes('3')) starClass = 'star3';
        else if (r.distinction && r.distinction.includes('2')) starClass = 'star2';
        else if (r.distinction && r.distinction.includes('1')) starClass = 'star1';
        else if (r.distinction && r.distinction.includes('Bib')) starClass = 'green';

        const priceDisplay = r.priceTwoAdults
          ? `<strong>${esc(r.priceTwoAdults)}</strong>${r.priceNote ? `<span class="sub">${esc(r.priceNote)}</span>` : ''}`
          : val(r.priceTwoAdults);

        return [
          `<strong>${esc(r.name)}</strong><span class="sub">${routeLink(r.address || r.name)}</span>`,
          `<span class="pill ${starClass}">${esc(r.distinction || 'Listed')}</span>`,
          r.clusterLabel ? `<span class="pill gray">${esc(r.clusterLabel)}</span>` : '<span class="blank">—</span>',
          val(r.cuisine),
          val(r.address),
          val(r.hours),
          val(r.exceptions),
          priceDisplay,
          r.guidePriceBand ? `<span class="pill gray">${esc(r.guidePriceBand)}</span>` : '<span class="blank">—</span>',
          `${link(r.officialUrl, 'Official site')}${r.officialUrl && r.sourceUrl ? '<br>' : ''}${link(r.sourceUrl, 'MICHELIN page')}${r.priceSourceUrl ? `<br>${link(r.priceSourceUrl, 'Menu source')}` : ''}`,
          socials(r.social),
          flags(r.flags)
        ];
      }
    },
    activities: {
      cols: ['Activity & Route', 'Category', 'Address / Area', 'Operating Hours', 'Exceptions & Schedule', 'Cost (2 Adults)', 'Transit (≤1 Hr)', 'Official Links', 'Social & Media', 'Flags / Review'],
      row: (a) => [
        `<strong>${esc(a.name)}</strong><span class="sub">${routeLink(a.address || a.name)}</span>`,
        `<span class="pill gray">${esc(a.category || 'Attraction')}</span>`,
        `${val(a.address)}${a.area ? `<span class="sub">${esc(a.area)}</span>` : ''}`,
        val(a.hours),
        val(a.exceptions),
        a.costTwoAdults ? `<strong>${esc(a.costTwoAdults)}</strong>` : val(a.costTwoAdults),
        a.transitNote ? `<span class="sub">${esc(a.transitNote)}</span>` : '<span class="blank">—</span>',
        `${link(a.officialUrl, 'Official site')}${a.officialUrl && a.sourceUrl ? '<br>' : ''}${link(a.sourceUrl, 'Source')}`,
        socials(a.social),
        flags(a.flags)
      ]
    },
    hotels: {
      cols: ['Rank & Hotel', 'Area / Address', 'Room & Bed Spec', 'Bathroom', '7-Night Stay (Feb 15–22)', 'Michelin Reach (≤1 Hr)', 'Cheapest Window', 'Official Links', 'Social Media', 'Flags / Review'],
      row: (h) => {
        const rankBadge = h.rank ? `<span class="badge-rank">#${h.rank}</span> ` : '';
        const tierBadge = h.tierBadge ? `<span class="pill amber" style="margin-left:4px">${esc(h.tierBadge)}</span>` : '';
        const priceBlock = (h.sevenNightTotal || h.sevenNightPreTax)
          ? `<strong>Pre-Tax: ${esc(h.sevenNightTotal || h.sevenNightPreTax)}</strong>${(h.allInSevenNights || h.sevenNightAllIn) ? `<span class="sub"><strong style="color:var(--brand)">All-In: ${esc(h.allInSevenNights || h.sevenNightAllIn)}</strong></span>` : ''}${h.taxBasis ? `<span class="sub">${esc(h.taxBasis)}</span>` : ''}`
          : val(h.sevenNightTotal || h.sevenNightPreTax);

        return [
          `${rankBadge}<strong>${esc(h.name)}</strong>${tierBadge}<span class="sub"><button class="origin-btn" data-origin="${esc(h.address || h.name)}" type="button">Set as route origin</button></span>`,
          `${val(h.address)}${h.area ? `<span class="sub">${esc(h.area)}</span>` : ''}`,
          `${val(h.room || h.bedVerified)}${h.keyStatus ? `<span class="sub">${esc(h.keyStatus)}</span>` : ''}`,
          val(h.privateBathroom),
          priceBlock,
          h.michelinWithin60Min ? `<span class="pill green" style="font-size:10px">${esc(h.michelinWithin60Min)}</span>` : '<span class="blank">—</span>',
          val(h.cheapestWindow),
          `${link(h.officialUrl, 'Property site')}${h.rateSourceUrl ? `<br>${link(h.rateSourceUrl, 'Rate snapshot')}` : ''}${h.sourceUrl ? `<br>${link(h.sourceUrl, 'MICHELIN Guide')}` : ''}`,
          socials(h.social),
          flags(h.flags)
        ];
      }
    },
    windows: {
      cols: ['Window ID', 'Dates (7 Nights)', 'Cheapest Qualifying Hotel', 'Pre-Tax Total', 'All-In Total', 'Nightly Pre-Tax', 'Notes & Key Dates', 'Rate Source'],
      row: (w) => [
        `<strong>${esc(w.windowId)}</strong>`,
        `<strong>${esc(w.dates)}</strong>`,
        val(w.cheapestQualifyingHotel),
        `<strong>${esc(w.preTaxTotalUsd)}</strong>`,
        `<strong>${esc(w.estimatedAllInUsd)}</strong>`,
        val(w.perNightPreTaxUsd),
        val(w.notes),
        link(w.sourceUrl, 'Search snapshot')
      ]
    },
    questions: {
      cols: ['ID', 'Category', 'Question', 'What We Know (Verified)', 'What Is Missing', 'Provisional Recommendation', 'Blocks Decision?', 'Discovery Playbook', 'Sources'],
      row: (q) => [
        `<strong>${esc(q.id)}</strong>`,
        `<span class="pill gray">${esc(q.category || 'Planning')}</span>`,
        `<strong>${esc(q.question)}</strong>`,
        val(q.whatWeKnow),
        val(q.whatWeDoNotKnow),
        val(q.provisionalAnswer),
        q.blocking ? '<span class="pill red">Yes — Blocking</span>' : '<span class="pill amber">No</span>',
        val(q.howToDiscover),
        (q.sources || [q.source]).filter(Boolean).map(s => `<a class="src" href="${esc(s)}" target="_blank" rel="noopener noreferrer">Source ↗</a>`).join('<br>')
      ]
    },
    suggestions: {
      cols: ['ID', 'Category', 'Suggestion Title', 'Action Detail & Implementation', 'Impact', 'Effort', 'Status', 'Source'],
      row: (s) => [
        `<strong>${esc(s.id)}</strong>`,
        `<span class="pill gray">${esc(s.category || 'Improvement')}</span>`,
        `<strong>${esc(s.title)}</strong>`,
        `${val(s.detail)}${s.actionPath ? `<span class="sub"><strong>Action:</strong> ${esc(s.actionPath)}</span>` : ''}`,
        `<span class="pill ${s.impact === 'High' ? 'red' : 'amber'}">${esc(s.impact || 'Medium')}</span>`,
        `<span class="pill gray">${esc(s.effort || 'Low')}</span>`,
        `<span class="pill ${s.status && s.status.includes('Implemented') ? 'green' : 'amber'}">${esc(s.status || 'Proposed')}</span>`,
        link(s.source, 'Source')
      ]
    },
    flags: {
      cols: ['ID', 'Severity', 'Issue / Title', 'Audit Detail & Context', 'Primary Source URL'],
      row: (f) => [
        `<strong>${esc(f.id)}</strong>`,
        `<span class="pill ${f.severity === 'High' ? 'red' : f.severity === 'Medium' ? 'amber' : 'gray'}">${esc(f.severity)}</span>`,
        `<strong>${esc(f.title)}</strong>`,
        val(f.detail),
        `<a class="src" href="${esc(f.source)}" target="_blank" rel="noopener noreferrer">Verify source ↗</a>`
      ]
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

  function addSearchAndFilter(input, filterBar, tableWrap) {
    if (!tableWrap) return;
    const update = () => {
      const q = input ? input.value.trim().toLowerCase() : '';
      const activeBtn = filterBar ? filterBar.querySelector('.filter-btn.active') : null;
      const filterKey = activeBtn ? activeBtn.dataset.filterKey : '';
      const filterVal = activeBtn ? activeBtn.dataset.filterVal : '';

      let shown = 0;
      tableWrap.querySelectorAll('tbody tr').forEach(tr => {
        const text = tr.textContent.toLowerCase();
        const matchesQuery = !q || text.includes(q);
        let matchesFilter = true;
        if (filterKey && filterVal && filterVal !== 'all') {
          matchesFilter = text.includes(filterVal.toLowerCase());
        }
        const visible = matchesQuery && matchesFilter;
        tr.style.display = visible ? '' : 'none';
        if (visible) shown++;
      });

      const counter = (input && input.parentElement) ? input.parentElement.querySelector('.count') : null;
      if (counter) counter.textContent = `${shown} of ${tableWrap.querySelectorAll('tbody tr').length} rows shown`;
    };

    if (input) input.addEventListener('input', update);
    if (filterBar) {
      filterBar.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          filterBar.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          update();
        });
      });
    }
  }

  function setCounts(data) {
    const d = (data.restaurants?.items || []).length;
    const a = (data.activities?.items || []).length;
    const h = (data.hotels?.items || []).length;
    const f = (data.decisions?.flags || []).length;
    const q = (data.decisions?.questions || []).length;
    const s = (data.decisions?.suggestions || []).length;

    document.querySelectorAll('[data-count]').forEach(el => {
      const map = {restaurants:d, activities:a, hotels:h, flags:f, questions:q, suggestions:s};
      if (map[el.dataset.count] != null) el.textContent = map[el.dataset.count];
    });
    document.querySelectorAll('[data-checked]').forEach(el => el.textContent = data.restaurants?.meta?.checkedOn || '2026-11-26');
  }

  function refreshOriginLabels() {
    const active = origin();
    document.querySelectorAll('[data-origin-now]').forEach(el => el.textContent = active);
    const originNote = document.getElementById('origin-note');
    if (originNote) originNote.textContent = 'Active route origin: ' + active;
    
    // Refresh all route links
    document.querySelectorAll('.route-link').forEach(a => {
      const href = a.getAttribute('href');
      if (href && href.includes('destination=')) {
        const dest = new URL(href).searchParams.get('destination');
        if (dest) a.setAttribute('href', route(dest));
      }
    });
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
        const specStr = el.dataset.table;
        const [kind, key] = specStr.split(':');
        let rows = [];
        let cfg = config[kind];

        if (kind === 'decisions') {
          rows = data.decisions[key] || [];
          cfg = config[key] || config.questions;
        } else if (kind === 'hotels' && key === 'windows') {
          rows = data.hotels.bookingWindows || [];
          cfg = config.windows;
        } else {
          rows = (data[kind]?.items) || [];
          cfg = config[kind];
        }

        renderTable(el, rows, cfg);
        const parent = el.closest('section') || el.parentElement;
        const input = parent.querySelector('input[type=search]');
        const filterBar = parent.querySelector('.filter-bar');
        addSearchAndFilter(input, filterBar, el.querySelector('.table-wrap'));
      });

      document.addEventListener('click', (e) => {
        const btn = e.target.closest('.origin-btn');
        if (!btn) return;
        const newOrigin = btn.dataset.origin;
        if (!newOrigin) return;
        try { localStorage.setItem(storeKey, newOrigin); } catch (err) {}
        document.querySelectorAll('.origin-btn').forEach(b => b.textContent = 'Set as route origin');
        btn.textContent = '✓ Route origin set';
        refreshOriginLabels();
      });

      refreshOriginLabels();
    } catch (err) {
      document.querySelectorAll('[data-table]').forEach(el => {
        el.innerHTML = `<p class="notice danger">Data could not be loaded: ${esc(err.message)}</p>`;
      });
      console.error(err);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
