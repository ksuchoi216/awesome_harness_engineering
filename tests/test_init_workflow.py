from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-init/SKILL.md"

def test_skill_md_contains_init_workflow_sections() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: ahe-init" in content, "Missing '## Command Workflow: ahe-init' section"
    assert "Workspace Inspection" in content, "Missing Workspace Inspection step description"
    assert "Sequential Conversation Flow" in content, "Missing Sequential Conversation Flow description"
    assert "Harness Generation" in content, "Missing Harness Generation step description"

def test_skill_md_contains_all_required_inputs() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_inputs = [
        "ask the user whether the current `AGENTS.md` is right",
        "ask for the purpose of this project",
        "PROJECT_PURPOSE",
        "project language is Python",
        "Which language do you use?",
    ]
    for required_input in required_inputs:
        assert required_input in content, f"Missing required input '{required_input}' in ahe-init workflow definition"

def test_skill_md_contains_generated_files() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_files = [
        "AGENTS.md",
        ".ahe/process_status.json",
    ]
    for required_file in required_files:
        assert required_file in content, f"Missing required output file '{required_file}' in ahe-init workflow definition"

def test_skill_md_contains_three_sequential_steps_and_status_tracking() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    expected_steps = [
        'call "ahe-spec"',
        'call "ahe-update"',
    ]
    for step in expected_steps:
        assert step in content, f"Missing step '{step}' in ahe-init workflow definition"

    expected_statuses = [
        'ahe-init',
        'ahe-spec',
        'ahe-update',
    ]
    for status in expected_statuses:
        assert status in content, f"Missing progress status '{status}' in ahe-init workflow definition"


def test_skill_md_absorbs_reset_and_backup_behavior_for_new_start() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_behaviors = [
        ".ahe/backups/",
        "Copy `AGENTS.md` into the backup directory",
        "Copy the current `docs/PRODUCT.md` into the backup directory",
        "Remove the previous `docs/PRODUCT.md`",
        "Remove the previous `feature-list.json`",
        "new start",
    ]
    for required_behavior in required_behaviors:
        assert required_behavior in content, (
            f"Missing absorbed reset behavior '{required_behavior}' in ahe-init"
        )


if __name__ == "__main__":
    test_skill_md_contains_init_workflow_sections()
    test_skill_md_contains_all_required_inputs()
    test_skill_md_contains_generated_files()
    test_skill_md_contains_three_sequential_steps_and_status_tracking()
    test_skill_md_absorbs_reset_and_backup_behavior_for_new_start()
    print("test_init_workflow.py passed!")
