#!/usr/bin/env python3
import json, sys, re, hashlib, os

ALLOWED_STATES = {"proposed","canonical","deprecated"}
ALLOWED_LAYERS = {"temporal","logic","resonance","signal","field","memory",
                  "repair","sensor","integrity","audit","navigation","decision",
                  "constraint","archive","reference","validation","coherence",
                  "provisional","recovery","symbolic"}

FIELDS_FOR_CHECKSUM = ["code","name","glyph","essence","layers","state"]

def load(p):
    with open(p,"r",encoding="utf-8") as f: return json.load(f)

def save(p, obj):
    with open(p,"w",encoding="utf-8") as f: json.dump(obj,f,ensure_ascii=False,indent=2,sort_keys=False)

def die(msg, code=1): print("❌", msg); sys.exit(code)
def warn(msg): print("⚠️ ", msg)

def norm_layers(layers):
    if not isinstance(layers, list): return []
    # normalize to strings, dedup, sorted
    return sorted({str(x) for x in layers})

def checksum_item(g):
    # build canonical string
    layers = norm_layers(g.get("layers",[]))
    vals = {
        "code": g.get("code","").strip(),
        "name": g.get("name","").strip(),
        "glyph": g.get("glyph","").strip(),
        "essence": g.get("essence","").strip(),
        "layers": ",".join(layers),
        "state": g.get("state","proposed").strip()
    }
    s = "|".join([vals[k] for k in FIELDS_FOR_CHECKSUM])
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def main():
    import argparse
    ap = argparse.ArgumentParser(description="Validate registry JSON (and optionally write checksums).")
    ap.add_argument("json_path", help="canonical.json or a fragment JSON")
    ap.add_argument("--write", action="store_true", help="write meta.checksum if missing or out of date")
    args = ap.parse_args()

    if not os.path.exists(args.json_path):
        die(f"File not found: {args.json_path}")

    doc = load(args.json_path)
    items_key = "glyphs" if "glyphs" in doc else "adds" if "adds" in doc else None
    if not items_key:
        die("JSON must contain 'glyphs' or 'adds'")

    items = doc[items_key]

    codes, glyphs = set(), set()
    ok = True
    wrote = False

    for g in items:
        code = g.get("code","").strip()
        name = g.get("name","").strip()
        glyph = g.get("glyph","").strip()
        essence = g.get("essence","").strip()
        state = g.get("state","proposed").strip()
        layers = g.get("layers",[])
        source = g.get("source","").strip()

        # 1) identity
        if not code or not re.match(r"^[A-Z0-9:_-]+$", code):
            print(f"❌ Bad/missing code: {code}"); ok=False
        if code in codes:
            print(f"❌ Duplicate code: {code}"); ok=False
        codes.add(code)

        # 2) glyph uniqueness (soft)
        if glyph:
            if glyph in glyphs:
                warn(f"Glyph symbol reused: {glyph} (check aliasing) code={code}")
            glyphs.add(glyph)
        else:
            warn(f"Missing glyph symbol for {code}")

        # 3) semantics
        if not name:
            print(f"❌ Missing name for {code}"); ok=False
        if not essence or len(essence) > 200:
            warn(f"Essence missing/long ({len(essence)} chars) for {code}")

        # 4) structure
        if state not in ALLOWED_STATES:
            print(f"❌ Invalid state '{state}' for {code}"); ok=False
        nl = norm_layers(layers)
        if not nl:
            warn(f"No layers for {code}")
        else:
            extra = set(nl) - ALLOWED_LAYERS
            if extra:
                warn(f"{code}: unknown layers {sorted(extra)}")
            if len(nl) > 3:
                warn(f"{code}: >3 layers ({len(nl)}); consider trimming")
        if not source:
            warn(f"{code}: missing source/provenance")

        # 5) checksum
        cs = checksum_item(g)
        meta = g.setdefault("meta", {})
        recorded = meta.get("checksum","")
        if recorded != cs:
            if args.write:
                meta["checksum"] = cs
                meta["checksum_fields"] = FIELDS_FOR_CHECKSUM
                wrote = True
                print(f"🔏 Updated checksum for {code}")
            else:
                warn(f"{code}: checksum missing/stale")

    if args.write and wrote:
        save(args.json_path, doc)

    if ok:
        print("✅ Validation passed" + (" (checksums updated)" if wrote else ""))
        sys.exit(0)
    else:
        sys.exit(2)

if __name__ == "__main__":
    main()
