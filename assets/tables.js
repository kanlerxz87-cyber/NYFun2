/* ==========================================================================
   NYC Trip Planning — table/column definitions consumed by assets/app.js
   Column keys map onto the objects in assets/data.js.
   ========================================================================== */

window.TABLES = {

  /* ---------------- MICHELIN coverage counters ---------------- */
  michelin_coverage: {
    columns: [
      { key: 'tier', label: 'Distinction' },
      { key: 'count', label: 'Count (official)', num: true },
      { key: 'meaning', label: 'What it means' },
      { key: 'enumerated', label: 'Catalogued on this site' },
      { key: 'url', label: 'Official list', render: 'link' }
    ],
    rows: window.MICHELIN_COVERAGE.map(function (r) {
      return Object.assign({}, r, { url: { link: r.url, text: 'MICHELIN list' } });
    })
  },

  /* ---------------- Hotels ---------------- */
  hotels: {
    columns: [
      { key: 'name', label: 'Hotel' },
      { key: 'district', label: 'Area' },
      { key: 'address', label: 'Address' },
      { key: 'bed', label: 'Bed' },
      { key: 'bath', label: 'Bathroom' },
      { key: 'nightly', label: '$ / night', num: true, render: 'money' },
      { key: 'total7', label: '7 nights, pre-tax', num: true, render: 'money' },
      { key: 'tax_line', label: 'Taxes & fees added' },
      { key: 'est_allin', label: '7 nights, est. all-in', num: true, render: 'money' },
      { key: 'terms', label: 'Rate terms' },
      { key: 'links', label: 'Sources', render: 'links' }
    ],
    rows: window.HOTELS.map(function (h) {
      return Object.assign({}, h, {
        links: { link: h.src_price, text: 'Rate snapshot' },
        official_link: h.src_official
      });
    })
  },

  /* ---------------- Michelin proximity ---------------- */
  hotel_clusters: {
    columns: [
      { key: 'name', label: 'Hotel' },
      { key: 'zip', label: 'ZIP' },
      { key: 'same_zip_starred', label: 'Starred venues in same ZIP', num: true },
      { key: 'venues', label: 'Which ones' },
      { key: 'transit_note', label: 'Transit note' },
      { key: 'dirs', label: 'Check transit time', render: 'link' }
    ],
    rows: window.HOTEL_CLUSTERS.map(function (r) {
      return Object.assign({}, r, {
        zip: r.zip || { v: '', flag: 'F-04' },
        same_zip_starred: (r.same_zip_starred === '' ? '' : r.same_zip_starred),
        dirs: { link: r.dirs, text: 'Google Maps transit' }
      });
    })
  },

  /* ---------------- Restaurants ---------------- */
  restaurants: {
    columns: [
      { key: 'name', label: 'Restaurant' },
      { key: 'stars', label: 'Distinction', render: 'distinction' },
      { key: 'cuisine', label: 'Cuisine' },
      { key: 'price_band', label: 'Price band' },
      { key: 'address', label: 'Address' },
      { key: 'hours', label: 'Days & hours' },
      { key: 'exceptions', label: 'Exceptions / rules' },
      { key: 'cost2', label: 'Cost for 2', render: 'dash' },
      { key: 'michelin', label: 'MICHELIN', render: 'link' },
      { key: 'official', label: 'Official site', render: 'links' },
      { key: 'social', label: 'Social', render: 'social' },
      { key: 'phone', label: 'Phone' }
    ],
    rows: window.RESTAURANTS.map(function (r) {
      return Object.assign({}, r, {
        michelin: { link: r.michelin, text: 'Record' },
        official: r.official ? { link: r.official, text: 'Website' } : ''
      });
    })
  },

  /* ---------------- Activities ---------------- */
  activities: {
    columns: [
      { key: 'name', label: 'Activity' },
      { key: 'category', label: 'Type' },
      { key: 'address', label: 'Address' },
      { key: 'hours', label: 'Days & hours' },
      { key: 'exceptions', label: 'Exceptions / rules' },
      { key: 'cost', label: 'Cost' },
      { key: 'booking', label: 'Booking' },
      { key: 'official', label: 'Official site', render: 'link' },
      { key: 'social', label: 'Social', render: 'social' },
      { key: 'transit', label: 'Getting there' }
    ],
    rows: window.ACTIVITIES.map(function (a) {
      return Object.assign({}, a, {
        official: { link: a.official, text: 'Official page' }
      });
    })
  },

  /* ---------------- Activity backlog ---------------- */
  activity_backlog: {
    columns: [
      { key: 'name', label: 'Candidate' },
      { key: 'why', label: 'Why it fits' },
      { key: 'status', label: 'Verification status' },
      { key: 'official', label: 'Official site', render: 'link' }
    ],
    rows: window.ACTIVITY_BACKLOG.map(function (a) {
      return Object.assign({}, a, { official: { link: a.official, text: 'Open' } });
    })
  },

  /* ---------------- Itinerary ---------------- */
  itinerary: {
    columns: [
      { key: 'day', label: 'Day' },
      { key: 'kind', label: 'Focus' },
      { key: 'morning', label: 'Morning' },
      { key: 'afternoon', label: 'Afternoon' },
      { key: 'evening', label: 'Evening' },
      { key: 'why', label: 'Why this day' }
    ],
    rows: window.ITINERARY
  },

  /* ---------------- Budget ---------------- */
  budget: {
    columns: [
      { key: 'item', label: 'Line item' },
      { key: 'amount', label: 'Amount (2 adults)', num: true, render: 'money' },
      { key: 'basis', label: 'Basis / arithmetic' },
      { key: 'status', label: 'Status', render: 'status' },
      { key: 'src', label: 'Source', render: 'links' }
    ],
    rows: window.BUDGET.map(function (b) {
      return Object.assign({}, b, {
        src: b.src ? { link: b.src, text: 'Source' } : ''
      });
    })
  },

  /* ---------------- Booking timing ---------------- */
  price_windows: {
    columns: [
      { key: 'window', label: 'Window / question' },
      { key: 'nights', label: 'Nights', num: true },
      { key: 'observed', label: 'What we observed' },
      { key: 'note', label: 'Detail' },
      { key: 'status', label: 'Status', render: 'status' }
    ],
    rows: window.PRICE_WINDOWS
  },

  /* ---------------- Suggestions ---------------- */
  suggestions: {
    columns: [
      { key: 'id', label: '#' },
      { key: 'title', label: 'Suggestion' },
      { key: 'impact', label: 'Impact' },
      { key: 'effort', label: 'Effort' },
      { key: 'problem', label: 'Problem it solves' },
      { key: 'proposal', label: 'Proposed change' },
      { key: 'done_when', label: 'Done when' }
    ],
    rows: window.SUGGESTIONS
  },

  /* ---------------- Questions ---------------- */
  questions: {
    columns: [
      { key: 'id', label: '#' },
      { key: 'area', label: 'Area' },
      { key: 'question', label: 'Question to settle' },
      { key: 'known', label: 'What we know', },
      { key: 'missing', label: 'What is missing' },
      { key: 'how', label: 'How to find it' }
    ],
    rows: window.QUESTIONS
  },

  /* ---------------- Flagged ---------------- */
  flagged: {
    columns: [
      { key: 'id', label: 'ID' },
      { key: 'severity', label: 'Severity' },
      { key: 'item', label: 'Item' },
      { key: 'detail', label: 'What happened' },
      { key: 'evidence', label: 'Evidence / what we do instead' },
      { key: 'action', label: 'Action' },
      { key: 'link', label: 'Where', render: 'link' }
    ],
    rows: window.FLAGGED.map(function (f) {
      var l = f.link || '';
      var isPage = /\.html/.test(l) && l.indexOf('http') !== 0;
      return Object.assign({}, f, {
        link: l ? { link: l, text: isPage ? 'On this site' : 'Source' } : ''
      });
    })
  },

  /* ---------------- Sources ---------------- */
  sources: {
    columns: [
      { key: 'id', label: 'ID' },
      { key: 'what', label: 'What it verified' },
      { key: 'type', label: 'Source type' },
      { key: 'read', label: 'Read on' },
      { key: 'url', label: 'Link', render: 'link' }
    ],
    rows: window.SOURCES.map(function (s) {
      return Object.assign({}, s, { url: { link: s.url, text: 'Open source' } });
    })
  },

  /* ---------------- Repo findings ---------------- */
  repo_findings: {
    columns: [
      { key: 'id', label: 'ID' },
      { key: 'severity', label: 'Severity' },
      { key: 'finding', label: 'Finding' },
      { key: 'detail', label: 'Detail' },
      { key: 'action', label: 'Action taken / recommended' }
    ],
    rows: window.REPO_FINDINGS
  }
};
