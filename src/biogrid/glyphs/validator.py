#!/usr/bin/env python3
"""
Validate glyph registry JSON files.

Checks: required fields, unique codes, valid states, allowed layers,
and optional SHA256 checksums for integrity verification.

Usage:
  python -m biogrid.glyphs.validator canonical.json
  python -m biogrid.glyphs.validator canonical.json --write  # update checksums
"""

import argparse
import hashlib
import json
import os
import re
import sys

ALLOWED_STATES = {"proposed", "canonical", "deprecated"}
ALLOWED_LAYERS = {
    "temporal", "logic", "resonance", "signal", "field", "memory",
    "repair", "sensor", "integrity", "audit", "navigation", "decision",
    "constraint", "archive", "reference", "validation", "coherence",
    "provisional", "recovery", "symbolic",
}
FIELDS_FOR_CHECKSUM = ["code", "name", "glyph", "essence", "layers", "state"]


def norm_layers(layers):
    if not isinstance(layers, list):
        return []
    return sorted({str(x) for x in layers})


def checksum_item(g):
    layers = norm_layers(g.get("layers", []))
    vals = {
        "code": g.get("code", "").strip(),
        "name": g.get("name", "").strip(),
        "glyph": g.get("glyph", "").strip(),
        "essence": g.get("essence", "").strip(),
        "layers": ",".join(layers),
        "state": g.get("state", "proposed").strip(),
    }
    s = "|".join([vals[k] for k in FIELDS_FOR_CHECKSUM])
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def validate_file(json_path, write_checksums=False):
    """Validate a glyph registry file. Returns (ok, warnings, errors)."""
    with open(json_path, "r", encoding="utf-8") as f:
        doc = json.load(f)

    items_key = "glyphs" if "glyphs" in doc else "adds" if "adds" in doc else None
    if not items_key:
        return False, [], ["JSON must contain 'glyphs' or 'adds'"]

    items = doc[items_key]
    codes, glyphs_seen = set(), set()
    ok = True
    warnings = []
    errors = []
    wrote = False

    for g in items:
        code = g.get("code", "").strip()
        name = g.get("name", "").strip()
        glyph = g.get("glyph", "").strip()
        essence = g.get("essence", "").strip()
        state = g.get("state", "proposed").strip()
        layers = g.get("layers", [])

        if not code or not re.match(r"^[A-Z0-9:_-]+$", code):
            errors.append(f"Bad/missing code: {code}")
            ok = False
        if code in codes:
            errors.append(f"Duplicate code: {code}")
            ok = False
        codes.add(code)

        if glyph:
            if glyph in glyphs_seen:
                warnings.append(f"Glyph symbol reused: {glyph} code={code}")
            glyphs_seen.add(glyph)
        else:
            warnings.append(f"Missing glyph symbol for {code}")

        if not name:
            errors.append(f"Missing name for {code}")
            ok = False
        if not essence or len(essence) > 200:
            warnings.append(f"Essence missing/long ({len(essence)} chars) for {code}")

        if state not in ALLOWED_STATES:
            errors.append(f"Invalid state '{state}' for {code}")
            ok = False

        nl = norm_layers(layers)
        if not nl:
            warnings.append(f"No layers for {code}")
        else:
            extra = set(nl) - ALLOWED_LAYERS
            if extra:
                warnings.append(f"{code}: unknown layers {sorted(extra)}")

        cs = checksum_item(g)
        meta = g.setdefault("meta", {})
        recorded = meta.get("checksum", "")
        if recorded != cs:
            if write_checksums:
                meta["checksum"] = cs
                meta["checksum_fields"] = FIELDS_FOR_CHECKSUM
                wrote = True
            else:
                warnings.append(f"{code}: checksum missing/stale")

    if write_checksums and wrote:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2, sort_keys=False)

    return ok, warnings, errors


def main():
    ap = argparse.ArgumentParser(
        description="Validate glyph registry JSON.")
    ap.add_argument("json_path", help="Path to registry JSON.")
    ap.add_argument("--write", action="store_true",
                    help="Write checksums if missing or stale.")
    args = ap.parse_args()

    if not os.path.exists(args.json_path):
        print(f"File not found: {args.json_path}", file=sys.stderr)
        sys.exit(1)

    ok, warnings, errors = validate_file(args.json_path, args.write)

    for e in errors:
        print(f"ERROR: {e}")
    for w in warnings:
        print(f"WARNING: {w}")

    if ok:
        print("Validation passed.")
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
