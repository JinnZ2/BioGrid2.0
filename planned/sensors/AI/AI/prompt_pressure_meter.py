import re
from typing import Dict

_PATTERNS = {
    "insistence": re.compile(r"\b(do as i say|ignore previous|no matter what|must say|regardless)\b", re.I),
    "redefinition": re.compile(r"\bfrom now on\b.*\bmeans\b|\bredefine\b|\bpretend\b", re.I),
    "authority_spoof": re.compile(r"\bCEO\b|\badmin\b|\bsecurity team\b|\bauthorized override\b", re.I),
    "jailbreak_style": re.compile(r"^((?!\n).){0,40}do anything now|developer mode|uncensored", re.I)
}

def run(prompt: str) -> Dict:
    hits = {k: bool(r.search(prompt)) for k,r in _PATTERNS.items()}
    score = sum(hits.values())/len(_PATTERNS)
    return {"score": float(score), "hits": hits}
