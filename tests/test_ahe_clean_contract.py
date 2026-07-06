from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
CLEAN_SKILL_MD_PATH = REPO_ROOT / "packages/ahe-codex/.codex/skills/ahe-clean/SKILL.md"
HARNESS_SKILL_MD_PATH = REPO_ROOT / "packages/ahe-codex/.codex/skills/ahe-harness/SKILL.md"
THINK_SKILL_MD_PATH = REPO_ROOT / "packages/ahe-codex/.codex/skills/ahe-think/SKILL.md"


def test_ahe_clean_is_internal_only() -> None:
    content = CLEAN_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "name: ahe-clean" in content
    assert "not a user-facing command" in content.lower()
    assert "feature-list.json" in content
    assert "session-handoff.md" in content


def test_ahe_clean_requires_summary_compaction_rules() -> None:
    content = CLEAN_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "all non-`done` features" in content
    assert "active feature from `progress.md`" in content
    assert "completed dependency features needed for the active feature" in content
    assert "one stable summary feature entry" in content
    assert "updated in place on future cleanup runs" in content
    assert "one compact summary bullet" in content


def test_ahe_harness_owns_tracker_cleanup_policy() -> None:
    content = HARNESS_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "not archival logs; they are current-work artifacts" in content
    assert "unrelated completed feature entries may be compacted" in content
    assert "unrelated completed handoff bullets may be compacted" in content
    assert "current-work-relevant completed context must remain" in content


def test_ahe_think_distinguishes_cleanup_from_harness_manager() -> None:
    content = THINK_SKILL_MD_PATH.read_text(encoding="utf-8")
    assert "ahe-clean" in content
    assert "valid but noisy" in content
    assert "too many `done` entries in `feature-list.json`" in content
    assert "too many stale bullets in `session-handoff.md`" in content
    assert "distinct from `@ahe-harness-manager` escalation" in content
