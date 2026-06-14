from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
INIT_SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-init/SKILL.md"
SPEC_SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-spec/SKILL.md"
UPDATE_SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-update/SKILL.md"


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


def test_skill_md_contains_spec_workflow() -> None:
    content = SPEC_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: ahe-spec" in content
    assert "docs/PRODUCT.md" in content
    assert "docs/constraints.md" in content
    assert "docs/achitecture.md" in content


def test_skill_md_contains_update_workflow() -> None:
    content = UPDATE_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: ahe-update" in content
    assert "docs/todo.md" in content
    assert "feature-list.json" in content
    assert "append" in content.lower() or "capture" in content.lower()
    assert "Apply the queued `docs/todo.md` content to `docs/PRODUCT.md`." in content
    assert "Remove the applied content from `docs/todo.md`" in content
    assert "Update `feature-list.json`." in content
    assert "Update `PROGRESS.md`." in content
    assert "Update `SESSION-HANDOFF.md`." in content


def test_internal_skills_are_no_longer_user_facing_commands() -> None:
    for skill_path in (
        REPO_ROOT / ".codex/skills/ahe-spec/SKILL.md",
        REPO_ROOT / ".codex/skills/ahe-update/SKILL.md",
    ):
        content = skill_path.read_text(encoding="utf-8")
        assert "not a user-facing command" in content.lower()


if __name__ == "__main__":
    test_skill_md_contains_init_workflow_details_absorbed_from_agent_and_copy()
    test_skill_md_contains_spec_workflow()
    test_skill_md_contains_update_workflow()
    test_internal_skills_are_no_longer_user_facing_commands()
    print("test_specialized_workflows.py passed!")
