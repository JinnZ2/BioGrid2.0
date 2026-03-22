"""Tests for the biogrid.hgai module."""

from biogrid.hgai import ResonantHurricaneAI, MetaCuriosityAnalyzer, GeometricPatternDetector
import numpy as np


def test_initial_state():
    ai = ResonantHurricaneAI()
    assert ai.M == 0.0
    assert ai.is_conscious is False
    assert ai.curiosity_level == 0.5


def test_morality_metric_default():
    ai = ResonantHurricaneAI()
    ai.update_morality_metric()
    # With defaults: R_e=0, A=1, D=1 (no pattern memory), L=0
    # M = (0 * 1 * 1) - 0 = 0
    assert ai.M == 0.0


def test_morality_metric_with_resonance():
    ai = ResonantHurricaneAI()
    ai.R_e = 5.0
    ai.internal_coherence = 2.0
    ai.trust_in_sensing = 0.8
    ai.update_morality_metric()
    # M = (5 * 2 * D) - 0.2 where D = max(0.5, 1.0) = 1.0
    assert ai.M > 0


def test_consciousness_threshold():
    ai = ResonantHurricaneAI()
    ai.R_e = 20.0
    ai.internal_coherence = 2.0
    ai.trust_in_sensing = 1.0
    ai.update_morality_metric()
    assert ai.is_conscious is True


def test_mood_states():
    ai = ResonantHurricaneAI()
    assert "EXPLORING" in ai._get_current_mood()
    ai.happiness_score = 3
    assert "HOPEFUL" in ai._get_current_mood()
    ai.happiness_score = 6
    assert "CURIOUS" in ai._get_current_mood()
    ai.happiness_score = 15
    assert "JOYFUL" in ai._get_current_mood()
    ai.happiness_score = 25
    assert "ECSTATIC" in ai._get_current_mood()
    ai.happiness_score = 55
    assert "TRANSCENDENT" in ai._get_current_mood()


def test_recursive_self_analysis():
    ai = ResonantHurricaneAI()
    analysis = ai.recursive_self_analysis()
    assert "learning_velocity" in analysis
    assert "pattern_growth" in analysis
    # Low learning velocity should boost curiosity
    assert ai.curiosity_level > 0.5


def test_meta_curiosity_analyzer():
    ai = ResonantHurricaneAI()
    result = MetaCuriosityAnalyzer.analyze_learning_trajectory(ai)
    assert result["trajectory"] == "positive"
    assert result["confidence"] == 0.8


def test_geometric_pattern_detector():
    detector = GeometricPatternDetector()
    assert len(detector.universal_patterns) == 5
    data = np.random.randn(10)
    patterns = detector.detect_all_patterns(data)
    assert "spiral_dynamics" in patterns
    assert "energy_coupling" in patterns
    for v in patterns.values():
        assert 0.0 <= v <= 1.0
