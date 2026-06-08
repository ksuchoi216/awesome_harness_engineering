from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe/SKILL.md"


def test_skill_md_contains_clarification_prompt_rule() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Clarification Prompt Rule" in content
    assert "needs clarification or a more detailed description" in content


def test_skill_md_contains_exact_clarification_prompt_format() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_lines = [
        "Please choose one option:",
        "1. Yes",
        "2. No",
        "3. Custom input",
        "Enter 1, 2, or type your own answer:",
    ]
    for required_line in required_lines:
        assert required_line in content, (
            f"Missing clarification prompt line '{required_line}'"
        )


def test_skill_md_defines_clarification_option_meanings() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_behaviors = [
        "If the user enters `1`, treat the answer as yes.",
        "If the user enters `2`, treat the answer as no.",
        "If the user enters `3` or any custom text",
        "continue the active AHE workflow",
    ]
    for required_behavior in required_behaviors:
        assert required_behavior in content, (
            f"Missing clarification behavior '{required_behavior}'"
        )


if __name__ == "__main__":
    test_skill_md_contains_clarification_prompt_rule()
    test_skill_md_contains_exact_clarification_prompt_format()
    test_skill_md_defines_clarification_option_meanings()
    print("test_clarification_prompt.py passed!")
