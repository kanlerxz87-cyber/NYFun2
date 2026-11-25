#!/usr/bin/env node
/**
 * check_render.js — proves every data table actually renders.
 *
 * Loads data.js + tables.js + app.js in a VM with a stub DOM, asks app.js to
 * render each table referenced by a page, then asserts:
 *   - each table produced markup
 *   - <tr>/<td> tags are balanced
 *   - no unrendered values leak out as ">undefined<", ">NaN<" or "[object Object]"
 *   - required anchors exist for cross-page links (flagged.html#F-xx, questions.html#Q-xx)
 *
 * Run: node tools/check_render.js
 */
'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');

const TABLES = [
  'michelin_coverage', 'hotels', 'hotel_clusters', 'restaurants', 'activities',
  'activity_backlog', 'itinerary', 'budget', 'price_windows', 'suggestions',
  'questions', 'flagged', 'sources', 'repo_findings'
];

const holders = TABLES.map(function (key) {
  return {
    _key: key,
    innerHTML: '',
    getAttribute: function (a) {
      if (a === 'data-table') return this._key;
      return null;
    }
  };
});

const sandbox = {
  window: {},
  console: console,
  location: { pathname: '/index.html' },
  document: {
    readyState: 'complete',
    getElementById: function () { return null; },
    querySelectorAll: function (sel) { return sel === '[data-table]' ? holders : []; },
    addEventListener: function () {}
  }
};
sandbox.globalThis = sandbox;
vm.createContext(sandbox);

['assets/data.js', 'assets/tables.js', 'assets/app.js'].forEach(function (f) {
  const full = path.join(ROOT, f);
  if (!fs.existsSync(full)) {
    console.error('MISSING FILE: ' + f);
    process.exit(1);
  }
  vm.runInContext(fs.readFileSync(full, 'utf8'), sandbox, { filename: f });
});

let failures = 0;
const problems = [];

function check(cond, msg) {
  if (!cond) { failures++; problems.push(msg); }
}

/* ---- per-table structural checks ---- */
holders.forEach(function (h) {
  const html = h.innerHTML;
  check(html.length > 0, h._key + ': table rendered empty');
  if (!html) return;

  const trOpen = (html.match(/<tr/g) || []).length;
  const trClose = (html.match(/<\/tr>/g) || []).length;
  const tdOpen = (html.match(/<td/g) || []).length;
  const tdClose = (html.match(/<\/td>/g) || []).length;

  check(trOpen === trClose, h._key + ': unbalanced <tr> (' + trOpen + ' open / ' + trClose + ' close)');
  check(tdOpen === tdClose, h._key + ': unbalanced <td> (' + tdOpen + ' open / ' + tdClose + ' close)');

  /* an unrendered JS value would show up as a bare token inside a cell */
  check(!/>\s*undefined\s*</.test(html), h._key + ': literal "undefined" inside a cell');
  check(!/>\s*NaN\s*</.test(html), h._key + ': literal "NaN" inside a cell');
  check(html.indexOf('[object Object]') === -1, h._key + ': "[object Object]" leaked into markup');

  const rows = (html.match(/<tr id=/g) || []).length;
  console.log('  ok  ' + h._key.padEnd(20) + ' rows=' + String(rows).padStart(2) + '  bytes=' + String(html.length).padStart(6));
});

/* ---- spot checks on values that must survive rendering ---- */
function table(key) {
  const h = holders.filter(function (x) { return x._key === key; })[0];
  return h ? h.innerHTML : '';
}

check(table('hotels').indexOf('$1,305') > -1, 'hotels: expected all-in figure $1,305');
check(table('hotels').indexOf('Hyatt Place') > -1, 'hotels: Hyatt Place row missing');
check(table('restaurants').indexOf('instagram.com/lebernardinny') > -1, 'restaurants: Le Bernardin Instagram link missing');
check(table('restaurants').indexOf('F-06') > -1, 'restaurants: cost-for-two should carry flag F-06');
check(table('flagged').indexOf('id="F-01"') > -1, 'flagged: anchor id="F-01" missing');
check(table('flagged').indexOf('id="F-15"') > -1, 'flagged: anchor id="F-15" missing');
check(table('questions').indexOf('id="Q-05"') > -1, 'questions: anchor id="Q-05" missing');
check(table('sources').length > 1000, 'sources: expected a populated register');

console.log('');
if (problems.length) {
  console.log('FAILURES');
  problems.forEach(function (p) { console.log('  x ' + p); });
  console.log('\nFAILED — ' + problems.length + ' render problem(s)');
  process.exit(1);
}
console.log('OK — all ' + holders.length + ' tables render cleanly');
