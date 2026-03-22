#!/usr/bin/env python3
"""
Merge glyph fragments into a canonical registry.

Handles additions, edits, deprecations, and preserves provenance chains.

Usage:
  python -m biogrid.glyphs.merge --canonical canonical.json --fragments fragments/
"""

import argparse
import glob
import json
import os
from datetime import datetime, timezone


def load_json(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(p, obj):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=False)


def merge_fragments(canon_path, frag_dir):
    """Merge all fragment files into canonical.json. Returns merge count."""
    if os.path.exists(canon_path):
        canon = load_json(canon_path)
    else:
        canon = {
            "version": "2.3",
            "updated": datetime.now(timezone.utc).isoformat(),
            "glyphs": [],
        }

    index = {g["code"]: g for g in canon.get("glyphs", [])}

    frag_files = sorted(glob.glob(os.path.join(frag_dir, "*.json")))
    for fp in frag_files:
        frag = load_json(fp)

        for add in frag.get("adds", []):
            code = add["code"]
            if code not in index:
                if add.get("state") == "proposed":
                    add["state"] = "canonical"
                add.setdefault("provenance_chain", []).append(
                    frag.get("provenance", "unknown"))
                index[code] = add
            else:
                g = index[code]
                for k, v in add.items():
                    if k == "code":
                        continue
                    if k == "layers":
                        g.setdefault("layers", [])
                        g["layers"] = sorted(set(g["layers"]) | set(v))
                    elif k == "meta":
                        g.setdefault("meta", {}).update(v)
                    else:
                        if k not in g or (isinstance(g[k], str) and not g[k].strip()):
                            g[k] = v
                g.setdefault("provenance_chain", []).append(
                    frag.get("provenance", "unknown"))

        for ed in frag.get("edits", []):
            c = ed.get("code")
            if c in index and ed.get("op") == "rename":
                index[c]["name"] = ed.get("to_name", index[c]["name"])

        for dep in frag.get("deprecations", []):
            c = dep.get("code")
            if c in index:
                index[c]["state"] = "deprecated"
                index[c].setdefault("meta", {})["deprecation_reason"] = dep.get("reason", "")

    canon["glyphs"] = sorted(index.values(), key=lambda g: g["code"])
    canon["updated"] = datetime.now(timezone.utc).isoformat()
    save_json(canon_path, canon)

    return len(frag_files)


def main():
    ap = argparse.ArgumentParser(
        description="Merge glyph fragments into canonical registry.")
    ap.add_argument("--canonical", default="canonical.json",
                    help="Path to canonical registry JSON.")
    ap.add_argument("--fragments", default="fragments",
                    help="Directory containing fragment JSON files.")
    args = ap.parse_args()

    count = merge_fragments(args.canonical, args.fragments)
    print(f"Merged {count} fragment file(s) into {args.canonical}")


if __name__ == "__main__":
    main()
