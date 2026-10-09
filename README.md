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
- Bandeau de consentement (`site/assets/consent.js`) : choix conservé 6 mois, boutons « Tout refuser » et « Tout accepter » équivalents, lien « Gérer mes cookies » en pied de page
- Les lecteurs YouTube et Instagram ne se chargent qu'après accord (ou au clic sur « Charger »)
- Polices auto-hébergées (aucune requête vers Google Fonts)
- Page `site/confidentialite/`
