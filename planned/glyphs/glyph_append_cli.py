#!/usr/bin/env python3
"""
glyph_append_cli.py — Safe appender/merger for glyph_canonical_master_v2.json

Features
- Validates schema for each new glyph (code, name, glyph, layers[] required)
- Backs up the master file to *.bak with timestamp before writing
- Prevents accidental overwrite: if code exists, merges non-destructively:
    - keeps existing name/glyph
    - unions layers
    - records alternative text under alt_name / alt_glyphs
- Maintains stable sort order by `code`
- Can add a single glyph JSON or a list of glyphs in one file

Usage
  python3 glyph_append_cli.py --master path/to/glyph_canonical_master_v2.json --add new_glyph.json
  python3 glyph_append_cli.py --master glyph_canonical_master_v2.json --add batch_new_glyphs.json

The `--add` file can be:
  {"code": "...", "name":"...", "glyph":"...", "layers":[...], "notes":"...", "alt_glyphs":[...], "alt_name":"..."}
or
  {"glyphs":[ {...}, {...}, ... ]}
"""

import argparse, json, time, os, sys
from pathlib import Path
from typing import List, Dict

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

def to_dict_by_code(glyphs: List[Dict]) -> Dict[str, Dict]:
    d = {}
    for g in glyphs:
        d[g["code"]] = g
    return d

def merge_one(existing: Dict, incoming: Dict) -> Dict:
    merged = dict(existing)
    # union layers
    merged["layers"] = sorted(set(existing.get("layers", []) + incoming.get("layers", [])))
    # alt name if different
    if incoming.get("name") and incoming["name"] != existing.get("name"):
        merged["alt_name"] = incoming["name"]
    # alt glyphs if different
    if incoming.get("glyph") and incoming["glyph"] != existing.get("glyph"):
        ag = list(merged.get("alt_glyphs", []))
        if incoming["glyph"] not in ag:
            ag.append(incoming["glyph"])
        merged["alt_glyphs"] = ag
    # notes: append if new and not substring
    if incoming.get("notes"):
        notes = (existing.get("notes") or "")
        if incoming["notes"] not in notes:
            merged["notes"] = (notes + "\n" + incoming["notes"]).strip()
    merged["source"] = "merged_append"
    return merged

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--master", required=True, help="Path to glyph_canonical_master_v2.json")
    ap.add_argument("--add", required=True, help="Path to new glyph .json (single or list under 'glyphs')")
    args = ap.parse_args()

    master_path = Path(args.master)
    add_path = Path(args.add)
    if not master_path.exists():
        print(f"[!] Master file not found: {master_path}", file=sys.stderr); sys.exit(1)
    if not add_path.exists():
        print(f"[!] Add file not found: {add_path}", file=sys.stderr); sys.exit(1)

    master = load_json(master_path)
    if "glyphs" not in master or not isinstance(master["glyphs"], list):
        print("[!] Master JSON missing 'glyphs' list.", file=sys.stderr); sys.exit(1)

    new_json = load_json(add_path)
    incoming_list = []
    if isinstance(new_json, dict) and "glyphs" in new_json and isinstance(new_json["glyphs"], list):
        incoming_list = new_json["glyphs"]
    elif isinstance(new_json, list):
        incoming_list = new_json
    elif isinstance(new_json, dict):
        incoming_list = [new_json]
    else:
        print("[!] Unsupported new glyph JSON format.", file=sys.stderr); sys.exit(1)

    # validate & normalize
    prepared = []
    for g in incoming_list:
        validate_glyph(g)
        prepared.append(normalize_glyph(g))

    # map by code
    by_code = { g["code"]: g for g in master["glyphs"] }
    updates = 0; inserts = 0
    for inc in prepared:
        code = inc["code"]
        if code in by_code:
            by_code[code] = merge_one(by_code[code], inc)
            updates += 1
        else:
            by_code[code] = inc
            inserts += 1

    # rebuild sorted list
    def sort_key(c):
        head = c.split(":")[0]
        return (head, c)
    merged_list = [by_code[k] for k in sorted(by_code.keys(), key=sort_key)]
    master["glyphs"] = merged_list
    master["updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    # backup
    bak = master_path.with_suffix(f".bak.{int(time.time())}.json")
    with open(bak, "w", encoding="utf-8") as f:
        json.dump(master, f, ensure_ascii=False, indent=2)
    # write
    with open(master_path, "w", encoding="utf-8") as f:
        json.dump(master, f, ensure_ascii=False, indent=2)

    print(f"[OK] Inserts: {inserts}, Updates: {updates}")
    print(f"[Backup] {bak}")
    print(f"[Written] {master_path}")

if __name__ == "__main__":
    main()
