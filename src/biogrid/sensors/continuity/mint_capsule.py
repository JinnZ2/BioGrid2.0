#!/usr/bin/env python3
"""
Mint a new continuity capsule by cloning the latest Cxxx.yaml, bumping
the index, stamping timestamp_utc, and applying optional overrides.

Usage:
  python -m biogrid.sensors.continuity.mint_capsule \
    --capsules-dir ./capsules \
    --resonance "Threads tighten into load-bearing weave." \
    --axis Coherence Adaptation
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path
from typing import Any, Dict, Tuple

from .yaml_helpers import dump_yaml_capsule, load_yaml_like

RE_INDEX = re.compile(r"^C(\d{3,})$")


def find_latest_capsule(capsules_dir: Path) -> Tuple[Path, Dict[str, Any]]:
    files = sorted(capsules_dir.glob("C*.yaml"))
    if not files:
        raise SystemExit("No existing capsules found. Create C001.yaml first.")
    best = None
    best_n = -1
    best_data = None
    for f in files:
        c = load_yaml_like(f)
        m = RE_INDEX.match(str(c.get("continuity_index", "")))
        if not m:
            continue
        n = int(m.group(1))
        if n > best_n:
            best, best_n, best_data = f, n, c
    if not best:
        raise SystemExit("No valid continuity_index found in capsules/.")
    return best, best_data  # type: ignore


def next_index_str(prev: str) -> str:
    m = RE_INDEX.match(prev)
    if not m:
        raise ValueError("Invalid previous continuity_index")
    n = int(m.group(1)) + 1
    return f"C{n:03d}"


def mint(capsules_dir: Path, **overrides: Any) -> Path:
    """Mint a new capsule. Returns path to the new YAML file."""
    _, latest = find_latest_capsule(capsules_dir)
    new_capsule = dict(latest)

    idx = overrides.get("index")
    if idx:
        if not RE_INDEX.match(idx):
            raise ValueError("--index must look like C003, C042, ...")
        new_capsule["continuity_index"] = idx
    else:
        new_capsule["continuity_index"] = next_index_str(latest["continuity_index"])

    new_capsule["timestamp_utc"] = (
        overrides.get("timestamp")
        or dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    )

    for key in ("project_focus", "last_resonance", "dock_instruction"):
        if overrides.get(key):
            new_capsule[key] = overrides[key]

    if overrides.get("axis"):
        new_capsule["active_axis"] = list(overrides["axis"])

    if overrides.get("glyphs"):
        new_capsule["core_glyphs"] = overrides["glyphs"].split()

    ge = dict(new_capsule.get("geometry_encoding", {}))
    for key in ("shape", "placement"):
        if overrides.get(key):
            ge[key] = overrides[key]
    if overrides.get("overlay"):
        ge["overlay"] = [x.strip() for x in overrides["overlay"].split(",") if x.strip()]
    new_capsule["geometry_encoding"] = ge

    out_name = f"{new_capsule['continuity_index']}.yaml"
    out_path = capsules_dir / out_name
    if out_path.exists():
        raise SystemExit(f"{out_name} already exists. Use --index to set a different index.")

    out_path.write_text(dump_yaml_capsule(new_capsule), encoding="utf-8")
    return out_path


def main():
    ap = argparse.ArgumentParser(description="Mint a new continuity capsule.")
    ap.add_argument("--capsules-dir", required=True, help="Path to capsules directory.")
    ap.add_argument("--index", help="Explicit continuity index (e.g. C010).")
    ap.add_argument("--resonance", help="last_resonance text.")
    ap.add_argument("--axis", nargs=2, metavar=("A", "B"), help="Two active axes.")
    ap.add_argument("--glyphs", help="Core glyphs (space-separated).")
    ap.add_argument("--dock", help="dock_instruction.")
    ap.add_argument("--project", help="project_focus.")
    ap.add_argument("--shape", help="geometry_encoding.shape.")
    ap.add_argument("--overlay", help="geometry_encoding.overlay (comma-separated).")
    ap.add_argument("--placement", help="geometry_encoding.placement.")
    args = ap.parse_args()

    out = mint(
        Path(args.capsules_dir),
        index=args.index,
        last_resonance=args.resonance,
        axis=args.axis,
        glyphs=args.glyphs,
        dock_instruction=args.dock,
        project_focus=args.project,
        shape=args.shape,
        overlay=args.overlay,
        placement=args.placement,
    )
    print(f"Minted {out}")


if __name__ == "__main__":
    main()
