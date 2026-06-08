from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_MD_PATHS = (
    REPO_ROOT / ".codex/skills/ahe-init/SKILL.md",
    REPO_ROOT / ".codex/skills/ahe-agent/SKILL.md",
    REPO_ROOT / ".codex/skills/ahe-product/SKILL.md",
    REPO_ROOT / ".codex/skills/ahe-todo/SKILL.md",
    REPO_ROOT / ".codex/skills/ahe-constraints/SKILL.md",
    REPO_ROOT / ".codex/skills/ahe-architecture/SKILL.md",
    REPO_ROOT / ".codex/skills/ahe-clear/SKILL.md",
    REPO_ROOT / ".codex/skills/ahe-copy/SKILL.md",
)


def test_skill_md_contains_clarification_prompt_rule() -> None:
    for skill_path in SKILL_MD_PATHS:
        content = skill_path.read_text(encoding="utf-8")
        assert "## Clarification Rule" in content
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

    product_content = (
        REPO_ROOT / ".codex/skills/ahe-product/SKILL.md"
    ).read_text(encoding="utf-8")
    assert "docs/PRODUCT.md" in product_content
    assert "success" in product_content.lower()

    copy_content = (
        REPO_ROOT / ".codex/skills/ahe-copy/SKILL.md"
    ).read_text(encoding="utf-8")
    assert "overwrite" in copy_content.lower()
    assert "explicit" in copy_content.lower()


if __name__ == "__main__":
    test_skill_md_contains_clarification_prompt_rule()
    test_skill_md_contains_clarification_judgment_sections()
    test_skill_md_contains_representative_skill_specific_rules()
    print("test_clarification_prompt.py passed!")
