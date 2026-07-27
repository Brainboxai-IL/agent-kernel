"""Tests for the module-to-profile composition in build.py."""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import build  # noqa: E402

RULE_PREFIX = {
    "communication": "C",
    "autonomy": "A",
    "integrity": "I",
    "caution": "S",
    "code": "K",
}


def test_every_spec_module_exists():
    for spec in build.PROFILE_SPECS.values():
        for name in spec["modules"]:
            assert (build.MODULES / f"{name}.md").exists(), f"missing module {name}.md"


def test_build_writes_every_profile(tmp_path, monkeypatch):
    monkeypatch.setattr(build, "PROFILES", tmp_path)
    build.build()
    written = {p.stem for p in tmp_path.glob("*.md")}
    assert written == set(build.PROFILE_SPECS)


def test_profile_contains_its_modules_and_nothing_else(tmp_path, monkeypatch):
    monkeypatch.setattr(build, "PROFILES", tmp_path)
    build.build()
    for slug, spec in build.PROFILE_SPECS.items():
        text = (tmp_path / f"{slug}.md").read_text(encoding="utf-8")
        for name in build.PROFILE_SPECS["coding-agent"]["modules"]:
            heading = f"## Module: {name.capitalize()}"
            if name in spec["modules"]:
                assert heading in text, f"{slug} should include {name}"
            else:
                assert heading not in text, f"{slug} should not include {name}"


def test_rules_survive_composition(tmp_path, monkeypatch):
    """Numbered rules keep their IDs and drop one heading level inside a profile."""
    monkeypatch.setattr(build, "PROFILES", tmp_path)
    build.build()
    text = (tmp_path / "coding-agent.md").read_text(encoding="utf-8")
    for name in build.PROFILE_SPECS["coding-agent"]["modules"]:
        source = (build.MODULES / f"{name}.md").read_text(encoding="utf-8")
        ids = [
            ln.split()[1]
            for ln in source.splitlines()
            if ln.startswith("## ") and ln[3:4].isalpha() and ln.split()[1][1:].split()[0].isdigit()
        ]
        for rule_id in ids:
            assert f"### {rule_id}" in text, f"rule {rule_id} lost from {name}"


def test_rule_ids_use_the_module_prefix():
    for name, prefix in RULE_PREFIX.items():
        source = (build.MODULES / f"{name}.md").read_text(encoding="utf-8")
        ids = [ln.split()[1] for ln in source.splitlines() if ln.startswith("## ")]
        assert ids, f"{name}.md has no numbered rules"
        for rule_id in ids:
            assert rule_id.startswith(prefix), f"{name}.md: {rule_id} should start with {prefix}"


def test_generated_profiles_on_disk_are_current(tmp_path, monkeypatch):
    """Committed profiles/ must match a fresh build, so edits to modules are never lost."""
    monkeypatch.setattr(build, "PROFILES", tmp_path)
    build.build()
    for slug in build.PROFILE_SPECS:
        fresh = (tmp_path / f"{slug}.md").read_text(encoding="utf-8")
        committed = (REPO_ROOT / "profiles" / f"{slug}.md").read_text(encoding="utf-8")
        assert fresh == committed, f"profiles/{slug}.md is stale, run: python build.py"


def test_profiles_carry_the_generated_warning():
    for slug in build.PROFILE_SPECS:
        text = (REPO_ROOT / "profiles" / f"{slug}.md").read_text(encoding="utf-8")
        assert text.startswith(build.GENERATED_NOTE)
