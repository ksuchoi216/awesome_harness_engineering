from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / ".codex/skills"


def test_repository_contains_only_the_expected_ahe_skill_names() -> None:
    actual_skill_names = sorted(path.name for path in SKILL_DIR.iterdir() if path.is_dir())
    expected_skill_names = sorted(
        [
            "ahe-agent",
            "ahe-architecture",
            "ahe-ask-user",
            "ahe-clear",
            "ahe-constraints",
            "ahe-help",
            "ahe-copy",
            "ahe-init",
            "ahe-product",
            "ahe-todo",
            "ahe-update",
        ]
    )
    assert actual_skill_names == expected_skill_names


def test_help_skill_does_not_expose_internal_protocols() -> None:
    help_content = (SKILL_DIR / "ahe-help/SKILL.md").read_text(encoding="utf-8")

    user_facing_commands = (
        "$ahe-init",
        "$ahe-agent",
        "$ahe-product",
        "$ahe-todo",
        "$ahe-constraints",
        "$ahe-architecture",
        "$ahe-update",
        "$ahe-clear",
        "$ahe-help",
        "$ahe-copy",
    )

    for command in user_facing_commands:
        assert command in help_content

    assert "$ahe-ask-user" not in help_content
    assert "ahe-ask-user" not in help_content


def test_split_skill_set_covers_required_context_docs() -> None:
    combined_content = "\n".join(
        skill_path.read_text(encoding="utf-8")
        for skill_path in sorted(SKILL_DIR.glob("*/SKILL.md"))
    )
    for required_file in (
        "docs/constraints.md",
        "docs/achitecture.md",
        "docs/todo.md",
        "feature-list.json",
        "PROGRESS.md",
        "SESSION-HANDOFF.md",
    ):
        assert required_file in combined_content, f"Missing file reference '{required_file}'"


if __name__ == "__main__":
    test_repository_contains_only_the_expected_ahe_skill_names()
    test_split_skill_set_covers_required_context_docs()
    print("test_command_set.py passed!")
