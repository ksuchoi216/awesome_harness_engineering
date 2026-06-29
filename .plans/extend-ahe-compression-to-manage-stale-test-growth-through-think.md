# Extend AHE Compression To Manage Stale Test Growth Through `think`

## Handoff Summary
Extend AHE compression so it manages stale overlapping tests as well as oversized harness files. Keep `think` as the first decision point for explicit compression queries, and add deterministic stale-test detection plus canonical consolidation rules for legacy overlapping tests.

## Source Plan
# Extend AHE Compression To Manage Stale Test Growth Through `think`

## Summary

Keep the external behavior centered on `think`: any explicit `ahe <query>` compression request, including `ahe compress feature-list` and the new documented `ahe compress tests`, must still enter through the hook and be judged by `think` first.

Expand compression from “oversized harness files” to “oversized or stale AHE maintenance context,” where stale test growth means legacy workflow-style tests whose contract is already covered by newer canonical AHE test files. In this repo, the first concrete stale candidates are `tests/test_new_workflow.py`, `tests/test_spec_workflow.py`, and `tests/test_specialized_workflows.py`.

## Key Changes

- Update `packages/ahe-codex/.codex/hooks/ahe-hook.js`, `packages/ahe-codex/.codex/skills/think/SKILL.md`, `packages/ahe-codex/.codex/skills/compress/SKILL.md`, `packages/ahe-codex/.codex/skills/harness/SKILL.md`, `README.md`, and `docs/product.md` so the contract is explicit:
  - `think` remains the first gate for all compression requests.
  - `compress` now covers stale overlapping tests as well as large harness files.
  - `harness` remains responsible for tracker compression, while test-suite cleanup is routed by `think` through `review` first and then `solve` or `harness` as needed.

- Add a deterministic test-overlap detector script under `packages/ahe-codex/.codex/skills/compress/scripts/`:
  - Input: current `tests/test_*.py` inventory.
  - Output lines: `REVIEW_TEST\t<legacy-file>\tcovered_by=<keeper-files>` for stale candidates.
  - Exit with code `2` and end with `TEST_COMPRESSION_REQUIRED` when any stale candidate exists.
  - First-pass hardcoded overlap map:
    - `tests/test_new_workflow.py` -> `tests/test_ahe_new.py`
    - `tests/test_spec_workflow.py` -> `tests/test_clarification_prompt.py`, `tests/test_ahe_new.py`
    - `tests/test_specialized_workflows.py` -> `tests/test_ahe_new.py`, `tests/test_clarification_prompt.py`, `tests/test_command_set.py`
  - Do not attempt semantic deduplication beyond this explicit map in v1.

- Extend the compression protocol:
  - Existing line-count detector stays unchanged for harness files.
  - `think` runs the test-overlap detector when the user’s explicit AHE query is compression-oriented.
  - If either detector returns compression required, `think` must not send the user straight to `compress`; it must decide whether the next step is:
    - `harness` for harness-file compaction,
    - `review` for stale-test confirmation and keeper selection,
    - or both in sequence.
  - `compress` itself must not directly delete tests; it only signals compression pressure and the required route.

- Define the consolidation behavior for the stale test set:
  - Unique assertions from each legacy workflow test must be copied into the mapped keeper file before removal.
  - After all unique assertions are preserved, delete the legacy test file.
  - Do not add a new archive directory for tests.
  - Do not create new broad “workflow summary” test files going forward; extend the canonical keeper file instead.

## Public Interface / Contract Updates

- Keep explicit `ahe <query>` as the only query entrypoint.
- Continue supporting `ahe compress feature-list`.
- Add documented support for `ahe compress tests` as an example explicit query.
- Add new detector marker contract:
  - `TEST_COMPRESSION_REQUIRED`
  - `REVIEW_TEST\t<legacy-file>\tcovered_by=<keeper-files>`

## Test Plan

- Add detector tests that verify:
  - no stale-test signal when only keeper files exist,
  - stale-test signal and exit code `2` when mapped legacy files exist,
  - reported `covered_by=` values match the hardcoded map.

- Update hook and skill contract tests to assert:
  - explicit compression queries still route through `think`,
  - compression language now mentions stale overlapping tests,
  - `compress` is not described as a direct user-facing delete path.

- Add/adjust regression tests around the concrete legacy files so that:
  - required assertions survive in keeper files,
  - removed legacy files are no longer referenced by setup/command tests,
  - `pytest tests/ -x` still passes after consolidation.

## Assumptions

- “Past tests” means legacy workflow/spec summary tests already covered by newer canonical surface tests, not every old test file.
- v1 uses an explicit overlap map for this repo instead of a generic similarity engine.
- The goal is to reduce unnecessary test-file growth safely and readably, not to auto-prune arbitrary tests without review evidence.

## Execution Context
- Repository: `/Users/KC/Codes/awesome_harness_engineering`
- Current AHE structure is package-based: `packages/ahe-codex` and `packages/ahe-antigravity`.
- Existing compression logic lives under `packages/ahe-codex/.codex/skills/compress/`.
- Existing routing contract is enforced through hook, skill markdown, docs, and pytest contract tests.

## Assumptions
- The overlap map above is the entire v1 stale-test detection scope.
- Consolidation should preserve behavior, not historical file names.
- If a legacy test contains unique assertions, they move before file deletion.

## Constraints
- Keep `think` as the first gate for explicit compression queries.
- Do not route ship work through `think`, `harness`, `solve`, or other AHE agents.
- Keep code simple, readable, and pythonic where Python is touched.
- Do not modify `templates/` or `ref/`.
- Preserve existing test and hook contracts unless this plan explicitly changes them.

## Verification Plan
- Run focused detector and routing tests for stale-test detection and query routing.
- Run updated contract tests for hook and skill markdown.
- Run `pytest tests/ -x` after consolidation.
- Run any syntax checks already used by this repo for touched scripts.

## Risks and Open Questions
- Some legacy tests may still contain one-off assertions that are not obviously duplicated.
- The repo currently mixes older workflow-summary tests with newer canonical tests; consolidation must avoid silent coverage loss.
- The packaged ship skill path in this repo differs from older root-level skill paths, so touched references must stay consistent.

## Instructions for Next Agent
Implement the plan exactly as written. Prefer deterministic rules over heuristics. When consolidating tests, move unique assertions first, then remove the legacy test files. Keep the final contract explicit in hook text, skill docs, product docs, and tests.
