(function () {
  var KEY = "mc-consent", MAX = 180 * 864e5; // choix conservé 6 mois
  function get() {
    try { var v = JSON.parse(localStorage.getItem(KEY)); if (v && (v.v === "all" || v.v === "none") && Date.now() - v.t < MAX) return v.v; } catch (e) {}
    return null;
  }
  function set(v) { try { localStorage.setItem(KEY, JSON.stringify({ v: v, t: Date.now() })); } catch (e) {} }
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
  function loadAll() { var n = document.querySelectorAll("[data-embed]"); for (var i = 0; i < n.length; i++) load(n[i]); }
  var banner;
  function hide() { if (banner && banner.parentNode) banner.parentNode.removeChild(banner); banner = null; }
  function show(home) {
    if (banner) return;
    banner = document.createElement("div");
    banner.id = "consent";
    banner.setAttribute("role", "dialog");
    banner.setAttribute("aria-labelledby", "consent-t");
    banner.innerHTML =
      '<h2 id="consent-t">Cookies et contenus tiers</h2>' +
      "<p>Ce site ne dépose pas de cookie publicitaire et ne mesure pas ton audience. Les vidéos YouTube et Instagram sont des contenus tiers : ces services peuvent déposer des cookies et collecter ton adresse IP. Elles ne se chargent que si tu l’acceptes. " +
      '<a href="' + home + 'confidentialite/' + (location.protocol === "file:" ? "index.html" : "") + '">En savoir plus</a></p>' +
      '<div class="row"><button type="button" class="btn alt" data-c="none">Tout refuser</button><button type="button" class="btn alt" data-c="all">Tout accepter</button></div>';
    document.body.appendChild(banner);
    banner.addEventListener("click", function (e) {
      var c = e.target && e.target.getAttribute && e.target.getAttribute("data-c");
      if (!c) return;
      var before = get();
      set(c); hide();
      if (c === "all") loadAll();
      else if (before === "all") location.reload();
    });
  }
  var home = document.currentScript ? (document.currentScript.getAttribute("data-home") || "") : "";
  document.addEventListener("click", function (e) {
    var t = e.target;
    if (t && t.closest) {
      var o = t.closest("[data-consent-open]"); if (o) { e.preventDefault(); show(home); return; }
      var b = t.closest(".ph-load"); if (b) { var box = b.closest("[data-embed]"); if (box) load(box); }
    }
  });
  var c = get();
  if (c === "all") loadAll();
  if (c === null) show(home);
})();
