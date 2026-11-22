#!/usr/bin/env bash
# Entpackt die verschlüsselten Video-Kits nach studio/kits/_unpacked (nie committen).
# Schlüssel: Umgebungsvariable STUDIO_KIT_KEY (GitHub-Secret).
set -e
D="$(cd "$(dirname "$0")" && pwd)"
[ -n "$STUDIO_KIT_KEY" ] || { echo "STUDIO_KIT_KEY fehlt"; exit 1; }
rm -rf "$D/_unpacked"; mkdir -p "$D/_unpacked"
openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -in "$D/kits.tgz.enc" -pass env:STUDIO_KIT_KEY | tar xz -C "$D/_unpacked"
ls "$D/_unpacked"
