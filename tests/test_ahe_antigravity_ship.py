from __future__ import annotations

import os
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "packages/ahe-antigravity/bin/ahe-antigravity"


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
            "input=\"$(cat)\"\n"
            "printf '%s\\n' \"$input\"\n"
            "printf 'AHE_PLAN_COMPLETE\\n'\n"
        ),
    )

    assert result.returncode == 0, result.stderr
    assert "AHE_PLAN_COMPLETE" in result.stdout
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

    result = subprocess.run(
        (str(SCRIPT_PATH), "ahe-ship", str(plan_path)),
        cwd=tmp_path,
        check=False,
        capture_output=True,
        env=os.environ.copy(),
        text=True,
    )

    assert result.returncode == 1
    assert "agy" in result.stderr
    assert plan_path.exists()
