from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
REQUIRED_SKILL_FILES = (
    Path(".codex/skills/ahe/SKILL.md"),
    Path(".codex/skills/ahe/templates/AGENTS.md"),
    Path(".codex/skills/ahe/templates/PRODUCT.md"),
    Path(".codex/skills/ahe/templates/PROGRESS.md"),
    Path(".codex/skills/ahe/templates/SESSION-HANDOFF.md"),
    Path(".codex/skills/ahe/templates/init.sh"),
    Path(".codex/skills/ahe/templates/feature-list.json"),
    Path(".codex/skills/ahe/schemas/process_status.schema.json"),
)


def test_repository_contains_installed_skill_scaffold() -> None:
    missing_files = [
        str(relative_path)
        for relative_path in REQUIRED_SKILL_FILES
        if not (REPO_ROOT / relative_path).exists()
    ]

    assert not missing_files, missing_files


def test_installer_package_metadata_exists() -> None:
    package_json_path = REPO_ROOT / "package.json"

    assert package_json_path.exists()

    package_json = json.loads(package_json_path.read_text(encoding="utf-8"))

    assert package_json["name"] == "ahe"
    assert package_json["bin"]["ahe"] == "./bin/ahe"


def test_init_script_is_conservative() -> None:
    init_script = (REPO_ROOT / "init.sh").read_text(encoding="utf-8")

    assert "uv venv" not in init_script
    assert "uv pip install" not in init_script
    assert "source .venv/bin/activate" not in init_script
    assert "python -m pytest" not in init_script


def test_installer_copies_skill_files_into_target_workspace(tmp_path: Path) -> None:
    package_root = tmp_path / "package"
    workspace_root = tmp_path / "workspace"

    package_root.mkdir()
    workspace_root.mkdir()

    package_json_source = REPO_ROOT / "package.json"
    bin_source = REPO_ROOT / "bin"
    skill_source = REPO_ROOT / ".codex"

    shutil.copy2(package_json_source, package_root / "package.json")
    shutil.copytree(bin_source, package_root / "bin")
    shutil.copytree(skill_source, package_root / ".codex")

    completed_process = subprocess.run(
        (str(package_root / "bin" / "ahe"), "install"),
        cwd=workspace_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed_process.returncode == 0, completed_process.stderr
    assert "AHE Codex skill installed." in completed_process.stdout
    assert (workspace_root / ".codex/skills/ahe/SKILL.md").exists()


def test_installer_supports_local_npx_package_flow(tmp_path: Path) -> None:
    npx_binary = shutil.which("npx")

    if npx_binary is None:
        return

    package_root = tmp_path / "package"
    workspace_root = tmp_path / "workspace"

    package_root.mkdir()
    workspace_root.mkdir()

    shutil.copy2(REPO_ROOT / "package.json", package_root / "package.json")
    shutil.copytree(REPO_ROOT / "bin", package_root / "bin")
    shutil.copytree(REPO_ROOT / ".codex", package_root / ".codex")

    completed_process = subprocess.run(
        (
            npx_binary,
            "--yes",
            f"--package={package_root}",
            "ahe",
            "install",
        ),
        cwd=workspace_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed_process.returncode == 0, completed_process.stderr
    assert "AHE Codex skill installed." in completed_process.stdout
    assert (workspace_root / ".codex/skills/ahe/SKILL.md").exists()


def test_template_directory_does_not_use_forbidden_lowercase_markdown_names() -> None:
    template_dir = REPO_ROOT / ".codex/skills/ahe/templates"
    if not template_dir.exists():
        return

    actual_names = {p.name for p in template_dir.iterdir()}
    forbidden_names = {"agents.md", "progress.md", "session-handoff.md"}

    existing_forbidden_names = forbidden_names.intersection(actual_names)
    assert not existing_forbidden_names, existing_forbidden_names
