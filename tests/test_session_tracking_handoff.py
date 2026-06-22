from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_MD_PATH = REPO_ROOT / ".codex/skills/ahe-harness/SKILL.md"


def test_skill_md_contains_tracking_sync_sections() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "## Session Tracking and Handoff Sync" in content
    assert "Tracking Update Rules" in content
    assert "Progress and Handoff Content Requirements" in content


def test_skill_md_contains_required_process_status_sync_rules() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_rules = [
        "Update `.ahe/process_status.json` at workflow start",
        "Update `.ahe/process_status.json` after every answered question",
        "Refresh `updated_at` every time workflow state changes",
        "Keep `current_command`, `current_step`, and `workflow_complete` aligned with the active workflow state",
        "Keep the `files` status map aligned with the actual workspace files",
    ]
    for required_rule in required_rules:
        assert required_rule in content, (
            f"Missing process status sync rule '{required_rule}' in session tracking definition"
        )


def test_skill_md_contains_required_progress_and_handoff_rules() -> None:
    content = SKILL_MD_PATH.read_text(encoding="utf-8")
    required_rules = [
        "Update `PROGRESS.md` whenever the active feature, workflow status, blockers, or verification state changes",
        "Update `SESSION-HANDOFF.md` whenever the current objective, completed work, important files, verification evidence, or recommended next step changes",
        "PROGRESS.md must reflect the current active feature and latest completed work",
        "SESSION-HANDOFF.md must leave the next Codex session with a concrete startup path",
    ]
    for required_rule in required_rules:
        assert required_rule in content, (
            f"Missing progress or handoff rule '{required_rule}' in session tracking definition"
        )


if __name__ == "__main__":
    test_skill_md_contains_tracking_sync_sections()
    test_skill_md_contains_required_process_status_sync_rules()
    test_skill_md_contains_required_progress_and_handoff_rules()
    print("test_session_tracking_handoff.py passed!")
