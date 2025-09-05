#!/usr/bin/env python3
import json, sys
def load(p): 
    with open(p,"r",encoding="utf-8") as f: return json.load(f)
if len(sys.argv)<2:
    print("Usage: list_checksums.py canonical.json"); sys.exit(1)
doc = load(sys.argv[1])
items = doc.get("glyphs", doc.get("adds", []))
for g in items:
    print(f"{g.get('code')}: {g.get('meta',{}).get('checksum','<none>')}")
