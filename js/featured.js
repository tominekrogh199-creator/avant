/*
 * Featured Edit – leser featured.json og lager ett kort per plagg.
 * Hvert kort får id = plaggets "id", så lenken blir featured.html#<id>.
 * Nytt plagg? Se README.md → «Slik legger du til et nytt plagg».
 */
(function () {
  "use strict";
  var rutenett = document.getElementById("rutenett");
  var base = location.href.split("#")[0];

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function trygUrl(u) { return /^(https?:|mailto:|index\.html|featured\.html|#)/i.test(u || "") ? u : ""; }
  function lenke(url, tekst, ekstern) {
    url = trygUrl(url); if (!url) return "";
    return '<a class="lenke" href="' + esc(url) + '"' + (ekstern ? ' target="_blank" rel="noopener"' : "") + ">" + esc(tekst) + ' <span class="pil" aria-hidden="true">→</span></a>';
  }

  function kort(p, i) {
    var id = esc(p.id || "plagg-" + (i + 1));
    var nr = String(i + 1).padStart(2, "0");
    var visuelt;
    if (p.bilde) {
      visuelt = '<div class="bilde-ramme kort__bilde">' + (p.plassholder ? '<span class="merkelapp smaa">Kommer snart</span>' : "") +
        '<img src="' + esc(p.bilde) + '" alt="' + esc(p.bildeAlt || p.plagg || "") + '" loading="lazy" decoding="async" width="800" height="1000"></div>';
    } else {
      var v = p.flate === "sand" ? " kort__flate--sand" : p.flate === "burgunder" ? " kort__flate--burgunder" : "";
      visuelt = '<div class="kort__flate' + v + '"><span class="smaa">' + esc(p.utgave || "Featured Edit") + '</span><span class="stor">' + (p.flatetekst ? esc(p.flatetekst).replace(/\*(.+?)\*/g, "<em>$1</em>") : "AVANT") + '</span><span class="smaa">Nr. ' + nr + "</span></div>";
    }
    var lenker = [];
    if (p.plassholder) {
      lenker.push(lenke(p.ctaUrl || "index.html#kontakt", p.ctaTekst || "Er du designer? Ta kontakt"));
    } else {
      lenker.push(lenke(p.merkeNettside, "Merkets nettside", true));
      lenker.push(lenke(p.merkeInstagram, "Merket på Instagram", true));
      lenker.push(lenke(p.innleggInstagram, "Se innlegget på Instagram", true));
      lenker.push(lenke(p.innleggTiktok, "Se videoen på TikTok", true));
      lenker.push('<button type="button" class="lenke kopier" data-id="' + id + '">Kopier lenke</button>');
    }
    return '<article class="kort vis" id="' + id + '">' + visuelt +
      '<div class="kort__meta smaa"><span>' + esc(p.utgave || "") + "</span><span>Nr. " + nr + "</span></div>" +
      "<h3>" + esc(p.plagg) + "</h3>" +
      (p.merke ? '<p class="kort__merke">' + esc(p.merke) + (p.skaper ? " · stylet av " + esc(p.skaper) : "") + "</p>" : "") +
      (p.tekst ? '<p class="kort__tekst">' + esc(p.tekst) + "</p>" : "") +
      '<div class="kort__lenker">' + lenker.join("") + "</div></article>";
  }

  function fremhev() {
    var id = decodeURIComponent(location.hash.slice(1));
    document.querySelectorAll(".kort.fremhevet").forEach(function (k) { k.classList.remove("fremhevet"); });
    if (!id) return;
    var el = document.getElementById(id);
    if (el && el.classList.contains("kort")) {
      el.classList.add("fremhevet", "synlig");
      el.scrollIntoView({ block: "start" });
    }
  }

  fetch("featured.json", { cache: "no-cache" })
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (data) {
      var plagg = (data.plagg || []).filter(function (p) { return p && p.vis !== false; });
      if (data.utgave) { var u = document.getElementById("utgave-tekst"); if (u) u.textContent = data.utgave; }
      rutenett.innerHTML = plagg.length ? plagg.map(kort).join("") : '<p class="laster">Første utgave kommer snart.</p>';
      window.avantVis && window.avantVis(rutenett);
      fremhev();
    })
    .catch(function () {
      rutenett.innerHTML = '<p class="feilmelding">Kunne ikke laste plaggene akkurat nå. Prøv å laste siden på nytt.</p>';
    });

  window.addEventListener("hashchange", fremhev);

  rutenett.addEventListener("click", function (e) {
    var b = e.target.closest(".kopier"); if (!b) return;
    var url = base + "#" + b.getAttribute("data-id");
    var ok = function () { b.textContent = "Lenke kopiert"; setTimeout(function () { b.textContent = "Kopier lenke"; }, 2000); };
    if (navigator.clipboard) navigator.clipboard.writeText(url).then(ok, function () { prompt("Kopier lenken:", url); });
    else prompt("Kopier lenken:", url);
  });
})();
