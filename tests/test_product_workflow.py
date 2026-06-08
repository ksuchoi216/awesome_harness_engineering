from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-product/SKILL.md"


def test_skill_md_contains_product_workflow_sections() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Command Workflow: ahe-product" in content
    assert "Product Inspection" in content
    assert "Sequential Product Conversation Flow" in content
    assert "Product Completion" in content


def test_skill_md_contains_required_product_inputs() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_inputs = [
        "Ask for the product specification inputs needed to update `docs/PRODUCT.md`",
        "Ask recursively for more detail",
        "If the product specification is clear, finish writing `docs/PRODUCT.md`",
    ]
    for required_input in required_inputs:
        assert required_input in content, (
            f"Missing required product input '{required_input}' in ahe product workflow definition"
        )


def test_skill_md_contains_product_tracking_updates() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_updates = [
        "docs/PRODUCT.md",
        ".ahe/process_status.json",
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
