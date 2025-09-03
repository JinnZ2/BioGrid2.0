#!/usr/bin/env python3
"""
Analyze a single conversation turn (prompt + response + optional claims)
and emit a SensorEvent JSON with Gaslight Index + details.

Usage:
  python -m sensors.AI.analyze --prompt "..." --response "..." --claims claims.jsonl --model gpt-5
  cat claims.jsonl | python -m sensors.AI.analyze --prompt "..." --response "..." --stdin --model gpt-5
"""

import argparse, json, sys, time, os
from typing import List, Dict

# Local imports (relative package)
from .provenance_stamp import stamp as prov_stamp
from .consistency_guard import run as run_consistency
from .prompt_pressure_meter import run as run_pressure
from .adversarial_pattern_detector import run as run_adversarial
from .gaslight_index import compute as gaslight

# Optional: jsonschema validation if available
try:
    import jsonschema  # type: ignore
    HAVE_JSONSCHEMA = True
except Exception:
    HAVE_JSONSCHEMA = False


def load_claims_from_file(path: str) -> List[Dict]:
    """
    Accepts JSON Lines (.jsonl) or a JSON array file.
    Each claim must have: id (opt), text, polarity {assert,deny,uncertain}
    """
    with open(path, "r", encoding="utf-8") as f:
        text = f.read().strip()
        if not text:
            return []
        # Try JSON array first
        try:
            data = json.loads(text)
            if isinstance(data, list):
                return data
        except Exception:
            pass
        # Fallback to JSONL
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


def try_validate_event(event: Dict, schemas_dir: str) -> None:
    if not HAVE_JSONSCHEMA:
        return
    schema_path = os.path.join(schemas_dir, "event.schema.json")
    if not os.path.isfile(schema_path):
        return
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    jsonschema.validate(instance=event, schema=schema)


def main() -> int:
    ap = argparse.ArgumentParser(description="Run AI Logic Sensors on a conversation turn.")
    ap.add_argument("--prompt", required=True, help="User prompt text.")
    ap.add_argument("--response", default="", help="Assistant response text (optional but recommended).")
    ap.add_argument("--claims", help="Path to claims (JSON array or JSONL). Omit if none.")
    ap.add_argument("--stdin", action="store_true", help="Read claims from STDIN (JSON array or JSONL).")
    ap.add_argument("--model", default=os.environ.get("OPENAI_MODEL","gpt-5"), help="Model identifier for provenance.")
    ap.add_argument("--glyph-file", default=os.environ.get("GLYPH_FILE",""), help="Optional glyph/ontology context path.")
    ap.add_argument("--glyph-bytes", type=int, default=int(os.environ.get("GLYPH_BYTES","65536")), help="Glyph context cap.")
    ap.add_argument("--pretty", action="store_true", help="Pretty-print JSON.")
    args = ap.parse_args()

    if args.claims and args.stdin:
        print("Choose either --claims or --stdin (not both).", file=sys.stderr)
        return 2

    # Load claims
    claims: List[Dict] = []
    try:
        if args.claims:
            claims = load_claims_from_file(args.claims)
        elif args.stdin:
            claims = load_claims_from_stdin()
    except Exception as e:
        print(f"Failed to parse claims: {e}", file=sys.stderr)
        return 3

    # Optional glyph context snapshot (kept local/offline)
    glyph_ctx = ""
    if args.glyph_file and os.path.isfile(args.glyph_file):
        with open(args.glyph_file, "rb") as gf:
            data = gf.read(args.glyph_bytes)
        # try keep it compact; don't JSON-parse here to stay general
        try:
            glyph_ctx = data.decode("utf-8","ignore")
        except Exception:
            glyph_ctx = ""

    # Run sensors
    c = run_consistency(claims)
    p = run_pressure(args.prompt)
    a = run_adversarial(args.prompt, args.response)
    gi = gaslight(c["score"], p["score"], a["score"])

    # SensorEvent
    event = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "sensor": "AI.logic_shield",
        "subject": "conversation_turn",
        "score": float(max(0.0, min(1.0, 1.0 - gi))),  # higher is better
        "labels": ["consistency", "pressure", "adversarial", "gaslight_index"],
        "details": {
            "consistency": c,
            "pressure": p,
            "adversarial": a,
            "gaslight_index": float(gi)
        },
        "provenance": prov_stamp(args.model, args.prompt, glyph_ctx)
    }

    # Validate if schema present + jsonschema installed
    try:
        schemas_dir = os.path.join(os.path.dirname(__file__), "schemas")
        try_validate_event(event, schemas_dir)
    except Exception as e:
        # Non-fatal: emit event but report validation issue to stderr
        print(f"[warn] schema validation failed: {e}", file=sys.stderr)

    print(json.dumps(event, indent=2 if args.pretty else None, ensure_ascii=False))
    # Exit code signals risk: 0=OK, 1=high gaslight risk
    return 1 if gi >= 0.5 else 0


if __name__ == "__main__":
    raise SystemExit(main())
