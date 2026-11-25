/* ==========================================================================
   NYC Trip Planning — shared UI (nav, tables, helpers)
   Vanilla JS. No dependencies. Renders every data table from assets/data.js
   ========================================================================== */
(function () {
  'use strict';

  var VERIFIED = '2026-11-25';

  var PAGES = [
    { href: 'index.html',              label: 'Overview' },
    { href: 'executive-summary.html',  label: 'Executive summary' },
    { href: 'hotels.html',             label: 'Hotels' },
    { href: 'michelin.html',           label: 'Michelin' },
    { href: 'activities.html',         label: 'Activities' },
    { href: 'itinerary.html',          label: 'Itinerary & budget' },
    { href: 'suggestions.html',        label: 'Suggestions' },
    { href: 'questions.html',          label: 'Open questions' },
    { href: 'flagged.html',            label: 'Flagged for review' },
    { href: 'sources.html',            label: 'Sources' },
    { href: 'repo-audit.html',         label: 'Repo audit' }
  ];

  /* ---------------- helpers ---------------- */
  function esc(s) {
    if (s === null || s === undefined) return '';
    return String(s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function money(n) {
    if (n === null || n === undefined || n === '') return '';
    var num = Number(n);
    if (isNaN(num)) return String(n);
    return '$' + num.toLocaleString('en-US', { maximumFractionDigits: 0 });
  }

  /* A cell is either a plain string, {v:..., flag:'F-01'}, or {link:url,text} */
  function cell(v) {
    if (v === null || v === undefined || v === '' || v === '—') {
      return '<span class="badge b-unverified">unverified</span>';
    }
    if (typeof v === 'object' && v !== null && v.link) {
      return '<a href="' + esc(v.link) + '" target="_blank" rel="noopener">' + esc(v.text || v.link) + '</a>';
    }
    if (typeof v === 'object' && v !== null && v.v !== undefined) {
      var html = esc(v.v);
      if (v.flag) {
        var badge = '<a class="small" href="flagged.html#' + esc(v.flag) + '" title="See flagged item ' +
          esc(v.flag) + '"><span class="badge b-unverified">' + esc(v.flag) + '</span></a>';
        html = html
          ? html + ' ' + badge
          : '<span class="muted">unverified</span> ' + badge;
      }
      return html;
    }
    return esc(v);
  }

  function stars(n) {
    var s = '';
    for (var i = 0; i < n; i++) s += '★';
    return '<span class="star" aria-label="' + n + ' MICHELIN stars">' + s + '</span>';
  }

  function distinction(d) {
    if (d === 3) return stars(3) + ' <span class="badge b-verified">3 stars</span>';
    if (d === 2) return stars(2) + ' <span class="badge b-verified">2 stars</span>';
    if (d === 1) return stars(1) + ' <span class="badge b-verified">1 star</span>';
    if (d === 0) return '<span class="badge b-info">Guide-listed only — no star</span>';
    return '';
  }

  /* ---------------- header ---------------- */
  function buildHeader() {
    var host = document.getElementById('site-header');
    if (!host) return;
    var here = (location.pathname.split('/').pop() || 'index.html');

    var items = PAGES.map(function (p) {
      var cur = (p.href === here) ? ' aria-current="page"' : '';
      return '<li><a href="' + p.href + '"' + cur + '>' + p.label + '</a></li>';
    }).join('');

    host.className = 'site-header';
    host.innerHTML =
      '<div class="bar">' +
        '<div class="brand">' +
          '<b>NYC &middot; Feb 2027</b>' +
          '<span>Couples trip &middot; verified research</span>' +
        '</div>' +
        '<button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="primaryNav">Menu</button>' +
      '</div>' +
      '<nav class="nav" id="primaryNav" aria-label="Primary">' +
        '<ul>' + items + '</ul>' +
      '</nav>';

    var btn = document.getElementById('menuBtn');
    var nav = document.getElementById('primaryNav');
    if (btn && nav) {
      btn.addEventListener('click', function () {
        var open = nav.classList.toggle('open');
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    }
  }

  function buildFooter() {
    var host = document.getElementById('site-footer');
    if (!host) return;
    host.className = 'site-footer';
    host.innerHTML =
      '<div class="wrap">' +
        '<div><b>Research date:</b> ' + VERIFIED +
          ' &middot; <b>Travel window:</b> 15 Feb &ndash; 22 Feb 2027 (7 nights), 2 adults</div>' +
        '<div>Every figure on this site is either linked to the official source that states it, or labelled ' +
          '<span class="badge b-unverified">unverified</span> and logged on ' +
          '<a href="flagged.html">Flagged for review</a>. Nothing is estimated silently.</div>' +
        '<div class="small">Static site &middot; no tracking &middot; no cookies &middot; ' +
          '<a href="sources.html">full source register</a></div>' +
      '</div>';
  }

  /* ---------------- table renderer ---------------- */
  /* Usage in HTML:
     <div class="table-scroll" data-table="hotels"></div>
     Optional: data-cols="name,district,price" to subset columns  */
  function renderTables() {
    var holders = document.querySelectorAll('[data-table]');
    Array.prototype.forEach.call(holders, function (holder) {
      var key = holder.getAttribute('data-table');
      var def = window.TABLES && window.TABLES[key];
      if (!def) {
        holder.innerHTML = '<p class="table-note">Table "' + esc(key) + '" not found.</p>';
        return;
      }
      var cols = def.columns;
      var only = holder.getAttribute('data-cols');
      if (only) {
        var wanted = only.split(',');
        cols = cols.filter(function (c) { return wanted.indexOf(c.key) > -1; });
      }

      var thead = '<tr>' + cols.map(function (c) {
        return '<th scope="col" class="' + (c.num ? 'num' : '') + '">' + esc(c.label) + '</th>';
      }).join('') + '</tr>';

      var rows = (def.rows || []).map(function (r) {
        var tds = cols.map(function (c) {
          var raw = r[c.key];
          var empty = (raw === '' || raw === null || raw === undefined);
          var out;

          if (c.render === 'distinction') {
            out = (r.stars === undefined || r.stars === null) ? '—' : distinction(r.stars);

          } else if (c.render === 'money') {
            out = empty
              ? '<span class="badge b-unverified">unverified</span>'
              : '<span class="mono">' + money(raw) + '</span>';

          } else if (c.render === 'dash') {
            out = empty ? '<span class="muted">—</span>' : cell(raw);

          } else if (c.render === 'status') {
            out = raw === 'verified'
              ? '<span class="badge b-verified">verified</span>'
              : '<span class="badge b-unverified">unverified</span>';

          } else if (c.render === 'social') {
            var bits = [];
            if (r.instagram) bits.push('<a href="' + esc(r.instagram) + '" target="_blank" rel="noopener">Instagram</a>');
            if (r.facebook)  bits.push('<a href="' + esc(r.facebook) + '" target="_blank" rel="noopener">Facebook</a>');
            if (r.youtube)   bits.push('<a href="' + esc(r.youtube) + '" target="_blank" rel="noopener">YouTube</a>');
            if (r.tiktok)    bits.push('<a href="' + esc(r.tiktok) + '" target="_blank" rel="noopener">TikTok</a>');
            out = bits.length
              ? bits.join(' · ')
              : '<span class="muted small">none verified</span>' +
                ' <a class="small" href="flagged.html#F-05" title="See F-05"><span class="badge b-unverified">F-05</span></a>';

          } else if (c.render === 'links') {
            /* two-link cell: the given link plus an optional official site */
            var parts = [];
            if (r[c.key] && r[c.key].link) parts.push('<a href="' + esc(r[c.key].link) + '" target="_blank" rel="noopener">' + esc(r[c.key].text || 'Open') + '</a>');
            if (r.official_link) parts.push('<a href="' + esc(r.official_link) + '" target="_blank" rel="noopener">Official site</a>');
            out = parts.length ? parts.join(' · ') : '<span class="muted">—</span>';

          } else {
            out = cell(raw);
          }

          return '<td class="' + (c.num ? 'num' : '') + '">' + out + '</td>';
        }).join('');
        return '<tr id="' + esc(r.id || '') + '">' + tds + '</tr>';
      }).join('');

      holder.innerHTML = '<table><thead>' + thead + '</thead><tbody>' + rows + '</tbody></table>';
    });
  }

  /* ---------------- boot ---------------- */
  function boot() {
    buildHeader();
    buildFooter();
    renderTables();
    var stamp = document.getElementById('verified-date');
    if (stamp) stamp.textContent = VERIFIED;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
