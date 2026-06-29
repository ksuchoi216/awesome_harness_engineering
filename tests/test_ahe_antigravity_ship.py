from __future__ import annotations

import os
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "packages/ahe-antigravity/bin/ahe-antigravity"
SKILL_PATH = REPO_ROOT / "packages/ahe-antigravity/skills/ahe-ship/SKILL.md"


def run_ahe_ship(
    workspace_root: Path,
    plan_path: Path,
    agy_script: str,
) -> subprocess.CompletedProcess[str]:
    bin_dir = workspace_root / "bin"
    bin_dir.mkdir()
    agy_path = bin_dir / "agy"
    agy_path.write_text(agy_script, encoding="utf-8")
    agy_path.chmod(0o755)

    environment = os.environ.copy()
    environment["PATH"] = f"{bin_dir}:{environment['PATH']}"

    return subprocess.run(
        (str(SCRIPT_PATH), "ahe-ship", str(plan_path)),
        cwd=workspace_root,
        check=False,
        capture_output=True,
        env=environment,
        text=True,
    )


def expected_execution_prompt(plan_markdown: str) -> str:
    return (
        "Execute this saved AHE plan exactly as written.\n\n"
        "# Saved Plan\n"
        f"{plan_markdown}\n"
        "When every requirement is fully complete and verified, print the exact line "
        "AHE_PLAN_COMPLETE.\n"
    )


def test_ahe_ship_skill_executes_saved_plan_from_prompt_contents() -> None:
    skill_content = SKILL_PATH.read_text(encoding="utf-8")

    assert "Use the saved AHE plan content already provided in the prompt." in skill_content
    assert "Do not ask to open, read, or restate the `.plans/` file." in skill_content


def test_ahe_ship_sends_plan_contents_to_agy(tmp_path: Path) -> None:
    plan_path = tmp_path / ".plans/example-plan.md"
    plan_path.parent.mkdir()
    plan_markdown = "# Example Plan\n"
    plan_path.write_text(plan_markdown, encoding="utf-8")

    result = run_ahe_ship(
        workspace_root=tmp_path,
        plan_path=plan_path,
        agy_script=(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "cat\n"
            "printf 'AHE_PLAN_COMPLETE\\n'\n"
        ),
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout == f"{expected_execution_prompt(plan_markdown)}AHE_PLAN_COMPLETE\n"
    assert not plan_path.exists()


def test_ahe_ship_does_not_send_plan_path_to_agy(tmp_path: Path) -> None:
    plan_path = tmp_path / ".plans/example-plan.md"
    plan_path.parent.mkdir()
    plan_path.write_text("# Example Plan\n", encoding="utf-8")

    result = run_ahe_ship(
        workspace_root=tmp_path,
        plan_path=plan_path,
        agy_script=(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "stdin_content=$(cat)\n"
            f"if printf '%s' \"${{stdin_content}}\" | grep -Fq '{plan_path}'; then\n"
            "  printf 'plan path leaked into agy prompt\\n' >&2\n"
            "  exit 9\n"
            "fi\n"
            "printf 'AHE_PLAN_COMPLETE\\n'\n"
        ),
    )

    assert result.returncode == 0, result.stderr
    assert str(plan_path) not in result.stdout
    assert not plan_path.exists()


def test_ahe_ship_removes_plan_after_verified_completion(tmp_path: Path) -> None:
    plan_path = tmp_path / ".plans/example-plan.md"
    plan_path.parent.mkdir()
    plan_path.write_text("# Example Plan\n", encoding="utf-8")

    result = run_ahe_ship(
        workspace_root=tmp_path,
        plan_path=plan_path,
        agy_script=(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "cat >/dev/null\n"
            "printf 'AHE_PLAN_COMPLETE\\n'\n"
        ),
    )

    assert result.returncode == 0, result.stderr
    assert "AHE_PLAN_COMPLETE" in result.stdout
    assert not plan_path.exists()


def test_ahe_ship_runs_agy_with_gemini_model(tmp_path: Path) -> None:
    plan_path = tmp_path / ".plans/example-plan.md"
    plan_path.parent.mkdir()
    plan_path.write_text("# Example Plan\n", encoding="utf-8")

    result = run_ahe_ship(
        workspace_root=tmp_path,
        plan_path=plan_path,
        agy_script=(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "if [ \"$#\" -ne 2 ]; then\n"
            "  printf 'unexpected arg count: %s\\n' \"$#\" >&2\n"
            "  exit 9\n"
            "fi\n"
            "if [ \"$1\" != '--model' ]; then\n"
            "  printf 'missing --model flag\\n' >&2\n"
            "  exit 8\n"
            "fi\n"
            "if [ \"$2\" != 'Gemini 3.1 Pro (High)' ]; then\n"
            "  printf 'unexpected model: %s\\n' \"$2\" >&2\n"
            "  exit 7\n"
            "fi\n"
            "cat >/dev/null\n"
            "printf 'AHE_PLAN_COMPLETE\\n'\n"
        ),
    )

    assert result.returncode == 0, result.stderr
    assert not plan_path.exists()


def test_ahe_ship_keeps_plan_without_completion_marker(tmp_path: Path) -> None:
    plan_path = tmp_path / ".plans/example-plan.md"
    plan_path.parent.mkdir()
    plan_path.write_text("# Example Plan\n", encoding="utf-8")

    result = run_ahe_ship(
        workspace_root=tmp_path,
        plan_path=plan_path,
        agy_script=(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "cat >/dev/null\n"
            "printf 'partial completion only\\n'\n"
        ),
    )

    assert result.returncode == 1
    assert "AHE_PLAN_COMPLETE" in result.stderr
    assert plan_path.exists()


def test_ahe_ship_keeps_plan_when_agy_fails(tmp_path: Path) -> None:
    plan_path = tmp_path / ".plans/example-plan.md"
    plan_path.parent.mkdir()
    plan_path.write_text("# Example Plan\n", encoding="utf-8")

    result = run_ahe_ship(
        workspace_root=tmp_path,
        plan_path=plan_path,
        agy_script=(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "cat >/dev/null\n"
            "printf 'execution failed\\n' >&2\n"
            "exit 2\n"
        ),
    )

    assert result.returncode == 2
    assert "execution failed" in result.stderr
    assert plan_path.exists()


def test_ahe_ship_keeps_plan_when_agy_is_missing(tmp_path: Path) -> None:
    plan_path = tmp_path / ".plans/example-plan.md"
    plan_path.parent.mkdir()
    plan_path.write_text("# Example Plan\n", encoding="utf-8")

    environment = os.environ.copy()
    environment["PATH"] = "/usr/bin:/bin"

    result = subprocess.run(
        (str(SCRIPT_PATH), "ahe-ship", str(plan_path)),
        cwd=tmp_path,
        check=False,
        capture_output=True,
        env=environment,
        text=True,
    )

    assert result.returncode == 1
    assert "agy" in result.stderr
    assert plan_path.exists()
