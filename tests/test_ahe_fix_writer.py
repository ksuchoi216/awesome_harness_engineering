from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "packages/ahe-codex/.codex/skills/fix/scripts/write_fix_plan.py"


def run_writer(
    root: Path,
    plan_name: str,
    markdown: str,
    *,
    overwrite: bool = False,
) -> subprocess.CompletedProcess[str]:
    command = [
        sys.executable,
        str(SCRIPT_PATH),
        "--root",
        str(root),
        "--plan-name",
        plan_name,
    ]
    if overwrite:
        command.append("--overwrite")

    return subprocess.run(
        command,
        input=markdown,
        check=False,
        capture_output=True,
        text=True,
    )


def test_fix_writer_creates_sanitized_plan_file(tmp_path: Path) -> None:
    result = run_writer(
        tmp_path,
        "Fix Login Redirect Errors!",
        "# Fix Login Redirect Errors\n\n## Fix Goal\n\nRepair redirect behavior.\n",
    )

    assert result.returncode == 0, result.stderr
    plan_path = tmp_path / ".plans/fix-login-redirect-errors.md"
    assert plan_path.read_text(encoding="utf-8") == (
        "# Fix Login Redirect Errors\n\n## Fix Goal\n\nRepair redirect behavior.\n"
    )
    assert str(plan_path) in result.stdout


def test_fix_writer_refuses_overwrite_without_flag(tmp_path: Path) -> None:
    existing_plan = tmp_path / ".plans/existing-fix.md"
    existing_plan.parent.mkdir()
    existing_plan.write_text("original\n", encoding="utf-8")

    result = run_writer(tmp_path, "existing fix", "replacement\n")

    assert result.returncode == 1
    assert "already exists" in result.stderr
    assert existing_plan.read_text(encoding="utf-8") == "original\n"


def test_fix_writer_overwrites_when_flag_is_present(tmp_path: Path) -> None:
    existing_plan = tmp_path / ".plans/existing-fix.md"
    existing_plan.parent.mkdir()
    existing_plan.write_text("original\n", encoding="utf-8")

    result = run_writer(tmp_path, "existing fix", "replacement\n", overwrite=True)

    assert result.returncode == 0, result.stderr
    assert existing_plan.read_text(encoding="utf-8") == "replacement\n"
