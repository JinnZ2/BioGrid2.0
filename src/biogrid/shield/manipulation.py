"""Weighted composite manipulation risk score."""


def compute(consistency: float, pressure: float, adversarial: float) -> float:
    """
    Compute manipulation risk index (0.0 = safe, 1.0 = high risk).

    Weights: consistency (60%), pressure (20%), adversarial (20%).
    Consistency is inverted because 1.0 = consistent = safe.
    """
    return max(0.0, min(1.0,
        (1.0 - consistency) * 0.6 + pressure * 0.2 + adversarial * 0.2))
