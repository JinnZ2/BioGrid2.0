#!/usr/bin/env python3
"""
Scan folders for glyph JSON/Markdown, compare against a master registry,
and produce a merge-pack JSON with only missing glyphs.

Usage:
  python -m biogrid.glyphs.collector \
    --master master_registry.json --search ./ \
    --wander WANDER.md --out merge_pack.json
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

REQ_FIELDS = {"code", "name", "glyph"}


def load_master(master_path):
    try:
        with open(master_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        master_glyphs = data.get("glyphs", [])
        index = {g.get("code"): g for g in master_glyphs if "code" in g}
        return index, data
    except Exception as e:
        print(f"[ERROR] Failed to load master registry: {e}", file=sys.stderr)
        return {}, {"glyphs": []}


def extract_from_json_obj(obj):
    out = []
    if isinstance(obj, dict):
        if "glyphs" in obj and isinstance(obj["glyphs"], list):
            out.extend(obj["glyphs"])
        if "additions" in obj and isinstance(obj["additions"], list):
            out.extend(obj["additions"])
    return out


def scan_json_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return extract_from_json_obj(data)
    except Exception:
        return []


def find_json_code_blocks(md_text):
    pattern = re.compile(r"```json\s*(.*?)```", re.DOTALL | re.IGNORECASE)
    return pattern.findall(md_text)


def scan_md_file(path):
    out = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        blocks = find_json_code_blocks(text)
        for block in blocks:
            try:
                obj = json.loads(block)
                out.extend(extract_from_json_obj(obj))
            except Exception:
                continue
    except Exception:
        pass
    return out


def collect_glyphs(search_root, master_path):
    """Collect glyphs from a directory tree, returning (new, provisional) lists."""
    master_index, _ = load_master(master_path)
    found = []
    for base, _, files in os.walk(search_root):
        for fn in files:
            p = os.path.join(base, fn)
            if fn.lower().endswith(".json"):
                found.extend(scan_json_file(p))
            elif fn.lower().endswith((".md", ".markdown")):
                found.extend(scan_md_file(p))

    missing = []
    provisional = []
    seen_codes = set()

    for g in found:
        code = g.get("code")
        if not code or code in seen_codes:
            continue
        seen_codes.add(code)
        if code in master_index:
            continue
        if not REQ_FIELDS.issubset(set(g.keys())):
            provisional.append(g)
            continue
        missing.append({k: g.get(k) for k in ["code", "name", "glyph", "layers", "source"] if k in g})

    # De-dup by code
    dedup = []
    seen = set()
    for g in missing:
        c = g.get("code")
        if c and c not in seen:
            dedup.append(g)
            seen.add(c)

    return dedup, provisional


def write_merge_pack(out_path, entries):
    pack = {
        "version": "merge-pack-1.0",
        "updated": datetime.now(timezone.utc).isoformat(),
        "additions": entries,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(pack, f, ensure_ascii=False, indent=2)


def append_wander(wander_path, provisional):
    if not provisional:
        return
    header = (
        "\n\n---\n\n## Auto-collected Provisional Glyphs ("
        + datetime.now(timezone.utc).isoformat() + ")\n"
    )
    lines = [header]
    for g in provisional:
        lines.append(f"### {g.get('code', '(no code)')} — {g.get('name', '(no name)')}")
        lines.append(f"- Glyph: {g.get('glyph', '(none)')}")
        layers = g.get("layers")
        if layers:
            lines.append(f"- Layers: {', '.join(layers)}")
        src = g.get("source", "(unknown)")
        lines.append(f"- Source: {src}")
        lines.append("- Status: provisional — missing required fields\n")
    with open(wander_path, "a", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser(
        description="Collect scattered glyphs and build a merge pack.")
    ap.add_argument("--master", required=True,
                    help="Path to master registry JSON.")
    ap.add_argument("--search", required=True,
                    help="Root directory to scan.")
    ap.add_argument("--wander", required=True,
                    help="Path to WANDER.md for provisional logging.")
    ap.add_argument("--out", required=True,
                    help="Path to write merge_pack.json.")
    args = ap.parse_args()

    dedup, provisional = collect_glyphs(args.search, args.master)

    write_merge_pack(args.out, dedup)
    append_wander(args.wander, provisional)

    master_index, _ = load_master(args.master)
    print(f"[SUMMARY] Master codes: {len(master_index)}")
    print(f"[SUMMARY] New merge-ready additions: {len(dedup)} -> {args.out}")
    print(f"[SUMMARY] Provisional (missing fields): {len(provisional)} -> appended to {args.wander}")


if __name__ == "__main__":
    main()
