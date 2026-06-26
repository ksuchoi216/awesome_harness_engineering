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
        'call "ahe-harness"',
    ]
    for step in expected_steps:
        assert step in content, f"Missing step '{step}' in ahe-init workflow definition"

    expected_statuses = [
        'ahe-init',
        'ahe-harness',
    ]
    for status in expected_statuses:
        assert status in content, f"Missing progress status '{status}' in ahe-init workflow definition"


def test_skill_md_absorbs_reset_behavior_without_backups_for_new_start() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_behaviors = [
        "Remove the previous `docs/PRODUCT.md` and `docs/INSTRUCTIONS.md`",
        "Remove the previous `feature-list.json`",
        "new start",
        "Do not create backup copies of the replaced harness files",
    ]
    for required_behavior in required_behaviors:
        assert required_behavior in content, (
            f"Missing absorbed reset behavior '{required_behavior}' in ahe-init"
        )

    forbidden_behaviors = [
        ".ahe/backups/",
        "backup directory",
        "back up the current product/specification files",
    ]
    for forbidden_behavior in forbidden_behaviors:
        assert forbidden_behavior not in content, (
            f"Unexpected backup behavior '{forbidden_behavior}' still present in ahe-init"
        )


def test_skill_md_requires_restart_scope_before_resetting_existing_harness() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_behaviors = [
        "If no AHE-managed harness files exist, start initialization normally without asking a restart-scope question.",
        "If any AHE-managed harness file already exists, read the existing files first.",
        "summarize the current project purpose and product specification state",
        "ask what restart scope the user wants before removing, overwriting, or refreshing existing harness files",
        "Interpret the restart scope from the user's free-form answer",
        "`purpose` means restart the whole harness from the project purpose",
        "`product` means preserve the project purpose in `AGENTS.md`",
        "summarize the replaced harness history in the refreshed tracking artifacts instead of creating backups",
    ]
    for required_behavior in required_behaviors:
        assert required_behavior in content, (
            f"Missing restart-scope behavior '{required_behavior}' in ahe-init"
        )


def test_skill_md_keeps_specification_details_out_of_agents_md() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_behaviors = [
        "Keep `AGENTS.md` limited to the project purpose and base agent settings.",
        "Do not put product specification details in `AGENTS.md`.",
        "Send product behavior, scope, requirements, success criteria, and workflow details to `ahe-harness` so they are written in `docs/PRODUCT.md` first.",
        "Generating an empty `feature-list.json` from a template is allowed, but do not write concrete feature items until `docs/PRODUCT.md` is populated.",
    ]
    for required_behavior in required_behaviors:
        assert required_behavior in content, (
            f"Missing specification placement behavior '{required_behavior}' in ahe-init"
        )


if __name__ == "__main__":
    test_skill_md_contains_init_workflow_sections()
    test_skill_md_contains_all_required_inputs()
    test_skill_md_contains_generated_files()
    test_skill_md_contains_three_sequential_steps_and_status_tracking()
    test_skill_md_absorbs_reset_behavior_without_backups_for_new_start()
    test_skill_md_requires_restart_scope_before_resetting_existing_harness()
    test_skill_md_keeps_specification_details_out_of_agents_md()
    print("test_init_workflow.py passed!")
