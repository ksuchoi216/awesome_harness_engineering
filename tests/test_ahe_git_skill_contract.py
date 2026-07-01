from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
CODEX_SKILL_PATH = REPO_ROOT / "packages/ahe-codex/.codex/skills/ahe-git/SKILL.md"
AGY_SKILL_PATH = REPO_ROOT / "packages/ahe-antigravity/skills/ahe-git/SKILL.md"


def test_ahe_git_codex_skill_contract() -> None:
    skill_content = CODEX_SKILL_PATH.read_text(encoding="utf-8")

    assert "Scan for both `.git` directories and `.git` files" in skill_content
    assert "If the repo is locally ahead of upstream and has local changes, continue to Dirty-State Review." in skill_content
    assert "If the repo has local changes and upstream has commits not present locally, **stop and explain the issue**." in skill_content
    assert "auto-stash, auto-merge, auto-rebase, auto-resolve conflicts, or change branch topology." in skill_content


def test_ahe_git_agy_skill_contract() -> None:
    skill_content = AGY_SKILL_PATH.read_text(encoding="utf-8")

    assert "Scan for both `.git` directories and `.git` files" in skill_content
    assert "If the repo is locally ahead of upstream and has local changes, continue to Dirty-State Review." in skill_content
    assert "If the repo has local changes and upstream has commits not present locally, **stop and explain the issue**." in skill_content
    assert "auto-stash, auto-merge, auto-rebase, auto-resolve conflicts, or change branch topology." in skill_content
    assert "Print the exact line `AHE_GIT_COMPLETE`" in skill_content
