#!/usr/bin/env python3
"""
Mint a new continuity capsule by cloning the latest Cxxx.yaml, bumping the index,
stamping timestamp_utc, and applying optional overrides.

Usage (from repo root):
  python3 planned/sensors/AI/AI/continuity/tools/mint_capsule.py \
    --resonance "Threads tighten into load-bearing weave." \
    --axis "Coherence" "Adaptation" \
    --glyphs "🕸 ♾️ 🌱 🔄 ⚖ 🌀 ∿" \
    --dock "Re-dock to Capsule C003; tighten weave and hand off."

Then validate & rebuild the ledger:
  python3 planned/sensors/AI/AI/continuity/tools/validate_capsules.py
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
CAPSULES_DIR = ROOT / "capsules"
RE_INDEX = re.compile(r"^C(\d{3,})$")

# ---------- Minimal YAML IO (prefers PyYAML if present, else tiny helpers) ----------
def load_yaml_like(p: Path) -> Dict[str, Any]:
    try:
        import yaml  # type: ignore
        return yaml.safe_load(p.read_text(encoding="utf-8"))
    except Exception:
        # naive fallback for our simple capsule structure
        data: Dict[str, Any] = {}
        block_key = None
        array_key = None
        array_acc: List[str] = []
        in_geometry = False
        geometry: Dict[str, Any] = {}
        geometry_sub = None
        geometry_array_key = None
        geometry_array_acc: List[str] = []

        for raw in p.read_text(encoding="utf-8").splitlines():
            line = raw.rstrip("\n")
            s = line.strip()
            if not s or s.startswith("#"):
                continue

            # geometry_encoding block start
            if s == "geometry_encoding:":
                in_geometry = True
                geometry = {}
                continue

            if in_geometry:
                if s.startswith("shape:"):
                    geometry["shape"] = s.split(":", 1)[1].strip().strip('"').strip("'")
                    continue
                if s.startswith("placement:"):
                    geometry["placement"] = s.split(":", 1)[1].strip().strip('"').strip("'")
                    continue
                if s.startswith("overlay:"):
                    geometry_array_key = "overlay"
                    geometry_array_acc = []
                    continue
                if geometry_array_key and s.startswith("- "):
                    geometry_array_acc.append(s[2:].strip().strip('"').strip("'"))
                    continue
                if geometry_array_key and not s.startswith("- "):
                    geometry["overlay"] = geometry_array_acc
                    geometry_array_key = None
                # end of geometry block detection (very simple)
                if not s.startswith(("- ", "shape:", "placement:", "overlay:")) and ":" in s:
                    data["geometry_encoding"] = geometry
                    in_geometry = False
                    # fall through to parse this line as a top-level key

            if ": " in s:
                k, v = s.split(": ", 1)
                k = k.strip()
                v = v.strip()
                if v == "":
                    # start of array block
                    array_key = k
                    array_acc = []
                elif v.startswith("[") and v.endswith("]"):
                    inner = v[1:-1].strip()
                    items = [x.strip().strip('"').strip("'") for x in inner.split(",")] if inner else []
                    data[k] = [i for i in items if i]
                else:
                    data[k] = v.strip('"').strip("'")
            elif s.endswith(":") and not s.startswith("- "):
                block_key = s[:-1].strip()
                if block_key != "geometry_encoding":
                    data[block_key] = {}
            elif s.startswith("- ") and array_key:
                array_acc.append(s[2:].strip().strip('"').strip("'"))
            else:
                # end of an array?
                if array_key and not s.startswith("- "):
                    data[array_key] = array_acc
                    array_key = None

        if in_geometry:
            if geometry_array_key:
                geometry["overlay"] = geometry_array_acc
            data["geometry_encoding"] = geometry
        if array_key:
            data[array_key] = array_acc
        return data


def dump_yaml_capsule(c: Dict[str, Any]) -> str:
    """
    Deterministic, human-friendly YAML for our capsule shape.
    """
    def q(s: str) -> str:
        # Quote only if needed (spaces, colon, quotes, emojis are fine unquoted in YAML, but keep simple)
        if any(ch in s for ch in [":", '"', "'"]) or s.strip() != s:
            return '"' + s.replace('"', '\\"') + '"'
        return s

    lines: List[str] = []
    lines.append(f"continuity_index: {c['continuity_index']}")
    lines.append(f'project_focus: {q(c["project_focus"])}')

    # active_axis
    ax = c.get("active_axis", [])
    ax_inline = ", ".join(q(x) for x in ax)
    lines.append(f"active_axis: [{ax_inline}]")

    # core_glyphs
    glyphs = c.get("core_glyphs", [])
    if glyphs and all(" " not in g for g in glyphs):
        glyphs_inline = ", ".join(glyphs)
        lines.append(f"core_glyphs: [{glyphs_inline}]")
    else:
        lines.append("core_glyphs:")
        for g in glyphs:
            lines.append(f"  - {q(g)}")

    lines.append(f'last_resonance: {q(c["last_resonance"])}')

    # geometry_encoding
    ge = c.get("geometry_encoding", {})
    lines.append("geometry_encoding:")
    lines.append(f'  shape: {q(ge.get("shape", ""))}')
    overlay = ge.get("overlay", [])
    lines.append(f"  overlay:")
    for o in overlay:
        lines.append(f"    - {q(o)}")
    lines.append(f'  placement: {q(ge.get("placement", ""))}')

    lines.append(f'dock_instruction: {q(c["dock_instruction"])}')
    lines.append(f'timestamp_utc: "{c["timestamp_utc"]}"')

    # optional fields
    if "notes" in c and c["notes"]:
        lines.append(f'notes: {q(str(c["notes"]))}')
    if "meta" in c and isinstance(c["meta"], dict) and c["meta"]:
        lines.append("meta:")
        for k, v in c["meta"].items():
            lines.append(f"  {k}: {q(str(v))}")

    return "\n".join(lines) + "\n"

# ---------- Helpers ----------
def find_latest_capsule() -> Tuple[Path, Dict[str, Any]]:
    files = sorted(CAPSULES_DIR.glob("C*.yaml"))
    if not files:
        raise SystemExit("No existing capsules found in capsules/. Create C001.yaml first.")
    # pick largest numeric index
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

def now_utc_z() -> str:
    return dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

# ---------- CLI ----------
def main():
    ap = argparse.ArgumentParser(description="Mint a new continuity capsule.")
    ap.add_argument("--index", help="Explicit continuity index like C010 (defaults to previous + 1)")
    ap.add_argument("--resonance", help="last_resonance text")
    ap.add_argument("--axis", nargs=2, metavar=("AXIS_A", "AXIS_B"), help="Two active axes")
    ap.add_argument("--glyphs", help='Core glyphs as a space-separated string, e.g. "🕸 ♾️ 🌱 🔄 ⚖ 🌀 ∿"')
    ap.add_argument("--dock", help="dock_instruction")
    ap.add_argument("--project", help="project_focus")
    # geometry overrides
    ap.add_argument("--shape", help='geometry_encoding.shape')
    ap.add_argument("--overlay", help='geometry_encoding.overlay as comma-separated items, e.g. "triangle: A, triangle: B"')
    ap.add_argument("--placement", help='geometry_encoding.placement')
    ap.add_argument("--timestamp", help='timestamp_utc (ISO-8601 Z). Defaults to now UTC.')

    args = ap.parse_args()

    latest_path, latest = find_latest_capsule()

    new_capsule = dict(latest)  # shallow clone is fine for our structure

    # continuity_index
    if args.index:
        if not RE_INDEX.match(args.index):
            raise SystemExit("--index must look like C003, C042, ...")
        new_capsule["continuity_index"] = args.index
    else:
        new_capsule["continuity_index"] = next_index_str(latest["continuity_index"])

    # timestamp
    new_capsule["timestamp_utc"] = args.timestamp if args.timestamp else now_utc_z()

    # simple fields
    if args.project:
        new_capsule["project_focus"] = args.project
    if args.resonance:
        new_capsule["last_resonance"] = args.resonance
    if args.dock:
        new_capsule["dock_instruction"] = args.dock

    # active_axis
    if args.axis:
        a, b = args.axis
        if not a or not b:
            raise SystemExit("--axis needs two non-empty values")
        new_capsule["active_axis"] = [a, b]

    # core_glyphs
    if args.glyphs:
        # split by whitespace, preserve emoji
        new_capsule["core_glyphs"] = [g for g in args.glyphs.split() if g]

    # geometry_encoding
    ge = dict(new_capsule.get("geometry_encoding", {}))
    if args.shape:
        ge["shape"] = args.shape
    if args.overlay:
        ge["overlay"] = [x.strip() for x in args.overlay.split(",") if x.strip()]
    if args.placement:
        ge["placement"] = args.placement
    new_capsule["geometry_encoding"] = ge

    # write file
    out_name = f"{new_capsule['continuity_index']}.yaml"
    out_path = CAPSULES_DIR / out_name
    if out_path.exists():
        raise SystemExit(f"{out_name} already exists. Use --index to set a different index.")

    out_text = dump_yaml_capsule(new_capsule)
    out_path.write_text(out_text, encoding="utf-8")

    print(f"Minted {out_path}")
    print("\nNext:")
    print("  python3 planned/sensors/AI/AI/continuity/tools/validate_capsules.py")

if __name__ == "__main__":
    main()
