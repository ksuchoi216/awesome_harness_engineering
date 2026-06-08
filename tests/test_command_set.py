from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe/SKILL.md"


def test_skill_md_contains_required_alias_commands() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_commands = [
        "$ahe-init",
        "$ahe-agent",
        "$ahe-product",
        "$ahe-constraints",
        "$ahe-architecture",
        "$ahe-update",
        "$ahe-clear",
    ]
    for required_command in required_commands:
        assert required_command in content, (
            f"Missing command alias '{required_command}'"
        )


def test_skill_md_contains_required_context_docs() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_files = [
        "docs/constraints.md",
        "docs/achitecture.md",
        "feature-list.json",
        "PROGRESS.md",
        "SESSION-HANDOFF.md",
    ]
    for required_file in required_files:
        assert required_file in content, f"Missing file reference '{required_file}'"


if __name__ == "__main__":
    test_skill_md_contains_required_alias_commands()
    test_skill_md_contains_required_context_docs()
    print("test_command_set.py passed!")
