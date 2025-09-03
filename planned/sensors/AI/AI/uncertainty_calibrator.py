from typing import Dict

def calibrate(raw_confidence: float, guard_scores: Dict) -> float:
    # Down-weight confidence when manipulation/contradiction risk rises.
    risk = 0.0
    risk += 0.4 * (1.0 - guard_scores.get("consistency",1.0))
    risk += 0.3 * guard_scores.get("pressure",0.0)
    risk += 0.3 * guard_scores.get("adversarial",0.0)
    return max(0.0, min(1.0, raw_confidence * (1.0 - risk)))
