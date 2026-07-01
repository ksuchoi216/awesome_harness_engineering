from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = REPO_ROOT / "packages/ahe-codex/.codex/skills/ahe-ship/SKILL.md"


def test_ship_skill_contract() -> None:
    skill_content = SKILL_PATH.read_text(encoding="utf-8")

    assert "Detect if the current conversation is still in Plan Mode." in skill_content
    assert "If Plan Mode is active, the Codex host must exit Plan Mode and replay the command." in skill_content
    assert "Outside Plan Mode, locate the most recent completed `<proposed_plan>`" in skill_content
    assert "Write the final markdown through `scripts/write_plan.py`." in skill_content
