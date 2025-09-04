#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-.}"
# Known variant fixes (left → right is canonical)
declare -A FIX=(
  ["🕸"]="🕸️"   # add VS16
  ["⟲"]="⟳"    # recheck
  ["↻"]="⟳"    # recheck
  ["–"]="-"
)
# Sweep JSON/MD
find "$ROOT" -type f \( -name "*.json" -o -name "*.md" \) | while read -r f; do
  TMP="$f.tmp.$$"; cp "$f" "$TMP"
  for k in "${!FIX[@]}"; do
    LC_ALL=C sed -i "s/${k}/${FIX[$k]}/g" "$TMP"
  done
  if ! cmp -s "$f" "$TMP"; then mv "$TMP" "$f"; echo "normalized: $f"; else rm "$TMP"; fi
done
echo "[ok] normalization pass complete."
