from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe/SKILL.md"


def test_skill_md_contains_clear_workflow_section() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: ahe clear" in content
    assert "Clear Preparation" in content
    assert "New Product Conversation Flow" in content
    assert "Clear Completion" in content


def test_skill_md_contains_required_clear_backup_behavior() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_behaviors = [
        "Copy the current `docs/PRODUCT.md` into the backup directory",
        "Copy the current `AGENTS.md` into the backup directory",
        "preserving the `docs/PRODUCT.md` relative path",
        "preserving the `AGENTS.md` relative path",
        "Do not delete or overwrite `docs/PRODUCT.md` or `AGENTS.md`",
    ]
    for required_behavior in required_behaviors:
        assert required_behavior in content, (
            f"Missing clear backup behavior '{required_behavior}'"
        )


def test_skill_md_contains_required_clear_conversation_behavior() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_behaviors = [
        "set `current_command` to `ahe clear`",
        "set `workflow_complete` to `false`",
        "set `current_step` to `ask_new_goal`",
        "Ask exactly ONE focused question at a time",
        "First ask the user for the new goal",
        "advance `current_step` to `ask_new_product_spec`",
        "Then ask the user for the new `docs/PRODUCT.md` content or product specification inputs",
        "Save progress after every answer",
    ]
    for required_behavior in required_behaviors:
        assert required_behavior in content, (
            f"Missing clear conversation behavior '{required_behavior}'"
        )


if __name__ == "__main__":
    test_skill_md_contains_clear_workflow_section()
    test_skill_md_contains_required_clear_backup_behavior()
    test_skill_md_contains_required_clear_conversation_behavior()
    print("test_clear_workflow.py passed!")
