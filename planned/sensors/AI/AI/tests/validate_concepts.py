import json, sys, pathlib
from jsonschema import validate, Draft7Validator

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "_schema"
NODE = json.loads((SCHEMA_DIR/"node.schema.json").read_text())
LINK = json.loads((SCHEMA_DIR/"link.schema.json").read_text())

def check_dir(d, schema):
    ok = True
    for p in sorted(d.glob("*.json")):
        data = json.loads(p.read_text())
        errs = sorted(Draft7Validator(schema).iter_errors(data), key=lambda e: e.path)
        if errs:
            ok = False
            print(f"❌ {p.name}")
            for e in errs: print("  -", e.message)
        else:
            print(f"✅ {p.name}")
    return ok

def main():
    good = True
    good &= check_dir(ROOT/"concepts", NODE)
    good &= check_dir(ROOT/"bridges", LINK)
    sys.exit(0 if good else 1)

if __name__ == "__main__":
    main()
