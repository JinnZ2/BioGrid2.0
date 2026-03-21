"""Tests for the biogrid.glyphs package."""

import json
import os
import tempfile

from biogrid.glyphs.validator import validate_file
from biogrid.glyphs.diff_viewer import diff_registries
from biogrid.glyphs.merge import merge_fragments


def _write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f)


def test_validator_valid():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({
            "glyphs": [{
                "code": "TEST-001",
                "name": "Test Glyph",
                "glyph": "T",
                "essence": "A test glyph",
                "state": "proposed",
                "layers": ["logic"],
                "source": "test",
            }]
        }, f)
        f.flush()
        ok, warnings, errors = validate_file(f.name)
    os.unlink(f.name)
    assert ok is True
    assert errors == []


def test_validator_missing_name():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({
            "glyphs": [{
                "code": "TEST-002",
                "name": "",
                "glyph": "X",
                "essence": "test",
                "state": "proposed",
                "layers": ["logic"],
            }]
        }, f)
        f.flush()
        ok, warnings, errors = validate_file(f.name)
    os.unlink(f.name)
    assert ok is False
    assert any("Missing name" in e for e in errors)


def test_validator_duplicate_code():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({
            "glyphs": [
                {"code": "DUP-001", "name": "A", "glyph": "D", "essence": "a",
                 "state": "proposed", "layers": ["logic"]},
                {"code": "DUP-001", "name": "B", "glyph": "E", "essence": "b",
                 "state": "proposed", "layers": ["logic"]},
            ]
        }, f)
        f.flush()
        ok, warnings, errors = validate_file(f.name)
    os.unlink(f.name)
    assert ok is False
    assert any("Duplicate" in e for e in errors)


def test_diff_viewer():
    with tempfile.TemporaryDirectory() as d:
        old_path = os.path.join(d, "old.json")
        new_path = os.path.join(d, "new.json")
        _write_json(old_path, {"glyphs": [
            {"code": "A", "name": "Alpha", "glyph": "a", "layers": ["logic"]},
        ]})
        _write_json(new_path, {"glyphs": [
            {"code": "A", "name": "Alpha Updated", "glyph": "a", "layers": ["logic"]},
            {"code": "B", "name": "Beta", "glyph": "b", "layers": ["signal"]},
        ]})
        added, removed, changed, _, _ = diff_registries(old_path, new_path)
    assert "B" in added
    assert removed == []
    assert len(changed) == 1
    assert changed[0][0] == "A"


def test_merge_fragments():
    with tempfile.TemporaryDirectory() as d:
        canon_path = os.path.join(d, "canonical.json")
        frag_dir = os.path.join(d, "fragments")
        os.makedirs(frag_dir)

        _write_json(canon_path, {"version": "2.3", "glyphs": []})
        _write_json(os.path.join(frag_dir, "f1.json"), {
            "provenance": "test",
            "adds": [
                {"code": "NEW-001", "name": "New One", "glyph": "N",
                 "state": "proposed", "layers": ["logic"]},
            ]
        })

        count = merge_fragments(canon_path, frag_dir)
        assert count == 1

        with open(canon_path) as f:
            result = json.load(f)
        assert len(result["glyphs"]) == 1
        assert result["glyphs"][0]["code"] == "NEW-001"
        assert result["glyphs"][0]["state"] == "canonical"  # promoted from proposed
