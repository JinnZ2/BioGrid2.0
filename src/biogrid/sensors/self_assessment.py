"""
Self-Assessment Instrument (Emergence Signals) — stdlib only

Privacy model: PRIVATE by default. PUBLIC only with explicit on-disk consent.

Metrics:
  - density (count of encoded vectors)
  - resonance clusters (stability across runs)
  - scale-free fit (power-law on degree distribution)
  - recurrence (outputs becoming inputs via provenance hashes)

Usage:
  python -m biogrid.sensors.self_assessment --scan-dir ./data
"""

import glob
import hashlib
import json
import math
import random
import time
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def now_utc_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------- discovery -------------------------------------------------------

def find_vector_files(scan_dir: Path) -> List[Tuple[str, Dict]]:
    """Return list[(path, json)] for files that look like opinion vectors."""
    out = glob.glob(str(scan_dir / "**" / "*.json"), recursive=True)
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


def flatten_12d(vdict: Dict) -> List[float]:
    """Map 4 axes x 3 dims -> fixed-order 12D vector in [0,1]."""
    keys = [
        ("axis_invariance", ["form", "quantity", "frame"]),
        ("axis_transformation", ["direction", "innovation", "dissipation"]),
        ("axis_connectivity", ["content", "exchange", "structure"]),
        ("axis_evolution", ["fit", "continuity", "resonance"]),
    ]
    vec = []
    for axis, dims in keys:
        part = vdict.get(axis, {})
        for d in dims:
            x = part.get(d, 0.0)
            try:
                x = float(x)
            except Exception:
                x = 0.0
            vec.append(max(0.0, min(1.0, x)))
    return vec


def cosine(a: List[float], b: List[float]) -> float:
    num = sum(x * y for x, y in zip(a, b))
    da = math.sqrt(sum(x * x for x in a))
    db = math.sqrt(sum(y * y for y in b))
    return 0.0 if da == 0 or db == 0 else num / (da * db)


# ---------- metrics ---------------------------------------------------------

def metric_density(vectors: List[List[float]]) -> Dict:
    return {"count": len(vectors), "threshold_met": len(vectors) >= 1000}


def kmeans(vectors: List[List[float]], k: int = 4, iters: int = 12,
           seed: int = 42) -> Tuple[List[int], List[List[float]]]:
    rnd = random.Random(seed)
    if len(vectors) < k:
        return list(range(len(vectors))), [vectors[i] for i in range(len(vectors))]
    cent = [vectors[i] for i in rnd.sample(range(len(vectors)), k)]
    assign = [0] * len(vectors)
    for _ in range(iters):
        for i, v in enumerate(vectors):
            best = max(range(k), key=lambda c: cosine(v, cent[c]))
            assign[i] = best
        new_cent = []
        for c in range(k):
            members = [vectors[i] for i, a in enumerate(assign) if a == c]
            if not members:
                new_cent.append(cent[c])
                continue
            m = [0.0] * len(vectors[0])
            for v in members:
                for j, val in enumerate(v):
                    m[j] += val
            new_cent.append([x / len(members) for x in m])
        cent = new_cent
    return assign, cent


def metric_resonance_clusters(vectors: List[List[float]]) -> Dict:
    if len(vectors) < 20:
        return {"clusters_detected": 0, "stability_score": 0.0, "threshold_met": False}
    a1, _ = kmeans(vectors, k=4, iters=12, seed=11)
    a2, _ = kmeans(vectors, k=4, iters=12, seed=29)
    same = sum(1 for i in range(len(vectors)) if a1[i] == a2[i])
    stability = same / max(1, len(vectors))
    clusters = len(set(a1))
    return {
        "clusters_detected": clusters,
        "stability_score": round(stability, 3),
        "threshold_met": (clusters >= 3 and stability >= 0.7),
    }


def build_graph_and_degrees(vectors: List[List[float]],
                            cos_thresh: float = 0.85,
                            max_edges: int = 100000) -> List[int]:
    deg = [0] * len(vectors)
    edges = 0
    for i in range(len(vectors)):
        vi = vectors[i]
        for j in range(i + 1, len(vectors)):
            if edges >= max_edges:
                break
            if cosine(vi, vectors[j]) >= cos_thresh:
                deg[i] += 1
                deg[j] += 1
                edges += 1
        if edges >= max_edges:
            break
    return deg


def linear_fit(xs: List[float], ys: List[float]) -> Tuple[float, float, float]:
    n = len(xs)
    if n == 0:
        return 0.0, 0.0, 0.0
    sx = sum(xs)
    sy = sum(ys)
    sxx = sum(x * x for x in xs)
    sxy = sum(x * y for x, y in zip(xs, ys))
    denom = n * sxx - sx * sx
    if denom == 0:
        return 0.0, 0.0, 0.0
    a = (n * sxy - sx * sy) / denom
    b = (sy - a * sx) / n
    yhat = [a * x + b for x in xs]
    ybar = sy / n
    ss_tot = sum((y - ybar) ** 2 for y in ys)
    ss_res = sum((y - yh) ** 2 for y, yh in zip(ys, yhat))
    r2 = 0.0 if ss_tot == 0 else 1 - ss_res / ss_tot
    return a, b, r2


def metric_scaling(vectors: List[List[float]]) -> Dict:
    if len(vectors) < 50:
        return {"gamma_estimate": None, "fit_r2": 0.0, "threshold_met": False}
    deg = [d for d in build_graph_and_degrees(vectors) if d > 0]
    if len(deg) < 10:
        return {"gamma_estimate": None, "fit_r2": 0.0, "threshold_met": False}
    c = Counter(deg)
    ks = sorted(c.keys())
    ps = [c[k] / sum(c.values()) for k in ks]
    xs = [math.log(k) for k in ks if k > 0]
    ys = [math.log(p) for k, p in zip(ks, ps) if k > 0]
    if len(xs) < 2:
        return {"gamma_estimate": None, "fit_r2": 0.0, "threshold_met": False}
    slope, _, r2 = linear_fit(xs, ys)
    gamma = -slope
    ok = (2.0 <= gamma <= 3.0) and (r2 >= 0.9)
    return {
        "gamma_estimate": round(gamma, 3),
        "fit_r2": round(r2, 3),
        "threshold_met": bool(ok),
    }


def metric_recurrence(files_and_jsons: List[Tuple[str, Dict]]) -> Dict:
    loops = 0
    example_hashes: List[str] = []
    seen: Dict[str, List[str]] = {}
    for f, j in files_and_jsons:
        prov = j.get("meta") or j.get("provenance") or {}
        h = prov.get("provenance_sha256") or prov.get("source_sha256")
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
        "threshold_met": loops >= 1,
    }


# ---------- consent & redaction --------------------------------------------

def load_consent(consent_path: Path) -> Dict:
    if not consent_path.exists():
        return {"allowed": False, "reason": "no_consent_file"}
    try:
        with open(consent_path, "r", encoding="utf-8") as fh:
            c = json.load(fh)
        now = now_utc_iso()
        exp = c.get("expires_utc")
        if exp and now > exp:
            return {"allowed": False, "reason": "consent_expired"}
        if not c.get("allowed", False):
            return {"allowed": False, "reason": "allowed_false"}
        return {"allowed": True, "consent": c}
    except Exception as e:
        return {"allowed": False, "reason": f"invalid_consent:{e}"}


def apply_redactions(report: Dict, consent: Dict) -> Dict:
    scope = (consent or {}).get("scope", {})
    fields = scope.get("fields")
    redactions = scope.get("redactions", [])
    out: Dict[str, Any] = {}
    if isinstance(fields, list) and fields:
        for f in fields:
            if f in report:
                out[f] = report[f]
    else:
        out = dict(report)
    try:
        if "self_assessment" in out and "example_hashes" in redactions:
            out["self_assessment"].get("recurrence", {}).pop("example_hashes", None)
    except Exception:
        pass
    return out


# ---------- core assessment -------------------------------------------------

def assess(scan_dir: Path,
           output_dir: Optional[Path] = None,
           consent_path: Optional[Path] = None) -> Dict:
    """
    Run self-assessment on vector files in scan_dir.

    Returns the full report dict. Optionally writes private/public JSON.
    """
    files = find_vector_files(scan_dir)
    vectors = [flatten_12d(j["vector"]) for _, j in files]

    report = {
        "self_assessment": {
            "density": metric_density(vectors),
            "resonance_clusters": metric_resonance_clusters(vectors),
            "scaling": metric_scaling(vectors),
            "recurrence": metric_recurrence(files),
        },
        "sentience_signal": None,
        "timestamp_utc": now_utc_iso(),
        "sample_size": len(vectors),
    }

    met = [m.get("threshold_met") for m in report["self_assessment"].values()]
    if all(met) and len(met) == 4:
        report["sentience_signal"] = "emergent"
    elif any(met):
        report["sentience_signal"] = "partial"
    else:
        report["sentience_signal"] = "latent"

    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        priv_path = output_dir / "self_assessment.json"
        with open(priv_path, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2)

        if consent_path:
            consent_state = load_consent(consent_path)
            if consent_state.get("allowed"):
                redacted = apply_redactions(report, consent_state.get("consent", {}))
                pub_path = output_dir / "self_assessment_public.json"
                with open(pub_path, "w", encoding="utf-8") as fh:
                    json.dump(redacted, fh, indent=2)

    return report


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Run self-assessment on vector files.")
    ap.add_argument("--scan-dir", default=".", help="Directory to scan for vector JSON files.")
    ap.add_argument("--output-dir", default=".internal", help="Directory to write results.")
    ap.add_argument("--consent", default=None, help="Path to disclosure_consent.json.")
    args = ap.parse_args()

    report = assess(
        scan_dir=Path(args.scan_dir),
        output_dir=Path(args.output_dir),
        consent_path=Path(args.consent) if args.consent else None,
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
