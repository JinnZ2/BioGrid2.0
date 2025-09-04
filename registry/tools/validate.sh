#!/usr/bin/env bash
set -e
echo "[*] Validating repos.index.json shape…"
jq -e . BioGrid2.0/registry/repos.index.json >/dev/null || exit 1
echo "[*] Validating glyph atlas shape…"
jq -e . BioGrid2.0/planned/glyphs/atlas.json >/dev/null || jq -e . BioGrid2.0/registry/atlas.glyphs.json >/dev/null
echo "[*] Validating shapes cross-map…"
jq -e . BioGrid2.0/registry/atlas.shapes.json >/dev/null
echo "[ok] Basic JSON shape checks passed."
