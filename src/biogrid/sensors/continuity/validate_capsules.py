#!/usr/bin/env python3
"""
Validate all continuity capsules against schema and rebuild ledger.md.
Standard library only (no external jsonschema dep).

Usage:
  python -m biogrid.sensors.continuity.validate_capsules --capsules-dir ./capsules
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path
from typing import Any, Dict, List

from .yaml_helpers import load_yaml_like

RE_INDEX = re.compile(r"^C(\d{3,})$")
ISO_UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

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


def validate_capsule(c: Dict[str, Any]) -> List[str]:
    """Validate a single capsule dict. Returns list of error strings."""
    errors: List[str] = []

    for k in REQUIRED_TOP:
        if k not in c:
            errors.append(f"Missing required field: {k}")

    idx = c.get("continuity_index", "")
    if not RE_INDEX.match(str(idx)):
        errors.append("continuity_index must match ^C\\d{3,}$ (e.g., C001).")

    ax = c.get("active_axis", [])
    if not (isinstance(ax, list) and len(ax) == 2
            and all(isinstance(a, str) and a for a in ax)):
        errors.append("active_axis must be an array of exactly two non-empty strings.")

    glyphs = c.get("core_glyphs", [])
    if not (isinstance(glyphs, list) and len(glyphs) >= 1
            and all(isinstance(g, str) and g for g in glyphs)):
        errors.append("core_glyphs must be a non-empty array of strings.")

    ge = c.get("geometry_encoding", {})
    if not isinstance(ge, dict):
        errors.append("geometry_encoding must be an object.")
    else:
        for sub in ["shape", "overlay", "placement"]:
            if sub not in ge:
                errors.append(f"geometry_encoding.{sub} is required.")
        if "overlay" in ge:
            ov = ge["overlay"]
            if not (isinstance(ov, list) and len(ov) >= 1
                    and all(isinstance(o, str) and o for o in ov)):
                errors.append("geometry_encoding.overlay must be a non-empty array of strings.")

    ts = c.get("timestamp_utc", "")
    if not isinstance(ts, str) or not ISO_UTC_RE.match(ts):
        errors.append("timestamp_utc must be ISO-8601 UTC like 2025-09-03T18:00:00Z.")
    else:
        try:
            dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
        except Exception:
            errors.append("timestamp_utc not parseable.")

    return errors


def build_ledger(capsules: List[Dict[str, Any]]) -> str:
    """Build ledger markdown from validated capsules."""
    parts = [
        "# Continuity Ledger — BioGrid 2.0\n",
        "Master chain of capsule HANDOFFs. Auto-generated.\n",
        "---\n",
    ]
    for c in capsules:
        axis = c["active_axis"]
        glyphs = " ".join(c["core_glyphs"])
        block = (
            "HANDOFF_START\n"
            f"Project Focus: {c['project_focus']}\n"
            f"Active Axis: {axis[0]} + {axis[1]}\n"
            f"Core Glyphs: {glyphs}\n"
            f'Last Resonance: "{c["last_resonance"]}"\n'
            f"Continuity Index: {c['continuity_index']}\n"
            "HANDOFF_END"
        )
        parts.append(f"## Capsule {c['continuity_index']}\n\n{block}\n\n---\n")
    return "\n".join(parts).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser(
        description="Validate capsules and rebuild ledger.")
    ap.add_argument("--capsules-dir", required=True,
                    help="Directory containing C*.yaml files.")
    ap.add_argument("--ledger", default=None,
                    help="Path to write ledger.md (default: capsules-dir/../ledger.md).")
    args = ap.parse_args()

    cap_dir = Path(args.capsules_dir)
    files = sorted(cap_dir.glob("C*.yaml"))
    if not files:
        print("No capsule files found.")
        raise SystemExit(1)

    capsules: List[Dict[str, Any]] = []
    problems = False

    for f in files:
        c = load_yaml_like(f)
        errs = validate_capsule(c)
        if errs:
            problems = True
            print(f"FAIL {f.name}:")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"OK   {f.name}")
            capsules.append(c)

    if problems:
        print("\nFix errors above and rerun.")
        raise SystemExit(2)

    def idx_num(c):
        return int(RE_INDEX.match(c["continuity_index"]).group(1))

    capsules.sort(key=idx_num)

    ledger_path = Path(args.ledger) if args.ledger else cap_dir.parent / "ledger.md"
    ledger_path.write_text(build_ledger(capsules), encoding="utf-8")
    print(f"\nLedger rebuilt: {ledger_path}")


if __name__ == "__main__":
    main()
