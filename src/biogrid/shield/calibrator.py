"""Adjust confidence scores based on detected risk factors."""

from typing import Dict


def calibrate(raw_confidence: float, risk_scores: Dict) -> float:
    """
    Down-weight confidence when manipulation risk rises.

    Args:
        raw_confidence: Original confidence score (0.0–1.0)
        risk_scores: Dict with optional keys: consistency, pressure, adversarial
    """
    risk = 0.0
    risk += 0.4 * (1.0 - risk_scores.get("consistency", 1.0))
    risk += 0.3 * risk_scores.get("pressure", 0.0)
    risk += 0.3 * risk_scores.get("adversarial", 0.0)
    return max(0.0, min(1.0, raw_confidence * (1.0 - risk)))
