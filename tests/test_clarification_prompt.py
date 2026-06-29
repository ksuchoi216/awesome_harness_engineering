from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_MD_PATHS = (
    REPO_ROOT / "packages/ahe-codex/.codex/skills/new/SKILL.md",
    REPO_ROOT / "packages/ahe-codex/.codex/skills/harness/SKILL.md",
)
CONVERSATION_SKILL_MD_PATH = REPO_ROOT / "packages/ahe-codex/.codex/skills/converse/SKILL.md"
THINKING_SKILL_MD_PATH = REPO_ROOT / "packages/ahe-codex/.codex/skills/think/SKILL.md"
COMPRESSION_SKILL_MD_PATH = REPO_ROOT / "packages/ahe-codex/.codex/skills/compress/SKILL.md"
REVIEWER_SKILL_MD_PATH = REPO_ROOT / "packages/ahe-codex/.codex/skills/review/SKILL.md"
SOLVER_SKILL_MD_PATH = REPO_ROOT / "packages/ahe-codex/.codex/skills/solve/SKILL.md"
SKILL_MD_PATH = REPO_ROOT / "packages/ahe-codex/.codex/skills/harness/SKILL.md"
HARNESS_SKILL_MD_PATH = REPO_ROOT / "packages/ahe-codex/.codex/skills/harness/SKILL.md"


def test_skill_md_contains_clarification_prompt_rule() -> None:
    for skill_path in SKILL_MD_PATHS:
        content = skill_path.read_text(encoding="utf-8")
        assert "## Clarification Rule" in content
        assert "follow the `converse` protocol" in content
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
        REPO_ROOT / "packages/ahe-codex/.codex/skills/new/SKILL.md"
    ).read_text(encoding="utf-8")
    assert "PROJECT_PURPOSE" in init_content
    assert "Which language do you use?" in init_content

    spec_content = (
        REPO_ROOT / "packages/ahe-codex/.codex/skills/harness/SKILL.md"
    ).read_text(encoding="utf-8")
    assert "docs/product.md" in spec_content
    assert "docs/INSTRUCTIONS.md" in spec_content
    assert "success" in spec_content.lower()
    assert "feature-list.json" in spec_content

    assert "overwrite" in init_content.lower()


def test_ahe_conversation_defines_internal_protocol() -> None:
    content = CONVERSATION_SKILL_MD_PATH.read_text(encoding="utf-8")

    assert "name: ahe-converse" in content
    assert "internal" in content.lower()
    assert "not a user-facing command" in content.lower()
    assert "Do not treat `$converse` as a user command." in content
    assert "status.json" in content
    assert "progress.md" in content
    assert "session-handoff.md" in content
    assert "one question at a time" in content.lower()
    assert "conversation state" in content.lower()
    assert "Codex-supported structured response request" in content
    assert "Resume" in content


def test_ahe_thinking_defines_internal_orchestration_protocol() -> None:
    content = THINKING_SKILL_MD_PATH.read_text(encoding="utf-8")

    assert "name: ahe-think" in content
    assert "internal" in content.lower()
    assert "not a user-facing command" in content.lower()
    assert "Do not treat `$think` as a user command." in content
    assert "`project`, `feature`, or `sub-feature`" in content
    assert "`Why`, `What`, and `How`" in content
    assert "project" in content.lower()
    assert "feature" in content.lower()
    assert "converse" in content
    assert "compress" in content
    assert "review" in content
    assert "harness" in content
    assert "solve" in content


def test_ahe_compression_defines_internal_protocol() -> None:
    content = COMPRESSION_SKILL_MD_PATH.read_text(encoding="utf-8")

    assert "name: ahe-compress" in content
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

    assert "think" in conversation_content
    assert "missing `Why`, `What`, or `How`" in conversation_content
    assert "judge what is missing" in thinking_content.lower()
    assert "one question at a time" in conversation_content.lower()


def test_reviewer_and_solver_reference_network_handoffs() -> None:
    reviewer_content = REVIEWER_SKILL_MD_PATH.read_text(encoding="utf-8")
    solver_content = SOLVER_SKILL_MD_PATH.read_text(encoding="utf-8")

    assert "think" in reviewer_content
    assert ".codegraph" in reviewer_content
    assert "harness" in reviewer_content
    assert "review" in solver_content
    assert "converse" in solver_content
    assert "divide" in solver_content.lower()
    assert "plan" in solver_content.lower()

def test_skill_md_contains_spec_workflow_sections() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: harness" in content
    assert "Harness Inspection" in content
    assert "Harness Decision Paths" in content
    assert "Harness Completion" in content



def test_skill_md_contains_expected_spec_conversation_contract() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_inputs = [
        "Clarify product goal, scope, and success criteria",
        "Clarify project instructions",
        "Clarify what next feature or goal should be tracked",
        "Update only the relevant docs",
    ]
    for required_input in required_inputs:
        assert required_input in content, (
            f"Missing required input '{required_input}' in harness workflow definition"
        )



def test_skill_md_targets_all_spec_docs_and_tracking_files() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_updates = [
        "docs/product.md",
        "docs/INSTRUCTIONS.md",
        "status.json",
        "progress.md",
        "session-handoff.md",
    ]
    for required_update in required_updates:
        assert required_update in content, (
            f"Missing required update target '{required_update}' in ahe-spec workflow definition"
        )



def test_skill_md_contains_harness_workflow() -> None:
    content = HARNESS_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: harness" in content
    assert "docs/product.md" in content
    assert "docs/INSTRUCTIONS.md" in content



def test_skill_md_contains_harness_tracking_workflow() -> None:
    content = HARNESS_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "docs/todo.md" in content
    assert "feature-list.json" in content
    assert "append" in content.lower() or "capture" in content.lower()
    assert "Apply the queued `docs/todo.md` content to `docs/product.md`." in content
    assert "Remove the applied content from `docs/todo.md`" in content
    assert "Update `feature-list.json` to derive the specific feature items from the updated `docs/product.md`." in content
    assert "Update `progress.md`." in content
    assert "Update `session-handoff.md`." in content
    assert "If no new feature can be derived from `docs/product.md`, call `converse`" in content




if __name__ == "__main__":
    test_skill_md_contains_clarification_prompt_rule()
    test_skill_md_contains_clarification_judgment_sections()
    test_skill_md_contains_representative_skill_specific_rules()
    test_ahe_conversation_defines_internal_protocol()
    test_ahe_thinking_defines_internal_orchestration_protocol()
    test_ahe_compression_defines_internal_protocol()
    test_ahe_conversation_and_thinking_split_responsibilities()
    print("test_clarification_prompt.py passed!")
