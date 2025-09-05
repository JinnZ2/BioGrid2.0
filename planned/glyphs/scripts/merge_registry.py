#!/usr/bin/env python3
import json, os, glob, sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
canon_path = os.path.join(ROOT, "canonical.json")
frag_dir   = os.path.join(ROOT, "fragments")

def load_json(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(p, obj):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=False)

# Load or init canonical
if os.path.exists(canon_path):
    canon = load_json(canon_path)
else:
    canon = {"version":"2.3", "updated": datetime.utcnow().isoformat()+"Z", "glyphs": []}

# Build index by code
index = {g["code"]: g for g in canon.get("glyphs", [])}

# Merge fragments
for fp in sorted(glob.glob(os.path.join(frag_dir, "*.json"))):
    frag = load_json(fp)
    for add in frag.get("adds", []):
        code = add["code"]
        if code not in index:
            # new glyph → canonicalize if proposed
            if add.get("state") == "proposed":
                add["state"] = "canonical"
            add.setdefault("provenance_chain", []).append(frag.get("provenance","unknown"))
            index[code] = add
        else:
            # already present → merge fields gently, extend provenance
            g = index[code]
            for k,v in add.items():
                if k in ("code",): 
                    continue
                if k == "layers":
                    g.setdefault("layers", [])
                    g["layers"] = sorted(set(g["layers"]) | set(v))
                elif k == "meta":
                    g.setdefault("meta", {}).update(v)
                else:
                    # keep existing canonical values; do not overwrite glyph/name/glyph unless explicitly blank
                    if k not in g or (isinstance(g[k], str) and not g[k].strip()):
                        g[k] = v
            g.setdefault("provenance_chain", []).append(frag.get("provenance","unknown"))

    # handle edits
    for ed in frag.get("edits", []):
        c = ed.get("code")
        if c in index and ed.get("op") == "rename":
            index[c]["name"] = ed.get("to_name", index[c]["name"])

    # handle deprecations
    for dep in frag.get("deprecations", []):
        c = dep.get("code")
        if c in index:
            index[c]["state"] = "deprecated"
            index[c].setdefault("meta", {})["deprecation_reason"] = dep.get("reason","")

# Write back
canon["glyphs"] = sorted(index.values(), key=lambda g: g["code"])
canon["updated"] = datetime.utcnow().isoformat()+"Z"
save_json(canon_path, canon)

print(f"Merged {len(glob.glob(os.path.join(frag_dir,'*.json')))} fragment file(s) into canonical.json")
