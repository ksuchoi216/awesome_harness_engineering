from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / "packages/ahe-codex/.codex/skills"
SOLVER_SKILL_MD_PATH = SKILL_DIR / "ahe-solve/SKILL.md"


def test_repository_contains_only_the_expected_ahe_skill_names() -> None:
    actual_skill_names = sorted(path.parent.name for path in SKILL_DIR.glob("*/SKILL.md"))
    assert "ahe-fix" not in actual_skill_names
    for expected_skill_name in (
        "ahe",
        "ahe-clean",
        "ahe-converse",
        "ahe-feature",
        "ahe-git",
        "ahe-harness",
        "ahe-harness-checker",
        "ahe-new",
        "ahe-overview",
        "ahe-review",
        "ahe-ship",
        "ahe-solve",
        "ahe-think",
    ):
        assert expected_skill_name in actual_skill_names


def test_public_command_skills_are_user_facing_commands() -> None:
    ahe_content = (SKILL_DIR / "ahe/SKILL.md").read_text(encoding="utf-8")
    assert "exact `ahe`" in ahe_content
    assert "ahe-think" in ahe_content

    init_content = (SKILL_DIR / "ahe-new/SKILL.md").read_text(encoding="utf-8")
    assert "not a user-facing command" in init_content.lower()

    ship_content = (SKILL_DIR / "ahe-ship/SKILL.md").read_text(encoding="utf-8")
    assert "ahe-ship" in ship_content
    assert "ahe-ship" in ship_content
    assert "independent" in ship_content.lower()
    assert "plan" in ship_content.lower()

    overview_content = (SKILL_DIR / "ahe-overview/SKILL.md").read_text(encoding="utf-8")
    assert "ahe-overview" in overview_content
    assert "ahe-think" in overview_content
    assert "ahe-harness" in overview_content
    assert "ahe-review" in overview_content
    assert "ahe-converse" in overview_content
    assert "ahe ship" in overview_content

    git_content = (SKILL_DIR / "ahe-git/SKILL.md").read_text(encoding="utf-8")
    assert "ahe-git" in git_content
    assert "independent" in git_content.lower()

    internal_skill_names = (
        "ahe-clean",
        "ahe-converse",
        "ahe-harness",
        "ahe-harness-checker",
        "ahe-new",
        "ahe-review",
        "ahe-solve",
        "ahe-think",
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
        "ahe-clean",
        "ahe-think",
        "ahe-review",
        "ahe-converse",
        "ahe-harness",
        "ahe-solve",
    ):
        assert required_skill_name in combined_content, (
            f"Missing internal agent reference '{required_skill_name}'"
        )

def test_internal_skills_are_no_longer_user_facing_commands() -> None:
    for skill_path in (
        REPO_ROOT / "packages/ahe-codex/.codex/skills/ahe-harness/SKILL.md",
        REPO_ROOT / "packages/ahe-codex/.codex/skills/ahe-solve/SKILL.md",
    ):
        content = skill_path.read_text(encoding="utf-8")
        assert "not a user-facing command" in content.lower()



def test_solver_skill_describes_divide_and_plan_behavior() -> None:
    content = SOLVER_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "divide" in content.lower()
    assert "plan" in content.lower()
    assert "review" in content
    assert "converse" in content




if __name__ == "__main__":
    test_repository_contains_only_the_expected_ahe_skill_names()
    test_split_skill_set_covers_required_context_docs()
    print("test_command_set.py passed!")
