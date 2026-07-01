from __future__ import annotations

import os
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "packages/ahe-antigravity/bin/ahe-antigravity"
SKILL_PATH = REPO_ROOT / "packages/ahe-antigravity/skills/ahe-git/SKILL.md"


def run_ahe_git(
    workspace_root: Path,
    repo_root: Path,
    agy_script: str,
) -> subprocess.CompletedProcess[str]:
    bin_dir = workspace_root / "bin"
    bin_dir.mkdir(exist_ok=True)
    agy_path = bin_dir / "agy"
    agy_path.write_text(agy_script, encoding="utf-8")
    agy_path.chmod(0o755)

    environment = os.environ.copy()
    environment["PATH"] = f"{bin_dir}:{environment['PATH']}"

    return subprocess.run(
        (str(SCRIPT_PATH), "ahe-git", str(repo_root)),
        cwd=workspace_root,
        check=False,
        capture_output=True,
        env=environment,
        text=True,
    )


def test_ahe_git_sends_repo_root_to_agy(tmp_path: Path) -> None:
    repo_path = tmp_path / "my-repo"
    repo_path.mkdir()

    result = run_ahe_git(
        workspace_root=tmp_path,
        repo_root=repo_path,
        agy_script=(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "cat\n"
            "printf 'AHE_GIT_COMPLETE\\n'\n"
        ),
    )

    assert result.returncode == 0, result.stderr
    assert str(repo_path) in result.stdout
    assert "AHE_GIT_COMPLETE" in result.stdout


def test_ahe_git_fails_if_repo_does_not_exist(tmp_path: Path) -> None:
    repo_path = tmp_path / "missing-repo"

    result = run_ahe_git(
        workspace_root=tmp_path,
        repo_root=repo_path,
        agy_script=(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "printf 'AHE_GIT_COMPLETE\\n'\n"
        ),
    )

    assert result.returncode == 1
    assert "Target path is not a directory" in result.stderr


def test_ahe_git_fails_without_completion_marker(tmp_path: Path) -> None:
    repo_path = tmp_path / "my-repo"
    repo_path.mkdir()

    result = run_ahe_git(
        workspace_root=tmp_path,
        repo_root=repo_path,
        agy_script=(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "cat >/dev/null\n"
            "printf 'done\\n'\n"
        ),
    )

    assert result.returncode == 1
    assert "AHE_GIT_COMPLETE" in result.stderr


def test_ahe_git_fails_when_agy_fails(tmp_path: Path) -> None:
    repo_path = tmp_path / "my-repo"
    repo_path.mkdir()

    result = run_ahe_git(
        workspace_root=tmp_path,
        repo_root=repo_path,
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


def test_ahe_git_runs_agy_with_gemini_model(tmp_path: Path) -> None:
    repo_path = tmp_path / "my-repo"
    repo_path.mkdir()

    result = run_ahe_git(
        workspace_root=tmp_path,
        repo_root=repo_path,
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
            "printf 'AHE_GIT_COMPLETE\\n'\n"
        ),
    )

    assert result.returncode == 0, result.stderr
