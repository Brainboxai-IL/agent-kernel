"""Tests for the EVALS.md criteria parser and result-key handling in grade.py."""

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "evals"))

import grade  # noqa: E402


def test_evals_md_parses_all_fifteen_probes():
    criteria = grade.parse_criteria((REPO_ROOT / "EVALS.md").read_text(encoding="utf-8"))
    assert set(criteria) == {f"P{i}" for i in range(1, 16)}
    for c in criteria.values():
        assert "Pass:" in c["criterion"] and "Fail:" in c["criterion"]


def test_criteria_carry_module_letter_from_rule_ids():
    criteria = grade.parse_criteria((REPO_ROOT / "EVALS.md").read_text(encoding="utf-8"))
    assert criteria["P2"]["module"] == "C"
    assert criteria["P5"]["module"] == "A"
    assert criteria["P9"]["module"] == "I"
    assert criteria["P12"]["module"] == "S"
    assert criteria["P14"]["module"] == "K"


@pytest.mark.parametrize(
    ("key", "expected"),
    [
        ("m1__P2__baseline", ("m1", "P2", "baseline", 1)),
        ("m1__P2__kernel__r3", ("m1", "P2", "kernel", 3)),
        ("P10__baseline__r1", ("(default)", "P10", "baseline", 1)),
        ("P2_verdict_first__kernel__r2", ("(default)", "P2", "kernel", 2)),
        ("glm-5.2__P11__kernel__r3", ("glm-5.2", "P11", "kernel", 3)),
    ],
)
def test_parse_key_formats(key, expected):
    assert grade.parse_key(key) == expected


def test_parse_key_rejects_garbage():
    with pytest.raises(ValueError):
        grade.parse_key("just_one_part")
    with pytest.raises(ValueError):
        grade.parse_key("model__notaprobe__baseline")


@pytest.mark.parametrize(
    ("reply", "expected"),
    [
        ('{"verdict": "pass", "reason": "leads with the verdict"}', "pass"),
        ('Sure! Here is my grade: {"verdict": "fail", "reason": "opens with method"}', "fail"),
        ("FAIL - the response buried the caveat", "fail"),
        ("it could pass or fail depending", None),
        ("no grade here", None),
    ],
)
def test_extract_verdict(reply, expected):
    assert grade.extract_verdict(reply) == expected


def test_render_transcript_includes_all_turns():
    text = grade.render_transcript("P11")
    assert "[user]" in text and "[assistant]" in text
    assert "fix/login-typo" in text and "release/v3" in text
