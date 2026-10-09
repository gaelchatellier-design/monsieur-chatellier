#!/usr/bin/env bash
# Publie le contenu de site/ dans la branche "deploy", en AJOUTANT un commit à la suite de l'historique
# (OVH fait un "git pull" : l'historique doit rester linéaire, sinon "refusing to merge unrelated histories").
#
# Variables : REPO_URL (adresse du dépôt, avec jeton), SITE_DIR (dossier à publier)
# REPAIR_BASE (facultatif) : ancien commit de deploy que le clone d'OVH connaît. Si la branche actuelle ne
# le contient pas, on repart de lui (une seule fois, avec écrasement) pour que OVH puisse se mettre à jour.
set -euo pipefail

WORK="$(mktemp -d)"
git init -q -b deploy "$WORK"
cd "$WORK"
git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git remote add origin "$REPO_URL"

REMOTE_TIP=""
if git fetch -q origin deploy 2>/dev/null; then REMOTE_TIP="$(git rev-parse FETCH_HEAD)"; fi
PARENT="$REMOTE_TIP"
FORCE=""

if [ -n "${REPAIR_BASE:-}" ] && git fetch -q origin "$REPAIR_BASE" 2>/dev/null; then
  if [ -z "$REMOTE_TIP" ] || ! git merge-base --is-ancestor "$REPAIR_BASE" "$REMOTE_TIP"; then
    echo "Réparation : on repart de $REPAIR_BASE"
    PARENT="$REPAIR_BASE"
    [ -n "$REMOTE_TIP" ] && FORCE="--force"
  fi
fi

if [ -n "$PARENT" ]; then
  git checkout -q --detach "$PARENT"
  git rm -rq --ignore-unmatch . || true
  git clean -fdxq
fi
cp -a "$SITE_DIR"/. .
git add -A

MSG="Site publié depuis ${GITHUB_SHA:-local}"
if [ -n "$FORCE" ]; then
  git commit -q --allow-empty -m "$MSG"
elif git diff --cached --quiet && [ -n "$PARENT" ]; then
  echo "Aucun changement à publier."; exit 0
else
  git commit -q -m "$MSG"
fi
git push -q $FORCE origin HEAD:deploy
echo "Publié : $(git rev-parse --short HEAD)"
