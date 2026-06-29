# Remove `.ahe` Directory From AHE Contract

## Handoff Summary
Remove `.ahe` as an AHE-managed workspace concept. The workflow-state artifact must become root `status.json`, and all AHE contract text and contract tests must stop treating `.ahe/process_status.json` or `.ahe` as required workspace structure.

## Source Plan
- Update `.codex/skills/ahe-init/SKILL.md` so it reads, tracks, and creates root `status.json` instead of `.ahe/process_status.json`.
- Update `.codex/skills/ahe-harness/SKILL.md` so inspection, workflow alignment, and tracking-sync rules refer to root `status.json`.
- Update `.codex/skills/ahe-conversator/SKILL.md` so pause/resume persistence uses root `status.json`.
- Update `docs/product.md` so the formal AHE product contract names root `status.json` and no longer implies `.ahe` as a workspace directory.
- Update `src/templates/agents.md` so the workflow-state artifact is `status.json`.
- Update the contract tests that currently enforce `.ahe/process_status.json` to instead enforce `status.json` at the root.
- Keep `tests/test_ahe_hook.py` aligned so obsolete `.ahe/process_status.json` is rejected, without introducing unrelated restrictions.
- Update only additional direct `.ahe` contract references that fail focused verification or are clearly user-facing workspace-contract text.

## Execution Context
- Repository: `/Users/KC/Codes/awesome_harness_engineering`
- Current user intent: remove the `.ahe` folder from the AHE contract entirely because it is not needed.
- Existing workspace state: `AGENTS.md` is already modified before this handoff and must not be overwritten or reverted.
- `ahe-antigravity` was not found on `PATH` during preflight in this session.

## Assumptions
- The canonical workflow-state file is exactly root `status.json`.
- `.ahe` should not be required or described as part of the current AHE workspace layout.
- This is a contract rename/removal, not a schema redesign.
- Incidental strings such as temp filename suffixes do not need to change unless they create failing tests or user-visible confusion.

## Constraints
- Keep scope tight to the AHE contract surfaces.
- Do not modify `templates/` contents directly.
- Do not revert unrelated user changes.
- Prefer clear, simple, pythonic edits and readable test updates.

## Verification Plan
- Run focused tests first:
  - `pytest tests/test_init_workflow.py tests/test_spec_workflow.py tests/test_clarification_prompt.py tests/test_session_tracking_handoff.py tests/test_ahe_hook.py -x`
- If another direct contract dependency appears, update only that dependency and rerun the focused set.
- Then run broad regression:
  - `pytest tests/ -x`

## Risks and Open Questions
- `docs/product.md` and some tests still contain older `.ahe` wording, including historical backup references; only active contract wording should change unless broader cleanup is required by failing tests.
- `AGENTS.md` is dirty already, so execution must avoid accidental edits there.
- Antigravity may not be installed in this environment, which prevents verified completion cleanup.

## Instructions for Next Agent
Implement only the root `status.json` and `.ahe` removal contract changes described above. Keep edits narrow, respect existing dirty workspace state, run the focused tests before broad regression, and treat the plan as complete only if verification passes. If Antigravity or any wrapper reports success without emitting `AHE_PLAN_COMPLETE`, do not delete the `.plans` file.
