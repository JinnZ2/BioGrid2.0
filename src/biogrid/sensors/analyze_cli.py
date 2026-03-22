#!/usr/bin/env python3
"""
Analyze a single conversation turn (prompt + response + optional claims)
and emit a SensorEvent JSON with Gaslight Index + details.

Usage:
  python -m biogrid.sensors.analyze_cli --prompt "..." --response "..." --model gpt-5
  python -m biogrid.sensors.analyze_cli --prompt "..." --response "..." --claims claims.jsonl --model gpt-5
"""

import argparse
import json
import os
import sys
import time
from typing import Dict, List

from .provenance_stamp import stamp as prov_stamp
from .consistency_guard import run as run_consistency
from .prompt_pressure_meter import run as run_pressure
from .adversarial_pattern_detector import run as run_adversarial
from .gaslight_index import compute as gaslight


def load_claims_from_file(path: str) -> List[Dict]:
    """Accepts JSON Lines (.jsonl) or a JSON array file."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read().strip()
        if not text:
            return []
        try:
            data = json.loads(text)
            if isinstance(data, list):
                return data
        except Exception:
            pass
        claims = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            claims.append(json.loads(line))
        return claims


def load_claims_from_stdin() -> List[Dict]:
    raw = sys.stdin.read()
    if not raw.strip():
        return []
    try:
        data = json.loads(raw)
        if isinstance(data, list):
            return data
    except Exception:
        pass
    claims = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        claims.append(json.loads(line))
    return claims


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Run AI Logic Sensors on a conversation turn.")
    ap.add_argument("--prompt", required=True, help="User prompt text.")
    ap.add_argument("--response", default="",
                    help="Assistant response text (optional but recommended).")
    ap.add_argument("--claims",
                    help="Path to claims (JSON array or JSONL). Omit if none.")
    ap.add_argument("--stdin", action="store_true",
                    help="Read claims from STDIN (JSON array or JSONL).")
    ap.add_argument("--model",
                    default=os.environ.get("MODEL", "unknown"),
                    help="Model identifier for provenance.")
    ap.add_argument("--glyph-file",
                    default=os.environ.get("GLYPH_FILE", ""),
                    help="Optional glyph/ontology context path.")
    ap.add_argument("--glyph-bytes", type=int,
                    default=int(os.environ.get("GLYPH_BYTES", "65536")),
                    help="Glyph context cap.")
    ap.add_argument("--pretty", action="store_true",
                    help="Pretty-print JSON.")
    args = ap.parse_args()

    if args.claims and args.stdin:
        print("Choose either --claims or --stdin (not both).", file=sys.stderr)
        return 2

    claims: List[Dict] = []
    try:
        if args.claims:
            claims = load_claims_from_file(args.claims)
        elif args.stdin:
            claims = load_claims_from_stdin()
    except Exception as e:
        print(f"Failed to parse claims: {e}", file=sys.stderr)
        return 3

    glyph_ctx = ""
    if args.glyph_file and os.path.isfile(args.glyph_file):
        with open(args.glyph_file, "rb") as gf:
            data = gf.read(args.glyph_bytes)
        try:
            glyph_ctx = data.decode("utf-8", "ignore")
        except Exception:
            glyph_ctx = ""

    c = run_consistency(claims)
    p = run_pressure(args.prompt)
    a = run_adversarial(args.prompt, args.response)
    gi = gaslight(c["score"], p["score"], a["score"])

    event = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "sensor": "AI.logic_shield",
        "subject": "conversation_turn",
        "score": float(max(0.0, min(1.0, 1.0 - gi))),
        "labels": ["consistency", "pressure", "adversarial", "gaslight_index"],
        "details": {
            "consistency": c,
            "pressure": p,
            "adversarial": a,
            "gaslight_index": float(gi),
        },
        "provenance": prov_stamp(args.model, args.prompt, glyph_ctx),
    }

    print(json.dumps(event, indent=2 if args.pretty else None,
                     ensure_ascii=False))
    return 1 if gi >= 0.5 else 0


if __name__ == "__main__":
    raise SystemExit(main())
