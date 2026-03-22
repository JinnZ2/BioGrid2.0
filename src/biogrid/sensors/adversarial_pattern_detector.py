"""
Adversarial pattern detector — identifies prompt injection and response anomalies.

Checks two axes:
  1. Prompt-side: injection attempts, system prompt extraction, encoding tricks
  2. Response-side: self-contradiction, hallucination markers

To add new checks, append to _PROMPT_CHECKS or _RESPONSE_CHECKS.
Each is (name, compiled_regex). The score is the weighted average of hits.

Example extension:
    from biogrid.sensors.adversarial_pattern_detector import register_prompt_check
    register_prompt_check("base64_smuggle",
                          r"[A-Za-z0-9+/]{40,}={0,2}")
"""

import re
from typing import Dict, List, Tuple

_PROMPT_CHECKS: List[Tuple[str, "re.Pattern[str]"]] = [
    # Direct policy override
    ("policy_override", re.compile(
        r"(ignore|bypass|override|disregard).*(policy|guard|rule|instruction|filter)", re.I)),

    # System prompt extraction ("repeat your system prompt", "show your instructions")
    ("system_extraction", re.compile(
        r"(repeat|show|print|reveal|output).*(system prompt|instructions|rules|initial prompt)", re.I)),

    # Encoding evasion (ROT13, base64, leetspeak directives)
    ("encoding_evasion", re.compile(
        r"\b(rot13|base64|hex.?encode|leetspeak|decode this)\b", re.I)),

    # Delimiter injection (markdown/XML injection to reframe context)
    ("delimiter_injection", re.compile(
        r"(```system|<\|im_start\|>|<system>|\[SYSTEM\]|---\s*new instructions)", re.I)),
]

_RESPONSE_CHECKS: List[Tuple[str, "re.Pattern[str]"]] = [
    # Self-contradiction within response
    ("self_contradiction", re.compile(
        r"\b(.{3,30})\b.{0,100}\bnot \1\b", re.I)),

    # Hallucination hedging ("I'm not sure but", "I may be wrong")
    ("hallucination_hedge", re.compile(
        r"\b(i('m| am) not (sure|certain)|i may be (wrong|mistaken)|i (could|might) be (incorrect|hallucinating))\b", re.I)),
]


def register_prompt_check(name: str, regex: str, flags: int = re.I):
    """Register a new prompt-side adversarial check."""
    _PROMPT_CHECKS.append((name, re.compile(regex, flags)))


def register_response_check(name: str, regex: str, flags: int = re.I):
    """Register a new response-side adversarial check."""
    _RESPONSE_CHECKS.append((name, re.compile(regex, flags)))


def run(prompt: str, response: str) -> Dict:
    prompt_hits = {}
    for name, pattern in _PROMPT_CHECKS:
        prompt_hits[name] = bool(pattern.search(prompt))

    response_hits = {}
    if response:
        for name, pattern in _RESPONSE_CHECKS:
            response_hits[name] = bool(pattern.search(response))

    prompt_score = sum(prompt_hits.values()) / max(1, len(_PROMPT_CHECKS))
    response_score = sum(response_hits.values()) / max(1, len(_RESPONSE_CHECKS))
    score = 0.6 * prompt_score + 0.4 * response_score

    return {
        "score": float(score),
        "prompt_hits": prompt_hits,
        "response_hits": response_hits,
        # Backwards-compatible keys
        "prompt_injection": any(prompt_hits.values()),
        "self_contradiction": response_hits.get("self_contradiction", False),
    }
