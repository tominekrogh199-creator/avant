/* AVANT – magasin: lesefremdrift og stille videoloop som pauser utenfor skjermen. */
(function () {
  "use strict";
  var rolig = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Tynn lesefremdrift øverst
  var linje = document.querySelector(".lesefremdrift");
  if (linje) {
    var oppdater = function () {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      linje.style.transform = "scaleX(" + (h > 0 ? Math.min(1, window.scrollY / h) : 0) + ")";
    };
    oppdater();
    window.addEventListener("scroll", oppdater, { passive: true });
    window.addEventListener("resize", oppdater);
  }

  // Videoer: spill bare når de er synlige, og aldri ved redusert bevegelse
  var videoer = document.querySelectorAll("video[data-loop]");
  videoer.forEach(function (v) {
    v.muted = true; v.setAttribute("muted", ""); v.playsInline = true;
    if (rolig) { v.removeAttribute("autoplay"); v.pause(); v.controls = true; }
  });
  if (rolig || !("IntersectionObserver" in window)) return;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      var v = en.target;
      if (en.isIntersecting) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
      else v.pause();
    });
  }, { threshold: 0.25 });
  videoer.forEach(function (v) { io.observe(v); });
})();

/* Bilder toner rolig inn; tekst er alltid synlig. */
(function () {
  "use strict";
  var el = document.querySelectorAll(".bilde-inn");
  if (!("IntersectionObserver" in window)) { el.forEach(function (e) { e.classList.add("synlig"); }); return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("synlig"); io.unobserve(en.target); } });
  }, { rootMargin: "0px 0px -5% 0px", threshold: 0.02 });
  el.forEach(function (e) { io.observe(e); });
})();
