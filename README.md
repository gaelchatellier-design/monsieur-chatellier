# monsieur-chatellier

Refonte de chatellier.fr : la maison de Monsieur Châtellier (chroniques OK Boomer, vidéos, livre).

- `site/` : site statique (HTML/CSS), SEO et GEO intégrés (balises, JSON-LD, sitemap, robots.txt, llms.txt)
- `maquettes/` : maquettes de design (Zine retenue, Skate mag écartée)
- `assets/` : images sources (portrait, dessins de Gilles Rapaport, images de vidéos)

## À compléter avant mise en ligne
- Chroniques sans date de publication (choix assumé)
- Vidéos : lecteurs YouTube et Instagram intégrés (à tester en ligne ; titres des reels éventuels)
- Livre : page dédiée quand le titre et la date de sortie sont connus

## Cookies et vie privée
- Bandeau de consentement (`site/assets/consent.js`) : choix conservé 6 mois, boutons « Tout refuser », « Personnaliser » et « Tout accepter » équivalents, lien « Gérer mes cookies » en pied de page
- Google Analytics 4 (ID dans le générateur, `GA_ID`) : chargé seulement après accord, signaux Google désactivés, cookies limités à 13 mois
- Les lecteurs YouTube et Instagram ne se chargent qu'après accord (ou au clic sur « Charger »)
- Polices auto-hébergées (aucune requête vers Google Fonts)
- Page `site/confidentialite/`

## Régénérer le site
Le dossier `site/` est produit par `generator/` (HTML, CSS et images sources) :

    python3 generator/build.py site prod

Pour une version ouvrable en double-clic (liens en `index.html`) : `python3 generator/build.py apercu local`.

## Déploiement sur OVH
Chaque fusion sur `main` publie le contenu de `site/` dans la branche `deploy` (`.github/workflows/deploy.yml`).
L'intégration Git de l'hébergement OVH (Multisite → site → Git) récupère cette branche :
- Dépôt : `git@github.com:gaelchatellier-design/monsieur-chatellier.git` (SSH, dépôt privé), branche `deploy`
- Clé publique fournie par OVH : à ajouter dans GitHub (Settings → Deploy keys, lecture seule)
- Mise à jour automatique : l'URL de webhook d'OVH est à ajouter dans GitHub (Settings → Webhooks, événement push)

## Redirections des anciennes adresses WordPress
La liste est dans `generator/redirects.txt` (une ligne par ancienne adresse : `ancienne-adresse nouvelle-adresse`), reprise dans `site/.htaccess`.
Les 127 anciens articles redirigent vers `/chroniques/`, les anciennes pages vers leur équivalent. L'ancien WordPress reste intact dans le dossier `www` d'OVH (ne pas le supprimer avant plusieurs mois).
