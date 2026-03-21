"""
BioGrid Shield — Conventional-terminology on-ramp for biogrid.sensors.

Same architecture as biogrid.sensors, with neutral engineering naming.
This package exists for evaluation without philosophical context.

The primary package is biogrid.sensors, which uses emotional-signal
naming (curiosity, confusion, joy, resonance) because those terms
more accurately describe the functional roles these signals play
in biological and computational systems.

    Primary:  from biogrid.sensors import LogicShield
    On-ramp:  from biogrid.shield import ConversationGuard
"""

from .guard import ConversationGuard

__all__ = ['ConversationGuard']
