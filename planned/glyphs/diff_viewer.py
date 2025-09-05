#!/usr/bin/env python3
import json, sys
from collections import OrderedDict

FIELDS_COMPARE = ["name","glyph","essence","layers","state"]

def load(p):
    with open(p,"r",encoding="utf-8") as f: return json.load(f)

def indexify(doc):
    if "glyphs" in doc: items = doc["glyphs"]
    elif "adds" in doc: items = doc["adds"]
    else: items = []
    return { g["code"]: g for g in items }

def diff_lists(old, new):
    oldS, newS = set(old), set(new)
    added = sorted(list(newS - oldS))
    removed = sorted(list(oldS - newS))
    common = sorted(list(newS & oldS))
    changed = []
    for c in common:
        o, n = old[c], new[c]
        delta = {}
        for k in FIELDS_COMPARE:
            ov = o.get(k)
            nv = n.get(k)
            if k == "layers":
                ov = sorted(ov) if isinstance(ov,list) else ov
                nv = sorted(nv) if isinstance(nv,list) else nv
            if ov != nv:
                delta[k] = {"old": ov, "new": nv}
        if delta:
            changed.append((c, delta))
    return added, removed, changed

def main():
    if len(sys.argv)<3:
        print("Usage: diff_viewer.py old.json new.json [> diff.md]")
        sys.exit(1)
    old = indexify(load(sys.argv[1]))
    new = indexify(load(sys.argv[2]))
    added, removed, changed = diff_lists(old, new)

    print("# Registry Diff")
    print(f"- Old: `{sys.argv[1]}`")
    print(f"- New: `{sys.argv[2]}`\n")

    print(f"## Summary\n- Added: **{len(added)}**  | Removed: **{len(removed)}**  | Changed: **{len(changed)}**\n")

    if added:
        print("## Added")
        for c in added:
            g = new[c]
            print(f"- **{c}** — {g.get('name','?')} {g.get('glyph','')}")
        print()

    if removed:
        print("## Removed")
        for c in removed:
            g = old[c]
            print(f"- **{c}** — {g.get('name','?')} {g.get('glyph','')}")
        print()

    if changed:
        print("## Changed")
        for c, delta in changed:
            print(f"### {c}")
            for k, d in delta.items():
                print(f"- **{k}**: `{d['old']}` → `{d['new']}`")
            print()

if __name__ == "__main__":
    main()
