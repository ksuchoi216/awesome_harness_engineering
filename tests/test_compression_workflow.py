from __future__ import annotations

import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / "packages/ahe-codex/.codex/skills/ahe-compress"
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
    harness_file = tmp_path / "progress.md"
    harness_file.write_text(
        "\n".join(f"- item {index}" for index in range(180)) + "\n",
        encoding="utf-8",
    )

    completed_process = run_detector(tmp_path, "progress.md")

    assert completed_process.returncode == 2
    assert "COMPRESS\tprogress.md\t180\tlimit=180" in completed_process.stdout
    assert "COMPRESSION_REQUIRED" in completed_process.stdout


def test_detector_checks_numbered_product_stage_docs(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    stage_file = docs_dir / "product1.md"
    stage_file.write_text(
        "\n".join(f"- stage item {index}" for index in range(180)) + "\n",
        encoding="utf-8",
    )

    completed_process = run_detector(tmp_path)

    assert completed_process.returncode == 2
    assert "COMPRESS\tdocs/product1.md\t180\tlimit=180" in completed_process.stdout
    assert "COMPRESSION_REQUIRED" in completed_process.stdout


def test_detector_ignores_non_numeric_product_docs_by_default(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    stage_file = docs_dir / "product-alpha.md"
    stage_file.write_text(
        "\n".join(f"- ignored item {index}" for index in range(180)) + "\n",
        encoding="utf-8",
    )

    completed_process = run_detector(tmp_path)

    assert completed_process.returncode == 0
    assert "docs/product-alpha.md" not in completed_process.stdout
    assert "COMPRESSION_NOT_REQUIRED" in completed_process.stdout


def test_product_docs_route_thinking_to_compression() -> None:
    thinking_content = (
        REPO_ROOT / "packages/ahe-codex/.codex/skills/ahe-think/SKILL.md"
    ).read_text(encoding="utf-8")
    harness_content = (
        REPO_ROOT / "packages/ahe-codex/.codex/skills/ahe-harness/SKILL.md"
    ).read_text(encoding="utf-8")
    product_content = (REPO_ROOT / "docs/product.md").read_text(encoding="utf-8")
    hook_content = (
        REPO_ROOT / "packages/ahe-codex/.codex/hooks/ahe-hook.js"
    ).read_text(encoding="utf-8")
    bin_content = (
        REPO_ROOT / "packages/ahe-codex/bin/ahe-codex"
    ).read_text(encoding="utf-8")

    assert "check-harness-size.sh" in thinking_content
    assert "COMPRESSION_REQUIRED" in thinking_content
    assert "detect_stale_tests.py" in thinking_content
    assert "must not delete tests directly" in thinking_content
    assert "Run both compression detectors before choosing the next compression step." in thinking_content
    assert "stale overlapping tests" in product_content
    assert "TEST_COMPRESSION_REQUIRED" in product_content
    assert "For `ahe compress`, run both the harness-size detector and the stale-test detector." in product_content
    assert "replace old completed feature entries with one summarized done feature" in harness_content
    assert "Do not create backup copies when compressing harness history." in harness_content
    assert "ahe-compress" in product_content
    assert "ahe-compress" in hook_content
    assert '"ahe-compress"' in bin_content
    assert ".ahe/backups" not in harness_content


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
