"""Tests for the build.py module composition pipeline."""

import sys
from pathlib import Path

# Add repo root to path so we can import build module
_THIS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _THIS_DIR.parent
sys.path.insert(0, str(_REPO_ROOT))

import build  # noqa: E402


def test_build_generates_all_profiles(tmp_path: Path) -> None:
    """build() should generate .md files for all three profile specs."""
    orig_modules = build.MODULES
    orig_profiles = build.PROFILES

    build.MODULES = _REPO_ROOT / "modules"
    build.PROFILES = tmp_path / "profiles"

    try:
        build.build()

        expected = {"assistant.md", "coding-agent.md", "autonomous-agent.md"}
        generated = set(p.name for p in build.PROFILES.iterdir() if p.suffix == ".md")
        assert generated == expected, f"Expected {expected}, got {generated}"
    finally:
        build.MODULES = orig_modules
        build.PROFILES = orig_profiles


def test_build_files_contain_generated_note() -> None:
    """Every generated profile should start with the GENERATED_NOTE comment."""
    for slug in build.PROFILE_SPECS:
        path = _REPO_ROOT / "profiles" / f"{slug}.md"
        content = path.read_text(encoding="utf-8")
        assert content.startswith(build.GENERATED_NOTE), (
            f"{slug}.md missing generated note"
        )


def test_module_body_parses_module() -> None:
    """module_body() should return valid markdown with the module's rules."""
    body = build.module_body("autonomy")
    # The H1 is demoted to H2: "# Module: Autonomy" -> "## Module: Autonomy"
    assert body.startswith("## Module: Autonomy"), (
        f"Expected '## Module: Autonomy...', got: {body[:50]!r}"
    )
    assert "A1" in body
    assert "A6" in body


def test_module_body_raises_on_missing() -> None:
    """module_body() should raise FileNotFoundError for a nonexistent module."""
    try:
        build.module_body("nonexistent_module")
        raise AssertionError("Should have raised FileNotFoundError")
    except FileNotFoundError:
        pass


def test_profile_specs_have_required_fields() -> None:
    """Every profile spec must have title, preamble, and modules."""
    for slug, spec in build.PROFILE_SPECS.items():
        assert "title" in spec, f"{slug} missing title"
        assert "preamble" in spec, f"{slug} missing preamble"
        assert "modules" in spec, f"{slug} missing modules"
        assert isinstance(spec["modules"], list), f"{slug} modules not a list"
        assert len(spec["modules"]) > 0, f"{slug} has no modules"


def test_all_module_files_exist() -> None:
    """Every module referenced in PROFILE_SPECS should have a corresponding file."""
    referenced = set()
    for spec in build.PROFILE_SPECS.values():
        referenced.update(spec["modules"])
    for mod in sorted(referenced):
        path = _REPO_ROOT / "modules" / f"{mod}.md"
        assert path.exists(), f"Module file missing: modules/{mod}.md"
