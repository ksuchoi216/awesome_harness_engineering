from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe/SKILL.md"


def test_skill_md_contains_check_workflow_sections() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: ahe check" in content
    assert "Validation Scope" in content
    assert "Check Reporting" in content


def test_skill_md_contains_required_check_rules() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_rules = [
        "Required files exist",
        "Required sections exist",
        "Required fields are filled",
        "Filename casing is correct",
        "AGENTS.md references docs/PRODUCT.md",
        ".ahe/process_status.json matches the actual workspace state",
        "feature-list.json is valid JSON",
    ]
    for required_rule in required_rules:
        assert required_rule in content, (
            f"Missing check rule '{required_rule}' in ahe check workflow definition"
        )


def test_skill_md_contains_resume_workflow_sections() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: ahe resume" in content
    assert "Resume State Inspection" in content
    assert "Resume Decision and Next Prompt" in content


def test_skill_md_contains_required_resume_behaviors() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_behaviors = [
        "Read `.ahe/process_status.json`",
        "Identify the previous `current_command`",
        "Identify the previous `current_step`",
        "Summarize already collected fields",
        "Ask the next missing question",
        "Run a lightweight AHE status check",
        "Recommend the next useful command",
        "No unfinished AHE workflow found.",
    ]
    for required_behavior in required_behaviors:
        assert required_behavior in content, (
            f"Missing resume behavior '{required_behavior}' in ahe resume workflow definition"
        )


if __name__ == "__main__":
    test_skill_md_contains_check_workflow_sections()
    test_skill_md_contains_required_check_rules()
    test_skill_md_contains_resume_workflow_sections()
    test_skill_md_contains_required_resume_behaviors()
    print("test_check_resume_workflows.py passed!")
