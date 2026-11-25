/* NYC Trip Planner — tiny progressive-enhancement layer.
   No framework, no network calls. Everything degrades gracefully without JS. */
(function () {
  "use strict";

  /* ---------------------------------------------------------------- mobile nav */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.textContent = open ? "Close" : "Menu";
    });
    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        nav.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.textContent = "Menu";
      }
    });
  }

  /* ------------------------------------------------- active nav link by path */
  var here = location.pathname.split("/").pop() || "index.html";
  Array.prototype.forEach.call(document.querySelectorAll("#site-nav a"), function (a) {
    var target = (a.getAttribute("href") || "").split("#")[0];
    if (target && target === here) a.setAttribute("aria-current", "page");
  });

  /* ------------------------------------------- tables: mark scrollability */
  Array.prototype.forEach.call(document.querySelectorAll(".table-scroll"), function (box) {
    var apply = function () {
      var scrollable = box.scrollWidth > box.clientWidth + 4;
      box.classList.toggle("is-scrollable", scrollable);
    };
    apply();
    window.addEventListener("resize", apply, { passive: true });
  });

  /* ------------------------------------------------ sortable wide tables */
  Array.prototype.forEach.call(document.querySelectorAll("table.data"), function (tbl) {
    var ths = tbl.querySelectorAll("thead th");
    if (ths.length < 2) return;
    Array.prototype.forEach.call(ths, function (th, idx) {
      th.classList.add("sortable");
      th.setAttribute("tabindex", "0");
      th.setAttribute("role", "button");
      th.title = "Sort by " + th.textContent.trim();
      var sort = function (dir) {
        var body = tbl.tBodies[0];
        var rows = Array.prototype.slice.call(body.rows);
        var val = function (tr) {
          var cell = tr.cells[idx];
          if (!cell) return "";
          var raw = cell.getAttribute("data-sort");
          if (raw !== null) return raw;
          return cell.textContent.trim();
        };
        rows.sort(function (a, b) {
          var x = val(a), y = val(b);
          var nx = parseFloat(String(x).replace(/[^0-9.\-]/g, ""));
          var ny = parseFloat(String(y).replace(/[^0-9.\-]/g, ""));
          var bothNumeric = !isNaN(nx) && !isNaN(ny) && /\d/.test(String(x)) && /\d/.test(String(y));
          if (bothNumeric) return dir * (nx - ny);
          return dir * String(x).localeCompare(String(y));
        });
        rows.forEach(function (r) { body.appendChild(r); });
      };
      var state = 1;
      var run = function () {
        state = state === 1 ? -1 : 1;
        sort(state);
      };
      th.addEventListener("click", run);
      th.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); run(); }
      });
    });
  });

  /* ------------------------------------------- suggestion accept / reject */
  var KEY = "nyfun2.suggestions.v1";
  var store = {};
  try { store = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { store = {}; }

  function paint(btn) {
    var id = btn.getAttribute("data-suggest-id");
    var wrap = btn.closest(".suggestion");
    if (!wrap) return;
    var stateEl = wrap.querySelector(".review-state");
    var current = store[id];
    wrap.classList.toggle("accepted", current === "accept");
    wrap.classList.toggle("rejected", current === "reject");
    if (stateEl) stateEl.textContent = current ? current + "ed · saved locally" : "proposed";
  }

  Array.prototype.forEach.call(document.querySelectorAll("[data-suggest-id]"), paint);
  Array.prototype.forEach.call(document.querySelectorAll("[data-suggest]"), function (btn) {
    btn.addEventListener("click", function () {
      var wrap = btn.closest(".suggestion");
      if (!wrap) return;
      var idEl = wrap.querySelector("[data-suggest-id]");
      if (!idEl) return;
      var id = idEl.getAttribute("data-suggest-id");
      var want = btn.getAttribute("data-suggest");
      store[id] = store[id] === want ? null : want;
      if (!store[id]) delete store[id];
      try { localStorage.setItem(KEY, JSON.stringify(store)); } catch (e) {}
      Array.prototype.forEach.call(document.querySelectorAll('[data-suggest-id="' + id + '"]'), paint);
    });
  });

  /* --------------------------------------------------- deep-link highlight */
  if (location.hash) {
    var target = document.getElementById(location.hash.slice(1));
    if (target) target.classList.add("flash");
  }

  /* ------------------------------------------------------ print affordance */
  Array.prototype.forEach.call(document.querySelectorAll("[data-print]"), function (b) {
    b.addEventListener("click", function () { window.print(); });
  });
})();
