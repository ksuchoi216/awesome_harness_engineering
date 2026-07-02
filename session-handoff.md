# session-handoff.md

## Current Product Context

- Goal: Keep AHE's Codex-facing harness workflow compact, explicit, and cheap to resume in chat.
- Current status: `feat-071 Retire AHE Compression Workflow` is complete.
- Branch / commit: `develop`; the live AHE contracts now install globally, read all existing `docs/*.md` files, use lowercase filenames for product/progress/session artifacts, ship independent Plan Mode and fix-plan exporters, support ordered staged product docs, execute saved ship plans through Antigravity with marker-gated cleanup, provide safe git orchestration, publish npm releases from guarded bare-semver tags, separate real publish from local release validation, and keep the installer implementation under `scripts/`.

## Last Completed Work

- [x] Deleted `packages/ahe-codex/.codex/skills/ahe-compress/` and removed the active compression workflow from the Codex installer allowlist, hook prompt, thinker contract, harness contract, README, and `docs/product.md`.
- [x] Deleted `tests/test_compression_workflow.py` and `tests/test_compress_detector.py`, then updated the surrounding contract tests to assert that AHE no longer exposes compression behavior.
- [x] Verified the retired compression contract with `./init.sh`, `pytest tests/ -x`, `ruff check tests/`, `bash -n packages/ahe-codex/bin/ahe-codex`, `node --check packages/ahe-codex/.codex/hooks/ahe-hook.js`, `python3 -m json.tool feature-list.json`, `./bin/ahe install --force`, and `./bin/ahe doctor`.
- [x] Tried the documented reinstall path via `bash scripts/install.sh`; it reached `sudo npm install -g .` and stopped on the host password prompt, so the global skills were restored with `./bin/ahe install --force`.
- [x] Deleted saved Antigravity ship plans after the required `AHE_PLAN_COMPLETE` marker and verified the formerly failing ship test plus the full pytest suite.
- [x] Applied the pending repo changes as separated `ahe-git` commits for Antigravity cleanup, install relocation, clone helper relocation, and tracking updates.
- [x] Moved the real reinstall flow from `install.sh` to `scripts/install.sh`.
- [x] Left a thin root `install.sh` wrapper in place so existing repo instructions that call `install.sh` keep working without changing `AGENTS.md`.
- [x] Moved the real npm publish flow into `scripts/deploy.sh`.
- [x] Added `scripts/test.sh` to run branch-local validation with `npm test` and `npm pack --dry-run` without publishing.
- [x] Updated `.github/workflows/publish.yml` so npm publish now triggers on bare semver tags like `0.1.8` instead of `v0.1.8`, while still requiring tag/package parity and `master` containment.
- [x] Replaced the remote release tag `v0.1.1` with `v0.1.7` so the current published tag matches the root/workspace package version `0.1.7`.
- [x] Added `.github/workflows/publish.yml` to publish on `v*.*.*` tag pushes, require the tagged commit to be contained in `master`, require the tag to match `package.json`, install `pytest`, and run `npm publish` with `NPM_TOKEN`.
- [x] Added `ahe-git` skill directories and `SKILL.md` files for both Codex and Antigravity.
- [x] Wired Codex hook detection in `ahe-hook.js` for `ahe git` and `ahe-git`.
- [x] Updated Codex installer and Antigravity wrapper to include `ahe-git` support.
- [x] Created `tests/test_ahe_git_skill_contract.py` and `tests/test_ahe_antigravity_git.py` and updated existing command/project setup tests.
- [x] Updated README, docs/product.md, feature-list.json, progress.md, and session-handoff.md for ahe-git.
- [x] Verified the new contract with `./init.sh`, focused pytest on the changed contract tests, `pytest tests/ -x`, `ruff check src/ tests/`, `bash -n bin/ahe`, `node --check .codex/hooks/ahe-hook.js`, `python3 -m json.tool feature-list.json`, and `sh .codex/skills/ahe-compress/scripts/check-harness-size.sh`.
- [x] Changed `bin/ahe` so install, doctor, and uninstall use `$CODEX_HOME` when set and `~/.codex` otherwise.
- [x] Generated global hook config with an absolute `ahe-hook.js` command so AHE can run from any workspace.
- [x] Updated `AGENTS.md` and internal AHE skills so every existing `docs/*.md` file is read as supporting project context.
- [x] Verified the global install/docs contract with focused tests, full tests, lint, shell syntax, hook syntax, and JSON validation.
- [x] Renamed `docs/product.md`, `progress.md`, `session-handoff.md`, and the matching shared templates to lowercase filenames while keeping `AGENTS.md` uppercase.
- [x] Updated hook context, skills, compression detector, docs, and tests to use lowercase artifact names.
- [x] Added `.codex/skills/ahe-ship/` with an independent `SKILL.md`, UI metadata, and `scripts/write_plan.py`.
- [x] Updated `.codex/hooks/ahe-hook.js` so exact `ahe ship`, `ahe-ship`, and `$ahe-ship` route directly to the ship workflow without `ahe-think`.
- [x] Updated `bin/ahe`, `README.md`, `docs/PRODUCT.md`, `feature-list.json`, `progress.md`, and focused tests for the shipped exporter.
- [x] Updated AHE hook and skill contracts so `docs/product.md` stays overview context while numbered docs such as `docs/product1.md` and `docs/product2.md` drive staged feature derivation in numeric order.
- [x] Updated the compression detector to include numeric staged product docs and ignore non-numeric product docs for default stage scanning.
- [x] Resolved the prior lowercase shared-template filename mismatch and compacted `docs/product.md` below the compression threshold.
- [x] Added `.codex/skills/ahe-fix/` with an independent `SKILL.md` and `scripts/write_fix_plan.py`.
- [x] Updated `.codex/hooks/ahe-hook.js` so exact `ahe fix`, `ahe-fix`, and `$ahe-fix` route directly to the fix-plan workflow without `ahe-think`.
- [x] Updated `bin/ahe`, `README.md`, `docs/PRODUCT.md`, `feature-list.json`, `progress.md`, and focused tests for the fix-plan exporter.
- [x] Added `ahe-antigravity execute <plan-path>` so saved ship plans run through `agy` and delete only after the exact `AHE_PLAN_COMPLETE` marker verifies full completion.
- [x] Updated the packaged Codex ship skill, hook text, docs, and focused/full tests so `ahe ship` now writes, executes, and conditionally removes `.plans/{plan_name}.md`.
- [x] Removed the ship writer's Python 3.11-only `match` syntax, changed the ship skill's writer example to `python`, and updated the writer test to use the active interpreter so `conda main` no longer falls through to system `python3`.
- [x] Updated the Antigravity ship wrapper to run `agy --model "Gemini 3.1 Pro (High)"`, documented that model contract in the Codex and Antigravity ship skills, and added focused test coverage for the explicit model argument.
- [x] Replaced `ahe compress feature-list` and `ahe compress tests` wording with a single `ahe compress` contract across the hook, compression skill, thinker, harness, installer help, README, and product doc.
- [x] Updated focused hook and compression tests so `ahe compress` now proves both detectors are checked from one entrypoint before follow-up routing.

## Current Open Questions

- The documented global reinstall path still depends on `sudo npm install -g .`; on this machine it stops for an interactive password prompt, so unattended reinstall remains blocked unless sudo is available.
- The new GitHub Actions workflow assumes the repository secret is named `NPM_TOKEN`; publish will fail until that secret exists in GitHub.
- `mypy src/ --strict` could not run because `mypy` is not installed in this environment.
- `make check` could not run because this repo has no `check` target.
- `quick_validate.py .codex/skills/ahe-ship` could not run with system Python because `yaml` is not installed.
- `conda run -n main which python3` still resolves to the system Python 3.8 binary on this machine, so AHE ship checks should avoid hardcoded `python3` when they depend on the active Conda interpreter.

## Important Files

- `.github/workflows/publish.yml` - Publishes `@ksuchoi216/ahe` when a bare semver tag push like `0.1.8` matches `package.json` and points to a commit reachable from `master`.
- `docs/product.md` - Canonical product and workflow contract for global AHE installation and the current non-compression AHE surface.
- `scripts/install.sh` - Real reinstall script for globally uninstalling, npm-installing, and re-installing the Codex and Antigravity skills.
- `scripts/deploy.sh` - Explicit real publish script that still performs npm login checks, optional branch switching, dry-run pack, and `npm publish`.
- `scripts/test.sh` - Local release validation script that runs `npm test` and `npm pack --dry-run` on the current branch without publishing.
- `bin/ahe` - Installer, doctor, and uninstaller now target the global Codex home.
- `AGENTS.md` - Startup workflow now tells Codex to read all existing `docs/*.md` files, especially product-style docs.
- `.codex/skills/ahe-init/SKILL.md` - Restart-scope workflow; now replaces in-scope harness files without creating backup copies and reads all docs context.
- `.codex/skills/ahe-harness/SKILL.md` - Harness maintenance contract for product, instructions, tracker, and todo sync without compression routing.
- `.codex/skills/ahe-review/SKILL.md` - Review scope now checks all existing `docs/*.md` files when reviewing harness state.
- `.codex/skills/ahe-think/SKILL.md`, `.codex/skills/ahe-solve/SKILL.md` - Active product-stage selection and feature-solving contract without compression preflight.
- `.codex/ahe-shared/templates/product.md`, `.codex/ahe-shared/templates/progress.md`, `.codex/ahe-shared/templates/session-handoff.md` - Shared templates now match the lowercase filename contract.
- `.codex/hooks/ahe-hook.js` - Exact `ahe`/`ahe new`/`ahe ship`/`ahe fix`/`ahe git` routing guidance without compression directives.
- `packages/ahe-codex/.codex/skills/ship/SKILL.md` - Codex-side ship workflow that now writes a plan and runs `ahe-antigravity execute`.
- `packages/ahe-codex/.codex/skills/ship/scripts/write_plan.py` - Deterministic `.plans/{plan_name}.md` writer with sanitization, overwrite protection, and Python parser compatibility beyond Python 3.11.
- `packages/ahe-antigravity/bin/ahe-antigravity` - Antigravity wrapper with the new `execute` command for stdin-driven `agy` execution and verified cleanup.
- `tests/test_ahe_antigravity_ship.py` - Ship execution contract coverage, including the explicit `Gemini 3.1 Pro (High)` model selection.
- `packages/ahe-antigravity/skills/execute/SKILL.md` - Execution contract that gates success on the exact `AHE_PLAN_COMPLETE` marker.
- `packages/ahe-codex/.codex/skills/fix/SKILL.md` - Independent user-facing fix-plan workflow for errors or changed intent.
- `packages/ahe-codex/.codex/skills/fix/scripts/write_fix_plan.py` - Deterministic `.plans/{plan_name}.md` fix-plan writer with sanitization and overwrite protection.
- `feature-list.json`, `progress.md`, `session-handoff.md` - Compressed live tracking artifacts that keep current state concise.
- `tests/test_init_workflow.py`, `tests/test_ahe_hook.py`, `tests/test_ahe_ship_writer.py`, `tests/test_project_setup.py`, `tests/test_command_set.py` - Contract coverage for restart, hook routing, plan export, installer setup, and the removed compression surface.

## Next Recommended Action

1. Read `AGENTS.md`.
2. Read `feature-list.json` and `progress.md`.
3. Run `./init.sh`.
4. If you need to refresh the global skills again on this machine, prefer `./bin/ahe install --force` unless you are ready to enter the sudo password for `scripts/install.sh`.
5. Add the `NPM_TOKEN` repository secret in GitHub before relying on the new publish workflow.
6. Create or push future release tags in `<package.json version>` format from `master` so the publish workflow accepts them.

## Verification Status

| Check | Command | Result | Notes |
|---|---|---|---|
| Compression retirement full suite | `pytest tests/ -x` | Pass | 106 passed after removing the compression skill, detectors, and compression-only tests. |
| Compression retirement lint | `ruff check tests/` | Pass | Updated Python test suite remains clean after deleting compression-only coverage. |
| Compression retirement shell syntax | `bash -n packages/ahe-codex/bin/ahe-codex` | Pass | Installer script parses cleanly after removing `ahe-compress` and `config.yaml` requirements. |
| Compression retirement hook syntax | `node --check packages/ahe-codex/.codex/hooks/ahe-hook.js` | Pass | Hook parses cleanly after removing compression guidance. |
| Compression retirement init sanity | `./init.sh` | Pass | Startup check still reports the expected Python-default environment guidance. |
| Direct global reinstall | `./bin/ahe install --force` | Pass | Restored both Codex and Antigravity skills directly from the checked-out repo after the sudo-blocked installer attempt. |
| Direct global doctor | `./bin/ahe doctor` | Pass | Both global skill installations report healthy after direct reinstall. |
| Scripted global reinstall | `bash scripts/install.sh` | Partial | Reached `sudo npm install -g .` and stopped at the host password prompt; no noninteractive sudo path was available. |
| Init sanity | `./init.sh` | Pass | Startup check still reports the expected Python-default environment guidance. |
| Remote tag replacement | `git push origin :refs/tags/v0.1.1`, `git push origin v0.1.7`, `git ls-remote --tags origin 'v0.1.*'` | Pass | Confirmed `origin` no longer has `v0.1.1` and now exposes only `v0.1.7` for the current release tag. |
| Publish workflow inspection | `sed -n '1,220p' .github/workflows/publish.yml` | Pass | Workflow now triggers on bare semver tags like `0.1.8`, checks `master` containment, enforces tag/package parity, installs `pytest`, and publishes with `NPM_TOKEN`. |
| Install script relocation | `bash -n install.sh scripts/install.sh`, `bash install.sh --help` | Partial | Syntax is valid and the root wrapper forwards into `scripts/install.sh`; the live run reaches the real uninstall/install flow and then stops on existing privileged filesystem deletes plus `sudo npm install -g .`, which this environment does not permit. |
| Lint | `ruff check tests/` | Pass | Existing tracked Python test files lint cleanly. |
| Diff hygiene | `git diff --check` | Pass | No whitespace or patch formatting errors in the workflow/tracking changes. |
| Full tests | `pytest tests/ -x` | Pass | 118 passed after marker-gated Antigravity plan cleanup. |
| Focused init contract | `pytest tests/test_init_workflow.py -x` | Pass | Confirms no-backup restart wording and summary-based replacement behavior. |
| Focused hook contract | `pytest tests/test_ahe_hook.py -x` | Pass | Confirms exact `ahe init`, explicit `ahe compress`, and independent `ahe ship` directives match the current contract. |
| Focused ship contract | `pytest tests/test_ahe_ship_writer.py tests/test_ahe_antigravity_execute.py tests/test_ahe_hook.py -k 'ship or execute' -x` | Pass | 8 passed; confirms writer behavior, wrapper execution, completion-marker cleanup, and direct hook route. |
| Focused compression contract | `pytest tests/test_compression_workflow.py -x` | Pass | Confirms summarized done-feature compression guidance and no backup-copy wording. |
| Focused single-command compression contract | `pytest tests/test_ahe_hook.py tests/test_compression_workflow.py -x` | Pass | Confirms `ahe compress` now checks both detectors and routes compression follow-up from one entrypoint. |
| Focused global/docs contract | `pytest tests/test_project_setup.py -x` | Pass | 10 passed after aligning the tests with the packaged `packages/` layout and isolated HOME for Antigravity install checks. |
| Focused staged product docs | `pytest tests/test_ahe_hook.py tests/test_spec_workflow.py tests/test_specialized_workflows.py tests/test_compression_workflow.py -x` | Pass | Confirms hook, harness, solver, and detector staged-doc contracts. |
| Full tests | `pytest tests/ -x` | Pass | 102 passed after updating the packaged-path test surface. |
| Lint | `ruff check src/ tests/` | Pass | Ruff reported all checks passed. |
| Hook syntax | `node --check packages/ahe-codex/.codex/hooks/ahe-hook.js` | Pass | Edited hook parses cleanly. |
| Shell syntax | `bash -n bin/ahe` | Pass | Installer script parses cleanly. |
| Package JSON validation | `python3 -m json.tool package.json` | Pass | `package.json` remains valid after postinstall text update. |
| Feature JSON validation | `python3 -m json.tool feature-list.json` | Pass | `feature-list.json` remains valid JSON after tracking update. |
| Writer syntax | `PYTHONPYCACHEPREFIX=/tmp/ahe-ship-pycache python3 -m py_compile packages/ahe-codex/.codex/skills/ship/scripts/write_plan.py` | Pass | Cache redirected outside the packaged skill tree. |
| Type check | `mypy src/ --strict` | Not run | `mypy` is not installed. |
| Skill validation | `python3 /Users/KC/.codex/skills/.system/skill-creator/scripts/quick_validate.py .codex/skills/ahe-ship` | Not run | System Python is missing the `yaml` module required by the validator. |
| Compression preflight | `sh .codex/skills/ahe-compress/scripts/check-harness-size.sh` | Pass | Detector checks lowercase harness files and reports compression not required. |
| Full tests after fix planner | `pytest tests/ -x` | Pass | 75 passed. |
| Antigravity wrapper syntax | `bash -n packages/ahe-antigravity/bin/ahe-antigravity` | Pass | New execute wrapper parses cleanly. |
| Focused Antigravity ship model contract | `pytest tests/test_ahe_antigravity_ship.py -x` | Pass | 5 passed; confirms `ahe ship` now calls `agy --model "Gemini 3.1 Pro (High)"`. |
| Codex installer syntax | `bash -n packages/ahe-codex/bin/ahe-codex` | Pass | Updated ship help text parses cleanly. |
| Focused ship contract in `conda main` | `conda run -n main pytest tests/test_ahe_antigravity_ship.py tests/test_ahe_ship_writer.py tests/test_ahe_hook.py -k 'ship or ahe_ship' -x` | Pass | 8 passed; confirms the writer no longer falls through to system Python 3.8 when the active environment is `main`. |
| Ship writer compile in `conda main` | `conda run -n main python -m py_compile packages/ahe-codex/.codex/skills/ship/scripts/write_plan.py tests/test_ahe_ship_writer.py` | Pass | Writer and focused test parse cleanly in the target Conda environment. |
| Fix hook smoke | `printf ... "ahe fix" ... | node packages/ahe-codex/.codex/hooks/ahe-hook.js` | Pass | Returned `AHE fix planning activated.` and `.plans/{plan_name}.md` guidance. |
| Fix writer smoke | `printf ... | python3 .codex/skills/ahe-fix/scripts/write_fix_plan.py --root /tmp/ahe-fix-smoke --plan-name 'Fix Smoke' --overwrite` | Pass | Created `/tmp/ahe-fix-smoke/.plans/fix-smoke.md`. |
| Fix writer syntax | `PYTHONPYCACHEPREFIX=/tmp/ahe-fix-pycache python3 -m py_compile .codex/skills/ahe-fix/scripts/write_fix_plan.py` | Pass | Cache redirected outside the repo. |
| Make check | `make check` | Not run | No `check` target exists in this repo. |
