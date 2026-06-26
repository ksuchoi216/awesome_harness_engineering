from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
REQUIRED_SKILL_FILES = (
    Path(".codex/skills/ahe-init/SKILL.md"),
    Path(".codex/skills/ahe-conversator/SKILL.md"),
    Path(".codex/skills/ahe-thinker/SKILL.md"),
    Path(".codex/skills/ahe-reviewer/SKILL.md"),
    Path(".codex/skills/ahe-harness/SKILL.md"),
    Path(".codex/skills/ahe-solver/SKILL.md"),
    Path(".codex/skills/ahe-compression/SKILL.md"),
    Path(".codex/ahe-shared/config.yaml"),
    Path(".codex/ahe-shared/templates/AGENTS.md"),
    Path(".codex/ahe-shared/templates/product.md"),
    Path(".codex/ahe-shared/templates/INSTRUCTIONS.md"),
    Path(".codex/ahe-shared/templates/progress.md"),
    Path(".codex/ahe-shared/templates/session-handoff.md"),
    Path(".codex/ahe-shared/templates/init.sh"),
    Path(".codex/ahe-shared/templates/feature-list.json"),
    Path(".codex/ahe-shared/schemas/process_status.schema.json"),
    Path(".codex/ahe-shared/schemas/feature-list-schema.json"),
    Path(".codex/hooks/hooks.json"),
    Path(".codex/hooks/ahe-hook.js"),
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

    assert package_json["name"] == "@ksuchoi216/ahe"
    assert package_json["bin"]["ahe"] == "./bin/ahe"


def test_product_contract_requires_global_installation() -> None:
    product_content = (REPO_ROOT / "docs/product.md").read_text(encoding="utf-8")
    readme_content = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    assert "AHE always installs into the global Codex home" in product_content
    assert "must not" in product_content
    assert "be copied into each target workspace" in product_content
    assert "AHE installs global Codex skills" in readme_content


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

    shutil.copy2(REPO_ROOT / "package.json", package_root / "package.json")
    shutil.copytree(REPO_ROOT / "bin", package_root / "bin")
    shutil.copytree(REPO_ROOT / ".codex", package_root / ".codex")

    completed_process = subprocess.run(
        (str(package_root / "bin" / "ahe"), "install"),
        cwd=workspace_root,
        check=False,
        capture_output=True,
        env={**os.environ, "CODEX_HOME": str(codex_home)},
        text=True,
    )

    assert completed_process.returncode == 0, completed_process.stderr
    assert "AHE Codex skill installed." in completed_process.stdout
    assert str(codex_home) in completed_process.stdout
    assert (codex_home / "skills/ahe-init/SKILL.md").exists()
    assert (codex_home / "skills/ahe-conversator/SKILL.md").exists()
    assert (codex_home / "skills/ahe-thinker/SKILL.md").exists()
    assert (codex_home / "skills/ahe-harness/SKILL.md").exists()
    assert (codex_home / "ahe-shared/templates/AGENTS.md").exists()
    assert (codex_home / "hooks/hooks.json").exists()
    assert (codex_home / "hooks/ahe-hook.js").exists()
    assert not (workspace_root / ".codex/skills/ahe-init/SKILL.md").exists()


def test_installer_removes_stale_ahe_config_entries(tmp_path: Path) -> None:
    package_root = tmp_path / "package"
    workspace_root = tmp_path / "workspace"
    codex_home = tmp_path / "codex-home"
    config_path = codex_home / "config.toml"

    package_root.mkdir()
    workspace_root.mkdir()
    config_path.parent.mkdir()

    shutil.copy2(REPO_ROOT / "package.json", package_root / "package.json")
    shutil.copytree(REPO_ROOT / "bin", package_root / "bin")
    shutil.copytree(REPO_ROOT / ".codex", package_root / ".codex")

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
        env={**os.environ, "CODEX_HOME": str(codex_home)},
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

    shutil.copy2(REPO_ROOT / "package.json", package_root / "package.json")
    shutil.copytree(REPO_ROOT / "bin", package_root / "bin")
    shutil.copytree(REPO_ROOT / ".codex", package_root / ".codex")
    shutil.copytree(package_root / ".codex/skills", codex_home / "skills")
    shutil.copytree(package_root / ".codex/ahe-shared", codex_home / "ahe-shared")
    shutil.copytree(package_root / ".codex/hooks", codex_home / "hooks")

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
        env={**os.environ, "CODEX_HOME": str(codex_home)},
        text=True,
    )

    assert completed_process.returncode == 0, completed_process.stderr
    config_content = config_path.read_text(encoding="utf-8")
    assert "@ksuchoi216/ahe" not in config_content
    assert '[plugins."other"]' in config_content
    assert not (codex_home / "skills/ahe-init").exists()
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

    shutil.copy2(REPO_ROOT / "package.json", package_root / "package.json")
    shutil.copytree(REPO_ROOT / "bin", package_root / "bin")
    shutil.copytree(REPO_ROOT / ".codex", package_root / ".codex")

    environment = os.environ.copy()
    environment["npm_config_cache"] = str(npm_cache_root)
    environment["CODEX_HOME"] = str(codex_home)

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
    assert (codex_home / "skills/ahe-harness/SKILL.md").exists()
    assert (codex_home / "skills/ahe-conversator/SKILL.md").exists()
    assert (codex_home / "skills/ahe-thinker/SKILL.md").exists()
    assert (codex_home / "ahe-shared/schemas/process_status.schema.json").exists()
    assert (codex_home / "hooks/hooks.json").exists()
    assert not (workspace_root / ".codex/skills/ahe-harness/SKILL.md").exists()


def test_helper_scripts_target_global_codex_home(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    codex_home = tmp_path / "global-codex"
    workspace_root.mkdir()
    codex_home.mkdir()

    package_root = tmp_path / "package"
    package_root.mkdir()

    shutil.copy2(REPO_ROOT / "package.json", package_root / "package.json")
    shutil.copytree(REPO_ROOT / "bin", package_root / "bin")
    shutil.copytree(REPO_ROOT / ".codex", package_root / ".codex")

    install_process = subprocess.run(
        (str(package_root / "bin" / "ahe"), "install"),
        cwd=workspace_root,
        check=False,
        capture_output=True,
        env={**os.environ, "CODEX_HOME": str(codex_home)},
        text=True,
    )

    assert install_process.returncode == 0, install_process.stderr
    assert (codex_home / "skills/ahe-harness/SKILL.md").exists()
    assert (codex_home / "skills/ahe-conversator/SKILL.md").exists()
    assert (codex_home / "skills/ahe-thinker/SKILL.md").exists()
    assert (codex_home / "ahe-shared/templates/product.md").exists()
    assert (codex_home / "hooks/ahe-hook.js").exists()
    assert not (workspace_root / ".codex/skills/ahe-harness/SKILL.md").exists()

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
        env={**os.environ, "CODEX_HOME": str(codex_home)},
        text=True,
    )

    assert uninstall_process.returncode == 0, uninstall_process.stderr
    assert not (codex_home / "skills/ahe-init").exists()
    assert not (codex_home / "skills/ahe-conversator").exists()
    assert not (codex_home / "skills/ahe-thinker").exists()
    assert not (codex_home / "ahe-shared").exists()
    assert not (codex_home / "hooks").exists()
    config_content = config_path.read_text(encoding="utf-8")
    assert "ahe-architecture-reviewer" not in config_content
    assert "[agents.explorer]" in config_content


def test_template_directory_keeps_only_agents_filename_uppercase() -> None:
    template_dir = REPO_ROOT / ".codex/ahe-shared/templates"

    actual_names = {path.name for path in template_dir.iterdir()}
    required_names = {"AGENTS.md", "product.md", "progress.md", "session-handoff.md"}
    forbidden_names = {"agents.md", "PRODUCT.md", "PROGRESS.md", "SESSION-HANDOFF.md"}

    missing_required_names = required_names.difference(actual_names)
    existing_forbidden_names = forbidden_names.intersection(actual_names)
    assert not missing_required_names, missing_required_names
    assert not existing_forbidden_names, existing_forbidden_names
