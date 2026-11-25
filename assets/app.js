// Shared navigation, formatting, data-loading, and helper utilities for NYFun2
window.NYFun2 = (function () {
  const NAV_ITEMS = [
    { href: 'index.html', label: 'Overview' },
    { href: 'michelin.html', label: 'Michelin NYC' },
    { href: 'hotels.html', label: 'Hotels & Dates' },
    { href: 'activities.html', label: 'Activities' },
    { href: 'itinerary.html', label: 'Itinerary & Budget' },
    { href: 'questions.html', label: 'Open Questions' },
    { href: 'suggestions.html', label: 'Improvements' },
    { href: 'review.html', label: 'Flagged Audit' }
  ];

  function currentPage() {
    const path = window.location.pathname.split('/').pop();
    return path && path.endsWith('.html') ? path : 'index.html';
  }

  function renderHeader() {
    const active = currentPage();
    const header = document.getElementById('site-header');
    if (!header) return;
    header.className = 'site-header';
    header.innerHTML = `
      <div class="nav-inner">
        <a class="brand" href="index.html">
          <span class="brand-mark">NY</span>
          <span>
            NYFun2
            <span class="brand-sub">NYC Couples Guide · Feb–Mar 2027</span>
          </span>
        </a>
        <button class="nav-toggle" id="nav-toggle" aria-expanded="false" aria-controls="nav-links">
          Menu ▾
        </button>
        <nav class="nav-links" id="nav-links" aria-label="Primary navigation">
          ${NAV_ITEMS.map(
            (item) =>
              `<a href="${item.href}" class="${active === item.href ? 'active' : ''}">${item.label}</a>`
          ).join('')}
        </nav>
      </div>
    `;
    const btn = document.getElementById('nav-toggle');
    const links = document.getElementById('nav-links');
    if (btn && links) {
      btn.addEventListener('click', () => {
        const open = links.classList.toggle('open');
        btn.setAttribute('aria-expanded', String(open));
        btn.textContent = open ? 'Close ✕' : 'Menu ▾';
      });
    }
  }

  function renderFooter() {
    const footer = document.getElementById('site-footer');
    if (!footer) return;
    footer.className = 'site-footer';
    footer.innerHTML = `
      <div class="footer-inner">
        <div>
          <strong>NYFun2</strong> — Verified NYC Travel Intelligence for 2 Adults (Feb 15 – Mar 23, 2027) · Last verified <strong>Nov 25, 2026</strong>.
        </div>
        <div>
          All unverified values are intentionally left blank & tracked on <a href="review.html">Flagged Audit</a> ·
          <a href="https://guide.michelin.com/us/en/new-york-state/new-york/restaurants" target="_blank" rel="noopener">Michelin Guide NYC</a> ·
          <a href="https://www.mta.info/document/195636" target="_blank" rel="noopener">MTA 2026–27 Fares</a>
        </div>
      </div>
    `;
  }

  async function loadJSON(path) {
    const res = await fetch(path);
    if (!res.ok) throw new Error(`Failed to load ${path} (${res.status})`);
    return res.json();
  }

  function fmtUSD(val) {
    if (val === null || val === undefined || Number.isNaN(Number(val))) return '— Unverified';
    return '$' + Math.round(Number(val)).toLocaleString('en-US');
  }

  function fmtUSDExact(val) {
    if (val === null || val === undefined || Number.isNaN(Number(val))) return '— Unverified';
    return '$' + Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  function escapeHTML(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function tierBadge(tier, label) {
    const map = {
      '3-star': 'badge-3star',
      '2-star': 'badge-2star',
      '1-star': 'badge-1star',
      'bib-gourmand': 'badge-bib',
      'selected': 'badge-selected'
    };
    const cls = map[tier] || 'badge-selected';
    const stars = tier === '3-star' ? '★★★ ' : tier === '2-star' ? '★★ ' : tier === '1-star' ? '★ ' : '';
    return `<span class="badge ${cls}">${stars}${escapeHTML(label)}</span>`;
  }

  function socialChips(links) {
    if (!links || !links.length) return '<span class="cell-sub">—</span>';
    return `<div class="link-row">${links
      .map((l) => {
        const p = (l.platform || '').toLowerCase();
        const cls = p.includes('youtube') ? 'yt' : p.includes('tiktok') ? 'tt' : p.includes('instagram') ? 'ig' : '';
        const icon = p.includes('youtube') ? '▶' : p.includes('tiktok') ? '♪' : p.includes('instagram') ? '◎' : '↗';
        return `<a class="link-chip ${cls}" href="${escapeHTML(l.url)}" target="_blank" rel="noopener">${icon} ${escapeHTML(l.platform)}: ${escapeHTML(l.label)}</a>`;
      })
      .join('')}</div>`;
  }

  document.addEventListener('DOMContentLoaded', () => {
    renderHeader();
    renderFooter();
  });

  return {
    loadJSON,
    fmtUSD,
    fmtUSDExact,
    escapeHTML,
    tierBadge,
    socialChips
  };
})();
