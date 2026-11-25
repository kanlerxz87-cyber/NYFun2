/* NYFun2 dashboard renderer. All displayed values come from data/*.json. */
(function () {
  'use strict';
  var ROOT = location.pathname.indexOf('/pages/') !== -1 ? '../' : './';
  var cache = {};

  function esc(v) {
    return String(v == null ? '' : v).replace(/[&<>"']/g, function (c) {
      return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c];
    });
  }
  function val(v) { return v === '' || v == null ? '<span class="blank" title="Not confirmed from official source">—</span>' : esc(v); }
  function load(name) {
    if (!cache[name]) cache[name] = fetch(ROOT + 'data/' + name + '.json').then(function (r) {
      if (!r.ok) throw new Error('Could not load ' + name);
      return r.json();
    });
    return cache[name];
  }
  function srcLinks(ids, sources) {
    if (!ids || !ids.length) return '<span class="blank">—</span>';
    return '<span class="src">' + ids.map(function (id) {
      var s = sources[id];
      if (!s) return '<span class="badge none">' + esc(id) + '</span>';
      return '<a href="' + esc(s.url) + '" target="_blank" rel="noopener noreferrer" title="' + esc(s.publisher + ' — ' + s.title) + '">' + esc(s.publisher) + ' ↗</a>';
    }).join('') + '</span>';
  }
  function socialLinks(list) {
    if (!list || !list.length) return '<span class="blank">—</span>';
    return list.map(function (s) {
      return '<a href="' + esc(s.url) + '" target="_blank" rel="noopener noreferrer" title="' + esc(s.label) + '">' + esc(s.platform) + ' ↗</a>';
    }).join('<br>');
  }
  function badge(status) {
    var cls = status === 'verified' ? 'ok' : (status === 'partial' ? 'partial' : 'none');
    return '<span class="badge ' + cls + '">' + esc(status) + '</span>';
  }
  function table(el, cols, rows) {
    var head = '<thead><tr>' + cols.map(function (c) { return '<th>' + esc(c.label) + '</th>'; }).join('') + '</tr></thead>';
    var body = rows.map(function (r) {
      return '<tr>' + cols.map(function (c) { return '<td>' + c.render(r) + '</td>'; }).join('') + '</tr>';
    }).join('');
    el.innerHTML = '<div class="table-wrap"><table>' + head + '<tbody>' + body + '</tbody></table></div>';
  }
  function filterBar(el, buttons, onPick) {
    el.innerHTML = '<div class="controls">' + buttons.map(function (b, i) {
      return '<button type="button" data-filter="' + esc(b.id) + '"' + (i === 0 ? ' class="active"' : '') + '>' + esc(b.label) + '</button>';
    }).join('') + '</div>';
    el.querySelectorAll('button').forEach(function (btn) {
      btn.addEventListener('click', function () {
        el.querySelectorAll('button').forEach(function (b) { b.classList.remove('active'); });
        btn.classList.add('active');
        onPick(btn.dataset.filter);
      });
    });
  }

  function renderRestaurants(data, sources) {
    var host = document.querySelector('[data-table="restaurants"]');
    if (!host) return;
    var cols = [
      {label: 'Restaurant', render: function (r) { return '<span class="name">' + esc(r.name) + '</span><br><span class="note">' + esc(r.cuisine) + '</span>'; }},
      {label: 'MICHELIN status', render: function (r) { return r.tier === '3 stars' ? '<span class="star">★★★</span> ' + esc(r.distinction) : (r.tier === '2 stars' ? '<span class="star">★★</span> ' + esc(r.distinction) : esc(r.distinction)); }},
      {label: 'Address / cluster', render: function (r) { return val(r.address) + '<br><span class="note">' + esc(r.cluster) + '</span>'; }},
      {label: 'Days', render: function (r) { return val(r.days); }},
      {label: 'Hours', render: function (r) { return val(r.hours); }},
      {label: 'Exceptions', render: function (r) { return val(r.exceptions); }},
      {label: 'Price band (Guide)', render: function (r) { return esc(r.priceBand); }},
      {label: 'Total for 2 adults', render: function (r) { return val(r.costFor2) + '<br><span class="note">' + esc(r.costNote) + '</span>'; }},
      {label: 'Social review link(s)', render: function (r) { return socialLinks(r.socials); }},
      {label: 'Official link', render: function (r) { return r.official ? '<a href="' + esc(r.official) + '" target="_blank" rel="noopener noreferrer">Official site ↗</a>' : '<span class="blank">—</span>'; }},
      {label: 'Source links (official)', render: function (r) { return srcLinks(r.sources, sources); }},
      {label: 'Verification', render: function (r) { return badge(r.verification); }}
    ];
    var bar = document.querySelector('[data-filter="restaurants"]');
    function draw(filter) {
      var rows = data.rows.filter(function (r) { return filter === 'all' || r.tier === filter || (filter === 'listed' && r.tier.indexOf('Guide-listed') === 0); });
      table(host, cols, rows);
      var count = document.querySelector('[data-count="restaurants"]');
      if (count) count.textContent = rows.length;
    }
    if (bar) filterBar(bar, [
      {id: 'all', label: 'All (' + data.rows.length + ')'},
      {id: '3 stars', label: '3 stars'},
      {id: '2 stars', label: '2 stars'},
      {id: '1 star', label: '1 star'},
      {id: 'listed', label: 'Guide-listed, no star'}
    ], draw);
    draw('all');
  }

  function renderActivities(data, sources) {
    var host = document.querySelector('[data-table="activities"]');
    if (!host) return;
    var cols = [
      {label: 'Activity', render: function (r) { return '<span class="name">' + esc(r.name) + '</span><br><span class="note">' + esc(r.area) + '</span>'; }},
      {label: 'Address', render: function (r) { return val(r.address); }},
      {label: 'Days', render: function (r) { return val(r.days); }},
      {label: 'Hours', render: function (r) { return val(r.hours); }},
      {label: 'Exceptions', render: function (r) { return val(r.exceptions); }},
      {label: 'Social review link(s)', render: function (r) { return socialLinks(r.socials); }},
      {label: 'Official link', render: function (r) { return '<a href="' + esc(r.link) + '" target="_blank" rel="noopener noreferrer">Official page ↗</a>' + (r.extraLink ? '<br><a href="' + esc(r.extraLink) + '" target="_blank" rel="noopener noreferrer">More detail ↗</a>' : ''); }},
      {label: 'Source links (official)', render: function (r) { return srcLinks(r.sources, sources); }},
      {label: 'Verification', render: function (r) { return badge(r.verification); }}
    ];
    table(host, cols, data.rows);
  }

  function renderHotels(data, sources) {
    var host = document.querySelector('[data-table="hotels"]');
    if (!host) return;
    var cols = [
      {label: 'Proxy rank', render: function (r) { return '#' + r.rank; }},
      {label: 'Hotel', render: function (r) { return '<span class="name">' + esc(r.name) + '</span><br><span class="note">' + esc(r.area) + '</span>'; }},
      {label: 'Address', render: function (r) { return val(r.address); }},
      {label: 'Bed', render: function (r) { return val(r.bed); }},
      {label: 'Bathroom', render: function (r) { return val(r.bathroom); }},
      {label: 'Amenities', render: function (r) { return val(r.amenities); }},
      {label: 'Guide entries in same address cluster (proxy)', render: function (r) { return r.proxyCount + ' — ' + esc(r.cluster); }},
      {label: 'Undated lead rate', render: function (r) { return val(r.leadRate); }},
      {label: '7-night total (15–22 Feb 2027)', render: function (r) { return val(r.total7); }},
      {label: 'Official / source link', render: function (r) { return '<a href="' + esc(r.link) + '" target="_blank" rel="noopener noreferrer">Hotel page ↗</a><br>' + srcLinks(r.sources, sources); }},
      {label: 'Verification', render: function (r) { return badge(r.verification); }}
    ];
    table(host, cols, data.rows);
    var ch = document.querySelector('[data-table="clusters"]');
    if (ch) table(ch, [
      {label: 'Address cluster', render: function (r) { return esc(r.cluster); }},
      {label: 'Entries in this site\'s table', render: function (r) { return String(r.count); }},
      {label: 'Restaurants counted', render: function (r) { return esc(r.rows); }}
    ], data.clusterCounts);
  }

  var FLAG_HELP = {
    'hours-partial': 'Only part of the weekly hours were captured from the official page.',
    'hours-possibly-incomplete': 'The displayed hours may omit a service period.',
    'hours-day-label-unclear': 'A closing day is displayed but its day label was not captured.',
    'hours-not-captured': 'No hours were captured from the official page.',
    'social-not-found': 'No direct social review link verified.',
    'official-website-not-captured': 'The venue\'s own website URL was not retrieved; the official Guide page is linked.',
    'cost-unverified': 'Price for two adults not confirmed from an official page.',
    'address-not-captured': 'Street address not confirmed from an official page.',
    'bath-not-verified': 'Bathroom details not confirmed from an official page.',
    'bath-privacy-wording-not-explicit': 'In-room bath/shower is described, but "private bathroom" is not explicitly stated.',
    'room-not-verified': 'Room type and bed not confirmed from an official page.',
    'price-unverified': 'No dated price confirmed for the trip dates.',
    'price-undated': 'Rate is official but not tied to the trip dates.',
    'total-unverified': 'Seven-night total not confirmed.',
    'transit-1h-unverified': 'Door-to-door travel time under one hour not verified.',
    'rank-is-cluster-proxy': 'Rank uses address clusters only, not measured travel time.',
    'brooklyn-cluster-not-counted': 'Brooklyn entries outside the Manhattan clusters are not in the proxy count.',
    'street-address-not-captured': 'Street address not captured from the official page.',
    'winter-2027-hours-to-reconfirm': 'February 2027 hours not published; re-check closer to travel.',
    'select-tuesday-dates-for-2027-not-published': 'Select Tuesday openings not published for 2027.',
    'walkway-status-to-reconfirm': 'Temporary walkway status may change.',
    'hall-closures-to-reconfirm': 'Temporary hall closures may change.',
    'show-schedule-not-published': 'February 2027 show schedule not published.',
    'hours-blank-unverified': 'No hours published by the official source.',
    'source-dated-2012': 'The linked NYC DOT document is dated 2012; confirm before travel.',
    'hours-to-reconfirm': 'Hours should be re-confirmed closer to travel.'
  };

  function renderFlagged(all, sources) {
    var host = document.querySelector('[data-table="flagged"]');
    if (!host) return;
    var rows = [];
    all.restaurants.rows.forEach(function (r) { r.flags.forEach(function (f) { rows.push({kind: 'Restaurant', name: r.name, flag: f, source: r.sources[0], url: sources[r.sources[0]] ? sources[r.sources[0]].url : ''}); }); });
    all.activities.rows.forEach(function (r) { r.flags.forEach(function (f) { rows.push({kind: 'Activity', name: r.name, flag: f, source: r.sources[0], url: sources[r.sources[0]] ? sources[r.sources[0]].url : ''}); }); });
    all.hotels.rows.forEach(function (r) { r.flags.forEach(function (f) { rows.push({kind: 'Hotel', name: r.name, flag: f, source: r.sources[0], url: sources[r.sources[0]] ? sources[r.sources[0]].url : ''}); }); });
    rows.sort(function (a, b) { return a.kind.localeCompare(b.kind) || a.name.localeCompare(b.name) || a.flag.localeCompare(b.flag); });
    table(host, [
      {label: 'Type', render: function (r) { return esc(r.kind); }},
      {label: 'Entry', render: function (r) { return esc(r.name); }},
      {label: 'Flag', render: function (r) { return '<code>' + esc(r.flag) + '</code>'; }},
      {label: 'What it means', render: function (r) { return esc(FLAG_HELP[r.flag] || 'Needs manual review.'); }},
      {label: 'Primary source', render: function (r) { return r.url ? '<a href="' + esc(r.url) + '" target="_blank" rel="noopener noreferrer">' + esc(r.source) + ' ↗</a>' : '<span class="blank">—</span>'; }}
    ], rows);
    var c = document.querySelector('[data-count="flagged"]');
    if (c) c.textContent = rows.length;
  }

  function renderSources(sources) {
    var host = document.querySelector('[data-table="sources"]');
    if (!host) return;
    var rows = Object.keys(sources).map(function (id) {
      var s = sources[id];
      return {id: id, publisher: s.publisher, title: s.title, url: s.url};
    });
    table(host, [
      {label: 'Source ID', render: function (r) { return '<code>' + esc(r.id) + '</code>'; }},
      {label: 'Publisher', render: function (r) { return esc(r.publisher); }},
      {label: 'Title / what it verifies', render: function (r) { return esc(r.title); }},
      {label: 'Link', render: function (r) { return '<a href="' + esc(r.url) + '" target="_blank" rel="noopener noreferrer">Open source ↗</a>'; }}
    ], rows);
    var c = document.querySelector('[data-count="sources"]');
    if (c) c.textContent = rows.length;
  }

  function navActive() {
    var here = location.pathname.split('/').pop();
    document.querySelectorAll('.nav a').forEach(function (a) {
      var target = a.getAttribute('href').split('/').pop();
      if (target === here || (here === '' && a.getAttribute('href') === './')) a.classList.add('active');
    });
  }

  Promise.all([load('sources'), load('restaurants'), load('activities'), load('hotels')]).then(function (res) {
    var sources = res[0].sources;
    renderRestaurants(res[1], sources);
    renderActivities(res[2], sources);
    renderHotels(res[3], sources);
    renderFlagged({restaurants: res[1], activities: res[2], hotels: res[3]}, sources);
    renderSources(sources);
    var counts = {
      restaurants: res[1].rows.length, activities: res[2].rows.length,
      hotels: res[3].rows.length, sources: Object.keys(sources).length,
      stars3: res[1].rows.filter(function (r) { return r.tier === '3 stars'; }).length,
      socials: res[1].rows.reduce(function (n, r) { return n + r.socials.length; }, 0) + res[2].rows.reduce(function (n, r) { return n + r.socials.length; }, 0)
    };
    document.querySelectorAll('[data-kpi]').forEach(function (el) {
      if (counts[el.dataset.kpi] != null) el.textContent = counts[el.dataset.kpi];
    });
    navActive();
  }).catch(function (err) {
    document.querySelectorAll('[data-table]').forEach(function (el) {
      el.innerHTML = '<div class="banner">Data could not be loaded: ' + esc(err.message) + '</div>';
    });
  });
})();
