from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_MD_PATH = REPO_ROOT / "packages/ahe-codex/.codex/skills/harness/SKILL.md"


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
        ".ahe/process_status.json",
        "progress.md",
        "session-handoff.md",
    ]
    for required_update in required_updates:
        assert required_update in content, (
            f"Missing required update target '{required_update}' in ahe-spec workflow definition"
        )


def test_product_spec_is_canonical_home_for_init_specification_details() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_behaviors = [
        "`docs/product.md` is the canonical home for product specification details collected during `ahe new`.",
        "Write product behavior, scope, requirements, success criteria, and workflow details into `docs/product.md`.",
        "`docs/product.md` is the canonical source of truth. Concrete feature items for `feature-list.json` must be derived from it only after it has been populated.",
        "Do not move product specification details into `AGENTS.md`.",
    ]
    for required_behavior in required_behaviors:
        assert required_behavior in content, (
            f"Missing canonical product-spec behavior '{required_behavior}' in harness"
        )


def test_product_spec_supports_ordered_stage_documents() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_behaviors = [
        "Treat `docs/product.md` as overview context even when a numbered product stage is active.",
        "Recognize only `docs/product{number}.md` files as ordered product stages.",
        "Ignore non-numeric product files such as `docs/product-alpha.md` for stage ordering.",
        "Choose the lowest-numbered product stage whose derived feature work is not complete.",
        "Derive concrete feature items from only the active product stage, not future stages.",
        "Advance from `docs/product1.md` to `docs/product2.md` only after all feature-list items derived from `docs/product1.md` are `done`.",
    ]
    for required_behavior in required_behaviors:
        assert required_behavior in content, (
            f"Missing staged product behavior '{required_behavior}' in harness"
        )


if __name__ == "__main__":
    test_skill_md_contains_spec_workflow_sections()
    test_skill_md_contains_expected_spec_conversation_contract()
    test_skill_md_targets_all_spec_docs_and_tracking_files()
    test_product_spec_is_canonical_home_for_init_specification_details()
    test_product_spec_supports_ordered_stage_documents()
    print("test_spec_workflow.py passed!")
