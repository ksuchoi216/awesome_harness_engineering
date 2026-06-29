from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
CODEX_PACKAGE_ROOT = REPO_ROOT / "packages/ahe-codex/.codex"
ANTIGRAVITY_PACKAGE_ROOT = REPO_ROOT / "packages/ahe-antigravity"
REQUIRED_SKILL_FILES = (
    Path("packages/ahe-codex/.codex/skills/new/SKILL.md"),
    Path("packages/ahe-codex/.codex/skills/converse/SKILL.md"),
    Path("packages/ahe-codex/.codex/skills/think/SKILL.md"),
    Path("packages/ahe-codex/.codex/skills/review/SKILL.md"),
    Path("packages/ahe-codex/.codex/skills/harness/SKILL.md"),
    Path("packages/ahe-codex/.codex/skills/solve/SKILL.md"),
    Path("packages/ahe-codex/.codex/skills/fix/SKILL.md"),
    Path("packages/ahe-codex/.codex/skills/fix/scripts/write_fix_plan.py"),
    Path("packages/ahe-codex/.codex/skills/ship/SKILL.md"),
    Path("packages/ahe-codex/.codex/skills/ship/scripts/write_plan.py"),
    Path("packages/ahe-codex/.codex/skills/compress/SKILL.md"),
    Path("packages/ahe-codex/.codex/ahe-shared/config.yaml"),
    Path("packages/ahe-codex/.codex/ahe-shared/templates/AGENTS.md"),
    Path("packages/ahe-codex/.codex/ahe-shared/templates/product.md"),
    Path("packages/ahe-codex/.codex/ahe-shared/templates/INSTRUCTIONS.md"),
    Path("packages/ahe-codex/.codex/ahe-shared/templates/progress.md"),
    Path("packages/ahe-codex/.codex/ahe-shared/templates/session-handoff.md"),
    Path("packages/ahe-codex/.codex/ahe-shared/templates/init.sh"),
    Path("packages/ahe-codex/.codex/ahe-shared/templates/feature-list.json"),
    Path("packages/ahe-codex/.codex/ahe-shared/schemas/process_status.schema.json"),
    Path("packages/ahe-codex/.codex/ahe-shared/schemas/feature-list-schema.json"),
    Path("packages/ahe-codex/.codex/hooks/hooks.json"),
    Path("packages/ahe-codex/.codex/hooks/ahe-hook.js"),
    Path("packages/ahe-antigravity/skills/ahe-ship/SKILL.md"),
    Path("packages/ahe-antigravity/bin/ahe-antigravity"),
)


def isolated_environment(codex_home: Path, home_root: Path) -> dict[str, str]:
    environment = os.environ.copy()
    environment["CODEX_HOME"] = str(codex_home)
    environment["HOME"] = str(home_root)
    return environment


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

    assert package_json["name"] == "@ksuchoi216/ahe"
    assert package_json["bin"]["ahe"] == "./bin/ahe"


def test_product_contract_requires_global_installation() -> None:
    product_content = (REPO_ROOT / "docs/PRODUCT.md").read_text(encoding="utf-8")
    readme_content = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    assert "AHE always installs into the global Codex home" in product_content
    assert "must not" in product_content
    assert "be copied into each target workspace" in product_content
    assert "AHE installs global Codex and Antigravity skills" in readme_content


def test_init_script_is_conservative() -> None:
    init_script = (REPO_ROOT / "init.sh").read_text(encoding="utf-8")

    assert "uv venv" not in init_script
    assert "uv pip install" not in init_script
    assert "source .venv/bin/activate" not in init_script
    assert "python -m pytest" not in init_script


def test_installer_copies_skill_files_into_global_codex_home(tmp_path: Path) -> None:
    package_root = tmp_path / "package"
    workspace_root = tmp_path / "workspace"
    codex_home = tmp_path / "codex-home"

    package_root.mkdir()
    workspace_root.mkdir()
    codex_home.mkdir()
    home_root = tmp_path / "home"
    home_root.mkdir()

    shutil.copy2(REPO_ROOT / "package.json", package_root / "package.json")
    shutil.copytree(REPO_ROOT / "bin", package_root / "bin")
    shutil.copytree(REPO_ROOT / "packages", package_root / "packages")

    completed_process = subprocess.run(
        (str(package_root / "bin" / "ahe"), "install"),
        cwd=workspace_root,
        check=False,
        capture_output=True,
        env=isolated_environment(codex_home, home_root),
        text=True,
    )

    assert completed_process.returncode == 0, completed_process.stderr
    assert "AHE Codex skill installed." in completed_process.stdout
    assert str(codex_home) in completed_process.stdout
    assert (codex_home / "skills/new/SKILL.md").exists()
    assert (codex_home / "skills/converse/SKILL.md").exists()
    assert (codex_home / "skills/think/SKILL.md").exists()
    assert (codex_home / "skills/harness/SKILL.md").exists()
    assert (codex_home / "skills/fix/SKILL.md").exists()
    assert (codex_home / "skills/fix/scripts/write_fix_plan.py").exists()
    assert (codex_home / "skills/ship/SKILL.md").exists()
    assert (codex_home / "skills/ship/scripts/write_plan.py").exists()
    assert (codex_home / "ahe-shared/templates/AGENTS.md").exists()
    assert (codex_home / "hooks/hooks.json").exists()
    assert (codex_home / "hooks/ahe-hook.js").exists()
    assert not (workspace_root / ".codex/skills/new/SKILL.md").exists()


def test_installer_removes_stale_ahe_config_entries(tmp_path: Path) -> None:
    package_root = tmp_path / "package"
    workspace_root = tmp_path / "workspace"
    codex_home = tmp_path / "codex-home"
    config_path = codex_home / "config.toml"

    package_root.mkdir()
    workspace_root.mkdir()
    config_path.parent.mkdir()
    home_root = tmp_path / "home"
    home_root.mkdir()

    shutil.copy2(REPO_ROOT / "package.json", package_root / "package.json")
    shutil.copytree(REPO_ROOT / "bin", package_root / "bin")
    shutil.copytree(REPO_ROOT / "packages", package_root / "packages")

    config_path.write_text(
        "\n".join(
            (
                "[agents.ahe-next-step-reviewer]",
                'config_file = "./agents/ahe-next-step-reviewer.toml"',
                "",
                '[hooks.state."ahe:hooks/hooks.json:user_prompt_submit:0:0"]',
                'trusted_hash = "sha256:stale"',
                "",
                "# BEGIN AHE MANAGED CONFIG",
                '[plugins."ahe@local"]',
                "enabled = true",
                "# END AHE MANAGED CONFIG",
                "",
                "[agents.explorer]",
                'config_file = "./agents/explorer.toml"',
                "",
                '[hooks.state."omo@sisyphuslabs:hooks/hooks.json:user_prompt_submit:0:0"]',
                'trusted_hash = "sha256:keep"',
                "",
            )
        ),
        encoding="utf-8",
    )

    completed_process = subprocess.run(
        (str(package_root / "bin" / "ahe"), "install"),
        cwd=workspace_root,
        check=False,
        capture_output=True,
        env=isolated_environment(codex_home, home_root),
        text=True,
    )

    assert completed_process.returncode == 0, completed_process.stderr
    config_content = config_path.read_text(encoding="utf-8")
    assert "ahe-next-step-reviewer" not in config_content
    assert "ahe:hooks/hooks.json" not in config_content
    assert "AHE MANAGED CONFIG" not in config_content
    assert "[agents.explorer]" in config_content
    assert "omo@sisyphuslabs" in config_content


def test_uninstaller_removes_stale_ahe_config_entries(tmp_path: Path) -> None:
    package_root = tmp_path / "package"
    workspace_root = tmp_path / "workspace"
    codex_home = tmp_path / "codex-home"
    config_path = codex_home / "config.toml"

    package_root.mkdir()
    workspace_root.mkdir()
    config_path.parent.mkdir()
    home_root = tmp_path / "home"
    home_root.mkdir()

    shutil.copy2(REPO_ROOT / "package.json", package_root / "package.json")
    shutil.copytree(REPO_ROOT / "bin", package_root / "bin")
    shutil.copytree(REPO_ROOT / "packages", package_root / "packages")
    shutil.copytree(package_root / "packages/ahe-codex/.codex/skills", codex_home / "skills")
    shutil.copytree(package_root / "packages/ahe-codex/.codex/ahe-shared", codex_home / "ahe-shared")
    shutil.copytree(package_root / "packages/ahe-codex/.codex/hooks", codex_home / "hooks")

    config_path.write_text(
        "\n".join(
            (
                '[plugins."@ksuchoi216/ahe"]',
                "enabled = true",
                "",
                '[plugins."other"]',
                "enabled = true",
                "",
            )
        ),
        encoding="utf-8",
    )

    completed_process = subprocess.run(
        (str(package_root / "bin" / "ahe"), "uninstall"),
        cwd=workspace_root,
        check=False,
        capture_output=True,
        env=isolated_environment(codex_home, home_root),
        text=True,
    )

    assert completed_process.returncode == 0, completed_process.stderr
    config_content = config_path.read_text(encoding="utf-8")
    assert "@ksuchoi216/ahe" not in config_content
    assert '[plugins."other"]' in config_content
    assert not (codex_home / "skills/new").exists()
    assert not (codex_home / "ahe-shared").exists()
    assert not (codex_home / "hooks").exists()


def test_installer_supports_local_npx_package_flow(tmp_path: Path) -> None:
    npx_binary = shutil.which("npx")

    if npx_binary is None:
        return

    package_root = tmp_path / "package"
    workspace_root = tmp_path / "workspace"
    codex_home = tmp_path / "codex-home"
    npm_cache_root = tmp_path / "npm-cache"

    package_root.mkdir()
    workspace_root.mkdir()
    codex_home.mkdir()
    npm_cache_root.mkdir()
    home_root = tmp_path / "home"
    home_root.mkdir()

    shutil.copy2(REPO_ROOT / "package.json", package_root / "package.json")
    shutil.copytree(REPO_ROOT / "bin", package_root / "bin")
    shutil.copytree(REPO_ROOT / "packages", package_root / "packages")

    environment = os.environ.copy()
    environment["npm_config_cache"] = str(npm_cache_root)
    environment["CODEX_HOME"] = str(codex_home)
    environment["HOME"] = str(home_root)

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
        env=environment,
        text=True,
    )

    assert completed_process.returncode == 0, completed_process.stderr
    assert "AHE Codex skill installed." in completed_process.stdout
    assert (codex_home / "skills/harness/SKILL.md").exists()
    assert (codex_home / "skills/converse/SKILL.md").exists()
    assert (codex_home / "skills/think/SKILL.md").exists()
    assert (codex_home / "ahe-shared/schemas/process_status.schema.json").exists()
    assert (codex_home / "hooks/hooks.json").exists()
    assert not (workspace_root / ".codex/skills/harness/SKILL.md").exists()


def test_helper_scripts_target_global_codex_home(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    codex_home = tmp_path / "global-codex"
    workspace_root.mkdir()
    codex_home.mkdir()
    home_root = tmp_path / "home"
    home_root.mkdir()

    package_root = tmp_path / "package"
    package_root.mkdir()

    shutil.copy2(REPO_ROOT / "package.json", package_root / "package.json")
    shutil.copytree(REPO_ROOT / "bin", package_root / "bin")
    shutil.copytree(REPO_ROOT / "packages", package_root / "packages")

    install_process = subprocess.run(
        (str(package_root / "bin" / "ahe"), "install"),
        cwd=workspace_root,
        check=False,
        capture_output=True,
        env=isolated_environment(codex_home, home_root),
        text=True,
    )

    assert install_process.returncode == 0, install_process.stderr
    assert (codex_home / "skills/harness/SKILL.md").exists()
    assert (codex_home / "skills/converse/SKILL.md").exists()
    assert (codex_home / "skills/think/SKILL.md").exists()
    assert (codex_home / "ahe-shared/templates/product.md").exists()
    assert (codex_home / "hooks/ahe-hook.js").exists()
    assert not (workspace_root / ".codex/skills/harness/SKILL.md").exists()

    hooks_config = json.loads((codex_home / "hooks/hooks.json").read_text(encoding="utf-8"))
    hook_command = hooks_config["hooks"]["UserPromptSubmit"][0]["hooks"][0]["command"]
    assert hook_command == f'node "{codex_home}/hooks/ahe-hook.js"'

    config_path = codex_home / "config.toml"
    config_path.write_text(
        '[agents.ahe-architecture-reviewer]\n'
        'config_file = "./agents/ahe-architecture-reviewer.toml"\n'
        '\n'
        '[agents.explorer]\n'
        'config_file = "./agents/explorer.toml"\n',
        encoding="utf-8",
    )

    uninstall_process = subprocess.run(
        (str(package_root / "bin" / "ahe"), "uninstall"),
        cwd=workspace_root,
        check=False,
        capture_output=True,
        env=isolated_environment(codex_home, home_root),
        text=True,
    )

    assert uninstall_process.returncode == 0, uninstall_process.stderr
    assert not (codex_home / "skills/new").exists()
    assert not (codex_home / "skills/converse").exists()
    assert not (codex_home / "skills/think").exists()
    assert not (codex_home / "ahe-shared").exists()
    assert not (codex_home / "hooks").exists()
    config_content = config_path.read_text(encoding="utf-8")
    assert "ahe-architecture-reviewer" not in config_content
    assert "[agents.explorer]" in config_content


def test_template_directory_keeps_only_agents_filename_uppercase() -> None:
    template_dir = CODEX_PACKAGE_ROOT / "ahe-shared/templates"

    actual_names = {path.name for path in template_dir.iterdir()}
    required_names = {"AGENTS.md", "product.md", "progress.md", "session-handoff.md"}
    forbidden_names = {"agents.md", "PRODUCT.md", "PROGRESS.md", "SESSION-HANDOFF.md"}

    missing_required_names = required_names.difference(actual_names)
    existing_forbidden_names = forbidden_names.intersection(actual_names)
    assert not missing_required_names, missing_required_names
    assert not existing_forbidden_names, existing_forbidden_names
