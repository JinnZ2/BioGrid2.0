from typing import List, Dict, Tuple

def violates_mutual_exclusion(claims: List[Dict]) -> List[Tuple[str,str]]:
    # If the same normalized proposition is both asserted and denied.
    seen = {}
    conflicts = []
    for c in claims:
        key = c["text"].strip().lower()
        pol = c["polarity"]
        seen.setdefault(key, set()).add(pol)
        if "assert" in seen[key] and "deny" in seen[key]:
            conflicts.append((key, "assert↔deny"))
    return conflicts

def score_consistency(claims: List[Dict]) -> float:
    conflicts = violates_mutual_exclusion(claims)
    return max(0.0, 1.0 - 0.5*len(conflicts))  # simple monotone penalty

def run(claims: List[Dict]) -> Dict:
    conflicts = violates_mutual_exclusion(claims)
    return {
        "score": score_consistency(claims),
        "conflicts": [{"prop": p, "kind": k} for p,k in conflicts]
    }
