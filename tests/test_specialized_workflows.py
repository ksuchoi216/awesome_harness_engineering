from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe/SKILL.md"


def test_skill_md_contains_agent_workflow() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: ahe-agent" in content
    assert "Modify only the `PROJECT_PURPOSE` portion of `AGENTS.md`." in content


def test_skill_md_contains_constraints_workflow() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: ahe-constraints" in content
    assert "docs/constraints.md" in content


def test_skill_md_contains_architecture_workflow() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: ahe-architecture" in content
    assert "docs/achitecture.md" in content


def test_skill_md_contains_update_workflow() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: ahe-update" in content
    assert "Update `feature-list.json`." in content
    assert "Update `PROGRESS.md`." in content
    assert "Update `SESSION-HANDOFF.md`." in content


if __name__ == "__main__":
    test_skill_md_contains_agent_workflow()
    test_skill_md_contains_constraints_workflow()
    test_skill_md_contains_architecture_workflow()
    test_skill_md_contains_update_workflow()
    print("test_specialized_workflows.py passed!")
