from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
INIT_SKILL_MD_PATH = REPO_ROOT / "packages/ahe-codex/.codex/skills/new/SKILL.md"
HARNESS_SKILL_MD_PATH = REPO_ROOT / "packages/ahe-codex/.codex/skills/harness/SKILL.md"
SOLVER_SKILL_MD_PATH = REPO_ROOT / "packages/ahe-codex/.codex/skills/solve/SKILL.md"


def test_skill_md_contains_init_workflow_details_absorbed_from_agent_and_copy() -> None:
    content = INIT_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: new" in content
    assert "Update only the `PROJECT_PURPOSE` portion of `AGENTS.md`." in content
    assert "project language is Python" in content
    assert "Which language do you use?" in content
    assert "template" in content.lower()
    assert "overwrite" in content.lower()
    assert "Codex-supported structured response request" in content
    assert "custom input" in content.lower()


def test_skill_md_contains_harness_workflow() -> None:
    content = HARNESS_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: harness" in content
    assert "docs/product.md" in content
    assert "docs/INSTRUCTIONS.md" in content


def test_skill_md_contains_harness_tracking_workflow() -> None:
    content = HARNESS_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "docs/todo.md" in content
    assert "feature-list.json" in content
    assert "append" in content.lower() or "capture" in content.lower()
    assert "Apply the queued `docs/todo.md` content to `docs/product.md`." in content
    assert "Remove the applied content from `docs/todo.md`" in content
    assert "Update `feature-list.json` to derive the specific feature items from the updated `docs/product.md`." in content
    assert "Update `progress.md`." in content
    assert "Update `session-handoff.md`." in content
    assert "If no new feature can be derived from `docs/product.md`, call `converse`" in content


def test_internal_skills_are_no_longer_user_facing_commands() -> None:
    for skill_path in (
        REPO_ROOT / "packages/ahe-codex/.codex/skills/harness/SKILL.md",
        REPO_ROOT / "packages/ahe-codex/.codex/skills/solve/SKILL.md",
    ):
        content = skill_path.read_text(encoding="utf-8")
        assert "not a user-facing command" in content.lower()


def test_solver_skill_describes_divide_and_plan_behavior() -> None:
    content = SOLVER_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "divide" in content.lower()
    assert "plan" in content.lower()
    assert "review" in content
    assert "converse" in content


def test_solver_reads_active_product_stage_context() -> None:
    content = SOLVER_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "docs/product.md" in content
    assert "active product stage" in content
    assert "docs/product1.md" in content
    assert "future product stages" in content


if __name__ == "__main__":
    test_skill_md_contains_init_workflow_details_absorbed_from_agent_and_copy()
    test_skill_md_contains_harness_workflow()
    test_skill_md_contains_harness_tracking_workflow()
    test_internal_skills_are_no_longer_user_facing_commands()
    test_solver_skill_describes_divide_and_plan_behavior()
    test_solver_reads_active_product_stage_context()
    print("test_specialized_workflows.py passed!")
