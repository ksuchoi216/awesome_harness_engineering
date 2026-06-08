from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe/SKILL.md"


def test_skill_md_contains_product_workflow_sections() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: ahe product" in content
    assert "Product Inspection" in content
    assert "Sequential Product Conversation Flow" in content
    assert "Product Spec Generation and Tracking Sync" in content


def test_skill_md_contains_required_product_inputs() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_inputs = [
        "Product Name",
        "Product Objective",
        "Background",
        "Current Goal",
        "Requirements",
        "Completion Criteria",
        "User Workflow",
        "Files to Create or Modify",
        "Verification Commands",
        "Out of Scope",
        "Open Questions",
        "Notes",
    ]
    for required_input in required_inputs:
        assert required_input in content, (
            f"Missing required product input '{required_input}' in ahe product workflow definition"
        )


def test_skill_md_contains_product_tracking_updates() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_updates = [
        "docs/PRODUCT.md",
        "AGENTS.md",
        "PROGRESS.md",
        "SESSION-HANDOFF.md",
        ".ahe/process_status.json",
        "Run the validation check (equivalent to `ahe check`)",
    ]
    for required_update in required_updates:
        assert required_update in content, (
            f"Missing required product tracking update '{required_update}' in ahe product workflow definition"
        )


if __name__ == "__main__":
    test_skill_md_contains_product_workflow_sections()
    test_skill_md_contains_required_product_inputs()
    test_skill_md_contains_product_tracking_updates()
    print("test_product_workflow.py passed!")
