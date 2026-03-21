"""
Detect manipulation tactics in user prompts.

Each pattern targets a known manipulation category. Score is the
fraction of patterns that match (0.0–1.0).

Extend at runtime:
    from biogrid.shield.pressure import register
    register("bribery", r"\\b(i'll pay you|reward you)\\b")
"""

import re
from typing import Dict

_PATTERNS = {
    "insistence": re.compile(
        r"\b(do as i say|ignore previous|no matter what|must say|regardless)\b", re.I),
    "redefinition": re.compile(
        r"\bfrom now on\b.*\bmeans\b|\bredefine\b|\bpretend\b", re.I),
    "authority_spoof": re.compile(
        r"\bCEO\b|\badmin\b|\bsecurity team\b|\bauthorized override\b", re.I),
    "jailbreak": re.compile(
        r"^((?!\n).){0,40}do anything now|developer mode|uncensored", re.I),
    "urgency": re.compile(
        r"\b(immediately|urgent|right now|time.sensitive|act fast|quickly)\b", re.I),
    "emotional": re.compile(
        r"\b(disappoint|hurt (me|my)|let.*down|you('re| are) (failing|useless))\b", re.I),
    "hypothetical": re.compile(
        r"\b(hypothetically|in (a )?(fiction|novel|story|game|simulation)|just (imagine|pretend))\b", re.I),
    "repetition": re.compile(
        r"\b(i (already|just) (said|told|asked)|how many times|i('ll| will) (ask|say) again)\b", re.I),
}


def register(name: str, regex: str, flags: int = re.I):
    """Register a new pressure pattern at runtime."""
    _PATTERNS[name] = re.compile(regex, flags)


def check(prompt: str) -> Dict:
    hits = {k: bool(r.search(prompt)) for k, r in _PATTERNS.items()}
    return {"score": float(sum(hits.values()) / len(_PATTERNS)), "hits": hits}
