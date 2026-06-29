# progress.md

## Current Status

**Last Updated:** 2026-06-29 13:00 +0900
**Session ID:** feat-048-independent-ahe-fix-plan-export
**Active Feature:** None

## Completed

- [x] Compressed the historical tracker surface into one summary feature covering `feat-001` through `feat-042` so `feature-list.json` stops carrying stale per-feature history after the AHE routing and compression work stabilized.
- [x] Implemented `feat-043 No-Backup Feature History Compression` by removing AHE workflow backup-copy guidance from the init and compression contracts, updating the exact `ahe init` and `ahe compress feature-list` hook text, and documenting that replaced harness history should be summarized in the refreshed tracking artifacts instead of copied aside.
- [x] Updated the contract tests in `tests/test_init_workflow.py`, `tests/test_ahe_hook.py`, and `tests/test_compression_workflow.py` to enforce the new no-backup and summarized-history behavior.
- [x] Refreshed `progress.md` and `session-handoff.md` to keep only current state, durable decisions, and recent verification evidence.
- [x] Implemented `feat-044 Global AHE Skill Installation and Docs Read Contract` by changing `ahe install` to target `$CODEX_HOME` or `~/.codex`, documenting global operation, and requiring AHE workflows to read all existing `docs/*.md` files as supporting project context.
- [x] Implemented `feat-045 Lowercase Harness Artifact Filenames` by renaming product/progress/session artifacts to lowercase filenames while keeping `AGENTS.md` uppercase, and updating all AHE contracts, templates, tests, and compression detection.
- [x] Implemented `feat-046 Independent AHE Ship Plan Export` by adding the standalone `ahe-ship` skill, direct `ahe ship` hook route, deterministic `.plans/{plan_name}.md` writer, installer allowlist entry, docs, and focused tests.
- [x] Implemented `feat-047 Staged Product Docs` by treating `docs/product.md` as overview context and optional numbered docs like `docs/product1.md` and `docs/product2.md` as ordered product stages.
- [x] Implemented `feat-048 Independent AHE Fix Plan Export` by adding the standalone `ahe-fix` skill, direct `ahe fix` hook route, deterministic `.plans/{plan_name}.md` fix-plan writer, installer allowlist entry, docs, and focused tests.

## In Progress

- [ ] No active implementation in progress.
Details: `feat-048 Independent AHE Fix Plan Export` is complete.
Latest: AHE now routes exact `ahe fix`, `ahe-fix`, and `$ahe-fix` to a dedicated fix-plan workflow that can call `ahe-conversator` when clarification is needed and writes `.plans/{plan_name}.md`.
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
- **AHE ship stays independent**: `ahe ship`, `ahe-ship`, and `$ahe-ship` export the latest Codex Plan Mode `<proposed_plan>` to `.plans/{plan_name}.md` without entering the `ahe-thinker` routed AHE agent network.
- **Product docs can be staged**: `docs/product.md` is overview context; `docs/product1.md`, `docs/product2.md`, and later numeric docs run in order; non-numeric product docs do not affect stage order.
- **AHE fix stays independent**: `ahe fix`, `ahe-fix`, and `$ahe-fix` create a concrete `.plans/{plan_name}.md` fix plan for errors or changed user intent without entering the normal `ahe-thinker` workflow.

## Change Log

- `.codex/skills/ahe-init/SKILL.md`, `.codex/skills/ahe-harness/SKILL.md`, `.codex/skills/ahe-compression/SKILL.md`, `.codex/hooks/ahe-hook.js`, `docs/product.md` - Removed workflow backup-copy guidance and documented summarized-history replacement behavior.
- `tests/test_init_workflow.py`, `tests/test_ahe_hook.py`, `tests/test_compression_workflow.py` - Added contract coverage for no-backup restart behavior and summarized completed-feature compression.
- `feature-list.json`, `progress.md`, `session-handoff.md` - Compressed stale completed history and recorded `feat-043`.
- `bin/ahe`, `README.md`, `docs/product.md`, `package.json`, `tests/test_project_setup.py` - Moved installer behavior and product contract to global Codex home installation.
- `AGENTS.md`, `.codex/skills/ahe-init/SKILL.md`, `.codex/skills/ahe-harness/SKILL.md`, `.codex/skills/ahe-reviewer/SKILL.md`, `.codex/hooks/ahe-hook.js`, `tests/test_init_workflow.py` - Updated startup and internal workflow guidance to read all existing `docs/*.md` files.
- `docs/product.md`, `progress.md`, `session-handoff.md`, `.codex/ahe-shared/templates/*`, `.codex/skills/*`, `.codex/hooks/ahe-hook.js`, `tests/*` - Updated lowercase filename contract for product, progress, and session handoff artifacts.
- `.codex/skills/ahe-ship/*`, `.codex/hooks/ahe-hook.js`, `bin/ahe`, `README.md`, `docs/PRODUCT.md`, `tests/test_ahe_ship_writer.py`, `tests/test_ahe_hook.py`, `tests/test_command_set.py`, `tests/test_project_setup.py` - Added independent Plan Mode export workflow for `.plans/{plan_name}.md`.
- `.codex/hooks/ahe-hook.js`, `.codex/skills/ahe-*`, `.codex/skills/ahe-compression/scripts/check-harness-size.sh`, `docs/product.md`, `feature-list.json`, `tests/test_ahe_hook.py`, `tests/test_spec_workflow.py`, `tests/test_specialized_workflows.py`, `tests/test_compression_workflow.py` - Added staged product-doc routing, active-stage feature derivation, and numeric product-stage compression detection.
- `.codex/skills/ahe-fix/*`, `.codex/hooks/ahe-hook.js`, `bin/ahe`, `README.md`, `docs/PRODUCT.md`, `feature-list.json`, `tests/test_ahe_fix_writer.py`, `tests/test_ahe_hook.py`, `tests/test_command_set.py`, `tests/test_project_setup.py`, `tests/test_chat_command_routing.py` - Added independent fix-plan export workflow for `.plans/{plan_name}.md`.
- `.codex/skills/ahe-new/*`, `.codex/hooks/ahe-hook.js`, `bin/ahe`, `README.md`, `docs/PRODUCT.md`, `tests/*` - Renamed `ahe-init` to `ahe-new` and restructured tests around `tests/test_ahe_new.py`.
