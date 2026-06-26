# progress.md

## Current Status

**Last Updated:** 2026-06-26 11:42 +0900
**Session ID:** feat-045-lowercase-harness-artifact-filenames
**Active Feature:** None

## Completed

- [x] Compressed the historical tracker surface into one summary feature covering `feat-001` through `feat-042` so `feature-list.json` stops carrying stale per-feature history after the AHE routing and compression work stabilized.
- [x] Implemented `feat-043 No-Backup Feature History Compression` by removing AHE workflow backup-copy guidance from the init and compression contracts, updating the exact `ahe init` and `ahe compress feature-list` hook text, and documenting that replaced harness history should be summarized in the refreshed tracking artifacts instead of copied aside.
- [x] Updated the contract tests in `tests/test_init_workflow.py`, `tests/test_ahe_hook.py`, and `tests/test_compression_workflow.py` to enforce the new no-backup and summarized-history behavior.
- [x] Refreshed `progress.md` and `session-handoff.md` to keep only current state, durable decisions, and recent verification evidence.
- [x] Implemented `feat-044 Global AHE Skill Installation and Docs Read Contract` by changing `ahe install` to target `$CODEX_HOME` or `~/.codex`, documenting global operation, and requiring AHE workflows to read all existing `docs/*.md` files as supporting project context.
- [x] Implemented `feat-045 Lowercase Harness Artifact Filenames` by renaming product/progress/session artifacts to lowercase filenames while keeping `AGENTS.md` uppercase, and updating all AHE contracts, templates, tests, and compression detection.

## In Progress

- [ ] No active implementation in progress.
Details: `feat-044 Global AHE Skill Installation and Docs Read Contract` is complete.
Latest: `feat-045 Lowercase Harness Artifact Filenames` is complete.
Blockers: None.

## Blocked

- [ ] No current blocker.

## Decisions

- **AHE workflow restarts no longer create backup copies**: `ahe-init` now asks for restart scope, replaces only the chosen harness files, and records the replaced state through concise tracker summaries instead of `.ahe/backups/`.
- **Completed feature history compresses into one summary feature**: `ahe compress feature-list` now replaces stale done entries with one summarized done feature while preserving unfinished, blocked, or active items in full detail.
- **Tracking artifacts should stay token-aware after compression**: `feature-list.json`, `progress.md`, and `session-handoff.md` now prefer concise historical summaries over long completed-history lists once work is stable.
- **AHE installs globally**: `ahe install`, `ahe doctor`, and `ahe uninstall` now use `$CODEX_HOME` when set and `~/.codex` otherwise; installed skills, shared files, and hooks should not be copied into each target workspace.
- **AHE reads all docs context**: Startup and internal AHE workflows must read every existing `docs/*.md` file as supporting project context, with product-style docs called out as especially important.
- **Only AGENTS stays uppercase**: AHE harness artifacts now use `docs/product.md`, `progress.md`, and `session-handoff.md`; template copies follow the same lowercase filenames except `AGENTS.md`.

## Change Log

- `.codex/skills/ahe-init/SKILL.md`, `.codex/skills/ahe-harness/SKILL.md`, `.codex/skills/ahe-compression/SKILL.md`, `.codex/hooks/ahe-hook.js`, `docs/product.md` - Removed workflow backup-copy guidance and documented summarized-history replacement behavior.
- `tests/test_init_workflow.py`, `tests/test_ahe_hook.py`, `tests/test_compression_workflow.py` - Added contract coverage for no-backup restart behavior and summarized completed-feature compression.
- `feature-list.json`, `progress.md`, `session-handoff.md` - Compressed stale completed history and recorded `feat-043`.
- `bin/ahe`, `README.md`, `docs/product.md`, `package.json`, `tests/test_project_setup.py` - Moved installer behavior and product contract to global Codex home installation.
- `AGENTS.md`, `.codex/skills/ahe-init/SKILL.md`, `.codex/skills/ahe-harness/SKILL.md`, `.codex/skills/ahe-reviewer/SKILL.md`, `.codex/hooks/ahe-hook.js`, `tests/test_init_workflow.py` - Updated startup and internal workflow guidance to read all existing `docs/*.md` files.
- `docs/product.md`, `progress.md`, `session-handoff.md`, `.codex/ahe-shared/templates/*`, `.codex/skills/*`, `.codex/hooks/ahe-hook.js`, `tests/*` - Updated lowercase filename contract for product, progress, and session handoff artifacts.
