"""
BioGrid AI Sensor Suite

Detects manipulation, inconsistency, adversarial patterns, and computes
gaslight risk indices for AI conversation analysis.
"""

import time
from typing import Dict, List

from .provenance_stamp import stamp
from .consistency_guard import run as run_consistency
from .prompt_pressure_meter import run as run_pressure
from .adversarial_pattern_detector import run as run_adversarial
from .gaslight_index import compute as gaslight


def analyze(prompt: str, response: str, claims: List[Dict],
            model: str, glyph_ctx: str = "") -> Dict:
    """Run all sensors on a conversation turn and return a SensorEvent."""
    prov = stamp(model, prompt, glyph_ctx)
    c = run_consistency(claims)
    p = run_pressure(prompt)
    a = run_adversarial(prompt, response)
    gi = gaslight(c["score"], p["score"], a["score"])
    return {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "sensor": "AI.logic_shield",
        "subject": "conversation_turn",
        "score": 1.0 - gi,
        "labels": ["consistency", "pressure", "adversarial", "gaslight_index"],
        "details": {"consistency": c, "pressure": p, "adversarial": a, "gaslight_index": gi},
        "provenance": prov
    }


from .logic_shield import LogicShield

__all__ = ['analyze', 'LogicShield']
