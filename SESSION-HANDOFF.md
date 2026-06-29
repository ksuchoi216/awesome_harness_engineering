# session-handoff.md

## Current Product Context

- Goal: Keep AHE's Codex-facing harness workflow compact, explicit, and cheap to resume in chat.
- Current status: `feat-048 Independent AHE Fix Plan Export` is complete.
- Branch / commit: `develop`; the live AHE contracts now install globally, read all existing `docs/*.md` files, use lowercase filenames for product/progress/session artifacts, ship independent Plan Mode and fix-plan exporters, and support ordered staged product docs.

## Last Completed Work

- [x] Removed AHE workflow backup-copy guidance from `.codex/skills/ahe-init/SKILL.md`, `.codex/skills/ahe-compression/SKILL.md`, `.codex/skills/ahe-harness/SKILL.md`, `.codex/hooks/ahe-hook.js`, and `docs/product.md`.
- [x] Changed the `ahe compress feature-list` contract so old completed entries collapse into one summarized done feature while unfinished work remains detailed.
- [x] Compressed `feature-list.json` into a historical summary entry plus `feat-043`.
- [x] Shortened `progress.md` and this handoff so the next session reads only current state, durable decisions, and recent verification.
- [x] Verified the new contract with `./init.sh`, focused pytest on the changed contract tests, `pytest tests/ -x`, `ruff check src/ tests/`, `bash -n bin/ahe`, `node --check .codex/hooks/ahe-hook.js`, `python3 -m json.tool feature-list.json`, and `sh .codex/skills/ahe-compression/scripts/check-harness-size.sh`.
- [x] Changed `bin/ahe` so install, doctor, and uninstall use `$CODEX_HOME` when set and `~/.codex` otherwise.
- [x] Generated global hook config with an absolute `ahe-hook.js` command so AHE can run from any workspace.
- [x] Updated `AGENTS.md` and internal AHE skills so every existing `docs/*.md` file is read as supporting project context.
- [x] Verified the global install/docs contract with focused tests, full tests, lint, shell syntax, hook syntax, and JSON validation.
- [x] Renamed `docs/product.md`, `progress.md`, `session-handoff.md`, and the matching shared templates to lowercase filenames while keeping `AGENTS.md` uppercase.
- [x] Updated hook context, skills, compression detector, docs, and tests to use lowercase artifact names.
- [x] Added `.codex/skills/ahe-ship/` with an independent `SKILL.md`, UI metadata, and `scripts/write_plan.py`.
- [x] Updated `.codex/hooks/ahe-hook.js` so exact `ahe ship`, `ahe-ship`, and `$ahe-ship` route directly to the ship workflow without `ahe-thinker`.
- [x] Updated `bin/ahe`, `README.md`, `docs/PRODUCT.md`, `feature-list.json`, `progress.md`, and focused tests for the shipped exporter.
- [x] Updated AHE hook and skill contracts so `docs/product.md` stays overview context while numbered docs such as `docs/product1.md` and `docs/product2.md` drive staged feature derivation in numeric order.
- [x] Updated the compression detector to include numeric staged product docs and ignore non-numeric product docs for default stage scanning.
- [x] Resolved the prior lowercase shared-template filename mismatch and compacted `docs/product.md` below the compression threshold.
- [x] Added `.codex/skills/ahe-fix/` with an independent `SKILL.md` and `scripts/write_fix_plan.py`.
- [x] Updated `.codex/hooks/ahe-hook.js` so exact `ahe fix`, `ahe-fix`, and `$ahe-fix` route directly to the fix-plan workflow without `ahe-thinker`.
- [x] Updated `bin/ahe`, `README.md`, `docs/PRODUCT.md`, `feature-list.json`, `progress.md`, and focused tests for the fix-plan exporter.

## Current Open Questions

- `mypy src/ --strict` could not run because `mypy` is not installed in this environment.
- `make check` could not run because this repo has no `check` target.
- `quick_validate.py .codex/skills/ahe-ship` could not run with system Python because `yaml` is not installed.

## Important Files

- `docs/product.md` - Canonical product and workflow contract for global AHE installation plus no-backup restart/compression behavior.
- `bin/ahe` - Installer, doctor, and uninstaller now target the global Codex home.
- `AGENTS.md` - Startup workflow now tells Codex to read all existing `docs/*.md` files, especially product-style docs.
- `.codex/skills/ahe-init/SKILL.md` - Restart-scope workflow; now replaces in-scope harness files without creating backup copies and reads all docs context.
- `.codex/skills/ahe-harness/SKILL.md` - Harness maintenance contract; now summarizes old completed feature history into one done feature and reads all docs context.
- `.codex/skills/ahe-reviewer/SKILL.md` - Review scope now checks all existing `docs/*.md` files when reviewing harness state.
- `.codex/skills/ahe-thinker/SKILL.md`, `.codex/skills/ahe-solver/SKILL.md` - Active product-stage selection and feature-solving contract.
- `.codex/ahe-shared/templates/product.md`, `.codex/ahe-shared/templates/progress.md`, `.codex/ahe-shared/templates/session-handoff.md` - Shared templates now match the lowercase filename contract.
- `.codex/skills/ahe-compression/SKILL.md` and `.codex/skills/ahe-compression/scripts/check-harness-size.sh` - Compression protocol and detector now include numbered product stage docs.
- `.codex/hooks/ahe-hook.js` - Exact `ahe init` and explicit `ahe compress feature-list` directive text for the new behavior.
- `.codex/skills/ahe-ship/SKILL.md` - Independent user-facing exporter workflow for latest Plan Mode output.
- `.codex/skills/ahe-ship/scripts/write_plan.py` - Deterministic `.plans/{plan_name}.md` writer with sanitization and overwrite protection.
- `.codex/skills/ahe-fix/SKILL.md` - Independent user-facing fix-plan workflow for errors or changed intent.
- `.codex/skills/ahe-fix/scripts/write_fix_plan.py` - Deterministic `.plans/{plan_name}.md` fix-plan writer with sanitization and overwrite protection.
- `feature-list.json`, `progress.md`, `session-handoff.md` - Compressed live tracking artifacts that keep current state concise.
- `tests/test_init_workflow.py`, `tests/test_ahe_hook.py`, `tests/test_compression_workflow.py`, `tests/test_ahe_ship_writer.py` - Contract coverage for the restart, compression, hook routing, and plan export rules.

## Next Recommended Action

1. Read `AGENTS.md`.
2. Read `feature-list.json` and `progress.md`.
3. Run `./init.sh`.
4. Use `ahe ship` immediately after a Codex Plan Mode `<proposed_plan>` to write a portable `.plans/*.md` handoff.
5. Use `ahe fix` when the desired output is a fix plan for an error or changed user intent.
6. When staged product docs exist, continue the first numeric product stage whose derived `feature-list.json` items are not all `done`.

## Verification Status

| Check | Command | Result | Notes |
|---|---|---|---|
| Init sanity | `./init.sh` | Pass | Startup check still reports the expected Python-default environment guidance. |
| Focused init contract | `pytest tests/test_init_workflow.py -x` | Pass | Confirms no-backup restart wording and summary-based replacement behavior. |
| Focused hook contract | `pytest tests/test_ahe_hook.py -x` | Pass | Confirms exact `ahe init`, explicit `ahe compress feature-list`, and independent `ahe ship` directives match the current contract. |
| Focused ship contract | `pytest tests/test_ahe_ship_writer.py tests/test_ahe_hook.py -k 'ship or ahe_ship' -x` | Pass | 4 passed; confirms writer behavior and direct hook route. |
| Focused compression contract | `pytest tests/test_compression_workflow.py -x` | Pass | Confirms summarized done-feature compression guidance and no backup-copy wording. |
| Focused global/docs contract | `pytest tests/test_project_setup.py -x` | Fail | Fails after the `ahe-ship` installer assertions on pre-existing lowercase shared-template filename expectations. |
| Focused staged product docs | `pytest tests/test_ahe_hook.py tests/test_spec_workflow.py tests/test_specialized_workflows.py tests/test_compression_workflow.py -x` | Pass | Confirms hook, harness, solver, and detector staged-doc contracts. |
| Full tests | `pytest tests/ -x` | Pass | 71 passed. |
| Lint | `ruff check src/ tests/` | Pass | Ruff reported all checks passed. |
| Hook syntax | `node --check .codex/hooks/ahe-hook.js` | Pass | Edited hook parses cleanly. |
| Shell syntax | `bash -n bin/ahe` | Pass | Installer script parses cleanly. |
| Package JSON validation | `python3 -m json.tool package.json` | Pass | `package.json` remains valid after postinstall text update. |
| Feature JSON validation | `python3 -m json.tool feature-list.json` | Pass | `feature-list.json` remains valid JSON after tracking update. |
| Writer syntax | `PYTHONPYCACHEPREFIX=/tmp/ahe-ship-pycache python3 -m py_compile .codex/skills/ahe-ship/scripts/write_plan.py` | Pass | Cache redirected because `.codex` cannot receive `__pycache__` in this sandbox. |
| Type check | `mypy src/ --strict` | Not run | `mypy` is not installed. |
| Skill validation | `python3 /Users/KC/.codex/skills/.system/skill-creator/scripts/quick_validate.py .codex/skills/ahe-ship` | Not run | System Python is missing the `yaml` module required by the validator. |
| Compression preflight | `sh .codex/skills/ahe-compression/scripts/check-harness-size.sh` | Pass | Detector checks lowercase harness files and reports compression not required. |
| Full tests after fix planner | `pytest tests/ -x` | Pass | 75 passed. |
| Fix hook smoke | `printf ... "ahe fix" ... | node .codex/hooks/ahe-hook.js` | Pass | Returned `AHE fix planning activated.` and `.plans/{plan_name}.md` guidance. |
| Fix writer smoke | `printf ... | python3 .codex/skills/ahe-fix/scripts/write_fix_plan.py --root /tmp/ahe-fix-smoke --plan-name 'Fix Smoke' --overwrite` | Pass | Created `/tmp/ahe-fix-smoke/.plans/fix-smoke.md`. |
| Fix writer syntax | `PYTHONPYCACHEPREFIX=/tmp/ahe-fix-pycache python3 -m py_compile .codex/skills/ahe-fix/scripts/write_fix_plan.py` | Pass | Cache redirected outside the repo. |
| Make check | `make check` | Not run | No `check` target exists in this repo. |
