import json, os, re, sys, shutil, html

OUT = sys.argv[1]            # dossier de sortie
LOCAL = sys.argv[2] == "local"   # liens en index.html pour ouvrir sans serveur
READY = False                # passer à True quand les 4 chroniques sont complètes
BASE = "https://www.chatellier.fr"
SUBSTACK = "https://monsieurchatellier.substack.com"
YT = "https://www.youtube.com/@GaelChatellier"
IG = "https://www.instagram.com/monsieurchatellier/"
LI = "https://www.linkedin.com/in/gaelchatellier/"
TODAY = "2026-10-06"
GA_ID = "G-0XRCHZ5LZZ"
YT_ID = "HKUi054TpNc"
YT_TITLE = "Le VTTAE c’est pour les feignants ?"
YT_DESC = "Vlog sur une randonnée VTTAE (les vrais disent VTT élec !) en plein hiver près de Brioude en Haute-Loire (le Bled ou La Comté pour Monsieur Châtellier)."
IG_REELS = ["DYwcu7iMwvE", "DZGGgLEv0Cl"]
GEN = os.path.dirname(os.path.abspath(__file__))

CHRONIQUES = [
    dict(slug="mon-chien-ce-hpi", title="Mon chien, ce HPI",
         excerpt=["Que ceux qui ont résisté me jettent la première balle. J’en connais même qui, dans ma situation, ont fait signer des contrats à leurs enfants. Alors hein, bon. Il a envie d’être tranquille. Je le connais maintenant. Dès qu’il me tourne le dos pour commencer à taper sur son clavier en m’ignorant, c’est le signe qu’il veut travailler ou que sais-je. Je vais lui laisser quelques minutes parce que je ne suis pas un monstre… Voilà, c’est bon, il a eu le temps nécessaire pour faire ses trucs.",
                  "[…]",
                  "Je commence à gémir doucement. Très doucement. Il ne faut pas le brusquer, je le connais maintenant : s’il se braque, il peut aller jusqu’à me dire non. Il m’a entendue, ses épaules viennent de se crisper. Le pauvre, il connaît la suite. Pourtant, il ne se retourne pas et continue son activité. Le ballet commence.",
                  "J’augmente un peu le volume de mon deuxième gémissement, et, là, sa tête s’affaisse, il ne va pas pouvoir y échapper. Mais il résiste encore, alors je lui assène un troisième crissement de craie sur le tableau noir de sa tranquillité. Il pivote sur sa chaise et me dit en prenant sa grosse voix : « Stop ! », en détachant bien les lettres comme si je pouvais lire sur ses lèvres. Je lui retourne son regard en activant le mode « Mon Maître à Moi », mes deux « adorables petites billes rondes » — je les ai entendus dire ça un jour — vrillées dans ses yeux. Suppliante. Marie aux pieds des soldats romains n’aurait pas fait mieux. Il dit : « Tu exagères vraiment là, on vient juste de sortir. » Oui, mais j’ai de nouveau envie de prendre l’air, c’est comme ça. Il tente un dernier coup de dés, met ses écouteurs et bondit sur son clavier, ses doigts virevoltant sur les touches pour faire apparaître des mots sur l’écran. Bien joué, mais je ne me laisse pas faire, c’est l’heure du coup de grâce. Je m’approche de lui, je m’assois à ses pieds, dans son champ de vision basse, sur sa gauche et, là, je porte l’estocade : je tapote sa cuisse avec ma patte et je lui fais ma meilleure imitation du chat dans Shrek. Sans surprise, mais ce n’est jamais lassant, il capitule, se lève, enfile ses baskets et attrape la laisse pour me sortir ; il n’a pas les armes pour se battre.",
                  "Y’a pas à dire, ces chats ils en connaissent un beau morceau en matière de manipulation de nos humains. Moi je n’ai pas fréquenté leurs écoles Montesouris, mais je ne suis pas en reste quand il faut les faire marcher."],
         alt="Dessin de Gilles Rapaport : Monsieur Châtellier, casquette jaune, à quatre pattes et tenu en laisse par un petit chien, bulle « Je sors avec une HPI. »", complete=True),
    dict(slug="club-memories", title="Club Memories",
         excerpt=["Alors que certains se lancent dans l’établissement de listes des meilleurs films de leur vie, des albums de référence de progressive rock islandais voire des meilleurs crêperies de Concarneau, j’ai de mon côté décidé d’établir un classement des discothèques qui ont marqué ces quelques dizaines d’années de ma vie terrestre.",
                  "J’aimerais vous écrire que la boîte idéale, celle dont je me souviendrai toute ma vie, celle dont je ressens encore les basses résonner jusque dans mes os, l’odeur du tabac couvrant celle de la sueur des usagers en transe sur les tubes de ma jeunesse, c’est évidemment Le Repaire. Oui, à Brioude, là-bas dans La Comté, le pays des gentils hobbits certes mais surtout des altiligériens à l’accent chantant dont les pieds sont bien moins larges et poilus alors qu’ils sont tout aussi gentils. Le Repaire, cette discothèque perchée comme une boîte à musique ou un petit château de conte de fées, à deux kilomètres à vol d’oiseau du café Le Saint-Laurent, dit « Le Saint-Lau », où nous nous échauffions à coup de monacos avant que de partir y danser. Un haut lieu donc, c’est amusant les mots, que je fréquentais assidûment à la fin des années 1980 et dans lequel j’officiai même un été comme DJ. C’est une autre histoire que j’ai déjà racontée, fidèle lecteur·rice. Mais non, ce n’est pas l’heureuse élue de mon panthéon des salles de danse de ma prime jeunesse."],
         alt="Dessin de Gilles Rapaport : Monsieur Châtellier, casquette jaune, bras écartés comme en plein vol, légende « Brioude libre… »", complete=True),
    dict(slug="vive-la-colo", title="Vive la colo !",
         excerpt=["Lâcher prise, s’abandonner, se laisser aller. C’est un défi de tous les jours par les temps qui courent. « C’est plus facile à dire qu’à faire, ma bonne dame ! », comme disait ma bouchère quand je mangeais encore de la viande, et que la susdite bouchère n’avait pas ses binocles ce qui explique qu’elle m’ait mégenré.",
                  "Je m’égare, revenons à nos moutons.",
                  "C’est d’ailleurs pour moi une des façons de pratiquer la pleine inconscience, cette méditation dont je revendique la paternité, que de les compter quand je suis en position allongée : d’aucuns qualifient cela de « sieste » ; moi, une pause bien méritée.",
                  "Au fil des ans, j’ai exploré toutes les positions, toutes les astuces, tous les lieux (sous un bureau, dans un parking à la pause dej’, sous un pommier dans un pré… faites votre choix), pour parfaire l’exercice dont je me suis autoproclamé l’un des experts mondiaux."],
         alt="Dessin de Gilles Rapaport : Monsieur Châtellier, casquette jaune, allongé sur une table d’examen médical, un médecin en bleu accroupi à ses pieds, bulle « Je ne suis pas Rapoport ! », écran IPA en arrière-plan", complete=True),
]

def esc(s): return html.escape(s, quote=True)

def short(t, n):
    if len(t) <= n: return t
    return t[:n].rsplit(" ", 1)[0].rstrip(" ,;:.") + "…"

def href(depth, path):
    """lien interne relatif ; path='' = accueil, 'chroniques/' etc."""
    pre = "../" * depth
    if LOCAL and (path == "" or path.endswith("/")):
        path += "index.html"
    return (pre + path) or "./"

RAP_URL = "https://dessins-rapaport.com/"
RAP_LINK = '<a href="%s" target="_blank" rel="noopener">Gilles Rapaport</a>' % RAP_URL

def link_rapaport(html_text):
    """Remplace « Gilles Rapaport » par un lien dans le texte visible : jamais dans une balise (alt...), un lien déjà présent ou un script."""
    out, in_a, in_script = [], 0, False
    for part in re.split(r"(<[^>]+>)", html_text):
        if part.startswith("<"):
            low = part.lower()
            if low.startswith("<a ") or low == "<a>": in_a += 1
            elif low.startswith("</a"): in_a = max(0, in_a - 1)
            elif low.startswith("<script") or low.startswith("<style") or low.startswith("<title"): in_script = True
            elif low.startswith("</script") or low.startswith("</style") or low.startswith("</title"): in_script = False
            out.append(part)
        else:
            out.append(part if (in_a or in_script) else part.replace("Gilles Rapaport", RAP_LINK))
    return "".join(out)

PERSON = {
    "@type": "Person", "@id": BASE + "/#gael",
    "name": "Gaël Châtellier", "alternateName": "Monsieur Châtellier",
    "url": BASE + "/", "image": BASE + "/assets/portrait.jpg",
    "description": "Gaël Châtellier, auteur sous le nom de Monsieur Châtellier : chroniques OK Boomer (newsletter), vlogs et vidéos.",
    "sameAs": [SUBSTACK, YT, IG, LI],
}

def page(depth, path, title, desc, body, schema, robots_index=True, image="assets/portrait.jpg"):
    canon = BASE + "/" + path
    pre = "../" * depth
    robots = "index, follow, max-image-preview:large" if robots_index else "noindex, follow"
    ld = "".join('<script type="application/ld+json">%s</script>\n' % json.dumps(s, ensure_ascii=False) for s in schema)
    items = [(href(depth, "chroniques/"), "Lire"), (href(depth, "") + "#regarder", "Regarder"),
             (href(depth, "") + "#livre", "Le livre"), (href(depth, "a-propos/"), "À propos")]
    nav = "".join('<a href="%s">%s</a>' % (u, l) for u, l in items)
    return """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(canon)s">
<meta name="robots" content="%(robots)s">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Monsieur Châtellier">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(canon)s">
<meta property="og:image" content="%(base)s/%(image)s">
<meta name="twitter:card" content="summary_large_image">
<link rel="alternate" type="application/rss+xml" title="Les chroniques OK Boomer (Substack)" href="%(ss)s/feed">
<link rel="icon" href="%(pre)sfavicon.ico" sizes="16x16 32x32 48x48">
<link rel="icon" type="image/png" sizes="32x32" href="%(pre)sfavicon-32.png">
<link rel="apple-touch-icon" href="%(pre)sapple-touch-icon.png">
<link rel="manifest" href="%(pre)ssite.webmanifest">
<meta name="theme-color" content="#efeadf">
<link rel="preload" href="%(pre)sassets/fonts/bebas-neue-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%(pre)sassets/fonts.css">
<link rel="stylesheet" href="%(pre)sassets/style.css">
%(ld)s</head>
<body>
<a class="skip" href="#main">Aller au contenu</a>
<header><div class="wrap">
  <a class="brand" href="%(home)s"><span>Monsieur</span> Châtellier</a>
  <nav aria-label="Navigation principale">%(nav)s</nav>
</div></header>
<main id="main">
%(body)s
</main>
<footer id="contact"><div class="wrap">
  <a class="brand" href="%(home)s">Monsieur Châtellier</a>
  <div><a href="mailto:gael@chatellier.fr">gael@chatellier.fr</a> ·
    <a href="%(yt)s" rel="me noopener" target="_blank">YouTube</a> ·
    <a href="%(ig)s" rel="me noopener" target="_blank">Instagram</a> ·
    <a href="%(ss)s" rel="me noopener" target="_blank">Newsletter</a></div>
  <p class="pro">Et aussi, dans la vraie vie, directeur de projets digitaux → <a href="%(li)s" rel="me noopener" target="_blank">mon profil LinkedIn</a></p>
  <p class="legal"><a href="%(priv)s">Confidentialité et cookies</a> · <button type="button" class="linkbtn" data-consent-open>Gérer mes cookies</button></p>
</div></footer>
<script src="%(pre)sassets/consent.js" data-home="%(pre)s" data-ga="%(ga)s" defer></script>
</body>
</html>
""" % dict(title=esc(title), desc=esc(desc), canon=canon, robots=robots, base=BASE, image=image, ss=SUBSTACK, pre=pre, ld=ld,
           home=href(depth, ""), nav=nav, body=link_rapaport(body), yt=YT, ig=IG, li=LI, priv=href(depth, "confidentialite/"), ga=GA_ID)

def signup(label="Recevez les chroniques OK Boomer", anchor=False):
    # Inscription gratuite directe : le formulaire envoie l'adresse à Substack (même requête que leur formulaire intégré),
    # sans passer par la page de soutien payant. Rien n'est chargé chez Substack avant l'envoi.
    return """<form class="signup"%(idattr)s action="%(ss)s/api/v1/free?nojs=true" method="post" target="_blank" rel="noopener">
  <label for="mail">%(label)s</label>
  <div class="row"><input id="mail" name="email" type="email" placeholder="votre@email.fr" autocomplete="email" required>
  <input type="hidden" name="first_url" value="%(base)s/"><input type="hidden" name="first_referrer" value="">
  <input type="hidden" name="current_url" value="%(base)s/"><input type="hidden" name="current_referrer" value="">
  <input type="hidden" name="referral_code" value=""><input type="hidden" name="source" value="embed">
  <button class="btn" type="submit">Je m'abonne</button></div>
  <small>Newsletter gratuite. Un e-mail de confirmation vous est envoyé par Substack.</small>
</form>""" % dict(ss=SUBSTACK, label=label, base=BASE, idattr=' id="abonnement"' if anchor else "")

def ph(provider, url, label, what):
    return ('<div class="ph"><p><strong>Contenu %s</strong><br>Ce contenu est hébergé par %s, qui peut déposer des cookies. Il se charge si vous l’autorisez.</p>'
            '<div class="phr"><button type="button" class="btn alt ph-load">Charger %s</button>'
            '<a href="%s" target="_blank" rel="noopener">%s</a></div></div>') % (provider.split(" ")[0], provider, what, url, label)

def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)

def crumbs(items):
    """items: [(nom, url_absolue)] -> BreadcrumbList"""
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}

# ---------- assets
os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
css = open(os.path.join(GEN, "zine.css"), encoding="utf-8").read() + open(os.path.join(GEN, "extra.css"), encoding="utf-8").read()
write("assets/style.css", css)
shutil.copy(os.path.join(GEN, "consent.js"), os.path.join(OUT, "assets/consent.js"))
shutil.copy(os.path.join(GEN, "fonts.css"), os.path.join(OUT, "assets/fonts.css"))
shutil.copytree(os.path.join(GEN, "fonts"), os.path.join(OUT, "assets/fonts"))
shutil.copy(os.path.join(GEN, "portrait.jpg"), os.path.join(OUT, "assets/portrait.jpg"))
shutil.copy(os.path.join(GEN, "apropos.jpg"), os.path.join(OUT, "assets/apropos.jpg"))
for _f in ("favicon.ico", "favicon-32.png", "apple-touch-icon.png", "icon-192.png", "icon-512.png", "site.webmanifest"):
    shutil.copy(os.path.join(GEN, _f), os.path.join(OUT, _f))
for _c in CHRONIQUES:
    shutil.copy(os.path.join(GEN, _c["slug"] + ".jpg"), os.path.join(OUT, "assets/%s.jpg" % _c["slug"]))

# ---------- accueil
def card_html(c):
    exc = short(c["excerpt"][0], 190) if c["excerpt"] else "Extrait à venir."
    return """<article class="card">
  <a class="img" href="%s" tabindex="-1" aria-hidden="true"><img src="assets/%s.jpg" width="1000" height="1000" loading="lazy" alt=""></a>
  <div class="body"><h3><a href="%s">%s</a></h3><p>%s</p>
  <a class="more" href="%s">Lire l'extrait →</a></div></article>
""" % (href(0, "chroniques/%s/" % c["slug"]), c["slug"], href(0, "chroniques/%s/" % c["slug"]), esc(c["title"]), esc(exc), href(0, "chroniques/%s/" % c["slug"]))

cards = "".join(card_html(c) for c in CHRONIQUES[:3])
cards_all = "".join(card_html(c) for c in CHRONIQUES)

home_body = """<div class="wrap">
<section class="hero" aria-labelledby="h1">
  <div class="photo"><i class="tape"></i><img src="assets/portrait.jpg" width="1275" height="1768" fetchpriority="high" alt="Portrait de Monsieur Châtellier, cheveux gris et barbe blanche, en noir et blanc"></div>
  <div>
    <span class="kicker">Né sous Pompidou · Toujours sur sa planche</span>
    <h1 id="h1">Monsieur Châtellier, plus jeune <em>boomer</em> de France</h1>
    <p class="lead">Monsieur Châtellier est un personnage né sous Pompidou, élevé sous Giscard, propulsé par Mitterrand et mentoré par le grand Jacques. Auteur des chroniques OK Boomer depuis 2019, il publie aussi des vlogs et prépare un livre.</p>
    <p class="baseline">Ubercool skater · Autobiographe · Humain</p>
    %s
  </div>
</section>
<div class="doors">
  <a class="door" href="%s"><span class="n">01</span><h2><span>Lire</span></h2><p>Les chroniques OK Boomer, illustrées par Gilles Rapaport.</p></a>
  <a class="door" href="#regarder"><span class="n">02</span><h2><span>Regarder</span></h2><p>Vlogs sur YouTube, vidéos sur Instagram.</p></a>
  <a class="door" href="#livre"><span class="sticker">Bientôt</span><span class="n">03</span><h2><span>Le livre</span></h2><p>Le recueil des chroniques OK Boomer.</p></a>
</div>
<section class="block" id="chroniques" aria-labelledby="h-chro">
  <div class="sec-head"><h2 id="h-chro">Chroniques OK Boomer</h2>
  <p>Des capsules humoristiques envoyées par e-mail : de petites pièces sur le temps qui a passé, illustrées par Gilles Rapaport.</p></div>
  <div class="chroniques">%s</div>
  <p class="mt"><a class="btn" href="%s">Toutes les chroniques</a></p>
</section>
<section class="block" id="regarder" aria-labelledby="h-vid">
  <div class="sec-head"><h2 id="h-vid">Regarder</h2><p>Vlogs sur YouTube, vidéos courtes sur Instagram.</p></div>
  <div class="videos">
    <figure class="vmain">
      <div class="frame frame16" data-embed="https://www.youtube-nocookie.com/embed/%s" data-title="%s">%s</div>
      <figcaption><h3>%s</h3><p>%s</p></figcaption>
    </figure>
    <div class="frame frameig" data-embed="https://www.instagram.com/reel/%s/embed" data-title="Reel Instagram de Monsieur Châtellier">%s</div>
    <div class="frame frameig" data-embed="https://www.instagram.com/reel/%s/embed" data-title="Reel Instagram de Monsieur Châtellier">%s</div>
  </div>
  <p class="mt links"><a class="btn alt" href="%s" target="_blank" rel="noopener">YouTube</a><a class="btn alt" href="%s" target="_blank" rel="noopener">Instagram</a></p>
</section>
<section class="block" id="livre" aria-labelledby="h-livre">
  <div class="book">
    <div class="cover" aria-hidden="true"><span>Monsieur Châtellier</span><h3>OK Boomer</h3><span>Le recueil · illustrations de Gilles&nbsp;Rapaport</span></div>
    <div><h2 id="h-livre">Le livre arrive</h2>
    <p class="wide">Les chroniques OK Boomer seront réunies dans un recueil, avec les dessins de Gilles Rapaport. Abonnez-vous à la newsletter pour être prévenue de la sortie.</p>
    <a class="btn" href="#abonnement">Me prévenir de la sortie</a></div>
  </div>
</section>
</div>""" % (signup(anchor=True), href(0, "chroniques/"), cards, href(0, "chroniques/"), YT_ID, esc(YT_TITLE), ph("YouTube (Google)", "https://www.youtube.com/watch?v=" + YT_ID, "Regarder sur YouTube", "la vidéo"), esc(YT_TITLE), esc(YT_DESC), IG_REELS[0], ph("Instagram (Meta)", "https://www.instagram.com/reel/" + IG_REELS[0] + "/", "Voir sur Instagram", "le reel"), IG_REELS[1], ph("Instagram (Meta)", "https://www.instagram.com/reel/" + IG_REELS[1] + "/", "Voir sur Instagram", "le reel"), YT, IG)

home_schema = [
    {"@context": "https://schema.org", "@type": "WebSite", "@id": BASE + "/#site", "url": BASE + "/", "name": "Monsieur Châtellier",
     "inLanguage": "fr-FR", "publisher": {"@id": BASE + "/#gael"}},
    dict(PERSON, **{"@context": "https://schema.org"}),
    {"@context": "https://schema.org", "@type": "VideoObject", "name": YT_TITLE, "description": YT_DESC,
     "thumbnailUrl": "https://i.ytimg.com/vi/%s/hqdefault.jpg" % YT_ID, "embedUrl": "https://www.youtube.com/embed/%s" % YT_ID,
     "contentUrl": "https://www.youtube.com/watch?v=%s" % YT_ID, "inLanguage": "fr-FR", "author": {"@id": BASE + "/#gael"}},
]
write("index.html", page(0, "", "Monsieur Châtellier — Chroniques OK Boomer, vlogs et livre",
      "Monsieur Châtellier, plus jeune boomer de France : chroniques OK Boomer illustrées par Gilles Rapaport (newsletter), vlogs YouTube, vidéos Instagram et recueil à venir.",
      home_body, home_schema))

# ---------- liste des chroniques
list_cards = cards_all.replace('src="assets/', 'src="../assets/')
list_body = """<div class="wrap article-wrap">
<nav class="crumbs" aria-label="Fil d'Ariane"><a href="%s">Accueil</a> › Chroniques OK Boomer</nav>
<h1>Chroniques OK Boomer</h1>
<p class="lead">Les chroniques OK Boomer sont des capsules humoristiques de Monsieur Châtellier, envoyées par e-mail depuis 2019. Ce sont de petites pièces sur le temps qui a passé, souvenirs d'autres époques qui ont forgé son humanité (et la vôtre ?). Elles sont illustrées par Gilles Rapaport, illustrateur et dessinateur de presse.</p>
<div class="chroniques mt">%s</div>
<div class="mt">%s</div>
</div>""" % (href(1, ""), list_cards.replace('href="chroniques/', 'href="').replace(href(0, "chroniques/"), "./"), signup("Lire les chroniques en entier, dans votre boîte mail"))
# liens relatifs depuis /chroniques/
list_body = list_body.replace('href="%s' % href(0, "chroniques/"), 'href="')
lst = []
for c in CHRONIQUES:
    lst.append({"@type": "ListItem", "position": len(lst) + 1, "url": BASE + "/chroniques/%s/" % c["slug"], "name": c["title"]})
write("chroniques/index.html", page(1, "chroniques/", "Chroniques OK Boomer — Monsieur Châtellier",
      "Toutes les chroniques OK Boomer de Monsieur Châtellier : capsules humoristiques envoyées par e-mail depuis 2019, illustrées par Gilles Rapaport.",
      list_body.replace('class="more" href="chroniques/', 'class="more" href="'), [
      {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Chroniques OK Boomer", "url": BASE + "/chroniques/",
       "inLanguage": "fr-FR", "author": {"@id": BASE + "/#gael"}, "mainEntity": {"@type": "ItemList", "itemListElement": lst}},
      crumbs([("Accueil", BASE + "/"), ("Chroniques OK Boomer", BASE + "/chroniques/")]), dict(PERSON, **{"@context": "https://schema.org"})],
      robots_index=sum(c["complete"] for c in CHRONIQUES) >= 3))

# ---------- pages chroniques
for c in CHRONIQUES:
    url = BASE + "/chroniques/%s/" % c["slug"]
    others = "".join('<li><a href="%s">%s</a></li>' % (href(2, "chroniques/%s/" % o["slug"]), esc(o["title"])) for o in CHRONIQUES if o is not c)
    paras = "".join('<p class="gap">%s</p>' % esc(p) if p == "[…]" else "<p>%s</p>" % esc(p) for p in c["excerpt"]) or '<p class="todo">[ Extrait à ajouter ]</p>'
    todo = "" if c["complete"] else '<p class="todo">[ Extrait étendu de 300 à 500 mots à coller ici, puis un résumé en une phrase au-dessus ]</p>'
    desc = short(c["excerpt"][0], 155) if c["excerpt"] else "Chronique OK Boomer de Monsieur Châtellier."
    body = """<div class="wrap article-wrap">
<nav class="crumbs" aria-label="Fil d'Ariane"><a href="%s">Accueil</a> › <a href="%s">Chroniques OK Boomer</a> › %s</nav>
<article>
<h1>%s</h1>
<p class="meta">Chronique OK Boomer de Monsieur Châtellier · illustrée par Gilles Rapaport</p>
<figure class="illus"><img src="%sassets/%s.jpg" width="1000" height="1000" fetchpriority="high" alt="%s"><figcaption>Illustration : Gilles Rapaport</figcaption></figure>
<h2>Extrait</h2>
<blockquote>%s</blockquote>
%s
<div class="cta"><h2>La suite dans la newsletter</h2>
<p>Cette chronique est publiée en entier dans la newsletter de Monsieur Châtellier, avec l'illustration complète.</p>
%s
<p class="mt"><a class="btn alt" href="%s" target="_blank" rel="noopener">Lire sur Substack</a></p></div>
</article>
<aside class="others"><h2>Autres chroniques</h2><ul>%s</ul></aside>
</div>""" % (href(2, ""), href(2, "chroniques/"), esc(c["title"]), esc(c["title"]), "../../", c["slug"], esc(c["alt"]), paras, todo, signup(), SUBSTACK, others)
    art = {"@context": "https://schema.org", "@type": "Article", "headline": c["title"], "url": url, "inLanguage": "fr-FR",
           "mainEntityOfPage": url, "author": {"@id": BASE + "/#gael"},
           "contributor": {"@type": "Person", "name": "Gilles Rapaport", "url": RAP_URL, "sameAs": [RAP_URL], "description": "Illustrateur et dessinateur de presse"},
           "isPartOf": {"@type": "CreativeWorkSeries", "name": "Chroniques OK Boomer", "url": BASE + "/chroniques/"},
           "image": BASE + "/assets/%s.jpg" % c["slug"], "publisher": {"@id": BASE + "/#gael"}}
    write("chroniques/%s/index.html" % c["slug"], page(2, "chroniques/%s/" % c["slug"], c["title"] + " — Chronique OK Boomer", desc, body,
          [art, crumbs([("Accueil", BASE + "/"), ("Chroniques OK Boomer", BASE + "/chroniques/"), (c["title"], url)]),
           dict(PERSON, **{"@context": "https://schema.org"})], robots_index=c["complete"], image="assets/%s.jpg" % c["slug"]))

# ---------- à propos + FAQ
FAQ = [
    ("Qui est Monsieur Châtellier ?",
     "Monsieur Châtellier est un personnage d'auteur né sous Pompidou, élevé sous Giscard, propulsé par Mitterrand et mentoré par le grand Jacques. Il écrit des chroniques depuis 2019 pour essayer de comprendre ce qui lui est arrivé. Il se définit comme plus jeune boomer de France, ubercool skater, autobiographe et humain."),
    ("Que sont les chroniques OK Boomer ?",
     "Les chroniques OK Boomer sont des capsules humoristiques envoyées par e-mail : de petites pièces sur le temps qui a passé, souvenirs d'autres époques qui ont forgé l'humanité de l'auteur. Elles forment une autobiographie épistolaire, suivie par quelques centaines de lecteurs."),
    ("Qui illustre les chroniques ?",
     "Les chroniques sont illustrées par Gilles Rapaport, dessinateur de presse et illustrateur de renom, qui collabore à l'aventure OK Boomer depuis le début."),
    ("Comment s'abonner à la newsletter ?",
     "L'abonnement se fait sur Substack, à l'adresse %s. Il suffit d'y saisir son adresse e-mail." % SUBSTACK),
    ("La newsletter est-elle gratuite ?",
     "Oui, la newsletter de Monsieur Châtellier est gratuite."),
    ("Où voir les vidéos de Monsieur Châtellier ?",
     "Les vlogs sont sur la chaîne YouTube @GaelChatellier et les vidéos courtes sur le compte Instagram @monsieurchatellier."),
    ("Un livre est-il prévu ?",
     "Oui. Un livre recueil des chroniques OK Boomer est à venir. L'annonce de sa sortie sera faite dans la newsletter."),
]
def faq_links(t):
    t = t.replace(SUBSTACK, '<a href="%s" target="_blank" rel="me noopener">%s</a>' % (SUBSTACK, SUBSTACK))
    t = t.replace("@GaelChatellier", '<a href="%s" target="_blank" rel="me noopener">@GaelChatellier</a>' % YT)
    t = t.replace("@monsieurchatellier", '<a href="%s" target="_blank" rel="me noopener">@monsieurchatellier</a>' % IG)
    return t

faq_html = "".join("<h3>%s</h3><p>%s</p>" % (esc(q), faq_links(esc(a))) for q, a in FAQ)
about_body = """<div class="wrap article-wrap">
<nav class="crumbs" aria-label="Fil d'Ariane"><a href="%s">Accueil</a> › À propos</nav>
<h1>À propos de Monsieur Châtellier</h1>
<p class="lead">Monsieur Châtellier, un personnage né sous Pompidou, élevé sous Giscard, propulsé par Mitterrand et mentoré par le grand Jacques.</p>
<div class="about-grid">
<div class="photo small"><img class="asis" src="%sassets/apropos.jpg" width="800" height="1200" loading="lazy" alt="Portrait de profil de Monsieur Châtellier, barbe grise et cheveux plaqués en arrière, en noir et blanc"></div>
<div>
<p>J'écris des chroniques depuis 2019 pour essayer de comprendre ce qui m'est arrivé, nous est arrivé peut-être ?, depuis l'époque des culottes courtes, des osselets et des cacolacs partagés avec les copains et copines qui s'appelaient Didier, Vincent, Hélène ou Valérie.</p>
<p>Une correctrice m'accompagne pour garder lisible tout ce que j'écris. Les chroniques sont illustrées par Gilles Rapaport, dessinateur de presse et illustrateur de renom.</p>
<p>Je vis à Paris, à South Pigalle. Une partie de mon cœur est plantée dans les Terres du Milieu, entre Brioude et Charbonnières-les-Vieilles.</p>
<p>À ce jour, quelques centaines de lecteurs suivent mon autobiographie épistolaire. Avec vous, cela fera un de plus ?</p>
<p>Et aussi, dans la vraie vie, je suis directeur de projets digitaux : <a href="%s" rel="me noopener" target="_blank">mon profil LinkedIn</a>.</p>
</div></div>
<h2>Questions fréquentes</h2>
%s
<div class="mt">%s</div>
</div>""" % (href(1, ""), "../", LI, faq_html, signup())
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
about_ld = {"@context": "https://schema.org", "@type": "AboutPage", "url": BASE + "/a-propos/", "name": "À propos de Monsieur Châtellier",
            "inLanguage": "fr-FR", "mainEntity": {"@id": BASE + "/#gael"}}
write("a-propos/index.html", page(1, "a-propos/", "À propos — Monsieur Châtellier, auteur des chroniques OK Boomer",
      "Qui est Monsieur Châtellier ? Auteur des chroniques OK Boomer depuis 2019, illustrées par Gilles Rapaport. Parcours, newsletter, vidéos et questions fréquentes.",
      about_body, [about_ld, faq_ld, crumbs([("Accueil", BASE + "/"), ("À propos", BASE + "/a-propos/")]), dict(PERSON, **{"@context": "https://schema.org"})]))

# ---------- confidentialité
priv_body = """<div class="wrap article-wrap">
<nav class="crumbs" aria-label="Fil d'Ariane"><a href="%s">Accueil</a> › Confidentialité et cookies</nav>
<h1>Confidentialité et cookies</h1>
<p class="lead">Ce site est édité par Gaël Châtellier (Monsieur Châtellier). Contact : <a href="mailto:gael@chatellier.fr">gael@chatellier.fr</a>.</p>
<h2>Ce que le site dépose lui-même</h2>
<p>Le site ne dépose aucun cookie publicitaire. Les polices de caractères sont hébergées sur le site. Votre choix sur les cookies est conservé dans votre navigateur (stockage local) pendant 6 mois.</p>
<h2>Mesure d’audience (Google Analytics)</h2>
<p>Avec votre accord uniquement, le site utilise Google Analytics 4 (Google) pour connaître sa fréquentation : pages consultées, provenance approximative, type d’appareil. Les signaux Google et la personnalisation publicitaire sont désactivés. Les cookies de mesure (<code>_ga</code>) durent au maximum 13 mois et les données sont conservées 14 mois. Si vous refusez, aucune donnée n’est envoyée à Google Analytics.</p>
<h2>Contenus de services tiers</h2>
<p>Certaines pages intègrent des vidéos YouTube (Google) et des reels Instagram (Meta). Ces services peuvent déposer des cookies et collecter des données, dont votre adresse IP, lorsque leur contenu s’affiche. Par défaut, ces contenus ne sont pas chargés : un bouton vous permet de les afficher, ou vous pouvez les regarder directement sur YouTube ou Instagram. Vous pouvez autoriser leur chargement automatique avec « Tout accepter » ou « Personnaliser ».</p>
<h2>Newsletter</h2>
<p>Quand vous envoyez le formulaire d’inscription, votre adresse e-mail est transmise à Substack, qui la traite selon sa propre politique de confidentialité. Rien n’est envoyé à Substack avant que vous ne validiez le formulaire, et ce site ne conserve pas votre adresse e-mail.</p>
<h2>Modifier votre choix</h2>
<p>Vous pouvez changer d’avis à tout moment avec le bouton ci-dessous.</p>
<p><button type="button" class="btn alt" data-consent-open>Gérer mes cookies</button></p>
<h2>Tes droits</h2>
<p>Pour toute question sur vos données ou pour exercer vos droits d’accès, de rectification ou de suppression, écrivez à <a href="mailto:gael@chatellier.fr">gael@chatellier.fr</a>.</p>
</div>""" % href(1, "")
write("confidentialite/index.html", page(1, "confidentialite/", "Confidentialité et cookies — Monsieur Châtellier",
      "Cookies, contenus tiers (YouTube, Instagram) et données personnelles sur le site de Monsieur Châtellier.", priv_body,
      [crumbs([("Accueil", BASE + "/"), ("Confidentialité et cookies", BASE + "/confidentialite/")])]))

# ---------- 404 + .htaccess (Apache / OVH)
import re
nf_body = """<div class="wrap article-wrap">
<h1>Page introuvable</h1>
<p class="lead">Cette page n’existe pas ou a changé d’adresse. Le plus simple : repartir de l’accueil ou lire les chroniques OK Boomer.</p>
<p class="mt links"><a class="btn" href="./">Accueil</a><a class="btn alt" href="chroniques/">Les chroniques</a></p>
</div>"""
nf = page(0, "404.html", "Page introuvable — Monsieur Châtellier", "Page introuvable sur le site de Monsieur Châtellier.", nf_body, [], robots_index=False)
nf = re.sub(r'(href|src)="(?!https?:|mailto:|#|/)(?:\./)?', r'\1="/', nf).replace('data-home=""', 'data-home="/"')
write("404.html", nf)
REDIRECTS = ""
for _l in open(os.path.join(GEN, "redirects.txt"), encoding="utf-8").read().splitlines():
    _l = _l.strip()
    if not _l or _l.startswith("#"): continue
    _src, _dst = _l.split(None, 1)
    REDIRECTS += "RewriteRule ^%s/?$ %s [R=301,L,NE]\n" % (_src, _dst)
write(".htaccess", """# Pas de liste de dossiers
Options -Indexes
ErrorDocument 404 /404.html
DirectoryIndex index.html

RewriteEngine On
# Toujours en HTTPS
RewriteCond %{HTTPS} !=on
RewriteCond %{HTTP:X-Forwarded-Proto} !https
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
# chatellier.fr -> www.chatellier.fr (seulement le domaine nu, pas les sous-domaines de test)
RewriteCond %{HTTP_HOST} ^chatellier\\.fr$ [NC]
RewriteRule ^ https://www.chatellier.fr%{REQUEST_URI} [L,R=301]

# Anciennes adresses WordPress -> nouvelles pages (liste dans generator/redirects.txt)
""" + REDIRECTS + """

<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json image/svg+xml text/plain application/xml
</IfModule>
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/html "access plus 0 seconds"
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
  ExpiresByType image/jpeg "access plus 1 month"
  ExpiresByType font/woff2 "access plus 1 year"
</IfModule>
""")

# ---------- robots, sitemap, llms
write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % BASE)
urls = ["", "a-propos/", "confidentialite/"] + ["chroniques/%s/" % c["slug"] for c in CHRONIQUES if c["complete"]]
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
      "".join("  <url><loc>%s/%s</loc><lastmod>%s</lastmod></url>\n" % (BASE, u, TODAY) for u in urls) + "</urlset>\n")
write("llms.txt", """# Monsieur Châtellier

> Site de Monsieur Châtellier (Gaël Châtellier), auteur des chroniques OK Boomer : une autobiographie épistolaire humoristique envoyée par e-mail depuis 2019, illustrée par Gilles Rapaport. Il publie aussi des vlogs et prépare un livre recueil.

## Pages
- [Accueil](%(b)s/): présentation, chroniques, vidéos, livre à venir
- [À propos](%(b)s/a-propos/): qui est Monsieur Châtellier, questions fréquentes
- [Chroniques OK Boomer](%(b)s/chroniques/): extraits des chroniques

## Liens officiels
- [Newsletter (Substack)](%(s)s)
- [YouTube](%(y)s)
- [Instagram](%(i)s)
- [LinkedIn](%(l)s): activité professionnelle (directeur de projets digitaux)
- [Gilles Rapaport](https://dessins-rapaport.com/): dessinateur de presse et illustrateur des chroniques OK Boomer
""" % dict(b=BASE, s=SUBSTACK, y=YT, i=IG, l=LI))
print("ok", OUT, "local" if LOCAL else "prod")
