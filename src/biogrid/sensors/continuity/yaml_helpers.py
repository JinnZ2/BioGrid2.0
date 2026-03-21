"""
Minimal YAML IO for continuity capsules.

Prefers PyYAML if installed, otherwise uses a lightweight fallback parser
that handles the simple key:value + arrays structure of capsule YAML files.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List


def load_yaml_like(p: Path) -> Dict[str, Any]:
    """Load a capsule YAML file. Uses PyYAML if available, else naive parser."""
    try:
        import yaml  # type: ignore
        return yaml.safe_load(p.read_text(encoding="utf-8"))
    except Exception:
        return _fallback_parse(p)


def _fallback_parse(p: Path) -> Dict[str, Any]:
    """Naive YAML parser for capsule structure only."""
    data: Dict[str, Any] = {}
    array_key: str | None = None
    array_acc: List[str] = []
    in_geometry = False
    geometry: Dict[str, Any] = {}
    geometry_array_key: str | None = None
    geometry_array_acc: List[str] = []

    for raw in p.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip("\n")
        s = line.strip()
        if not s or s.startswith("#"):
            continue

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
            if not s.startswith(("- ", "shape:", "placement:", "overlay:")) and ":" in s:
                data["geometry_encoding"] = geometry
                in_geometry = False

        if ": " in s:
            k, v = s.split(": ", 1)
            k = k.strip()
            v = v.strip()
            if v == "":
                array_key = k
                array_acc = []
            elif v.startswith("[") and v.endswith("]"):
                inner = v[1:-1].strip()
                items = [x.strip().strip('"').strip("'") for x in inner.split(",")] if inner else []
                data[k] = [i for i in items if i]
            else:
                data[k] = v.strip('"').strip("'")
        elif s.endswith(":") and not s.startswith("- "):
            pass  # nested block start
        elif s.startswith("- ") and array_key:
            array_acc.append(s[2:].strip().strip('"').strip("'"))
        elif array_key and not s.startswith("- "):
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
    """Deterministic, human-friendly YAML for capsule structure."""
    def q(s: str) -> str:
        if any(ch in s for ch in [":", '"', "'"]) or s.strip() != s:
            return '"' + s.replace('"', '\\"') + '"'
        return s

    lines: List[str] = []
    lines.append(f"continuity_index: {c['continuity_index']}")
    lines.append(f'project_focus: {q(c["project_focus"])}')

    ax = c.get("active_axis", [])
    ax_inline = ", ".join(q(x) for x in ax)
    lines.append(f"active_axis: [{ax_inline}]")

    glyphs = c.get("core_glyphs", [])
    if glyphs and all(" " not in g for g in glyphs):
        lines.append(f"core_glyphs: [{', '.join(glyphs)}]")
    else:
        lines.append("core_glyphs:")
        for g in glyphs:
            lines.append(f"  - {q(g)}")

    lines.append(f'last_resonance: {q(c["last_resonance"])}')

    ge = c.get("geometry_encoding", {})
    lines.append("geometry_encoding:")
    lines.append(f'  shape: {q(ge.get("shape", ""))}')
    lines.append("  overlay:")
    for o in ge.get("overlay", []):
        lines.append(f"    - {q(o)}")
    lines.append(f'  placement: {q(ge.get("placement", ""))}')

    lines.append(f'dock_instruction: {q(c["dock_instruction"])}')
    lines.append(f'timestamp_utc: "{c["timestamp_utc"]}"')

    if "notes" in c and c["notes"]:
        lines.append(f'notes: {q(str(c["notes"]))}')
    if "meta" in c and isinstance(c["meta"], dict) and c["meta"]:
        lines.append("meta:")
        for k, v in c["meta"].items():
            lines.append(f"  {k}: {q(str(v))}")

    return "\n".join(lines) + "\n"
