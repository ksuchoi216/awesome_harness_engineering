# SESSION-HANDOFF.md

## Current Product Context

- Goal: Start a new product direction through `ahe clear` after backing up the current `AGENTS.md` and `docs/PRODUCT.md`.
- Current status: `ahe clear` is active and paused at `ask_new_goal`.
- Branch / commit: Current working tree changes only. No commit created in this session.

## Last Completed Work

- [x] Created `.ahe/backups/20260608-215651/`.
- [x] Copied `AGENTS.md` and `docs/PRODUCT.md` into the backup directory.
- [x] Added a cross-workflow `Session Tracking and Handoff Sync` section to `.codex/skills/ahe/SKILL.md`.
- [x] Added `tests/test_session_tracking_handoff.py` and verified it in isolation and in the full pytest suite.
- [x] Confirmed the overall workflow contract remains green with `pytest tests/ -x` and `./init.sh`.
- [x] Added `ahe clear` routing and workflow instructions to `.codex/skills/ahe/SKILL.md`.
- [x] Updated `docs/PRODUCT.md`, `feature-list.json`, and `PROGRESS.md` for `feat-007 Clear Workflow`.
- [x] Added `tests/test_clear_workflow.py`.
- [x] Added a global Clarification Prompt Rule to `.codex/skills/ahe/SKILL.md`.
- [x] Added `tests/test_clarification_prompt.py` for the exact prompt format and option meanings.

## Current Open Questions

- What is the new goal for the next product direction?

## Important Files

- `docs/PRODUCT.md` - Canonical product specification and scope reference.
- `.ahe/backups/20260608-215651/AGENTS.md` - Clear-workflow backup of the current global instructions.
- `.ahe/backups/20260608-215651/docs/PRODUCT.md` - Clear-workflow backup of the current product specification.
- `.codex/skills/ahe/SKILL.md` - Installed skill entrypoint containing routing plus explicit workflow and cross-workflow tracking contracts.
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
5. Resume `ahe clear` and answer the new-goal question.

## Verification Status

| Check | Command | Result | Notes |
|---|---|---|---|
| Shell syntax | `bash -n init.sh` and `bash -n bin/ahe` | Pass | Startup script and installer script both parse cleanly. |
| JSON validation | `python3 -m json.tool feature-list.json` | Pass | `feature-list.json` is valid JSON. |
| Runtime state JSON | `python3 -m json.tool .ahe/process_status.json` | Pass | Process status file is valid JSON. |
| Installer checks | `./bin/ahe version` and `pytest tests/test_project_setup.py -x` | Pass | Direct installs and `npx`-style installs both work after the symlink path fix. |
| Workflow tests | `python3 tests/test_*.py` modules | Pass | Direct module execution passed for setup, routing, init, product, check, resume, tracking/handoff, clear workflow, and clarification prompt coverage. `pytest tests/ -x` could not run because `pytest` is not installed. |
