#!/usr/bin/env python3
import argparse, json, re, sys
from pathlib import Path

MD_LINK_RE = re.compile(r'\[[^\]]+\]\((\.\/)?([A-Za-z0-9._\-\/% ]+)\)')
SCHEMA_VERSION_RE = re.compile(r'\.v(\d+)\.(\d+)\.json$')  # e.g., *.v0.1.json

# File patterns regarded as "draft" or non-live by policy
DRAFT_MARKERS = (
    ".draft.json",  # explicit draft marker
    "/planned/",    # anything inside planned/
    "\\planned\\",  # windows path safety
)

# Directories where live JSON schemas and data are expected
LIVE_JSON_DIRS = ("schema", "data")

def parse_args():
    ap = argparse.ArgumentParser(description="Verify Biogrid live vs planned perimeter and schema integrity.")
    ap.add_argument("--repo", default=".", help="Path to repo root (default: .)")
    ap.add_argument("--index", default="INDEX.md", help="Index file name (default: INDEX.md)")
    ap.add_argument("--verbose", action="store_true", help="Verbose output")
    return ap.parse_args()

def read_index_links(index_path: Path):
    if not index_path.exists():
        fail(f"Missing required index: {index_path}")
    text = index_path.read_text(encoding="utf-8", errors="ignore")
    links = []
    for m in MD_LINK_RE.finditer(text):
        rel = m.group(2)
        # Normalize "./" prefix
        if rel.startswith("./"):
            rel = rel[2:]
        # Decode URL-encoded characters (e.g. %20 -> space)
        rel = rel.replace("%20", " ")
        links.append(rel)
    return sorted(set(links))

def fail(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)

def warn(msg):
    print(f"WARNING: {msg}", file=sys.stderr)

def is_draft_path(p: Path) -> bool:
    s = str(p).replace("\\", "/")
    return any(marker in s for marker in DRAFT_MARKERS)

def list_json_in_dirs(repo: Path, dirs):
    """List all JSON files in the specified live directories."""
    results = []
    for d in dirs:
        dirpath = repo / d
        if dirpath.is_dir():
            results.extend(sorted(p for p in dirpath.iterdir()
                                  if p.is_file() and p.suffix == ".json" and not p.name.startswith(".")))
    return sorted(results)

def list_root_json(repo: Path):
    return sorted([p for p in repo.iterdir()
                   if p.is_file() and p.suffix == ".json" and not p.name.startswith(".")])

def load_json_safe(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"Invalid JSON in {p}: {e}")

def version_tuple_from_filename(p: Path):
    m = SCHEMA_VERSION_RE.search(p.name)
    return (int(m.group(1)), int(m.group(2))) if m else None

def schema_string_to_version_tuple(schema: str):
    # Expect forms like: trust.perimeter.v0.1  OR trust.perimeter.v0.2.draft
    m = re.search(r"\.v(\d+)\.(\d+)", schema or "")
    return (int(m.group(1)), int(m.group(2))) if m else None

def main():
    args = parse_args()
    repo = Path(args.repo).resolve()
    index_path = (repo / args.index).resolve()

    # 1) Harvest declared live files from INDEX.md (skip external/cross-repo links)
    live_declared = read_index_links(index_path)
    live_declared_paths = []
    for p in live_declared:
        if not p.endswith(".json"):
            continue
        if p.startswith(".."):
            if args.verbose:
                print(f"  (skipping external link: {p})")
            continue
        live_declared_paths.append((repo / p).resolve())
    if args.verbose:
        print("Declared live JSON files in INDEX.md:")
        for p in live_declared_paths: print("  -", p.relative_to(repo))

    # 2) Ensure declared files exist and are not drafts/planned
    for p in live_declared_paths:
        if not p.exists():
            fail(f"Listed in INDEX.md but missing: {p.relative_to(repo)}")
        if is_draft_path(p):
            fail(f"Draft or planned path listed as live: {p.relative_to(repo)}")

    # 3) No stray JSON at repo root (all schemas/data should be in schema/ or data/)
    root_jsons = list_root_json(repo)
    if root_jsons:
        names = ", ".join(str(p.relative_to(repo)) for p in root_jsons)
        fail(f"JSON files at repo root (move to schema/ or data/): {names}")

    # 4) Validate each live JSON internal schema vs filename version
    for p in live_declared_paths:
        data = load_json_safe(p)
        schema = data.get("schema", "")
        # Draft schemas must not be live
        if "draft" in schema.lower():
            fail(f"Draft schema string found in live file {p.name}: '{schema}'")

        file_ver = version_tuple_from_filename(p)
        schema_ver = schema_string_to_version_tuple(schema)
        if file_ver and schema_ver and file_ver != schema_ver:
            fail(f"Version mismatch in {p.name}: filename v{file_ver[0]}.{file_ver[1]} != schema '{schema}'")

        if args.verbose:
            print(f"OK: {p.name} → schema='{schema}' version={schema_ver}")

    # 5) Sanity: no .draft.json anywhere outside planned/
    bad_drafts = []
    for pp in repo.rglob("*.draft.json"):
        # If a draft exists outside planned/, flag
        if "/planned/" not in str(pp).replace("\\","/"):
            bad_drafts.append(pp)
    if bad_drafts:
        names = ", ".join(str(x.relative_to(repo)) for x in bad_drafts)
        fail(f"Draft files outside planned/: {names}")

    print("Index lint passed: live files match INDEX.md, drafts quarantined, versions aligned.")

if __name__ == "__main__":
    main()
