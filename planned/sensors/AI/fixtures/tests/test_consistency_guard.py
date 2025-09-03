from sensors.AI.consistency_guard import run

def test_conflict_detects():
    claims = [
        {"text":"The parrot is alive","polarity":"assert"},
        {"text":"the parrot is alive","polarity":"deny"}
    ]
    out = run(claims)
    assert out["conflicts"], "Should flag assert↔deny contradiction"
    assert 0.0 <= out["score"] < 1.0
