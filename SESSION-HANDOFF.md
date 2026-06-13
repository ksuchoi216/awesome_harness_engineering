# SESSION-HANDOFF.md

## Current Product Context

- Goal: Keep AHE's Codex skill surface small and focused while preserving the harness specification docs.
- Current status: `feat-024 Consolidated AHE Spec Skill` is complete.
- Branch / commit: `develop`; consolidated `$ahe-spec` changes prepared in this session.

## Last Completed Work

- [x] Added `.codex/skills/ahe-spec/SKILL.md` as the single public workflow for product, constraints, and architecture specification updates.
- [x] Removed the old `$ahe-product`, `$ahe-constraints`, and `$ahe-architecture` skill files from the managed AHE skill set.
- [x] Updated `$ahe-init` to call `ahe-agent`, `ahe-spec`, `ahe-copy`, and `ahe-update` as the four initialization subprocesses.
- [x] Updated installer, uninstaller, `$ahe-help`, process-status schema, hook guidance, `docs/PRODUCT.md`, `feature-list.json`, `PROGRESS.md`, and tests for the reduced command surface.
- [x] Added `.codex/skills/ahe-ask-user/SKILL.md` as an internal protocol skill, not a user-facing command.
- [x] Updated all 8 interactive skill markdown files to follow the `ahe-ask-user` protocol while keeping skill-specific clarification criteria.
- [x] Updated `bin/ahe` and `scripts/uninstall.sh` so packaged install/uninstall include the internal skill.
- [x] Updated `docs/PRODUCT.md`, `feature-list.json`, `PROGRESS.md`, and this handoff for `feat-021`.
- [x] Updated `tests/test_command_set.py`, `tests/test_clarification_prompt.py`, and `tests/test_project_setup.py` to cover the internal skill and ensure `$ahe-help` does not expose it.
- [x] Verified the change with `./init.sh`, `pytest tests/ -x`, focused `ruff check` on edited tests, shell syntax checks, JSON validation, and installer doctor/version checks.
- [x] Updated all 8 interactive skill markdown files to replace the fixed plain-text clarification prompt with Codex-supported structured response request guidance, custom input handling, recursive re-asking, and skill-specific clarification criteria.
- [x] Updated all 8 interactive skill markdown files (`SKILL.md` under `ahe-init`, `ahe-agent`, `ahe-product`, `ahe-todo`, `ahe-constraints`, `ahe-architecture`, `ahe-clear`, `ahe-copy`) to include recursive clarification rule descriptions and formatting.
- [x] Updated `docs/PRODUCT.md` with the new clarification prompt format and recursive instruction.
- [x] Updated `tests/test_clarification_prompt.py` to check for the new format containing "Question: {question}" and recursive clarification assertions.
- [x] Added `.codex/skills/ahe-todo/SKILL.md`.
- [x] Updated `bin/ahe` to install the split skill set and shared assets.
- [x] Updated `scripts/uninstall.sh` to remove the split skill set and shared assets from `${HOME}/.codex`.
- [x] Rewrote the setup and workflow tests to validate the split skill layout.
- [x] Created `.ahe/backups/20260608-215651/`.
- [x] Expanded the clear-workflow backup to include `AGENTS.md`, the `docs/` folder, `PROGRESS.md`, `SESSION-HANDOFF.md`, and `init.sh`.
- [x] Updated the `ahe clear` contract so it resets the `AGENTS.md` objective and rewrites `docs/PRODUCT.md` recursively after backup.
- [x] Updated `scripts/install.sh` to install into `${HOME}/.codex`.
- [x] Updated `scripts/uninstall.sh` to remove `${HOME}/.codex/skills/ahe`.
- [x] Added helper-script coverage to `tests/test_project_setup.py`.
- [x] Rewrote the AHE command router around the seven `$ahe-*` commands only.
- [x] Added workflow coverage for `$ahe-agent`, `$ahe-constraints`, `$ahe-architecture`, and the reduced `$ahe-clear`.
- [x] Removed the old check/resume-focused contract surface.
- [x] Added a cross-workflow `Session Tracking and Handoff Sync` section to `.codex/skills/ahe/SKILL.md`.
- [x] Added `tests/test_session_tracking_handoff.py` and verified it in isolation and in the full pytest suite.
- [x] Confirmed the overall workflow contract remains green with `pytest tests/ -x` and `./init.sh`.
- [x] Added `ahe clear` routing and workflow instructions to `.codex/skills/ahe/SKILL.md`.
- [x] Updated `docs/PRODUCT.md`, `feature-list.json`, and `PROGRESS.md` for `feat-007 Clear Workflow`.
- [x] Added `tests/test_clear_workflow.py`.
- [x] Added a global Clarification Prompt Rule to `.codex/skills/ahe/SKILL.md`.
- [x] Added `tests/test_clarification_prompt.py` for the exact prompt format and option meanings.

## Current Open Questions

- Whether `ahe-update` should remove only the consumed `## TODO` entries or remove `docs/todo.md` entirely when the queue becomes empty.

## Important Files

- `docs/PRODUCT.md` - Canonical product specification and scope reference.
- `.codex/skills/ahe-ask-user/SKILL.md` - Internal clarification and state-persistence protocol used by interactive AHE skills.
- `.codex/skills/ahe-spec/SKILL.md` - Combined product, constraints, and architecture specification workflow.
- `.ahe/backups/20260608-215651/AGENTS.md` - Clear-workflow backup of the current global instructions.
- `.ahe/backups/20260608-215651/docs/` - Clear-workflow backup of the current docs folder.
- `.ahe/backups/20260608-215651/PROGRESS.md` - Clear-workflow backup of the current progress log.
- `.ahe/backups/20260608-215651/SESSION-HANDOFF.md` - Clear-workflow backup of the current handoff file.
- `.ahe/backups/20260608-215651/init.sh` - Clear-workflow backup of the current startup script.
- `.codex/skills/ahe-init/SKILL.md` through `.codex/skills/ahe-clear/SKILL.md`, plus `.codex/skills/ahe-spec/SKILL.md`, `.codex/skills/ahe-todo/SKILL.md`, `.codex/skills/ahe-help/SKILL.md`, and `.codex/skills/ahe-copy/SKILL.md` - The visible AHE skills now exposed in Codex.
- `tests/test_clarification_prompt.py` - Contract coverage for Codex UI-compatible clarification guidance, skill-specific clarification sections, and the internal `ahe-ask-user` protocol.
- `.codex/skills/ahe-update/SKILL.md` - Update workflow that now consumes `docs/todo.md` into `docs/PRODUCT.md`.
- `.codex/ahe-shared/` - Shared templates and schemas used by the split skills and installer.
- `scripts/install.sh`, `scripts/uninstall.sh` - Helper scripts for global Codex install and uninstall under `${HOME}/.codex`.
- `tests/test_specialized_workflows.py` - Contract coverage for `$ahe-agent`, `$ahe-spec`, `$ahe-todo`, `$ahe-update`, `$ahe-help`, and `$ahe-copy`.
- `tests/test_command_set.py` - Contract coverage for the reduced `$ahe-*` command surface.
- `.ahe/process_status.json` - Runtime state used by future `ahe` and `ahe resume` flows.
- `tests/test_clarification_prompt.py` - Contract coverage for the clarification prompt format.
- `tests/test_clear_workflow.py` - Contract coverage for the `ahe clear` backup and new-goal conversation behavior.
- `tests/test_session_tracking_handoff.py` - Contract coverage for process-status, progress-log, and handoff synchronization rules.
- `tests/test_project_setup.py`, `bin/ahe` - Packaging and installer coverage for direct and `npx` install paths.

## Next Recommended Action

1. Read `AGENTS.md`.
2. Read `feature-list.json` and `PROGRESS.md`.
3. Review this handoff.
4. Run `./init.sh` or the documented verification command before editing.
5. If the spec workflow changes again, update `ahe-spec`, `ahe-init`, `ahe-help`, installer lists, product docs, and the markdown contract tests together.

## Verification Status

| Check | Command | Result | Notes |
|---|---|---|---|
| Init sanity | `./init.sh` | Pass | Startup check still reports the expected Python-default environment guidance. |
| Full tests | `pytest tests/ -x` | Pass | Full contract suite passed after consolidating the spec workflow. |
| Focused lint | `ruff check tests/test_command_set.py tests/test_clarification_prompt.py tests/test_project_setup.py` | Pass | Edited Python tests pass ruff. |
| Shell syntax | `bash -n init.sh`, `bash -n bin/ahe`, and `bash -n scripts/uninstall.sh` | Pass | Startup, installer, and uninstaller scripts parse cleanly. |
| JSON validation | `python3 -m json.tool feature-list.json` | Pass | `feature-list.json` is valid JSON. |
| Runtime state JSON | `python3 -m json.tool .ahe/process_status.json` | Pass | Process status file is valid JSON. |
| Installer checks | `bash bin/ahe doctor`, `bash bin/ahe version`, and `pytest tests/test_project_setup.py -x` | Pass | Split-skill install metadata, copy behavior, `npx` flow, internal protocol installation, and global helper scripts passed. |
| Direct module tests | `python3 tests/test_*.py` modules | Not run this session | Full pytest coverage passed, so direct module execution was not repeated. |
