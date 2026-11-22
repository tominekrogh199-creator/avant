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

  // Contact: validate each field, then open a draft in the user's mail app.
  var skjema = document.getElementById("kontaktskjema");
  if (skjema) {
    skjema.noValidate = true;
    var status = document.getElementById("skjema-status");
    var requiredFields = [skjema.elements.navn, skjema.elements.epost, skjema.elements.melding];
    function validateField(field) {
      var value = field.value.trim();
      var message = "";
      if (!value) message = {navn:"Skriv navnet ditt.", epost:"Skriv e-postadressen din.", melding:"Skriv en melding."}[field.name];
      else if (field.name === "epost" && (field.validity.typeMismatch || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value))) message = "Skriv en gyldig e-postadresse, for eksempel navn@eksempel.no.";
      var error = document.getElementById(field.id + "-error");
      if (message) field.setAttribute("aria-invalid", "true"); else field.removeAttribute("aria-invalid");
      error.textContent = message; error.hidden = !message;
      return !message;
    }
    requiredFields.forEach(function (field) {
      field.addEventListener("input", function () {
        if (field.hasAttribute("aria-invalid")) validateField(field);
        status.textContent = "";
      });
    });
    skjema.addEventListener("submit", function (e) {
      e.preventDefault();
      var invalid = requiredFields.filter(function (field) { return !validateField(field); });
      if (invalid.length) {
        status.textContent = invalid.length === 1 ? "Rett det markerte feltet." : "Fyll ut de markerte feltene.";
        invalid[0].focus(); return;
      }
      var f = skjema.elements;
      var navn=f.navn.value.trim(), epost=f.epost.value.trim(), merke=f.merke.value.trim(), melding=f.melding.value.trim();
      var emne="Henvendelse til AVANT"+(merke ? " – "+merke : "")+" – "+navn;
      var tekst="Hei AVANT!\n\n"+melding+"\n\n—\nNavn: "+navn+"\nE-post: "+epost+(merke ? "\nMerke / Instagram: "+merke : "")+"\n";
      var til=cfg.epost || "Tominekrogh199@gmail.com";
      status.textContent="Åpner et utkast i e-postprogrammet ditt. Du sender det selv derfra. Skjer ingenting? Send direkte til "+til+".";
      window.location.href="mailto:"+til+"?subject="+encodeURIComponent(emne)+"&body="+encodeURIComponent(tekst);
    });
  }
})();
