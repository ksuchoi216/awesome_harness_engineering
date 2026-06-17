from __future__ import annotations

import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / ".codex/skills/ahe-compression"
SCRIPT_PATH = SKILL_DIR / "scripts/check-harness-size.sh"


def run_detector(cwd: Path, *files: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ("sh", str(SCRIPT_PATH), *files),
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )


def test_detector_reports_no_compression_for_small_harness_file(tmp_path: Path) -> None:
    harness_file = tmp_path / "AGENTS.md"
    harness_file.write_text("# Project\n\nShort purpose.\n", encoding="utf-8")

    completed_process = run_detector(tmp_path, "AGENTS.md")

    assert completed_process.returncode == 0
    assert "OK\tAGENTS.md" in completed_process.stdout
    assert "COMPRESSION_NOT_REQUIRED" in completed_process.stdout


def test_detector_requires_compression_for_oversized_file(tmp_path: Path) -> None:
    harness_file = tmp_path / "PROGRESS.md"
    harness_file.write_text(
        "\n".join(f"- item {index}" for index in range(180)) + "\n",
        encoding="utf-8",
    )

    completed_process = run_detector(tmp_path, "PROGRESS.md")

    assert completed_process.returncode == 2
    assert "COMPRESS\tPROGRESS.md\t180\tlimit=180" in completed_process.stdout
    assert "COMPRESSION_REQUIRED" in completed_process.stdout


def test_product_docs_route_thinking_to_compression() -> None:
    thinking_content = (
        REPO_ROOT / ".codex/skills/ahe-thinking/SKILL.md"
    ).read_text(encoding="utf-8")
    product_content = (REPO_ROOT / "docs/PRODUCT.md").read_text(encoding="utf-8")
    hook_content = (REPO_ROOT / ".codex/hooks/ahe-hook.js").read_text(encoding="utf-8")
    bin_content = (REPO_ROOT / "bin/ahe").read_text(encoding="utf-8")

    assert "check-harness-size.sh" in thinking_content
    assert "COMPRESSION_REQUIRED" in thinking_content
    assert "ahe-compression" in product_content
    assert "ahe-compression" in hook_content
    assert '"ahe-compression"' in bin_content


def test_config_yaml_overrides_thresholds(tmp_path: Path) -> None:
    config_dir = tmp_path / ".codex" / "ahe-shared"
    config_dir.mkdir(parents=True)
    config_file = config_dir / "config.yaml"
    config_file.write_text(
        "agent_md: 80\n"
        "product_md: 180\n"
        "# This is a comment\n\n"
        "total: 750\n",
        encoding="utf-8"
    )

    harness_file = tmp_path / "AGENTS.md"
    harness_file.write_text(
        "\n".join(f"- item {index}" for index in range(80)) + "\n",
        encoding="utf-8",
    )

    completed_process = run_detector(tmp_path, "AGENTS.md")

    assert completed_process.returncode == 2
    assert "COMPRESS\tAGENTS.md\t80\tlimit=80" in completed_process.stdout

    config_file.write_text("agent_md: 100\n", encoding="utf-8")
    
    completed_process = run_detector(tmp_path, "AGENTS.md")
    assert completed_process.returncode == 0
    assert "OK\tAGENTS.md\t80\tlimit=100" in completed_process.stdout


def test_config_yaml_total_override(tmp_path: Path) -> None:
    config_dir = tmp_path / ".codex" / "ahe-shared"
    config_dir.mkdir(parents=True)
    config_file = config_dir / "config.yaml"
    config_file.write_text("total: 100\n", encoding="utf-8")

    harness_file = tmp_path / "AGENTS.md"
    harness_file.write_text(
        "\n".join(f"- item {index}" for index in range(105)) + "\n",
        encoding="utf-8",
    )

    completed_process = run_detector(tmp_path, "AGENTS.md")

    assert completed_process.returncode == 2
    assert "COMPRESS_TOTAL\t105\tlimit=100" in completed_process.stdout


def test_missing_config_preserves_defaults(tmp_path: Path) -> None:
    harness_file = tmp_path / "AGENTS.md"
    harness_file.write_text(
        "\n".join(f"- item {index}" for index in range(179)) + "\n",
        encoding="utf-8",
    )

    completed_process = run_detector(tmp_path, "AGENTS.md")
    assert completed_process.returncode == 0
    assert "OK\tAGENTS.md\t179\tlimit=180" in completed_process.stdout


if __name__ == "__main__":
    test_product_docs_route_thinking_to_compression()
    print("test_compression_workflow.py passed!")
