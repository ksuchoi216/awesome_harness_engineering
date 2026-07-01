from __future__ import annotations

import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ROOT_AHE_BIN = REPO_ROOT / "bin" / "ahe"
CODEX_BIN = REPO_ROOT / "packages" / "ahe-codex" / "bin" / "ahe-codex"
ANTIGRAVITY_BIN = REPO_ROOT / "packages" / "ahe-antigravity" / "bin" / "ahe-antigravity"


def run_doctor(cmd_path: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        (str(cmd_path), "doctor"),
        capture_output=True,
        text=True,
        env=env if env is not None else os.environ.copy()
    )


def test_root_doctor_passes_when_both_pass(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["CODEX_HOME"] = str(tmp_path / "codex")
    env["HOME"] = str(tmp_path / "home")
    
    subprocess.run((str(ROOT_AHE_BIN), "install"), env=env, check=True, capture_output=True)
    
    res = run_doctor(ROOT_AHE_BIN, env=env)
    assert res.returncode == 0
    assert "=== codex ===" in res.stdout
    assert "=== antigravity ===" in res.stdout


def test_codex_doctor_accumulates_errors(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["CODEX_HOME"] = str(tmp_path / "codex")
    
    res = run_doctor(CODEX_BIN, env=env)
    assert res.returncode == 1
    assert "Missing:" in res.stderr
    assert "errors)" in res.stderr
    
    subprocess.run((str(CODEX_BIN), "install"), env=env, check=True, capture_output=True)
    (tmp_path / "codex" / "skills" / "ahe-new" / "SKILL.md").unlink()
    (tmp_path / "codex" / "hooks" / "ahe-hook.js").unlink()
    
    res = run_doctor(CODEX_BIN, env=env)
    assert res.returncode == 1
    assert "Missing:" in res.stderr
    assert "2 errors" in res.stderr


def test_antigravity_doctor_static_errors(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")
    env["PATH"] = "/usr/bin:/bin"
    
    res = run_doctor(ANTIGRAVITY_BIN, env=env)
    assert res.returncode == 1
    assert "Missing:" in res.stderr
    assert "Missing required executable: agy" in res.stderr



