#!/usr/bin/env python3
import json, sys, re
ALLOWED_STATES = {"proposed","canonical","deprecated"}
ALLOWED_LAYERS = {"temporal","logic","resonance","signal","field","memory",
                  "repair","sensor","integrity","audit","navigation",
                  "decision","constraint","archive","reference","validation",
                  "coherence","provisional","recovery","symbolic"}

def load(p): 
    with open(p,"r",encoding="utf-8") as f: return json.load(f)

def die(msg): print("❌", msg); sys.exit(1)
def warn(msg): print("⚠️ ", msg)

def main():
    if len(sys.argv)<2: die("Usage: auto_validator.py canonical_or_fragment.json")
    doc = load(sys.argv[1])
    # accept either {"glyphs":[...]} or {"adds":[...]}
    items = []
    if "glyphs" in doc: items = doc["glyphs"]
    elif "adds" in doc: items = doc["adds"]
    else: die("JSON must contain 'glyphs' or 'adds'")

    codes, glyphs = set(), set()
    ok = True
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
        if not isinstance(layers, list) or not layers:
            warn(f"No layers for {code}")
        else:
            extra = set(layers) - ALLOWED_LAYERS
            if extra:
                warn(f"{code}: unknown layers {sorted(extra)}")
            if len(layers) > 3:
                warn(f"{code}: >3 layers ({len(layers)}); consider trimming")
        if not source:
            warn(f"{code}: missing source/provenance")
        # 5) relations (optional, nudge)
        for f in ("relates_to","conflicts_with","supersedes"):
            if f in g and not isinstance(g[f], list):
                warn(f"{code}: {f} should be a list")
    if ok: 
        print("✅ Validation passed (with warnings as above)" if glyphs else "✅ Basic validation passed")
    else:
        sys.exit(2)

if __name__ == "__main__":
    main()
