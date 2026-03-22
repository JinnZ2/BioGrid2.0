"""Detect mutual exclusion violations in claims."""

from typing import Dict, List, Tuple


def find_conflicts(claims: List[Dict]) -> List[Tuple[str, str]]:
    """Return list of (proposition, conflict_type) for assert/deny pairs."""
    seen = {}
    conflicts = []
    for c in claims:
        key = c["text"].strip().lower()
        pol = c["polarity"]
        seen.setdefault(key, set()).add(pol)
        if "assert" in seen[key] and "deny" in seen[key]:
            conflicts.append((key, "assert/deny"))
    return conflicts


def score(claims: List[Dict]) -> float:
    """1.0 = fully consistent, 0.0 = heavily contradicted."""
    return max(0.0, 1.0 - 0.5 * len(find_conflicts(claims)))


def check(claims: List[Dict]) -> Dict:
    conflicts = find_conflicts(claims)
    return {
        "score": score(claims),
        "conflicts": [{"prop": p, "kind": k} for p, k in conflicts],
    }
