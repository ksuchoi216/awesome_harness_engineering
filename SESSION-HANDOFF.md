# SESSION-HANDOFF.md

## Current Product Context

- Goal: Complete the AHE chat workflow so Codex can guide harness setup, product specification, and future resume/check behavior from conversation.
- Current status: `feat-004 Product Workflow` is complete and verified. The next queued feature is `feat-005 Check and Resume Workflows`.
- Branch / commit: Current working tree changes only. No commit created in this session.

## Last Completed Work

- [x] Added a dedicated `ahe product` workflow to `.codex/skills/ahe/SKILL.md` with explicit inspection, question-by-question product input capture, required product sections, and tracking synchronization rules.
- [x] Added `tests/test_product_workflow.py` and verified it in isolation and in the full pytest suite.
- [x] Fixed `bin/ahe` so `npx ahe install` resolves the packaged skill path correctly when npm runs the entrypoint through `.bin`.

## Current Open Questions

- How strict the future `ahe check` workflow should be about product completeness versus installer-only setup state.

## Important Files

- `docs/PRODUCT.md` - Canonical product specification and scope reference.
- `.codex/skills/ahe/SKILL.md` - Installed skill entrypoint containing routing plus `ahe init` and `ahe product` workflow contracts.
- `.ahe/process_status.json` - Runtime state used by future `ahe` and `ahe resume` flows.
- `tests/test_product_workflow.py` - Contract coverage for the `ahe product` workflow.
- `tests/test_project_setup.py`, `bin/ahe` - Packaging and installer coverage for direct and `npx` install paths.

## Next Recommended Action

1. Read `AGENTS.md`.
2. Read `feature-list.json` and `PROGRESS.md`.
3. Review this handoff.
4. Run `./init.sh` or the documented verification command before editing.
5. Start `feat-005 Check and Resume Workflows` by implementing `ahe check` and `ahe resume` against the contracts already documented in `docs/PRODUCT.md`.

## Verification Status

| Check | Command | Result | Notes |
|---|---|---|---|
| Shell syntax | `bash -n init.sh` and `bash -n bin/ahe` | Pass | Startup script and installer script both parse cleanly. |
| JSON validation | `python3 -m json.tool feature-list.json` | Pass | `feature-list.json` is valid JSON. |
| Runtime state JSON | `python3 -m json.tool .ahe/process_status.json` | Pass | Process status file is valid JSON. |
| Installer checks | `./bin/ahe version` and `pytest tests/test_project_setup.py -x` | Pass | Direct installs and `npx`-style installs both work after the symlink path fix. |
| Workflow tests | `pytest tests/ -x` | Pass | All 14 tests passed, covering setup, routing, init, and product workflow contracts. |
