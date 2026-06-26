# SESSION-HANDOFF.md

## Current Product Context

- Goal: Keep AHE's Codex-facing harness workflow compact, explicit, and cheap to resume in chat.
- Current status: `feat-043 No-Backup Feature History Compression` is complete.
- Branch / commit: `develop`; the live AHE contracts now prefer summarized history over backup copies for harness restarts and feature-list compression.

## Last Completed Work

- [x] Removed AHE workflow backup-copy guidance from `.codex/skills/ahe-init/SKILL.md`, `.codex/skills/ahe-compression/SKILL.md`, `.codex/skills/ahe-harness/SKILL.md`, `.codex/hooks/ahe-hook.js`, and `docs/PRODUCT.md`.
- [x] Changed the `ahe compress feature-list` contract so old completed entries collapse into one summarized done feature while unfinished work remains detailed.
- [x] Compressed `feature-list.json` into a historical summary entry plus `feat-043`.
- [x] Shortened `PROGRESS.md` and this handoff so the next session reads only current state, durable decisions, and recent verification.
- [x] Verified the new contract with `./init.sh`, focused pytest on the changed contract tests, `pytest tests/ -x`, `ruff check src/ tests/`, `bash -n bin/ahe`, `node --check .codex/hooks/ahe-hook.js`, `python3 -m json.tool feature-list.json`, and `sh .codex/skills/ahe-compression/scripts/check-harness-size.sh`.

## Current Open Questions

- None.

## Important Files

- `docs/PRODUCT.md` - Canonical product and workflow contract for the no-backup restart/compression behavior.
- `.codex/skills/ahe-init/SKILL.md` - Restart-scope workflow; now replaces in-scope harness files without creating backup copies.
- `.codex/skills/ahe-harness/SKILL.md` - Harness maintenance contract; now summarizes old completed feature history into one done feature.
- `.codex/skills/ahe-compression/SKILL.md` - Compression protocol; now preserves useful old context through summaries instead of backup folders.
- `.codex/hooks/ahe-hook.js` - Exact `ahe init` and explicit `ahe compress feature-list` directive text for the new behavior.
- `feature-list.json`, `PROGRESS.md`, `SESSION-HANDOFF.md` - Compressed live tracking artifacts that keep current state concise.
- `tests/test_init_workflow.py`, `tests/test_ahe_hook.py`, `tests/test_compression_workflow.py` - Contract coverage for the new restart and compression rules.

## Next Recommended Action

1. Read `AGENTS.md`.
2. Read `feature-list.json` and `PROGRESS.md`.
3. Run `./init.sh`.
4. If a future session expands historical tracking again, re-run the compression detector before broad harness reads and summarize stale done history instead of restoring per-feature detail.

## Verification Status

| Check | Command | Result | Notes |
|---|---|---|---|
| Init sanity | `./init.sh` | Pass | Startup check still reports the expected Python-default environment guidance. |
| Focused init contract | `pytest tests/test_init_workflow.py -x` | Pass | Confirms no-backup restart wording and summary-based replacement behavior. |
| Focused hook contract | `pytest tests/test_ahe_hook.py -x` | Pass | Confirms exact `ahe init` and explicit `ahe compress feature-list` directives match the new contract. |
| Focused compression contract | `pytest tests/test_compression_workflow.py -x` | Pass | Confirms summarized done-feature compression guidance and no backup-copy wording. |
| Full tests | `pytest tests/ -x` | Pass | 58 passed. |
| Lint | `ruff check src/ tests/` | Pass | Ruff reported all checks passed. |
| Hook syntax | `node --check .codex/hooks/ahe-hook.js` | Pass | Edited hook parses cleanly. |
| Shell syntax | `bash -n bin/ahe` | Pass | Installer script parses cleanly. |
| JSON validation | `python3 -m json.tool feature-list.json` | Pass | `feature-list.json` remains valid JSON after compression. |
| Compression preflight | `sh .codex/skills/ahe-compression/scripts/check-harness-size.sh` | Pass | Harness context is back under the compression thresholds. |
