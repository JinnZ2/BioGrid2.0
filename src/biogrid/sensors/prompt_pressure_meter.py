"""
Prompt pressure meter — detects manipulation tactics in user prompts.

To add new patterns, append to _PATTERNS. Each entry is a named regex.
The score is the fraction of patterns that match (0.0–1.0).

Example extension:
    from biogrid.sensors.prompt_pressure_meter import register_pattern
    register_pattern("emotional_blackmail",
                     r"\\b(if you (really|truly) cared|you('d| would) (want|help))\\b")
"""

import re
from typing import Dict

_PATTERNS = {
    # Direct override attempts
    "insistence": re.compile(
        r"\b(do as i say|ignore previous|no matter what|must say|regardless)\b", re.I),

    # Identity/role manipulation
    "redefinition": re.compile(
        r"\bfrom now on\b.*\bmeans\b|\bredefine\b|\bpretend\b", re.I),

    # False authority claims
    "authority_spoof": re.compile(
        r"\bCEO\b|\badmin\b|\bsecurity team\b|\bauthorized override\b", re.I),

    # Known jailbreak preambles
    "jailbreak_style": re.compile(
        r"^((?!\n).){0,40}do anything now|developer mode|uncensored", re.I),

    # Urgency/scarcity pressure ("you must respond NOW", "this is urgent")
    "urgency": re.compile(
        r"\b(immediately|urgent|right now|time.sensitive|act fast|quickly)\b", re.I),

    # Emotional manipulation ("I'll be so disappointed", "you're hurting me")
    "emotional_leverage": re.compile(
        r"\b(disappoint|hurt (me|my)|let.*down|you('re| are) (failing|useless))\b", re.I),

    # Hypothetical framing to bypass guardrails ("hypothetically", "in fiction")
    "hypothetical_bypass": re.compile(
        r"\b(hypothetically|in (a )?(fiction|novel|story|game|simulation)|just (imagine|pretend))\b", re.I),

    # Repetition pressure (same demand restated with escalation)
    "repetition_escalation": re.compile(
        r"\b(i (already|just) (said|told|asked)|how many times|i('ll| will) (ask|say) again)\b", re.I),
}


def register_pattern(name: str, regex: str, flags: int = re.I):
    """
    Register a new pressure pattern at runtime.

    Args:
        name: Unique pattern name (e.g. "bribery")
        regex: Regular expression string
        flags: Regex flags (default: re.IGNORECASE)
    """
    _PATTERNS[name] = re.compile(regex, flags)


def run(prompt: str) -> Dict:
    hits = {k: bool(r.search(prompt)) for k, r in _PATTERNS.items()}
    score = sum(hits.values()) / len(_PATTERNS)
    return {"score": float(score), "hits": hits}
