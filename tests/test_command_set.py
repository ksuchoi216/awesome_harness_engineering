from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / ".codex/skills"


def test_repository_contains_only_the_expected_ahe_skill_names() -> None:
    actual_skill_names = sorted(path.parent.name for path in SKILL_DIR.glob("*/SKILL.md"))
    expected_skill_names = sorted(
        [
            "ahe-compression",
            "ahe-conversator",
            "ahe-fix",
            "ahe-harness",
            "ahe-new",
            "ahe-reviewer",
            "ahe-ship",
            "ahe-solver",
            "ahe-thinker",
        ]
    )
    assert actual_skill_names == expected_skill_names


def test_public_command_skills_are_user_facing_commands() -> None:
    init_content = (SKILL_DIR / "ahe-new/SKILL.md").read_text(encoding="utf-8")
    assert "$ahe-new" in init_content

    ship_content = (SKILL_DIR / "ahe-ship/SKILL.md").read_text(encoding="utf-8")
    assert "$ahe-ship" in ship_content
    assert "ahe ship" in ship_content
    assert "ahe-thinker" in ship_content
    assert "must not call" in ship_content.lower()

    fix_content = (SKILL_DIR / "ahe-fix/SKILL.md").read_text(encoding="utf-8")
    assert "$ahe-fix" in fix_content
    assert "ahe fix" in fix_content
    assert ".plans/{plan_name}.md" in fix_content
    assert "ahe-conversator" in fix_content

    internal_skill_names = (
        "ahe-compression",
        "ahe-conversator",
        "ahe-harness",
        "ahe-reviewer",
        "ahe-solver",
        "ahe-thinker",
    )

    for skill_name in internal_skill_names:
        content = (SKILL_DIR / f"{skill_name}/SKILL.md").read_text(encoding="utf-8")
        assert "not a user-facing command" in content.lower()


def test_split_skill_set_covers_required_context_docs() -> None:
    combined_content = "\n".join(
        skill_path.read_text(encoding="utf-8")
        for skill_path in sorted(SKILL_DIR.glob("*/SKILL.md"))
    )
    for required_file in (
        "docs/product.md",
        "docs/INSTRUCTIONS.md",
        "docs/todo.md",
        "feature-list.json",
        "progress.md",
        "session-handoff.md",
    ):
        assert required_file in combined_content, f"Missing file reference '{required_file}'"

    for required_skill_name in (
        "ahe-thinker",
        "ahe-reviewer",
        "ahe-conversator",
        "ahe-harness",
        "ahe-solver",
    ):
        assert required_skill_name in combined_content, (
            f"Missing internal agent reference '{required_skill_name}'"
        )


if __name__ == "__main__":
    test_repository_contains_only_the_expected_ahe_skill_names()
    test_split_skill_set_covers_required_context_docs()
    print("test_command_set.py passed!")
