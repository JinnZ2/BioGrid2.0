#!/usr/bin/env python3
"""
Validate all continuity capsules against schema.json and rebuild ledger.md.
Standard library only (no external jsonschema dep). Lightweight validation.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema.json"
CAPSULES_DIR = ROOT / "capsules"
LEDGER_PATH = ROOT / "ledger.md"

RE_INDEX = re.compile(r"^C(\d{3,})$")
ISO_UTC_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
)

REQUIRED_TOP = [
    "continuity_index",
    "project_focus",
    "active_axis",
    "core_glyphs",
    "last_resonance",
    "geometry_encoding",
    "dock_instruction",
    "timestamp_utc",
]

def load_yaml_like(p: Path) -> dict[str, Any]:
    """
    Minimal YAML loader for our simple key:value + arrays use case,
    so we can avoid extra deps. Supports quotes and bare strings.
    If you prefer, replace with `yaml.safe_load`.
    """
    try:
        import yaml  # type: ignore
        return yaml.safe_load(p.read_text())
    except Exception:
        # Fallback: very naive parser (expects valid YAML from our examples)
        # Not recommended for complex YAML.
        data: dict[str, Any] = {}
        current_key = None
        in_array = False
        arr: list[Any] = []
        for line in p.read_text().splitlines():
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            if in_array:
                if s.startswith("- "):
                    val = s[2:].strip().strip('"').strip("'")
                    arr.append(val)
                    continue
                else:
                    data[current_key] = arr
                    in_array = False
            if ": " in s:
                k, v = s.split(": ", 1)
                k = k.strip()
                v = v.strip()
                if v == "":
                    current_key = k
                    in_array = True
                    arr = []
                elif v.startswith("[") and v.endswith("]"):
                    # simple inline array of quoted or bare items
                    inner = v[1:-1].strip()
                    items = [x.strip().strip('"').strip("'") for x in inner.split(",")] if inner else []
                    data[k] = [i for i in items if i]
                else:
                    data[k] = v.strip('"').strip("'")
            else:
                # top-level bare key (start of nested object) — rely on real YAML if needed
                pass
        if in_array and current_key is not None:
            data[current_key] = arr
        return data

def validate_capsule(c: dict[str, Any], path: Path) -> list[str]:
    errors: list[str] = []

    # Required fields
    for k in REQUIRED_TOP:
        if k not in c:
            errors.append(f"Missing required field: {k}")

    # continuity_index
    idx = c.get("continuity_index", "")
    m = RE_INDEX.match(str(idx))
    if not m:
        errors.append("continuity_index must match ^C\\d{3,}$ (e.g., C001).")

    # active_axis
    ax = c.get("active_axis", [])
    if not (isinstance(ax, list) and len(ax) == 2 and all(isinstance(a, str) and a for a in ax)):
        errors.append("active_axis must be an array of exactly two non-empty strings.")

    # core_glyphs
    glyphs = c.get("core_glyphs", [])
    if not (isinstance(glyphs, list) and len(glyphs) >= 1 and all(isinstance(g, str) and g for g in glyphs)):
        errors.append("core_glyphs must be a non-empty array of strings.")

    # geometry_encoding
    ge = c.get("geometry_encoding", {})
    if not isinstance(ge, dict):
        errors.append("geometry_encoding must be an object.")
    else:
        for sub in ["shape", "overlay", "placement"]:
            if sub not in ge:
                errors.append(f"geometry_encoding.{sub} is required.")
        if "overlay" in ge:
            ov = ge["overlay"]
            if not (isinstance(ov, list) and len(ov) >= 1 and all(isinstance(o, str) and o for o in ov)):
                errors.append("geometry_encoding.overlay must be a non-empty array of strings.")

    # timestamp_utc (coarse check)
    ts = c.get("timestamp_utc", "")
    if not isinstance(ts, str) or not ISO_UTC_RE.match(ts):
        errors.append("timestamp_utc must be ISO-8601 UTC like 2025-09-03T18:00:00Z.")
    else:
        # ensure it parses
        try:
            dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
        except Exception:
            errors.append("timestamp_utc not parseable with %Y-%m-%dT%H:%M:%SZ.")

    return errors

def handoff_block(c: dict[str, Any]) -> str:
    axis = c["active_axis"]
    glyphs = " ".join(c["core_glyphs"])
    return (
        "HANDOFF_START\n"
        f"Project Focus: {c['project_focus']}\n"
        f"Active Axis: {axis[0]} + {axis[1]}\n"
        f"Core Glyphs: {glyphs}\n"
        f"Last Resonance: \"{c['last_resonance']}\"\n"
        f"Continuity Index: {c['continuity_index']}\n"
        "HANDOFF_END"
    )

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--capsules", default=str(CAPSULES_DIR), help="Capsules directory")
    args = ap.parse_args()

    cap_dir = Path(args.capsules)
    files = sorted(cap_dir.glob("C*.yaml"))
    if not files:
        print("No capsule files found.")
        raise SystemExit(1)

    capsules: list[dict[str, Any]] = []
    problems = False

    for f in files:
        c = load_yaml_like(f)
        errs = validate_capsule(c, f)
        if errs:
            problems = True
            print(f"✘ {f.name}:")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"✔ {f.name} OK")
            capsules.append(c)

    if problems:
        print("\nFix errors above and rerun.")
        raise SystemExit(2)

    # Sort by continuity_index numeric value
    def idx_num(c): return int(RE_INDEX.match(c["continuity_index"]).group(1))
    capsules.sort(key=idx_num)

    # Rebuild ledger.md
    parts = [
        "# Continuity Ledger — BioGrid 2.0\n",
        "Master chain of capsule HANDOFFs. Auto-generated by `tools/validate_capsules.py`.\n",
        "---\n"
    ]
    for c in capsules:
        parts.append(f"## Capsule {c['continuity_index']}\n\n{handoff_block(c)}\n\n---\n")

    LEDGER_PATH.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"\nLedger rebuilt: {LEDGER_PATH}")

if __name__ == "__main__":
    main()
