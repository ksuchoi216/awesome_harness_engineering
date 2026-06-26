# PROGRESS.md

## Current Status

**Last Updated:** 2026-06-23 18:18 +0900
**Session ID:** feat-043-no-backup-feature-history-compression
**Active Feature:** None

## Completed

- [x] Compressed the historical tracker surface into one summary feature covering `feat-001` through `feat-042` so `feature-list.json` stops carrying stale per-feature history after the AHE routing and compression work stabilized.
- [x] Implemented `feat-043 No-Backup Feature History Compression` by removing AHE workflow backup-copy guidance from the init and compression contracts, updating the exact `ahe init` and `ahe compress feature-list` hook text, and documenting that replaced harness history should be summarized in the refreshed tracking artifacts instead of copied aside.
- [x] Updated the contract tests in `tests/test_init_workflow.py`, `tests/test_ahe_hook.py`, and `tests/test_compression_workflow.py` to enforce the new no-backup and summarized-history behavior.
- [x] Refreshed `PROGRESS.md` and `SESSION-HANDOFF.md` to keep only current state, durable decisions, and recent verification evidence.

## In Progress

- [ ] No active implementation in progress.
Details: `feat-043 No-Backup Feature History Compression` is complete.
Blockers: None.

## Blocked

- [ ] No current blocker.

## Decisions

- **AHE workflow restarts no longer create backup copies**: `ahe-init` now asks for restart scope, replaces only the chosen harness files, and records the replaced state through concise tracker summaries instead of `.ahe/backups/`.
- **Completed feature history compresses into one summary feature**: `ahe compress feature-list` now replaces stale done entries with one summarized done feature while preserving unfinished, blocked, or active items in full detail.
- **Tracking artifacts should stay token-aware after compression**: `feature-list.json`, `PROGRESS.md`, and `SESSION-HANDOFF.md` now prefer concise historical summaries over long completed-history lists once work is stable.

## Change Log

- `.codex/skills/ahe-init/SKILL.md`, `.codex/skills/ahe-harness/SKILL.md`, `.codex/skills/ahe-compression/SKILL.md`, `.codex/hooks/ahe-hook.js`, `docs/PRODUCT.md` - Removed workflow backup-copy guidance and documented summarized-history replacement behavior.
- `tests/test_init_workflow.py`, `tests/test_ahe_hook.py`, `tests/test_compression_workflow.py` - Added contract coverage for no-backup restart behavior and summarized completed-feature compression.
- `feature-list.json`, `PROGRESS.md`, `SESSION-HANDOFF.md` - Compressed stale completed history and recorded `feat-043`.
