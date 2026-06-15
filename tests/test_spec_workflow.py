from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-spec/SKILL.md"


def test_skill_md_contains_spec_workflow_sections() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: ahe-spec" in content
    assert "Spec Inspection" in content
    assert "Sequential Spec Conversation Flow" in content
    assert "Spec Completion" in content


def test_skill_md_contains_expected_spec_conversation_contract() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_inputs = [
        "Clarify product goal, scope, and success criteria",
        "Clarify project constraints",
        "Clarify architecture direction",
        "Update only the relevant docs",
    ]
    for required_input in required_inputs:
        assert required_input in content, (
            f"Missing required input '{required_input}' in ahe-spec workflow definition"
        )


def test_skill_md_targets_all_spec_docs_and_tracking_files() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_updates = [
        "docs/PRODUCT.md",
        "docs/constraints.md",
        "docs/achitecture.md",
        ".ahe/process_status.json",
        "PROGRESS.md",
        "SESSION-HANDOFF.md",
    ]
    for required_update in required_updates:
        assert required_update in content, (
            f"Missing required update target '{required_update}' in ahe-spec workflow definition"
        )


def test_product_spec_is_canonical_home_for_init_specification_details() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_behaviors = [
        "`docs/PRODUCT.md` is the canonical home for product specification details collected during `ahe init`.",
        "Write product behavior, scope, requirements, success criteria, and workflow details into `docs/PRODUCT.md`.",
        "Do not move product specification details into `AGENTS.md`.",
    ]
    for required_behavior in required_behaviors:
        assert required_behavior in content, (
            f"Missing canonical product-spec behavior '{required_behavior}' in ahe-spec"
        )


if __name__ == "__main__":
    test_skill_md_contains_spec_workflow_sections()
    test_skill_md_contains_expected_spec_conversation_contract()
    test_skill_md_targets_all_spec_docs_and_tracking_files()
    test_product_spec_is_canonical_home_for_init_specification_details()
    print("test_spec_workflow.py passed!")
