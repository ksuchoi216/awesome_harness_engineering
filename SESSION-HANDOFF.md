# session-handoff.md

## Current Product Context

- Goal: Keep AHE's Codex-facing harness workflow compact, explicit, and cheap to resume in chat.
- Current status: `feat-045 Lowercase Harness Artifact Filenames` is complete.
- Branch / commit: `develop`; the live AHE contracts now install globally, read all existing `docs/*.md` files, and use lowercase filenames for product/progress/session artifacts.

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

## Current Open Questions

- None.

## Important Files

- `docs/product.md` - Canonical product and workflow contract for global AHE installation plus no-backup restart/compression behavior.
- `bin/ahe` - Installer, doctor, and uninstaller now target the global Codex home.
- `AGENTS.md` - Startup workflow now tells Codex to read all existing `docs/*.md` files, especially product-style docs.
- `.codex/skills/ahe-init/SKILL.md` - Restart-scope workflow; now replaces in-scope harness files without creating backup copies and reads all docs context.
- `.codex/skills/ahe-harness/SKILL.md` - Harness maintenance contract; now summarizes old completed feature history into one done feature and reads all docs context.
- `.codex/skills/ahe-reviewer/SKILL.md` - Review scope now checks all existing `docs/*.md` files when reviewing harness state.
- `.codex/ahe-shared/templates/product.md`, `.codex/ahe-shared/templates/progress.md`, `.codex/ahe-shared/templates/session-handoff.md` - Shared templates now match the lowercase filename contract.
- `.codex/skills/ahe-compression/SKILL.md` - Compression protocol; now preserves useful old context through summaries instead of backup folders.
- `.codex/hooks/ahe-hook.js` - Exact `ahe init` and explicit `ahe compress feature-list` directive text for the new behavior.
- `feature-list.json`, `progress.md`, `session-handoff.md` - Compressed live tracking artifacts that keep current state concise.
- `tests/test_init_workflow.py`, `tests/test_ahe_hook.py`, `tests/test_compression_workflow.py` - Contract coverage for the new restart and compression rules.

## Next Recommended Action

1. Read `AGENTS.md`.
2. Read `feature-list.json` and `progress.md`.
3. Run `./init.sh`.
4. Use `ahe install` with `$CODEX_HOME` when testing global install behavior in temporary environments.

## Verification Status

| Check | Command | Result | Notes |
|---|---|---|---|
| Init sanity | `./init.sh` | Pass | Startup check still reports the expected Python-default environment guidance. |
| Focused init contract | `pytest tests/test_init_workflow.py -x` | Pass | Confirms no-backup restart wording and summary-based replacement behavior. |
| Focused hook contract | `pytest tests/test_ahe_hook.py -x` | Pass | Confirms exact `ahe init` and explicit `ahe compress feature-list` directives match the new contract. |
| Focused compression contract | `pytest tests/test_compression_workflow.py -x` | Pass | Confirms summarized done-feature compression guidance and no backup-copy wording. |
| Focused global/docs contract | `pytest tests/test_project_setup.py tests/test_init_workflow.py tests/test_ahe_hook.py -x` | Pass | 31 passed; confirms global install behavior, startup docs guidance, and hook context. |
| Full tests | `pytest tests/ -x` | Pass | 62 passed. |
| Lint | `ruff check src/ tests/` | Pass | Ruff reported all checks passed. |
| Hook syntax | `node --check .codex/hooks/ahe-hook.js` | Pass | Edited hook parses cleanly. |
| Shell syntax | `bash -n bin/ahe` | Pass | Installer script parses cleanly. |
| Package JSON validation | `python3 -m json.tool package.json` | Pass | `package.json` remains valid after postinstall text update. |
| Feature JSON validation | `python3 -m json.tool feature-list.json` | Pass | `feature-list.json` remains valid JSON after tracking update. |
| Compression preflight | `sh .codex/skills/ahe-compression/scripts/check-harness-size.sh` | Pass | Detector now checks `docs/product.md`, `progress.md`, and `session-handoff.md`; compression not required. |
