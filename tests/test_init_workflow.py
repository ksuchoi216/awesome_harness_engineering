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

def test_skill_md_contains_four_sequential_steps_and_status_tracking() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    expected_steps = [
        'call "ahe-agent"',
        'call "ahe-spec"',
        'call "ahe-copy"',
        'call "ahe-update"',
    ]
    for step in expected_steps:
        assert step in content, f"Missing step '{step}' in ahe-init workflow definition"

    expected_statuses = [
        'ahe-agent',
        'ahe-spec',
        'ahe-copy',
        'ahe-update',
    ]
    for status in expected_statuses:
        assert status in content, f"Missing progress status '{status}' in ahe-init workflow definition"


if __name__ == "__main__":
    test_skill_md_contains_init_workflow_sections()
    test_skill_md_contains_all_required_inputs()
    test_skill_md_contains_generated_files()
    test_skill_md_contains_four_sequential_steps_and_status_tracking()
    print("test_init_workflow.py passed!")
