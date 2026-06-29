---
name: ahe-compress
description: Internal AHE compression workflow for detecting oversized harness-engineering files or stale overlapping tests, and compacting them before AHE thinker or harness routing reads large context. Use when AGENTS.md, docs/product.md, docs/product{number}.md, docs/INSTRUCTIONS.md, feature-list.json, progress.md, session-handoff.md, docs/todo.md, or other AHE harness artifacts have too many lines or waste context. It also covers stale overlapping tests.
---

# AHE Compression

This is an internal AHE workflow skill, not a user-facing command.

Do not treat `$compress` as a user command.
Use it after `think` or `harness` decides that harness context is too large to read
efficiently, or when test-suite cleanup is needed. When the user explicitly asks
for `ahe compress`, this skill must check both harness-file size pressure and
stale overlapping tests before deciding the next action.

## Test Overlap Detection

Run the deterministic test-overlap detector script:

```bash
python .codex/skills/compress/scripts/detect_stale_tests.py
```

The script checks for legacy tests already covered by newer canonical files and prints `REVIEW_TEST\t<legacy-file>\tcovered_by=<keeper-files>`.
It exits with code `2` and prints `TEST_COMPRESSION_REQUIRED` when stale candidates exist.

Note: `compress` must not directly delete tests; it only signals compression pressure. The actual test consolidation must be routed by `think` through `review` first and then `solve` or `harness` as needed.

## Size Detection

Run the deterministic line-count preflight before reading full harness files:

```bash
sh .codex/skills/compress/scripts/check-harness-size.sh
```

The script checks these AHE-managed files when they exist:

- `AGENTS.md`
- `docs/product.md`
- numbered product stage docs such as `docs/product1.md` and `docs/product2.md`
- `docs/INSTRUCTIONS.md`
- `feature-list.json`
- `progress.md`
- `session-handoff.md`
- `docs/todo.md`

Default thresholds are configured in `.codex/ahe-shared/config.yaml`:

- `agent_md`: 80
- `product_md`: 180
- `instructions_md`: 180
- `feature_list_json`: 180
- `progress_md`: 180
- `session_handoff_md`: 180
- `todo_md`: 180
- `total`: 750 (combined harness context limit)

Override thresholds only when the workspace has an explicit local rule using environment variables (e.g., `AHE_AGENT_MD_LIMIT`, `AHE_FILE_LINE_LIMIT`, `AHE_TOTAL_LINE_LIMIT`):

```bash
AHE_AGENT_MD_LIMIT=100 AHE_TOTAL_LINE_LIMIT=900 sh .codex/skills/compress/scripts/check-harness-size.sh
```

Exit code meanings:

- `0`: no compression needed.
- `2`: compression needed.
- Output ending in `COMPRESSION_REQUIRED`: compression needed.
- Any other nonzero code: detector failed; fall back to `wc -l` on the same
  file set and continue the decision manually.

## Compression Decision

- Run both compression detectors before choosing the next compression step.
- If the detector exits `2`, compress before normal AHE routing continues.
- If the harness-size detector exits `2`, compact harness files first.
- If the stale-test detector exits `2`, route through `review` before any test cleanup.
- If only one file exceeds the per-file threshold, compress that file first.
- If total harness context exceeds the total threshold, compress the largest
  AHE-managed files until the total is under the threshold.
- If `AGENTS.md` is oversized, obey the local `AGENTS.md` instructions before
  editing it. Compress only sections that local rules allow. If no section is
  safely editable, report the blocker and compress other harness files instead.
- Do not read an oversized file wholesale after detection. Read headings,
  current-status sections, JSON keys, or bounded line ranges needed to preserve
  behavior.

## Compression Rules

- Preserve active requirements, current decisions, incomplete work, blockers,
  dependencies, and verification evidence.
- Preserve required headers and file formats for `progress.md`,
  `session-handoff.md`, `feature-list.json`, and `AGENTS.md`.
- Keep `feature-list.json` valid JSON. Replace stale completed-feature history
  with one summarized done feature, preserve its `id`, `name`, `description`,
  `dependencies`, `status`, and short evidence, and keep current unfinished
  details as-is.
- Keep `docs/product.md` and `docs/INSTRUCTIONS.md` as the current harness
  contract. Remove duplicate historical wording only when the active contract
  remains clear.
- Keep numbered product stage docs in numeric suffix order. Ignore non-numeric
  product docs such as `docs/product-alpha.md` for stage ordering.
- Preserve the active product stage and do not merge future product stages into
  current feature-list work during compression.
- Keep `progress.md` focused on current status, recent completed work,
  decisions that still matter, blockers, and latest verification.
- Keep `session-handoff.md` focused on the startup path for the next session,
  important files, open questions, and current verification status.
- Do not create backup copies when compressing harness history. Preserve useful
  context through concise summaries in the refreshed harness files instead.

## Completion

- Re-run the size detector after compression.
- Run JSON validation when `feature-list.json` changed.
- Run the repository's normal harness verification command when compression
  changed tracked harness files.
- Update `progress.md` and `session-handoff.md` with the compression evidence
  when they changed or when compression affects the active workflow.
