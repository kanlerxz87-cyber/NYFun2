(function () {
  function esc(str) {
    return String(str == null ? "" : str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function renderBlank(val, flagMsg) {
    if (val && String(val).trim() !== "") return esc(val);
    return '<span class="blank-flag" title="' + esc(flagMsg || "Unverified on official site — left blank") + '">[Blank — Unverified]</span>';
  }

  function renderSocials(socials, emptyNote) {
    if (!Array.isArray(socials) || socials.length === 0) {
      return '<span class="blank-flag">' + esc(emptyNote || "[Blank — Flagged]") + '</span>';
    }
    return '<div class="social-list">' + socials.map(function (s) {
      var cls = s.platform === "YouTube" ? "yt" : (s.platform === "TikTok" ? "tt" : "ig");
      var prefix = s.platform === "YouTube" ? "YT" : (s.platform === "TikTok" ? "TT" : "IG");
      return '<a class="social-chip ' + cls + '" href="' + esc(s.url) + '" target="_blank" rel="noopener">' +
        prefix + ": " + esc(s.label) + "</a>";
    }).join("") + "</div>";
  }

  function distinctionBadge(item) {
    if (item.stars === 3) return '<span class="pill pill-star3">★★★ 3 Stars</span>';
    if (item.stars === 2) return '<span class="pill pill-star2">★★ 2 Stars</span>';
    if (item.stars === 1) return '<span class="pill pill-star1">★ 1 Star</span>';
    if (String(item.distinction).indexOf("Bib Gourmand") !== -1) {
      return '<span class="pill pill-bib">Bib Gourmand (No Star)</span>';
    }
    return '<span class="pill pill-sel">MICHELIN Selected (No Star)</span>';
  }

  async function initRestaurants() {
    var root = document.getElementById("restaurants-app");
    if (!root) return;
    var base = root.getAttribute("data-base") || ".";
    var res = await fetch(base + "/data/restaurants.json");
    var data = await res.json();

    var clusterBox = document.getElementById("clusters-grid");
    if (clusterBox && data.meta && Array.isArray(data.meta.clusters)) {
      clusterBox.innerHTML = data.meta.clusters.map(function (c) {
        return '<div class="card" style="margin-bottom:0">' +
          '<h3>' + esc(c.name) + '</h3>' +
          '<p class="muted" style="margin:0.2rem 0 0.5rem">Anchor: <strong>' + esc(c.anchor) + '</strong></p>' +
          '<div><span class="pill pill-star3">' + esc(c.starredInCluster) + ' Starred</span> ' +
          '<span class="pill pill-sel">' + esc(c.guideListedInCluster) + ' Guide-Listed (Bib/Selected)</span> ' +
          '<span class="pill pill-ok">' + esc(c.totalMichelinInCluster) + ' Total</span></div>' +
          '<p class="muted" style="margin:0.5rem 0 0">' + esc(c.transitNote) + '</p>' +
          '</div>';
      }).join("");
    }

    var searchEl = document.getElementById("rest-search");
    var tierEl = document.getElementById("rest-tier");
    var clusterEl = document.getElementById("rest-cluster");
    var tbody = document.getElementById("rest-tbody");
    var countEl = document.getElementById("rest-count");

    function render() {
      var q = (searchEl && searchEl.value || "").toLowerCase().trim();
      var tier = tierEl ? tierEl.value : "all";
      var cl = clusterEl ? clusterEl.value : "all";

      var rows = data.items.filter(function (r) {
        if (tier === "starred" && r.stars === 0) return false;
        if (tier === "3" && r.stars !== 3) return false;
        if (tier === "2" && r.stars !== 2) return false;
        if (tier === "1" && r.stars !== 1) return false;
        if (tier === "guide-only" && r.stars > 0) return false;
        if (cl !== "all" && r.clusterId !== cl) return false;
        if (q) {
          var hay = [r.name, r.cuisine, r.clusterLabel, r.distinction, r.daysOpen, r.coupleMenuTotal].join(" ").toLowerCase();
          if (hay.indexOf(q) === -1) return false;
        }
        return true;
      });

      if (countEl) countEl.textContent = rows.length + " of " + data.items.length + " venues shown";

      tbody.innerHTML = rows.map(function (r) {
        var venueLink = r.officialUrl
          ? '<a href="' + esc(r.officialUrl) + '" target="_blank" rel="noopener"><strong>' + esc(r.name) + '</strong></a>'
          : '<strong>' + esc(r.name) + '</strong> <span class="blank-flag">[No public site]</span>';
        var priceLink = r.priceSourceUrl
          ? '<div><a href="' + esc(r.priceSourceUrl) + '" target="_blank" rel="noopener">Official Menu / Price</a></div>'
          : "";
        var flagHtml = (r.flags && r.flags.length)
          ? '<div style="margin-top:0.35rem">' + r.flags.map(function (f) { return '<span class="pill pill-flag">Flag: ' + esc(f) + '</span>'; }).join(" ") + '</div>'
          : "";
        return "<tr>" +
          "<td>" + venueLink + '<div class="muted">' + esc(r.cuisine) + " · " + esc(r.address) + "</div></td>" +
          "<td>" + distinctionBadge(r) + '<div class="muted" style="margin-top:0.2rem">' + esc(r.statusCategory) + "</div></td>" +
          "<td><strong>" + esc(r.clusterLabel) + "</strong></td>" +
          "<td><strong>" + renderBlank(r.coupleMenuTotal, r.couplePriceBasis) + '</strong><div class="muted" style="margin-top:0.2rem">' + esc(r.couplePriceBasis) + "</div>" + flagHtml + "</td>" +
          "<td><strong>" + esc(r.daysOpen) + "</strong><div>" + esc(r.hours) + '</div><div class="muted" style="margin-top:0.2rem">' + esc(r.exceptions) + "</div></td>" +
          "<td>" + renderSocials(r.socials, "[Blank — Verified avoid mix-up]") + "</td>" +
          '<td><a href="' + esc(r.sourceUrl) + '" target="_blank" rel="noopener">MICHELIN Guide</a>' + priceLink + "</td>" +
          "</tr>";
      }).join("");
    }

    if (searchEl) searchEl.addEventListener("input", render);
    if (tierEl) tierEl.addEventListener("change", render);
    if (clusterEl) clusterEl.addEventListener("change", render);
    render();
  }

  async function initHotels() {
    var root = document.getElementById("hotels-app");
    if (!root) return;
    var base = root.getAttribute("data-base") || ".";
    var res = await fetch(base + "/data/hotels.json");
    var data = await res.json();

    var winTbody = document.getElementById("windows-tbody");
    if (winTbody && Array.isArray(data.crossWeekWindows)) {
      winTbody.innerHTML = data.crossWeekWindows.map(function (w) {
        var statusBadge = w.qualifiesQueenBath
          ? '<span class="pill pill-ok">Qualifies (Queen+/Bath)</span>'
          : '<span class="pill pill-flag">Disqualified (Twin Room)</span>';
        return "<tr>" +
          "<td><strong>" + esc(w.windowId) + ": " + esc(w.dates) + "</strong></td>" +
          "<td>" + esc(w.benchmarkHotel) + "<div>" + statusBadge + "</div></td>" +
          "<td><strong>" + esc(w.preTax7Night) + "</strong></td>" +
          "<td><strong>" + esc(w.estimatedAllIn7Night) + "</strong></td>" +
          "<td>" + esc(w.notes) + "</td>" +
          '<td><a href="' + esc(w.sourceUrl) + '" target="_blank" rel="noopener">Live Search Link</a></td>' +
          "</tr>";
      }).join("");
    }

    var searchEl = document.getElementById("hotel-search");
    var filterEl = document.getElementById("hotel-filter");
    var tbody = document.getElementById("hotels-tbody");

    function render() {
      var q = (searchEl && searchEl.value || "").toLowerCase().trim();
      var mode = filterEl ? filterEl.value : "all";
      var rows = data.items.filter(function (h) {
        if (mode === "dated" && !h.allIn7Night) return false;
        if (mode === "under1500" && (!h.allIn7Night || parseInt(h.allIn7Night.replace(/[^0-9]/g, ""), 10) > 1500)) return false;
        if (q) {
          var hay = [h.name, h.neighborhood, h.qualifyingRoom, h.amenities, h.badge].join(" ").toLowerCase();
          if (hay.indexOf(q) === -1) return false;
        }
        return true;
      });

      tbody.innerHTML = rows.map(function (h) {
        var flags = (h.flags || []).map(function (f) {
          return '<div style="margin-top:0.25rem"><span class="pill pill-flag">' + esc(f) + "</span></div>";
        }).join("");
        return "<tr>" +
          "<td><strong>#" + esc(h.rank) + "</strong></td>" +
          '<td><a href="' + esc(h.officialUrl) + '" target="_blank" rel="noopener"><strong>' + esc(h.name) + '</strong></a>' +
          '<div><span class="pill pill-sel">' + esc(h.badge) + '</span></div>' +
          '<div class="muted">' + esc(h.neighborhood) + " · " + esc(h.address) + "</div></td>" +
          "<td><strong>" + esc(h.qualifyingRoom) + "</strong><div class='muted'>" + esc(h.privateBathroom) + "</div></td>" +
          "<td><strong>" + renderBlank(h.allIn7Night, h.taxArithmetic) + "</strong>" +
          (h.preTax7Night ? '<div class="muted">Pre-tax: ' + esc(h.preTax7Night) + "</div>" : "") +
          '<div class="muted">' + esc(h.taxArithmetic) + "</div>" +
          '<div class="muted"><strong>Terms:</strong> ' + esc(h.cancellationTerms) + "</div>" + flags + "</td>" +
          "<td><strong>" + esc(h.michelinWithin60Min) + '</strong><div class="muted" style="margin-top:0.25rem">' + esc(h.clusterTransitBreakdown) + "</div></td>" +
          "<td>" + esc(h.amenities) + '<div class="muted" style="margin-top:0.25rem"><strong>Cheapest window:</strong> ' + renderBlank(h.cheapestWindow, "Dated Feb/Mar 2027 window unverified") + "</div></td>" +
          '<td><a href="' + esc(h.roomSourceUrl) + '" target="_blank" rel="noopener">Official Room</a><br>' +
          '<a href="' + esc(h.rateSourceUrl) + '" target="_blank" rel="noopener">Rate Source</a><br>' +
          '<a href="' + esc(h.transitSourceUrl) + '" target="_blank" rel="noopener">Transit Route</a></td>' +
          "</tr>";
      }).join("");
    }

    if (searchEl) searchEl.addEventListener("input", render);
    if (filterEl) filterEl.addEventListener("change", render);
    render();
  }

  async function initActivities() {
    var root = document.getElementById("activities-app");
    if (!root) return;
    var base = root.getAttribute("data-base") || ".";
    var res = await fetch(base + "/data/activities.json");
    var data = await res.json();

    var searchEl = document.getElementById("act-search");
    var catEl = document.getElementById("act-cat");
    var tbody = document.getElementById("act-tbody");

    function render() {
      var q = (searchEl && searchEl.value || "").toLowerCase().trim();
      var cat = catEl ? catEl.value : "all";
      var rows = data.items.filter(function (a) {
        if (cat === "free" && a.coupleCost.indexOf("$0") === -1) return false;
        if (cat === "seasonal" && a.category.toLowerCase().indexOf("seasonal") === -1) return false;
        if (cat === "museum" && a.category.toLowerCase().indexOf("museum") === -1) return false;
        if (q) {
          var hay = [a.name, a.category, a.neighborhood, a.daysOpen, a.exceptions].join(" ").toLowerCase();
          if (hay.indexOf(q) === -1) return false;
        }
        return true;
      });

      tbody.innerHTML = rows.map(function (a) {
        var flags = (a.flags || []).map(function (f) {
          return '<div style="margin-top:0.25rem"><span class="pill pill-flag">' + esc(f) + "</span></div>";
        }).join("");
        return "<tr>" +
          '<td><a href="' + esc(a.officialUrl) + '" target="_blank" rel="noopener"><strong>' + esc(a.name) + '</strong></a>' +
          '<div class="muted">' + esc(a.category) + " · " + esc(a.neighborhood) + "</div></td>" +
          "<td><strong>" + esc(a.coupleCost) + "</strong>" + flags + "</td>" +
          "<td><strong>" + esc(a.daysOpen) + "</strong><div>" + esc(a.hours) + '</div><div class="muted" style="margin-top:0.2rem">' + esc(a.exceptions) + "</div></td>" +
          "<td>" + esc(a.maxTransitFromShortlist) + "</td>" +
          "<td>" + renderSocials(a.socials) + "</td>" +
          '<td><a href="' + esc(a.sourceUrl) + '" target="_blank" rel="noopener">Official Visitor Page</a></td>' +
          "</tr>";
      }).join("");
    }

    if (searchEl) searchEl.addEventListener("input", render);
    if (catEl) catEl.addEventListener("change", render);
    render();
  }

  async function initDecisions() {
    var root = document.getElementById("decisions-app");
    if (!root) return;
    var base = root.getAttribute("data-base") || ".";
    var res = await fetch(base + "/data/decisions_and_audit.json");
    var data = await res.json();

    var itinEl = document.getElementById("itin-tbody");
    if (itinEl && data.itinerary7Night) {
      itinEl.innerHTML = data.itinerary7Night.days.map(function (d) {
        return "<tr><td><strong>" + esc(d.day) + "</strong></td><td><strong>" + esc(d.theme) + "</strong></td><td>" + esc(d.plan) + "</td><td>" + esc(d.maxTransit) + "</td></tr>";
      }).join("");
    }

    var qEl = document.getElementById("questions-tbody");
    if (qEl && Array.isArray(data.questions)) {
      qEl.innerHTML = data.questions.map(function (q) {
        return "<tr><td><strong>" + esc(q.id) + "</strong></td><td><strong>" + esc(q.question) + "</strong></td><td>" + esc(q.known) + "</td><td>" + esc(q.missing) + "</td><td>" + esc(q.howToDiscover) + '</td><td><a href="' + esc(q.sourceUrl) + '" target="_blank" rel="noopener">Official Source</a></td></tr>';
      }).join("");
    }

    var sEl = document.getElementById("suggestions-grid");
    if (sEl && Array.isArray(data.suggestions)) {
      sEl.innerHTML = data.suggestions.map(function (s) {
        return '<div class="card" style="margin-bottom:0">' +
          '<span class="pill pill-flag">' + esc(s.status) + "</span>" +
          "<h3>" + esc(s.id) + ": " + esc(s.title) + "</h3>" +
          '<p class="muted" style="margin:0.25rem 0">' + esc(s.category) + "</p>" +
          "<p style='margin:0.4rem 0 0'>" + esc(s.whyItHelps) + "</p></div>";
      }).join("");
    }

    var aEl = document.getElementById("audit-tbody");
    if (aEl && Array.isArray(data.auditFindings)) {
      aEl.innerHTML = data.auditFindings.map(function (a) {
        return "<tr><td><strong>" + esc(a.id) + '</strong><div><span class="pill pill-flag">' + esc(a.severity) + "</span></div></td>" +
          "<td><code>" + esc(a.file) + "</code></td>" +
          "<td>" + esc(a.finding) + "</td>" +
          "<td>" + esc(a.resolutionIn657520df) + "</td>" +
          '<td><a href="' + esc(a.manualVerifyUrl) + '" target="_blank" rel="noopener">Verify Source</a></td></tr>';
      }).join("");
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    initRestaurants();
    initHotels();
    initActivities();
    initDecisions();
  });
})();
