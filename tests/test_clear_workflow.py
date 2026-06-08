from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe/SKILL.md"


def test_skill_md_contains_clear_workflow_section() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: ahe-clear" in content
    assert "Clear Preparation" in content
    assert "Clear Removal" in content


def test_skill_md_contains_required_clear_backup_behavior() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_behaviors = [
        "Copy the current `docs/PRODUCT.md` into the backup directory",
        "Copy the current `PROGRESS.md` into the backup directory",
        "Copy the current `SESSION-HANDOFF.md` into the backup directory",
        "Copy the current `feature-list.json` into the backup directory",
        "preserving the `docs/PRODUCT.md` relative path",
        "preserving the `PROGRESS.md` relative path",
        "preserving the `SESSION-HANDOFF.md` relative path",
        "preserving the `feature-list.json` relative path",
    ]
    for required_behavior in required_behaviors:
        assert required_behavior in content, (
            f"Missing clear backup behavior '{required_behavior}'"
        )


def test_skill_md_contains_required_clear_removal_behavior() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_behaviors = [
        "Remove the previous `docs/PRODUCT.md`",
        "Remove the previous `PROGRESS.md`",
        "Remove the previous `SESSION-HANDOFF.md`",
        "Remove the previous `feature-list.json`",
        "current_command` is `$ahe-clear`",
        "workflow_complete` is `true`",
    ]
    for required_behavior in required_behaviors:
        assert required_behavior in content, (
            f"Missing clear removal behavior '{required_behavior}'"
        )


if __name__ == "__main__":
    test_skill_md_contains_clear_workflow_section()
    test_skill_md_contains_required_clear_backup_behavior()
    test_skill_md_contains_required_clear_removal_behavior()
    print("test_clear_workflow.py passed!")
