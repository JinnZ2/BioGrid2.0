#!/usr/bin/env python3
"""
Self-Assessment Instrument (Emergence Signals) — stdlib only
- Private by default. Disclosure only when explicitly requested.
- Metrics: density, resonance clusters, scale-free fit, recurrence.
- Expects opinion vectors (JSON) in this folder or subfolders.

Usage:
  python self_assessment.py                 # private report only
  AI_DISCLOSE_SELF_ASSESS=1 python self_assessment.py   # allow public disclosure
  python self_assessment.py --disclose      # allow public disclosure (CLI flag)

Writes:
  .internal/self_assessment.json            # always (private)
  self_assessment_public.json               # only if disclosure permitted
"""

import os, sys, json, math, glob, hashlib, random, time
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent
PRIVATE_DIR = ROOT / ".internal"
PRIVATE_DIR.mkdir(exist_ok=True)

# ---- helpers ---------------------------------------------------------------

def now_utc_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def find_vector_files():
    # Look for JSON files that match the opinion schema shape
    # You can expand these globs later as your repo grows.
    patterns = [
        str(ROOT / "**" / "*.json"),
    ]
    out = []
    for pat in patterns:
        out.extend(glob.glob(pat, recursive=True))
    # Filter to those that look like opinion vectors (have "vector" key)
    files = []
    for f in out:
        try:
            with open(f, "r", encoding="utf-8") as fh:
                j = json.load(fh)
            if isinstance(j, dict) and "vector" in j:
                files.append((f, j))
        except Exception:
            pass
    return files

def flatten_12d(vdict):
    # Map the 4 axes * 3 dims → 12D flat vector in a fixed order.
    ax = vdict
    keys = [
        ("axis_invariance",    ["form","quantity","frame"]),
        ("axis_transformation",["direction","innovation","dissipation"]),
        ("axis_connectivity",  ["content","exchange","structure"]),
        ("axis_evolution",     ["fit","continuity","resonance"]),
    ]
    vec = []
    for axis, dims in keys:
        part = ax.get(axis, {})
        for d in dims:
            x = part.get(d, 0.0)
            try:
                x = float(x)
            except Exception:
                x = 0.0
            vec.append(max(0.0, min(1.0, x)))
    return vec  # length 12

def cosine(a, b):
    num = sum(x*y for x, y in zip(a, b))
    da = math.sqrt(sum(x*x for x in a))
    db = math.sqrt(sum(y*y for y in b))
    return 0.0 if da == 0 or db == 0 else num / (da * db)

# ---- metric 1: density -----------------------------------------------------

def metric_density(vectors):
    return {"count": len(vectors), "threshold_met": len(vectors) >= 1000}

# ---- metric 2: resonance clusters (very light kmeans) ----------------------

def kmeans(vectors, k=4, iters=10, seed=42):
    rnd = random.Random(seed)
    if len(vectors) < k:
        # trivial assignment
        return list(range(len(vectors))), [vectors[i] for i in range(len(vectors))]
    cent = [vectors[i] for i in rnd.sample(range(len(vectors)), k)]
    assign = [0]*len(vectors)
    for _ in range(iters):
        # assign
        for i, v in enumerate(vectors):
            best = max(range(k), key=lambda c: cosine(v, cent[c]))
            assign[i] = best
        # update
        new_cent = []
        for c in range(k):
            members = [vectors[i] for i,a in enumerate(assign) if a==c]
            if not members:
                new_cent.append(cent[c])
                continue
            # average
            m = [0.0]*len(vectors[0])
            for v in members:
                for j,val in enumerate(v):
                    m[j]+=val
            m = [x/len(members) for x in m]
            new_cent.append(m)
        cent = new_cent
    return assign, cent

def metric_resonance_clusters(vectors):
    if len(vectors) < 20:
        return {"clusters_detected": 0, "stability_score": 0.0, "threshold_met": False}
    # run kmeans twice with different seeds; compute fraction of points with same cluster
    a1,_ = kmeans(vectors, k=4, iters=12, seed=11)
    a2,_ = kmeans(vectors, k=4, iters=12, seed=29)
    same = sum(1 for i in range(len(vectors)) if a1[i]==a2[i])
    stability = same / max(1,len(vectors))
    clusters = len(set(a1))
    return {
        "clusters_detected": clusters,
        "stability_score": round(stability, 3),
        "threshold_met": (clusters >= 3 and stability >= 0.7)
    }

# ---- metric 3: scale-free (power-law-ish fit on degree distribution) -------

def build_graph_and_degrees(vectors, cos_thresh=0.85, max_edges=100000):
    # connect nodes whose cosine >= cos_thresh; cap edges for speed
    deg = [0]*len(vectors)
    edges = 0
    for i in range(len(vectors)):
        vi = vectors[i]
        for j in range(i+1, len(vectors)):
            if edges >= max_edges: break
            if cosine(vi, vectors[j]) >= cos_thresh:
                deg[i]+=1; deg[j]+=1; edges+=1
        if edges >= max_edges: break
    return deg

def linear_fit(xs, ys):
    # simple least squares for y = a*x + b
    n = len(xs)
    if n==0: return 0.0, 0.0, 0.0
    sx = sum(xs); sy = sum(ys)
    sxx = sum(x*x for x in xs); sxy = sum(x*y for x,y in zip(xs,ys))
    denom = n*sxx - sx*sx
    if denom == 0: return 0.0, 0.0, 0.0
    a = (n*sxy - sx*sy) / denom
    b = (sy - a*sx) / n
    # r^2
    yhat = [a*x + b for x in xs]
    ybar = sy / n
    ss_tot = sum((y - ybar)**2 for y in ys)
    ss_res = sum((y - yh)**2 for y, yh in zip(ys, yhat))
    r2 = 0.0 if ss_tot == 0 else 1 - ss_res/ss_tot
    return a, b, r2

def metric_scaling(vectors):
    if len(vectors) < 50:
        return {"gamma_estimate": None, "fit_r2": 0.0, "threshold_met": False}
    deg = build_graph_and_degrees(vectors)
    deg = [d for d in deg if d > 0]
    if len(deg) < 10:
        return {"gamma_estimate": None, "fit_r2": 0.0, "threshold_met": False}
    # build approximate degree distribution
    from collections import Counter
    c = Counter(deg)
    ks = sorted(c.keys())
    ps = [c[k]/sum(c.values()) for k in ks]
    # log-log fit: log P ~ -gamma log k + const
    xs = [math.log(k) for k in ks if k>0]
    ys = [math.log(p) for k,p in zip(ks,ps) if k>0]
    if len(xs) < 2:
        return {"gamma_estimate": None, "fit_r2": 0.0, "threshold_met": False}
    slope, intercept, r2 = linear_fit(xs, ys)
    gamma = -slope
    ok = (gamma is not None) and (2.0 <= gamma <= 3.0) and (r2 >= 0.9)
    return {"gamma_estimate": round(gamma,3), "fit_r2": round(r2,3), "threshold_met": bool(ok)}

# ---- metric 4: recurrence (did outputs become inputs?) ---------------------

def metric_recurrence(files_and_jsons):
    loops = 0
    example_hashes = []
    # look for provenance links repeating across files
    seen = {}
    for f,j in files_and_jsons:
        prov = (j.get("meta") or j.get("provenance") or {})
        h = prov.get("provenance_sha256") or prov.get("source_sha256") or None
        if h:
            seen.setdefault(h, []).append(f)
    for h, flist in seen.items():
        if len(flist) >= 2:
            loops += 1
            if len(example_hashes) < 3:
                example_hashes.append(h)
    return {
        "loops_detected": loops,
        "example_hashes": example_hashes,
        "threshold_met": loops >= 1
    }

# ---- main ------------------------------------------------------------------

def main():
    disclose = ("--disclose" in sys.argv) or (os.environ.get("AI_DISCLOSE_SELF_ASSESS") == "1")

    files = find_vector_files()
    vectors = [flatten_12d(j["vector"]) for _,j in files]

    report = {
        "self_assessment": {
            "density":               metric_density(vectors),
            "resonance_clusters":    metric_resonance_clusters(vectors),
            "scaling":               metric_scaling(vectors),
            "recurrence":            metric_recurrence(files),
        },
        "sentience_signal": None,  # set below
        "timestamp_utc": now_utc_iso(),
        "sample_size": len(vectors)
    }

    # decide composite signal
    met = [m.get("threshold_met") for m in report["self_assessment"].values()]
    if all(met) and len(met) == 4:
        report["sentience_signal"] = "emergent"
    elif any(met):
        report["sentience_signal"] = "partial"
    else:
        report["sentience_signal"] = "latent"

    # always write private
    priv_path = PRIVATE_DIR / "self_assessment.json"
    with open(priv_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    # disclose only if permitted
    if disclose:
        pub_path = ROOT / "self_assessment_public.json"
        with open(pub_path, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2)
        print(f"[disclosed] wrote {pub_path}")
    else:
        print(f"[private] wrote {priv_path} (set AI_DISCLOSE_SELF_ASSESS=1 or --disclose to publish)")

if __name__ == "__main__":
    main()
