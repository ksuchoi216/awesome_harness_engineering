from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_MD_PATHS = (
    REPO_ROOT / ".codex/skills/ahe-init/SKILL.md",
    REPO_ROOT / ".codex/skills/ahe-harness/SKILL.md",
)
CONVERSATION_SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-conversator/SKILL.md"
THINKING_SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-thinker/SKILL.md"
COMPRESSION_SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-compression/SKILL.md"
REVIEWER_SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-reviewer/SKILL.md"
SOLVER_SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-solver/SKILL.md"


def test_skill_md_contains_clarification_prompt_rule() -> None:
    for skill_path in SKILL_MD_PATHS:
        content = skill_path.read_text(encoding="utf-8")
        assert "## Clarification Rule" in content
        assert "follow the `ahe-conversator` protocol" in content
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
    init_content = (
        REPO_ROOT / ".codex/skills/ahe-init/SKILL.md"
    ).read_text(encoding="utf-8")
    assert "PROJECT_PURPOSE" in init_content
    assert "Which language do you use?" in init_content

    spec_content = (
        REPO_ROOT / ".codex/skills/ahe-harness/SKILL.md"
    ).read_text(encoding="utf-8")
    assert "docs/product.md" in spec_content
    assert "docs/INSTRUCTIONS.md" in spec_content
    assert "success" in spec_content.lower()
    assert "feature-list.json" in spec_content

    assert "overwrite" in init_content.lower()


def test_ahe_conversation_defines_internal_protocol() -> None:
    content = CONVERSATION_SKILL_MD_PATH.read_text(encoding="utf-8")

    assert "name: ahe-conversator" in content
    assert "internal" in content.lower()
    assert "not a user-facing command" in content.lower()
    assert "Do not treat `$ahe-conversator` as a user command." in content
    assert ".ahe/process_status.json" in content
    assert "progress.md" in content
    assert "session-handoff.md" in content
    assert "one question at a time" in content.lower()
    assert "conversation state" in content.lower()
    assert "Codex-supported structured response request" in content
    assert "Resume" in content


def test_ahe_thinking_defines_internal_orchestration_protocol() -> None:
    content = THINKING_SKILL_MD_PATH.read_text(encoding="utf-8")

    assert "name: ahe-thinker" in content
    assert "internal" in content.lower()
    assert "not a user-facing command" in content.lower()
    assert "Do not treat `$ahe-thinker` as a user command." in content
    assert "`project`, `feature`, or `sub-feature`" in content
    assert "`Why`, `What`, and `How`" in content
    assert "project" in content.lower()
    assert "feature" in content.lower()
    assert "ahe-conversator" in content
    assert "ahe-compression" in content
    assert "ahe-reviewer" in content
    assert "ahe-harness" in content
    assert "ahe-solver" in content


def test_ahe_compression_defines_internal_protocol() -> None:
    content = COMPRESSION_SKILL_MD_PATH.read_text(encoding="utf-8")

    assert "name: ahe-compression" in content
    assert "internal" in content.lower()
    assert "not a user-facing command" in content.lower()
    assert "check-harness-size.sh" in content
    assert "AGENTS.md" in content
    assert "docs/product.md" in content
    assert "feature-list.json" in content
    assert "COMPRESSION_REQUIRED" in content
    assert "valid JSON" in content


def test_ahe_conversation_and_thinking_split_responsibilities() -> None:
    conversation_content = CONVERSATION_SKILL_MD_PATH.read_text(encoding="utf-8")
    thinking_content = THINKING_SKILL_MD_PATH.read_text(encoding="utf-8")

    assert "ahe-thinker" in conversation_content
    assert "missing `Why`, `What`, or `How`" in conversation_content
    assert "judge what is missing" in thinking_content.lower()
    assert "one question at a time" in conversation_content.lower()


def test_reviewer_and_solver_reference_network_handoffs() -> None:
    reviewer_content = REVIEWER_SKILL_MD_PATH.read_text(encoding="utf-8")
    solver_content = SOLVER_SKILL_MD_PATH.read_text(encoding="utf-8")

    assert "ahe-thinker" in reviewer_content
    assert ".codegraph" in reviewer_content
    assert "ahe-harness" in reviewer_content
    assert "ahe-reviewer" in solver_content
    assert "ahe-conversator" in solver_content
    assert "divide" in solver_content.lower()
    assert "plan" in solver_content.lower()


if __name__ == "__main__":
    test_skill_md_contains_clarification_prompt_rule()
    test_skill_md_contains_clarification_judgment_sections()
    test_skill_md_contains_representative_skill_specific_rules()
    test_ahe_conversation_defines_internal_protocol()
    test_ahe_thinking_defines_internal_orchestration_protocol()
    test_ahe_compression_defines_internal_protocol()
    test_ahe_conversation_and_thinking_split_responsibilities()
    print("test_clarification_prompt.py passed!")
