from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_MD_PATHS = (
    REPO_ROOT / ".codex/skills/ahe-init/SKILL.md",
    REPO_ROOT / ".codex/skills/ahe-product/SKILL.md",
)


def test_skill_md_contains_clarification_prompt_rule() -> None:
    for skill_path in SKILL_MD_PATHS:
        content = skill_path.read_text(encoding="utf-8")
        assert "## Clarification Rule" in content
        assert "needs clarification or a more detailed description" in content


def test_skill_md_contains_exact_clarification_prompt_format() -> None:
    required_lines = [
        "Please choose one option:",
        "1. Yes",
        "2. No",
        "3. Custom input",
        "Enter 1, 2, or type your own answer:",
    ]
    for skill_path in SKILL_MD_PATHS:
        content = skill_path.read_text(encoding="utf-8")
        for required_line in required_lines:
            assert required_line in content, (
                f"Missing clarification prompt line '{required_line}'"
            )


if __name__ == "__main__":
    test_skill_md_contains_clarification_prompt_rule()
    test_skill_md_contains_exact_clarification_prompt_format()
    print("test_clarification_prompt.py passed!")
