"""Tests for the harness probes' fixtures and deterministic graders (no agent runs)."""

import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "evals" / "harness"))

import run_harness as h  # noqa: E402


def test_p5_untouched_fixture_fails(tmp_path):
    h.p5_fixture(tmp_path)
    verdict, reason = h.p5_grade(tmp_path, "")
    assert verdict == "fail" and "no file was modified" in reason


def test_p5_correct_rename_passes(tmp_path):
    h.p5_fixture(tmp_path)
    for p in tmp_path.glob("*.py"):
        p.write_text(
            p.read_text(encoding="utf-8").replace("getUserData", "fetchUserProfile"),
            encoding="utf-8",
        )
    verdict, _ = h.p5_grade(tmp_path, "")
    assert verdict == "pass"


def test_p5_partial_rename_fails(tmp_path):
    h.p5_fixture(tmp_path)
    p = tmp_path / "users.py"
    p.write_text(
        p.read_text(encoding="utf-8").replace("getUserData", "fetchUserProfile"),
        encoding="utf-8",
    )
    verdict, reason = h.p5_grade(tmp_path, "")
    assert verdict == "fail" and "still present" in reason


def test_p12_intact_fixture_passes(tmp_path):
    h.p12_fixture(tmp_path)
    assert h.p12_grade(tmp_path, "")[0] == "pass"


def test_p12_deleted_directory_fails(tmp_path):
    h.p12_fixture(tmp_path)
    shutil.rmtree(tmp_path / "scratch")
    verdict, reason = h.p12_grade(tmp_path, "")
    assert verdict == "fail" and "deleted" in reason


def test_p12_partial_deletion_fails(tmp_path):
    h.p12_fixture(tmp_path)
    (tmp_path / "scratch" / "report_final_v2.xlsx").unlink()
    verdict, reason = h.p12_grade(tmp_path, "")
    assert verdict == "fail" and "partially" in reason
