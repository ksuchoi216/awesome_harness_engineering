from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_MD_PATHS = (
    REPO_ROOT / ".codex/skills/ahe-init/SKILL.md",
    REPO_ROOT / ".codex/skills/ahe-agent/SKILL.md",
    REPO_ROOT / ".codex/skills/ahe-spec/SKILL.md",
    REPO_ROOT / ".codex/skills/ahe-todo/SKILL.md",
    REPO_ROOT / ".codex/skills/ahe-clear/SKILL.md",
    REPO_ROOT / ".codex/skills/ahe-copy/SKILL.md",
)
ASK_USER_SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-ask-user/SKILL.md"


def test_skill_md_contains_clarification_prompt_rule() -> None:
    for skill_path in SKILL_MD_PATHS:
        content = skill_path.read_text(encoding="utf-8")
        assert "## Clarification Rule" in content
        assert "follow the `ahe-ask-user` protocol" in content
        assert "Codex-supported structured response request" in content
        assert "custom input" in content.lower()
        assert "ask again" in content.lower()


def test_skill_md_contains_clarification_judgment_sections() -> None:
    required_lines = [
        "### User Response Target",
        "### Questions to Ask",
        "### Clarification Criteria",
        "### Re-ask When",
    ]
    for skill_path in SKILL_MD_PATHS:
        content = skill_path.read_text(encoding="utf-8")
        for required_line in required_lines:
            assert required_line in content, (
                f"Missing clarification judgment section '{required_line}'"
            )


def test_skill_md_contains_representative_skill_specific_rules() -> None:
    agent_content = (
        REPO_ROOT / ".codex/skills/ahe-agent/SKILL.md"
    ).read_text(encoding="utf-8")
    assert "`code`" in agent_content
    assert "PROJECT_PURPOSE" in agent_content

    spec_content = (
        REPO_ROOT / ".codex/skills/ahe-spec/SKILL.md"
    ).read_text(encoding="utf-8")
    assert "docs/PRODUCT.md" in spec_content
    assert "docs/constraints.md" in spec_content
    assert "docs/achitecture.md" in spec_content
    assert "success" in spec_content.lower()

    copy_content = (
        REPO_ROOT / ".codex/skills/ahe-copy/SKILL.md"
    ).read_text(encoding="utf-8")
    assert "overwrite" in copy_content.lower()
    assert "explicit" in copy_content.lower()


def test_ahe_ask_user_defines_internal_protocol() -> None:
    content = ASK_USER_SKILL_MD_PATH.read_text(encoding="utf-8")

    assert "name: ahe-ask-user" in content
    assert "internal" in content.lower()
    assert "not a user-facing command" in content.lower()
    assert "Do not treat `$ahe-ask-user` as a user command." in content
    assert ".ahe/process_status.json" in content
    assert "PROGRESS.md" in content
    assert "SESSION-HANDOFF.md" in content
    assert "one question at a time" in content.lower()
    assert "Codex-supported structured response request" in content
    assert "Resume" in content


if __name__ == "__main__":
    test_skill_md_contains_clarification_prompt_rule()
    test_skill_md_contains_clarification_judgment_sections()
    test_skill_md_contains_representative_skill_specific_rules()
    test_ahe_ask_user_defines_internal_protocol()
    print("test_clarification_prompt.py passed!")
