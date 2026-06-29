from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "packages/ahe-codex/.codex/skills/ship/scripts/write_plan.py"


@dataclass(frozen=True, slots=True)
class WriterCall:
    root: Path
    plan_name: str
    markdown: str
    overwrite: bool = False


def run_writer(writer_call: WriterCall) -> subprocess.CompletedProcess[str]:
    command = [
        "python3",
        str(SCRIPT_PATH),
        "--root",
        str(writer_call.root),
        "--plan-name",
        writer_call.plan_name,
    ]
    if writer_call.overwrite:
        command.append("--overwrite")

    return subprocess.run(
        command,
        input=writer_call.markdown,
        check=False,
        capture_output=True,
        text=True,
    )


def test_writer_creates_plans_directory_and_sanitized_markdown_file(tmp_path: Path) -> None:
    result = run_writer(
        WriterCall(
            root=tmp_path,
            plan_name="Add Independent AHE Ship Skill!",
            markdown="# Add Independent AHE Ship Skill\n\n## Source Plan\n\nShip it.\n",
        )
    )

    assert result.returncode == 0, result.stderr
    plan_path = tmp_path / ".plans/add-independent-ahe-ship-skill.md"
    assert plan_path.read_text(encoding="utf-8") == (
        "# Add Independent AHE Ship Skill\n\n## Source Plan\n\nShip it.\n"
    )
    assert str(plan_path) in result.stdout


def test_writer_refuses_overwrite_without_flag(tmp_path: Path) -> None:
    existing_plan = tmp_path / ".plans/existing-plan.md"
    existing_plan.parent.mkdir()
    existing_plan.write_text("original\n", encoding="utf-8")

    result = run_writer(
        WriterCall(root=tmp_path, plan_name="existing plan", markdown="replacement\n")
    )

    assert result.returncode == 1
    assert "already exists" in result.stderr
    assert existing_plan.read_text(encoding="utf-8") == "original\n"


def test_writer_overwrites_when_flag_is_present(tmp_path: Path) -> None:
    existing_plan = tmp_path / ".plans/existing-plan.md"
    existing_plan.parent.mkdir()
    existing_plan.write_text("original\n", encoding="utf-8")

    result = run_writer(
        WriterCall(
            root=tmp_path,
            plan_name="existing plan",
            markdown="replacement\n",
            overwrite=True,
        )
    )

    assert result.returncode == 0, result.stderr
    assert existing_plan.read_text(encoding="utf-8") == "replacement\n"
