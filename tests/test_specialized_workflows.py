from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
AGENT_SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-agent/SKILL.md"
TODO_SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-todo/SKILL.md"
CONSTRAINTS_SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-constraints/SKILL.md"
ARCHITECTURE_SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-architecture/SKILL.md"
UPDATE_SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-update/SKILL.md"
HELP_SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-help/SKILL.md"
COPY_SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-copy/SKILL.md"


def test_skill_md_contains_agent_workflow() -> None:
    content = AGENT_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: ahe-agent" in content
    assert "Modify only the `PROJECT_PURPOSE` portion of `AGENTS.md`." in content
    assert "If `AGENTS.md` does not exist" in content
    assert "Copy `agents.md` from the template" in content or "Copy agents.md from templates" in content or "copy agents.md from templates" in content.lower()
    assert "Rename it to `AGENTS.md` (uppercase)" in content or "rename AGENTS.md(uppercase)" in content.lower() or "rename it to `AGENTS.md`" in content
    assert "Ask what the purpose of this project is to user." in content
    assert "Is your language Python?" in content
    assert "1. Yes" in content
    assert "2. No" in content
    assert "3. Custom input" in content
    assert "Which language do you use?" in content or "Which language do you use" in content


def test_skill_md_contains_constraints_workflow() -> None:
    content = CONSTRAINTS_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: ahe-constraints" in content
    assert "docs/constraints.md" in content


def test_skill_md_contains_todo_workflow() -> None:
    content = TODO_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: ahe-todo" in content
    assert "docs/todo.md" in content
    assert "feature-list.json" in content


def test_skill_md_contains_architecture_workflow() -> None:
    content = ARCHITECTURE_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: ahe-architecture" in content
    assert "docs/achitecture.md" in content


def test_skill_md_contains_update_workflow() -> None:
    content = UPDATE_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: ahe-update" in content
    assert "Apply the queued `docs/todo.md` content to `docs/PRODUCT.md`." in content
    assert "Remove the applied content from `docs/todo.md`" in content
    assert "Update `feature-list.json`." in content
    assert "Update `PROGRESS.md`." in content
    assert "Update `SESSION-HANDOFF.md`." in content


def test_skill_md_contains_help_workflow() -> None:
    content = HELP_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: ahe-help" in content
    assert "$ahe-help" in content
    assert "Show a list of commands" in content or "Show this command summary" in content


def test_skill_md_contains_copy_workflow() -> None:
    content = COPY_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: ahe-copy" in content
    assert "$ahe-copy" in content
    assert "Ignore `AGENTS.md`" in content
    assert "progress.md" in content or "PROGRESS.md" in content


if __name__ == "__main__":
    test_skill_md_contains_agent_workflow()
    test_skill_md_contains_todo_workflow()
    test_skill_md_contains_constraints_workflow()
    test_skill_md_contains_architecture_workflow()
    test_skill_md_contains_update_workflow()
    test_skill_md_contains_help_workflow()
    test_skill_md_contains_copy_workflow()
    print("test_specialized_workflows.py passed!")
