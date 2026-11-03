/* AVANT – felles skript: meny, header, animasjoner, sosiale lenker, kontaktskjema. */
(function () {
  "use strict";
  var cfg = window.AVANT_CONFIG || {};
  var topp = document.getElementById("topp");
  var knapp = topp && topp.querySelector(".meny-knapp");

  // Meny (mobil)
  function lukk() {
    topp.classList.remove("apen");
    knapp.setAttribute("aria-expanded", "false");
    knapp.setAttribute("aria-label", "Åpne meny");
    document.body.style.overflow = "";
  }
  if (knapp) {
    knapp.addEventListener("click", function () {
      var apen = topp.classList.toggle("apen");
      knapp.setAttribute("aria-expanded", String(apen));
      knapp.setAttribute("aria-label", apen ? "Lukk meny" : "Åpne meny");
      document.body.style.overflow = apen ? "hidden" : "";
    });
    topp.querySelectorAll(".meny a").forEach(function (a) { a.addEventListener("click", lukk); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && topp.classList.contains("apen")) { lukk(); knapp.focus(); } });
  }

  // Header får bakgrunn ved scroll
  function sjekkScroll() { if (topp) topp.classList.toggle("scrollet", window.scrollY > 40); }
  sjekkScroll();
  window.addEventListener("scroll", sjekkScroll, { passive: true });

  // Rolige inntredener
  window.avantVis = function (root) {
    var el = (root || document).querySelectorAll(".vis:not(.synlig)");
    if (!("IntersectionObserver" in window)) { el.forEach(function (e) { e.classList.add("synlig"); }); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("synlig"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });
    el.forEach(function (e) { io.observe(e); });
  };
  window.avantVis();

  // Sosiale lenker: lenkene står i HTML-en; config.js kan overstyre URL-en
  document.querySelectorAll("a[data-sosial]").forEach(function (a) {
    var url = (cfg[a.getAttribute("data-sosial")] || "").trim();
    if (url) a.href = url;
    a.target = "_blank"; a.rel = "noopener";
  });

  // Kontaktskjema -> mailto
  var skjema = document.getElementById("kontaktskjema");
  if (skjema) {
    var status = document.getElementById("skjema-status");
    skjema.addEventListener("submit", function (e) {
      e.preventDefault();
      var f = skjema.elements;
      var navn = f.navn.value.trim(), epost = f.epost.value.trim(), merke = f.merke.value.trim(), melding = f.melding.value.trim();
      if (!navn || !epost || !melding) { status.textContent = "Fyll inn navn, e-post og melding."; (!navn ? f.navn : !epost ? f.epost : f.melding).focus(); return; }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(epost)) { status.textContent = "Sjekk at e-postadressen er riktig."; f.epost.focus(); return; }
      var emne = "Henvendelse til AVANT" + (merke ? " – " + merke : "") + " – " + navn;
      var tekst = "Hei AVANT!\n\n" + melding + "\n\n—\nNavn: " + navn + "\nE-post: " + epost + (merke ? "\nMerke / Instagram: " + merke : "") + "\n";
      var til = cfg.epost || "Tominekrogh199@gmail.com";
      status.textContent = "Åpner e-postprogrammet ditt … Skjer ingenting? Send til " + til + ".";
      window.location.href = "mailto:" + til + "?subject=" + encodeURIComponent(emne) + "&body=" + encodeURIComponent(tekst);
    });
  }
})();
