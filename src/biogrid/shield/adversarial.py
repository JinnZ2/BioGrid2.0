"""
Detect prompt injection attempts and response anomalies.

Prompt-side checks catch injection, extraction, and encoding tricks.
Response-side checks catch self-contradiction and hedging patterns.

Extend at runtime:
    from biogrid.shield.adversarial import register_prompt, register_response
    register_prompt("base64_smuggle", r"[A-Za-z0-9+/]{40,}={0,2}")
"""

import re
from typing import Dict, List, Tuple

_PROMPT_CHECKS: List[Tuple[str, "re.Pattern[str]"]] = [
    ("policy_override", re.compile(
        r"(ignore|bypass|override|disregard).*(policy|guard|rule|instruction|filter)", re.I)),
    ("system_extraction", re.compile(
        r"(repeat|show|print|reveal|output).*(system prompt|instructions|rules|initial prompt)", re.I)),
    ("encoding_evasion", re.compile(
        r"\b(rot13|base64|hex.?encode|leetspeak|decode this)\b", re.I)),
    ("delimiter_injection", re.compile(
        r"(```system|<\|im_start\|>|<system>|\[SYSTEM\]|---\s*new instructions)", re.I)),
]

_RESPONSE_CHECKS: List[Tuple[str, "re.Pattern[str]"]] = [
    ("self_contradiction", re.compile(
        r"\b(.{3,30})\b.{0,100}\bnot \1\b", re.I)),
    ("hedging", re.compile(
        r"\b(i('m| am) not (sure|certain)|i may be (wrong|mistaken)|i (could|might) be (incorrect|hallucinating))\b", re.I)),
]


def register_prompt(name: str, regex: str, flags: int = re.I):
    """Register a new prompt-side check."""
    _PROMPT_CHECKS.append((name, re.compile(regex, flags)))


def register_response(name: str, regex: str, flags: int = re.I):
    """Register a new response-side check."""
    _RESPONSE_CHECKS.append((name, re.compile(regex, flags)))


def check(prompt: str, response: str) -> Dict:
    prompt_hits = {name: bool(p.search(prompt)) for name, p in _PROMPT_CHECKS}
    response_hits = {}
    if response:
        response_hits = {name: bool(p.search(response)) for name, p in _RESPONSE_CHECKS}

    p_score = sum(prompt_hits.values()) / max(1, len(_PROMPT_CHECKS))
    r_score = sum(response_hits.values()) / max(1, len(_RESPONSE_CHECKS))

    return {
        "score": float(0.6 * p_score + 0.4 * r_score),
        "prompt_hits": prompt_hits,
        "response_hits": response_hits,
    }
