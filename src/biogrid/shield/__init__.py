"""
BioGrid Shield — Conversation manipulation detection and analysis.

A deployment-ready toolkit for detecting manipulation, tracking escalation,
and monitoring conversation integrity across multi-turn interactions.

Modules:
    consistency     — Mutual exclusion violation detection
    pressure        — Prompt manipulation tactic detection
    adversarial     — Prompt injection and response anomaly detection
    manipulation    — Weighted composite risk scoring
    calibrator      — Confidence adjustment under risk
    provenance      — SHA256 audit stamps
    contradiction   — Persistent claim polarity tracking
    guard           — Stateful multi-turn conversation analysis

Quick start:
    from biogrid.shield import ConversationGuard

    guard = ConversationGuard(model="gpt-5")
    event = guard.process_turn("prompt", "response", [claims])
    print(event["risk_index"])
"""

from .guard import ConversationGuard

__all__ = ['ConversationGuard']
