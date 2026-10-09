(function () {
  var KEY = "mc-consent", MAX = 180 * 864e5; // choix conservé 6 mois
  var cs = document.currentScript;
  var HOME = (cs && cs.getAttribute("data-home")) || "";
  var GA = (cs && cs.getAttribute("data-ga")) || "";

  function get() {
    try {
      var v = JSON.parse(localStorage.getItem(KEY));
      if (v && typeof v.a === "number" && typeof v.m === "number" && Date.now() - v.t < MAX) return v;
    } catch (e) {}
    return null;
  }
  function save(a, m) { try { localStorage.setItem(KEY, JSON.stringify({ a: a, m: m, t: Date.now() })); } catch (e) {} }

  // ---- contenus tiers (YouTube, Instagram)
  function load(el) {
    if (el.querySelector("iframe")) return;
    var f = document.createElement("iframe");
    f.src = el.getAttribute("data-embed");
    f.title = el.getAttribute("data-title") || "";
    f.loading = "lazy";
    f.allowFullscreen = true;
    f.referrerPolicy = "strict-origin-when-cross-origin";
    f.allow = "accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
    el.textContent = "";
    el.appendChild(f);
  }
  function loadMedia() { var n = document.querySelectorAll("[data-embed]"); for (var i = 0; i < n.length; i++) load(n[i]); }

  // ---- mesure d'audience (Google Analytics 4)
  function loadAnalytics() {
    if (!GA || window.__mcGA) return;
    window.__mcGA = true;
    window["ga-disable-" + GA] = false;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", GA, { allow_google_signals: false, allow_ad_personalization_signals: false, cookie_expires: 34128000 });
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(GA);
    document.head.appendChild(s);
  }
  function clearGaCookies() {
    var host = location.hostname, parts = host.split("."), roots = [host, "." + host];
    if (parts.length > 2) roots.push("." + parts.slice(-2).join("."));
    document.cookie.split(";").forEach(function (c) {
      var n = c.split("=")[0].trim();
      if (n.indexOf("_ga") === 0) roots.forEach(function (d) { document.cookie = n + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; domain=" + d; });
      if (n.indexOf("_ga") === 0) document.cookie = n + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";
    });
  }

  function apply(c) { if (c.m) loadMedia(); if (c.a) loadAnalytics(); }

  // ---- bandeau
  var banner;
  function hide() { if (banner && banner.parentNode) banner.parentNode.removeChild(banner); banner = null; }
  function choose(a, m) {
    var before = get();
    save(a, m); hide();
    if ((before && ((before.m && !m) || (before.a && !a)))) {
      if (before.a && !a) { window["ga-disable-" + GA] = true; clearGaCookies(); }
      location.reload(); return;
    }
    apply({ a: a, m: m });
  }
  function show() {
    if (banner) return;
    var cur = get() || { a: 0, m: 0 };
    banner = document.createElement("div");
    banner.id = "consent";
    banner.setAttribute("role", "dialog");
    banner.setAttribute("aria-labelledby", "consent-t");
    banner.innerHTML =
      '<h2 id="consent-t">Cookies et contenus tiers</h2>' +
      "<p>Ce site ne dépose aucun cookie publicitaire. Avec ton accord, il mesure son audience (Google Analytics) et affiche les vidéos YouTube et Instagram, des contenus tiers qui peuvent déposer des cookies. " +
      '<a href="' + HOME + "confidentialite/" + (location.protocol === "file:" ? "index.html" : "") + '">En savoir plus</a></p>' +
      '<div class="cfg" hidden>' +
      '<label><input type="checkbox" id="c-m"' + (cur.m ? " checked" : "") + '> Vidéos et contenus tiers (YouTube, Instagram)</label>' +
      '<label><input type="checkbox" id="c-a"' + (cur.a ? " checked" : "") + '> Mesure d’audience (Google Analytics)</label>' +
      '<button type="button" class="btn alt" data-c="save">Enregistrer mon choix</button></div>' +
      '<div class="row main"><button type="button" class="btn alt" data-c="none">Tout refuser</button>' +
      '<button type="button" class="btn alt" data-c="cfg">Personnaliser</button>' +
      '<button type="button" class="btn alt" data-c="all">Tout accepter</button></div>';
    document.body.appendChild(banner);
    banner.addEventListener("click", function (e) {
      var c = e.target && e.target.getAttribute && e.target.getAttribute("data-c");
      if (!c) return;
      if (c === "none") choose(0, 0);
      else if (c === "all") choose(1, 1);
      else if (c === "cfg") { var p = banner.querySelector(".cfg"); p.hidden = !p.hidden; }
      else if (c === "save") choose(banner.querySelector("#c-a").checked ? 1 : 0, banner.querySelector("#c-m").checked ? 1 : 0);
    });
  }

  document.addEventListener("click", function (e) {
    var t = e.target;
    if (!t || !t.closest) return;
    var o = t.closest("[data-consent-open]"); if (o) { e.preventDefault(); show(); return; }
    var b = t.closest(".ph-load"); if (b) { var box = b.closest("[data-embed]"); if (box) load(box); }
  });
  var c = get();
  if (c) apply(c); else show();
})();
