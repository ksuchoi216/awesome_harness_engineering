from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
INIT_SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-init/SKILL.md"
HARNESS_SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-harness/SKILL.md"
SOLVER_SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-solver/SKILL.md"


def test_skill_md_contains_init_workflow_details_absorbed_from_agent_and_copy() -> None:
    content = INIT_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: ahe-init" in content
    assert "Update only the `PROJECT_PURPOSE` portion of `AGENTS.md`." in content
    assert "project language is Python" in content
    assert "Which language do you use?" in content
    assert "template" in content.lower()
    assert "overwrite" in content.lower()
    assert "Codex-supported structured response request" in content
    assert "custom input" in content.lower()


def test_skill_md_contains_harness_workflow() -> None:
    content = HARNESS_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: ahe-harness" in content
    assert "docs/PRODUCT.md" in content
    assert "docs/INSTRUCTIONS.md" in content


def test_skill_md_contains_harness_tracking_workflow() -> None:
    content = HARNESS_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "docs/todo.md" in content
    assert "feature-list.json" in content
    assert "append" in content.lower() or "capture" in content.lower()
    assert "Apply the queued `docs/todo.md` content to `docs/PRODUCT.md`." in content
    assert "Remove the applied content from `docs/todo.md`" in content
    assert "Update `feature-list.json` to derive the specific feature items from the updated `docs/PRODUCT.md`." in content
    assert "Update `PROGRESS.md`." in content
    assert "Update `SESSION-HANDOFF.md`." in content
    assert "If no new feature can be derived from `docs/PRODUCT.md`, call `ahe-conversator`" in content


def test_internal_skills_are_no_longer_user_facing_commands() -> None:
    for skill_path in (
        REPO_ROOT / ".codex/skills/ahe-harness/SKILL.md",
        REPO_ROOT / ".codex/skills/ahe-solver/SKILL.md",
    ):
        content = skill_path.read_text(encoding="utf-8")
        assert "not a user-facing command" in content.lower()


def test_solver_skill_describes_divide_and_plan_behavior() -> None:
    content = SOLVER_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "divide" in content.lower()
    assert "plan" in content.lower()
    assert "ahe-reviewer" in content
    assert "ahe-conversator" in content


if __name__ == "__main__":
    test_skill_md_contains_init_workflow_details_absorbed_from_agent_and_copy()
    test_skill_md_contains_harness_workflow()
    test_skill_md_contains_harness_tracking_workflow()
    test_internal_skills_are_no_longer_user_facing_commands()
    test_solver_skill_describes_divide_and_plan_behavior()
    print("test_specialized_workflows.py passed!")
