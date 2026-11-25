(function () {
  "use strict";

  function esc(str) {
    return String(str == null ? "" : str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function renderBlank(label) {
    return '<span class="blank-cell">' + esc(label || "Unverified — left blank") + "</span>";
  }

  function renderSocialPills(social) {
    if (!Array.isArray(social) || social.length === 0) {
      return renderBlank("No verified social link");
    }
    return (
      '<div class="social-pills">' +
      social
        .map(function (s) {
          var cls = "ig";
          var prefix = "IG";
          if (s.platform === "YouTube") {
            cls = "yt";
            prefix = "YT";
          } else if (s.platform === "TikTok") {
            cls = "tt";
            prefix = "TT";
          }
          var kind = s.type === "official" ? "Official" : "Review";
          return (
            '<a class="social-pill ' +
            cls +
            '" href="' +
            esc(s.url) +
            '" target="_blank" rel="noopener noreferrer" title="' +
            esc(s.label) +
            '">' +
            prefix +
            " · " +
            kind +
            "</a>"
          );
        })
        .join("") +
      "</div>"
    );
  }

  function tierBadge(tierGroup, statusText) {
    var cls = "badge-selected";
    if (tierGroup === "3-Star") cls = "badge-3star";
    else if (tierGroup === "2-Star") cls = "badge-2star";
    else if (tierGroup === "1-Star") cls = "badge-1star";
    else if (tierGroup === "Bib Gourmand") cls = "badge-bib";
    return '<span class="badge ' + cls + '">' + esc(statusText) + "</span>";
  }

  async function loadJson(relPath) {
    var res = await fetch(relPath);
    if (!res.ok) throw new Error("Failed to load " + relPath + " (" + res.status + ")");
    return res.json();
  }

  async function initOverview(base) {
    var d = await loadJson(base + "data/decisions.json");
    var findingsEl = document.getElementById("exec-findings");
    if (findingsEl && d.executiveSummary) {
      findingsEl.innerHTML = d.executiveSummary.keyFindings
        .map(function (f) {
          return (
            '<div class="info-card"><h3>' +
            esc(f.topic) +
            "</h3><p>" +
            esc(f.summary) +
            "</p></div>"
          );
        })
        .join("");
    }
  }

  async function initRestaurants(base) {
    var data = await loadJson(base + "data/restaurants.json");
    var clusterEl = document.getElementById("cluster-cards");
    if (clusterEl) {
      clusterEl.innerHTML = data.clusters
        .map(function (c) {
          return (
            '<div class="info-card">' +
            "<h3>" +
            esc(c.name) +
            "</h3>" +
            "<p><strong>Subway Hubs:</strong> " +
            esc(c.hubStations) +
            "</p>" +
            "<p><strong>Cluster Focus:</strong> " +
            esc(c.starredInGuideCluster) +
            "</p>" +
            "<p><strong>Anchor:</strong> " +
            esc(c.anchorVenue) +
            " (" +
            esc(c.featuredCount) +
            " curated rows)</p>" +
            "</div>"
          );
        })
        .join("");
    }

    var tbody = document.getElementById("restaurants-tbody");
    var searchIn = document.getElementById("rest-search");
    var tierSel = document.getElementById("rest-tier");
    var clusterSel = document.getElementById("rest-cluster");
    var countEl = document.getElementById("rest-count");

  function renderRows() {
      var q = ((searchIn && searchIn.value) || "").toLowerCase().trim();
      var tier = (tierSel && tierSel.value) || "ALL";
      var cl = (clusterSel && clusterSel.value) || "ALL";

      var rows = data.items.filter(function (r) {
        if (tier !== "ALL") {
          if (tier === "STARRED" && r.tierGroup.indexOf("Star") === -1) return false;
          if (tier === "GUIDE_ONLY" && r.tierGroup.indexOf("Star") !== -1) return false;
          if (tier !== "STARRED" && tier !== "GUIDE_ONLY" && r.tierGroup !== tier) return false;
        }
        if (cl !== "ALL" && r.clusterId !== cl) return false;
        if (q) {
          var hay = [r.name, r.cuisine, r.address, r.clusterLabel, r.daysOpen, r.totalPriceTwoAdults]
            .join(" ")
            .toLowerCase();
          if (hay.indexOf(q) === -1) return false;
        }
        return true;
      });

      if (countEl) countEl.textContent = "Showing " + rows.length + " of " + data.items.length + " verified venues";

      tbody.innerHTML = rows
        .map(function (r) {
          var flagsHtml =
            r.flags && r.flags.length
              ? '<div class="flag-note">Flag: ' + esc(r.flags.join(" ")) + "</div>"
              : "";
          var priceHtml = r.totalPriceTwoAdults
            ? "<strong>" +
              esc(r.totalPriceTwoAdults) +
              "</strong><br><small>" +
              esc(r.priceDetail) +
              (r.priceSourceUrl
                ? ' · <a href="' + esc(r.priceSourceUrl) + '" target="_blank" rel="noopener">Menu/Tock Source</a>'
                : "") +
              "</small>"
            : renderBlank("Official price unpublished — left blank") +
              "<br><small>" +
              esc(r.priceDetail) +
              "</small>";

          var siteLinks = r.officialUrl
            ? '<a href="' +
              esc(r.officialUrl) +
              '" target="_blank" rel="noopener">Official Site</a> · <a href="' +
              esc(r.sourceUrl) +
              '" target="_blank" rel="noopener">MICHELIN Listing</a>'
            : '<span class="blank-cell">Official URL unverified</span> · <a href="' +
              esc(r.sourceUrl) +
              '" target="_blank" rel="noopener">MICHELIN Listing</a>';
          var schedHtml = r.daysOpen
            ? "<strong>" + esc(r.daysOpen) + "</strong><br><small>" + esc(r.hours) + "</small>"
            : renderBlank("Hours unverified — left blank");

          return (
            "<tr>" +
            '<td data-label="Restaurant & Links"><strong>' +
            esc(r.name) +
            "</strong><br><small>" +
            esc(r.cuisine) +
            " · " +
            esc(r.address) +
            "</small><br><small>" +
            siteLinks +
            "</small></td>" +
            '<td data-label="Michelin Distinction">' +
            tierBadge(r.tierGroup, r.michelinStatus) +
            "<br><small>" +
            esc(r.clusterLabel) +
            "</small></td>" +
            '<td data-label="Couple Total (2 Adults)">' +
            priceHtml +
            flagsHtml +
            "</td>" +
            '<td data-label="Open Days & Hours">' +
            schedHtml +
            "</td>" +
            '<td data-label="Exceptions & Booking"><small>' +
            esc(r.exceptions) +
            "</small></td>" +
            '<td data-label="Reviews (YT / TT / IG)">' +
            renderSocialPills(r.social) +
            "</td>" +
            "</tr>"
          );
        })
        .join("");
    }

    if (searchIn) searchIn.addEventListener("input", renderRows);
    if (tierSel) tierSel.addEventListener("change", renderRows);
    if (clusterSel) clusterSel.addEventListener("change", renderRows);
    renderRows();
  }

  async function initHotels(base) {
    var data = await loadJson(base + "data/hotels.json");
    var winTbody = document.getElementById("windows-tbody");
    if (winTbody) {
      winTbody.innerHTML = data.bookingWindows
        .map(function (w) {
          var badge =
            w.windowId === "W1"
              ? '<span class="badge badge-ok">Cheapest Verified Queen Window</span>'
              : w.windowId === "W2"
              ? '<span class="badge badge-warn">Twin Room Trap ($836 Fails Queen+)</span>'
              : "";
          return (
            "<tr>" +
            '<td data-label="Window"><strong>' +
            esc(w.dates) +
            "</strong> " +
            badge +
            "</td>" +
            '<td data-label="Lowest Candidate">' +
            esc(w.cheapestQualifyingHotel) +
            "</td>" +
            '<td data-label="7-Night Pre-Tax"><strong>' +
            esc(w.preTaxTotalUsd) +
            "</strong> (" +
            esc(w.perNightPreTaxUsd) +
            "/nt)</td>" +
            '<td data-label="7-Night Est. All-In"><strong>' +
            esc(w.estimatedAllInUsd) +
            "</strong></td>" +
            '<td data-label="Notes & Source"><small>' +
            esc(w.notes) +
            ' · <a href="' +
            esc(w.sourceUrl) +
            '" target="_blank" rel="noopener">Dated Search Source</a></small></td>' +
            "</tr>"
          );
        })
        .join("");
    }

    var tbody = document.getElementById("hotels-tbody");
    if (tbody) {
      tbody.innerHTML = data.items
        .map(function (h) {
          var preTax = h.sevenNightPreTax ? "<strong>" + esc(h.sevenNightPreTax) + "</strong>" : renderBlank("Unverified 2027 total");
          var allIn = h.sevenNightAllIn ? "<strong>" + esc(h.sevenNightAllIn) + "</strong>" : renderBlank("Unverified 2027 total");
          var roomCell = h.qualifyingRoom
            ? "<strong>" + esc(h.qualifyingRoom) + "</strong><br><small>" + esc(h.privateBathroom) + "</small>"
            : renderBlank("Room/bath tier unverified for dated 2027 rate");
          var flagsHtml =
            h.flags && h.flags.length
              ? '<div class="flag-note">' + esc(h.flags.join(" ")) + "</div>"
              : "";

          return (
            "<tr>" +
            '<td data-label="Rank"><strong>#' +
            esc(h.rank) +
            "</strong></td>" +
            '<td data-label="Hotel & Official Links"><strong>' +
            esc(h.name) +
            '</strong><br><span class="badge badge-selected">' +
            esc(h.tierBadge) +
            "</span><br><small>" +
            esc(h.address) +
            '</small><br><small><a href="' +
            esc(h.officialUrl) +
            '" target="_blank" rel="noopener">Official Property</a> · <a href="' +
            esc(h.sourceUrl) +
            '" target="_blank" rel="noopener">Spec Source</a>' +
            (h.rateSourceUrl
              ? ' · <a href="' + esc(h.rateSourceUrl) + '" target="_blank" rel="noopener">2027 Rate Snapshot</a>'
              : "") +
            "</small></td>" +
            '<td data-label="Verified Queen+ & Private Bath">' +
            roomCell +
            "</td>" +
            '<td data-label="Michelin ≤60m Reach & Transit"><strong>' +
            esc(h.michelinWithin60Min) +
            "</strong><br><small>" +
            esc(h.clusterTransitBreakdown) +
            "</small></td>" +
            '<td data-label="7-Night Pre-Tax (15–22 Feb)">' +
            preTax +
            "</td>" +
            '<td data-label="7-Night All-In (w/ 14.75% Tax & Fees)">' +
            allIn +
            "<br><small>" +
            esc(h.taxAndFeeNotes) +
            "</small>" +
            flagsHtml +
            "</td>" +
            '<td data-label="Amenities & Video Reviews"><small>' +
            esc(h.amenities) +
            "</small><br>" +
            renderSocialPills(h.social) +
            "</td>" +
            "</tr>"
          );
        })
        .join("");
    }
  }

  async function initActivities(base) {
    var data = await loadJson(base + "data/activities.json");
    var dData = await loadJson(base + "data/decisions.json");
    var tbody = document.getElementById("activities-tbody");
    var searchIn = document.getElementById("act-search");
    var costSel = document.getElementById("act-cost");
    var countEl = document.getElementById("act-count");

    function renderRows() {
      var q = ((searchIn && searchIn.value) || "").toLowerCase().trim();
      var cf = (costSel && costSel.value) || "ALL";
      var rows = data.items.filter(function (a) {
        if (cf === "FREE" && a.costTwoAdults.indexOf("$0") === -1) return false;
        if (cf === "PAID" && (a.costTwoAdults.indexOf("$0.00 (Free") === 0 || !a.costTwoAdults)) return false;
        if (q) {
          var hay = [a.name, a.category, a.area, a.daysOpen, a.exceptions].join(" ").toLowerCase();
          if (hay.indexOf(q) === -1) return false;
        }
        return true;
      });
      if (countEl) countEl.textContent = "Showing " + rows.length + " of " + data.items.length + " verified activities";

      tbody.innerHTML = rows
        .map(function (a) {
          var costCell = a.costTwoAdults ? "<strong>" + esc(a.costTwoAdults) + "</strong>" : renderBlank("Dynamic checkout price — left blank");
          var flagsHtml =
            a.flags && a.flags.length
              ? '<div class="flag-note">' + esc(a.flags.join(" ")) + "</div>"
              : "";
          return (
            "<tr>" +
            '<td data-label="Activity & Official Links"><strong>' +
            esc(a.name) +
            '</strong><br><span class="badge badge-selected">' +
            esc(a.category) +
            "</span><br><small>" +
            esc(a.address) +
            '</small><br><small><a href="' +
            esc(a.officialUrl) +
            '" target="_blank" rel="noopener">Official Visit Page</a> · <a href="' +
            esc(a.sourceUrl) +
            '" target="_blank" rel="noopener">Pricing/Hours Source</a></small></td>' +
            '<td data-label="Couple Cost (2 Adults)">' +
            costCell +
            flagsHtml +
            "</td>" +
            '<td data-label="Open Days & Hours"><strong>' +
            esc(a.daysOpen) +
            "</strong><br><small>" +
            esc(a.hours) +
            "</small></td>" +
            '<td data-label="Exceptions & Cutoff Dates"><small>' +
            esc(a.exceptions) +
            "</small></td>" +
            '<td data-label="Transit from Hotels (≤60m)"><small>' +
            esc(a.transitNote) +
            "</small></td>" +
            '<td data-label="Reviews (YT / TT / IG)">' +
            renderSocialPills(a.social) +
            "</td>" +
            "</tr>"
          );
        })
        .join("");
    }

    if (searchIn) searchIn.addEventListener("input", renderRows);
    if (costSel) costSel.addEventListener("change", renderRows);
    renderRows();

    var itin3 = document.getElementById("itin-3night");
    if (itin3 && dData.itineraries && dData.itineraries.threeNight) {
      itin3.innerHTML = dData.itineraries.threeNight.days
        .map(function (day) {
          return (
            '<div class="info-card"><h3>' +
            esc(day.day) +
            '</h3><p><span class="badge badge-ok">Max Transit: ' +
            esc(day.maxTransit) +
            "</span> · <strong>" +
            esc(day.cluster) +
            "</strong></p><p><strong>Daytime:</strong> " +
            esc(day.morningAfternoon) +
            "</p><p><strong>Evening Dining:</strong> " +
            esc(day.evening) +
            "</p></div>"
          );
        })
        .join("");
    }

    var itin7 = document.getElementById("itin-7night");
    if (itin7 && dData.itineraries && dData.itineraries.sevenNight) {
      itin7.innerHTML = dData.itineraries.sevenNight.days
        .map(function (day) {
          return (
            '<div class="info-card"><h3>' +
            esc(day.day) +
            "</h3><p><strong>Cluster:</strong> " +
            esc(day.cluster) +
            "</p><p>" +
            esc(day.plan) +
            "</p></div>"
          );
        })
        .join("");
    }
  }

  async function initDecisions(base) {
    var d = await loadJson(base + "data/decisions.json");
    var qEl = document.getElementById("questions-tbody");
    if (qEl) {
      qEl.innerHTML = d.questions
        .map(function (q) {
          var pCls = q.priority === "Blocking" ? "badge-high" : q.priority === "High" ? "badge-warn" : "badge-selected";
          return (
            "<tr>" +
            '<td data-label="ID & Priority"><strong>' +
            esc(q.id) +
            '</strong><br><span class="badge ' +
            pCls +
            '">' +
            esc(q.priority) +
            "</span></td>" +
            '<td data-label="Decision Question"><strong>' +
            esc(q.question) +
            '</strong><br><small><a href="' +
            esc(q.sourceUrl) +
            '" target="_blank" rel="noopener">Official Reference</a></small></td>' +
            '<td data-label="What We Know (Verified)"><small>' +
            esc(q.known) +
            "</small></td>" +
            '<td data-label="What Is Missing"><small>' +
            esc(q.missing) +
            "</small></td>" +
            '<td data-label="Recommended Answer & How to Discover"><small><strong>Recommendation:</strong> ' +
            esc(q.answerFramework) +
            "<br><strong>How to Discover:</strong> " +
            esc(q.howToDiscover) +
            "</small></td>" +
            "</tr>"
          );
        })
        .join("");
    }

    var sEl = document.getElementById("suggestions-grid");
    if (sEl) {
      sEl.innerHTML = d.suggestions
        .map(function (s) {
          return (
            '<div class="info-card">' +
            '<p><span class="badge badge-selected">' +
            esc(s.id) +
            " · " +
            esc(s.category) +
            '</span> <span class="badge badge-ok">Impact: ' +
            esc(s.impact) +
            "</span></p>" +
            "<h3>" +
            esc(s.title) +
            "</h3>" +
            "<p><strong>Why it helps:</strong> " +
            esc(s.rationale) +
            "</p>" +
            "<p><strong>Proposed design:</strong> " +
            esc(s.proposedAction) +
            "</p>" +
            '<div class="flag-note">Status: ' +
            esc(s.status) +
            "</div>" +
            "</div>"
          );
        })
        .join("");
    }
  }

  async function initFlagged(base) {
    var d = await loadJson(base + "data/decisions.json");
    var flEl = document.getElementById("flags-tbody");
    if (flEl) {
      flEl.innerHTML = d.flags
        .map(function (f) {
          var cls = f.severity === "High" ? "badge-high" : f.severity === "Medium" ? "badge-warn" : "badge-selected";
          return (
            "<tr>" +
            '<td data-label="Flag ID"><strong>' +
            esc(f.id) +
            '</strong><br><span class="badge ' +
            cls +
            '">' +
            esc(f.severity) +
            "</span></td>" +
            '<td data-label="Category & Item"><strong>' +
            esc(f.item) +
            "</strong><br><small>" +
            esc(f.category) +
            "</small></td>" +
            '<td data-label="Irregularity / Unverified Detail"><small>' +
            esc(f.issue) +
            "</small></td>" +
            '<td data-label="Handling & Manual Review Link"><small>' +
            esc(f.resolution) +
            ' · <a href="' +
            esc(f.sourceUrl) +
            '" target="_blank" rel="noopener">Inspect Source</a></small></td>' +
            "</tr>"
          );
        })
        .join("");
    }

    var raEl = document.getElementById("repo-audit-cards");
    if (raEl && d.repoAudit) {
      raEl.innerHTML = d.repoAudit.findings
        .map(function (r) {
          return (
            '<div class="info-card">' +
            '<p><span class="badge badge-selected">' +
            esc(r.id) +
            '</span> <span class="badge badge-warn">' +
            esc(r.status) +
            "</span></p>" +
            "<h3>" +
            esc(r.area) +
            "</h3>" +
            "<p>" +
            esc(r.detail) +
            "</p>" +
            "</div>"
          );
        })
        .join("");
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    var page = document.body.getAttribute("data-page") || "";
    var base = document.body.getAttribute("data-base") || "./";
    var p = Promise.resolve();
    if (page === "overview") p = initOverview(base);
    else if (page === "restaurants") p = initRestaurants(base);
    else if (page === "hotels") p = initHotels(base);
    else if (page === "activities") p = initActivities(base);
    else if (page === "decisions") p = initDecisions(base);
    else if (page === "flagged") p = initFlagged(base);

    p.catch(function (err) {
      console.error(err);
      var main = document.querySelector(".container");
      if (main) {
        var box = document.createElement("div");
        box.className = "alert-banner";
        box.textContent = "Data load error: " + err.message;
        main.prepend(box);
      }
    });
  });
})();
