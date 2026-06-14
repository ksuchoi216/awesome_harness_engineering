# SESSION-HANDOFF.md

## Current Product Context

- Goal: Keep AHE's Codex skill surface small and focused while preserving the harness specification docs.
- Current status: `feat-031 Two-Entrypoint AHE Surface` is complete.
- Branch / commit: `develop`; users now rely on exact `ahe init` for a new start and exact `ahe` for progress, while `ahe-init` absorbs the old reset path.

## Last Completed Work

- [x] Removed `.codex/skills/ahe-help/SKILL.md`.
- [x] Removed `.codex/skills/ahe-clear/SKILL.md` and deleted `tests/test_clear_workflow.py`.
- [x] Folded the previous reset/backup semantics into `.codex/skills/ahe-init/SKILL.md`.
- [x] Updated `.codex/hooks/ahe-hook.js` so exact `ahe init` is the new-start path and exact `ahe` remains the progress path.
- [x] Updated `bin/ahe` and `scripts/uninstall.sh` so installs now include only `ahe-init`, `ahe-thinking`, `ahe-conversation`, `ahe-spec`, and `ahe-update`.
- [x] Updated `docs/PRODUCT.md`, `feature-list.json`, `PROGRESS.md`, and contract tests for the two-entrypoint UX.
- [x] Verified the change with `./init.sh`, `pytest tests/ -x`, and `python3 -m json.tool feature-list.json`.
- [x] Added `.codex/skills/ahe-thinking/SKILL.md` as a hidden internal decision protocol.
- [x] Updated `.codex/skills/ahe-conversation/SKILL.md` so it is called only after `ahe-thinking` identifies the missing `Why`, `What`, or `How`.
- [x] Updated `.codex/skills/ahe-init/SKILL.md`, `.codex/skills/ahe-spec/SKILL.md`, `.codex/skills/ahe-update/SKILL.md`, and `.codex/skills/ahe-clear/SKILL.md` to follow `ahe-thinking` before clarification when the next step is not obvious.
- [x] Updated `.codex/hooks/ahe-hook.js` so exact `ahe` classifies exactly one state: `harness engineering not enough`, `in the middle of building features`, or `completed all`.
- [x] Replaced the old post-table next-step confirmation contract with automatic continuation through `thinking -> conversation if needed -> execution -> thinking`.
- [x] Updated `bin/ahe` and `scripts/uninstall.sh` so packaged installs include and remove the internal `ahe-thinking` skill.
- [x] Updated `docs/PRODUCT.md`, `feature-list.json`, `PROGRESS.md`, and tests to reflect the new internal orchestration split.
- [x] Verified the change with `./init.sh`, `pytest tests/ -x`, and `python3 -m json.tool feature-list.json`.
- [x] Reduced the exact `ahe` first-response status table to `AGENTS.md`, `PRODUCT.md`, `feature-list.json`, and `PROGRESS.md`.
- [x] Removed the next-step choice from the report table so the first response stays short and readable.
- [x] Updated the exact `ahe` hook directive so AHE asks for one direct next-step confirmation after the table using `harness engineering`, `start a new task`, or `resume existing harness work`.
- [x] Updated `docs/PRODUCT.md`, `feature-list.json`, `PROGRESS.md`, and `tests/test_ahe_hook.py` for the simplified report and confirmation flow.
- [x] Updated the exact `ahe` hook directive so AHE checks `command -v codegraph` before harness status reporting.
- [x] Added adaptive CodeGraph behavior: run `codegraph init` when `.codegraph/` is missing, run `codegraph sync` when it exists, and skip both commands with `NOT INSTALLATION of codegraph` when the CLI is unavailable.
- [x] Updated the exact `ahe` hook directive so automatic operation first reports harness engineering status in a consistent Markdown table before edits or workflow execution.
- [x] Updated `docs/PRODUCT.md`, `feature-list.json`, `PROGRESS.md`, and `tests/test_ahe_hook.py` for the first-response status table behavior.
- [x] Replaced the previous internal clarification protocol with `.codex/skills/ahe-conversation/SKILL.md`.
- [x] Expanded the internal protocol wording to cover recursive clarification, conversation state, decision points, and resume-aware workflow continuation.
- [x] Updated interactive skills, installer/uninstaller lists, `docs/PRODUCT.md`, and tests so AHE now installs and references `ahe-conversation`.
- [x] Reduced the public AHE command set to `$ahe-init`, `$ahe-spec`, `$ahe-update`, `$ahe-clear`, and `$ahe-help`.
- [x] Removed the public `ahe-agent`, `ahe-copy`, and `ahe-todo` skill files from the managed AHE skill set.
- [x] Updated `$ahe-init` to absorb AGENTS/template setup behavior and to coordinate only `ahe-spec` and `ahe-update`.
- [x] Updated `$ahe-update` to absorb queued todo capture as well as queued todo application.
- [x] Updated installer, uninstaller, `$ahe-help`, process-status schema, hook guidance, `docs/PRODUCT.md`, `feature-list.json`, `PROGRESS.md`, and tests for the reduced command surface.
- [x] Added an internal clarification protocol skill, not a user-facing command.
- [x] Updated interactive skill markdown files to follow the internal clarification protocol while keeping skill-specific clarification criteria.
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
- `.codex/skills/ahe-conversation/SKILL.md` - Internal recursive clarification, conversation state, and resume-aware workflow protocol used by interactive AHE skills.
- `.codex/skills/ahe-thinking/SKILL.md` - Internal decision protocol that judges the current project, feature, or sub-feature and decides whether AHE should clarify or execute next.
- `.codex/skills/ahe-spec/SKILL.md` - Combined product, constraints, and architecture specification workflow.
- `.codex/hooks/ahe-hook.js` - Exact `ahe` and exact `ahe init` command hook; the directives now split new-start and progress routing while keeping adaptive CodeGraph preflight for progress.
- `.ahe/backups/20260608-215651/AGENTS.md` - Clear-workflow backup of the current global instructions.
- `.ahe/backups/20260608-215651/docs/` - Clear-workflow backup of the current docs folder.
- `.ahe/backups/20260608-215651/PROGRESS.md` - Clear-workflow backup of the current progress log.
- `.ahe/backups/20260608-215651/SESSION-HANDOFF.md` - Clear-workflow backup of the current handoff file.
- `.ahe/backups/20260608-215651/init.sh` - Clear-workflow backup of the current startup script.
- `.codex/skills/ahe-init/SKILL.md` - The only user-facing installed skill; it now covers both first-time setup and fresh-start reset behavior.
- `tests/test_clarification_prompt.py` - Contract coverage for Codex UI-compatible clarification guidance, skill-specific clarification sections, and the internal `ahe-conversation` protocol.
- `.codex/skills/ahe-update/SKILL.md` - Update workflow that now consumes `docs/todo.md` into `docs/PRODUCT.md`.
- `.codex/ahe-shared/` - Shared templates and schemas used by the split skills and installer.
- `scripts/install.sh`, `scripts/uninstall.sh` - Helper scripts for global Codex install and uninstall under `${HOME}/.codex`.
- `tests/test_specialized_workflows.py` - Contract coverage for `$ahe-init` and the remaining internal spec/update workflows.
- `tests/test_command_set.py` - Contract coverage for the reduced `$ahe-*` command surface.
- `.ahe/process_status.json` - Runtime state used by future `ahe` and `ahe resume` flows.
- `tests/test_clarification_prompt.py` - Contract coverage for the clarification prompt format.
- `tests/test_session_tracking_handoff.py` - Contract coverage for process-status, progress-log, and handoff synchronization rules.
- `tests/test_project_setup.py`, `bin/ahe` - Packaging and installer coverage for direct and `npx` install paths.

## Next Recommended Action

1. Read `AGENTS.md`.
2. Read `feature-list.json` and `PROGRESS.md`.
3. Review this handoff.
4. Run `./init.sh` or the documented verification command before editing.
5. If the internal orchestration changes again, update `ahe-thinking`, `ahe-conversation`, `ahe-init`, the remaining internal workflow skills, hook guidance, installer lists, product docs, and the markdown contract tests together.

## Verification Status

| Check | Command | Result | Notes |
|---|---|---|---|
| Init sanity | `./init.sh` | Pass | Startup check still reports the expected Python-default environment guidance. |
| Full tests | `pytest tests/ -x` | Pass | Full contract suite passed after adding the internal `ahe-thinking` orchestrator and automatic exact `ahe` state classification. |
| Lint | `ruff check src/` | Pass | Ruff reported no Python files under `src/` and still exited successfully. |
| Type check | `mypy src/ --strict` | Not applicable | Command exited with code 2 because `src/` contains no `.py` or `.pyi` files under `src/`. |
| Shell syntax | `bash -n bin/ahe` and `bash -n scripts/uninstall.sh` | Pass | Installer and uninstaller scripts parse cleanly. |
| JSON validation | `python3 -m json.tool feature-list.json` | Pass | `feature-list.json` is valid JSON. |
| CodeGraph sync | `codegraph sync` | Pass | Local CodeGraph index synced after adaptive CodeGraph preflight hook edits. |
| Runtime state JSON | `python3 -m json.tool .ahe/process_status.json` | Pass | Process status file is valid JSON. |
| Installer checks | `bash bin/ahe doctor`, `bash bin/ahe version`, and `pytest tests/test_project_setup.py -x` | Pass | Split-skill install metadata, copy behavior, `npx` flow, internal protocol installation, and global helper scripts passed. |
| Direct module tests | `python3 tests/test_*.py` modules | Not run this session | Full pytest coverage passed, so direct module execution was not repeated. |
