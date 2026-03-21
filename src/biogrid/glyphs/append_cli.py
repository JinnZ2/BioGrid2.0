#!/usr/bin/env python3
"""
Safe appender/merger for glyph master registries.

Features:
- Validates schema for each new glyph (code, name, glyph, layers[] required)
- Backs up the master file with timestamp before writing
- Non-destructive merge: keeps existing name/glyph, unions layers,
  records alternatives under alt_name / alt_glyphs
- Maintains stable sort order by code

Usage:
  python -m biogrid.glyphs.append_cli \
    --master glyph_canonical_master_v2.json --add new_glyph.json
"""

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Dict, List

REQUIRED_FIELDS = ["code", "name", "glyph", "layers"]


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_glyph(g: Dict):
    missing = [k for k in REQUIRED_FIELDS if k not in g]
    if missing:
        raise ValueError(f"Glyph missing required fields: {missing}. Offender: {g}")
    if not isinstance(g["layers"], list):
        raise ValueError(f"'layers' must be a list: {g}")


def normalize_glyph(g: Dict) -> Dict:
    g = dict(g)
    g.setdefault("layers", [])
    g.setdefault("notes", "")
    g.setdefault("alt_glyphs", [])
    g.setdefault("alt_name", "")
    g.setdefault("source", "manual_append")
    return g


def merge_one(existing: Dict, incoming: Dict) -> Dict:
    merged = dict(existing)
    merged["layers"] = sorted(set(existing.get("layers", []) + incoming.get("layers", [])))
    if incoming.get("name") and incoming["name"] != existing.get("name"):
        merged["alt_name"] = incoming["name"]
    if incoming.get("glyph") and incoming["glyph"] != existing.get("glyph"):
        ag = list(merged.get("alt_glyphs", []))
        if incoming["glyph"] not in ag:
            ag.append(incoming["glyph"])
        merged["alt_glyphs"] = ag
    if incoming.get("notes"):
        notes = existing.get("notes") or ""
        if incoming["notes"] not in notes:
            merged["notes"] = (notes + "\n" + incoming["notes"]).strip()
    merged["source"] = "merged_append"
    return merged


def append_to_master(master_path, add_path):
    """Append/merge glyphs into a master registry. Returns (inserts, updates) counts."""
    master_path = Path(master_path)
    add_path = Path(add_path)

    master = load_json(master_path)
    if "glyphs" not in master or not isinstance(master["glyphs"], list):
        raise ValueError("Master JSON missing 'glyphs' list.")

    new_json = load_json(add_path)
    if isinstance(new_json, dict) and "glyphs" in new_json:
        incoming_list = new_json["glyphs"]
    elif isinstance(new_json, list):
        incoming_list = new_json
    elif isinstance(new_json, dict):
        incoming_list = [new_json]
    else:
        raise ValueError("Unsupported new glyph JSON format.")

    prepared = []
    for g in incoming_list:
        validate_glyph(g)
        prepared.append(normalize_glyph(g))

    by_code = {g["code"]: g for g in master["glyphs"]}
    updates = 0
    inserts = 0
    for inc in prepared:
        code = inc["code"]
        if code in by_code:
            by_code[code] = merge_one(by_code[code], inc)
            updates += 1
        else:
            by_code[code] = inc
            inserts += 1

    def sort_key(c):
        head = c.split(":")[0]
        return (head, c)

    master["glyphs"] = [by_code[k] for k in sorted(by_code.keys(), key=sort_key)]
    master["updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    # backup
    bak = master_path.with_suffix(f".bak.{int(time.time())}.json")
    with open(bak, "w", encoding="utf-8") as f:
        json.dump(master, f, ensure_ascii=False, indent=2)
    # write
    with open(master_path, "w", encoding="utf-8") as f:
        json.dump(master, f, ensure_ascii=False, indent=2)

    return inserts, updates


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--master", required=True,
                    help="Path to master registry JSON.")
    ap.add_argument("--add", required=True,
                    help="Path to new glyph JSON (single or list).")
    args = ap.parse_args()

    inserts, updates = append_to_master(args.master, args.add)
    print(f"[OK] Inserts: {inserts}, Updates: {updates}")


if __name__ == "__main__":
    main()
