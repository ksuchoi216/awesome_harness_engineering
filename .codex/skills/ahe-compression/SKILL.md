---
name: ahe-compression
description: Internal AHE compression workflow for detecting oversized harness-engineering files and compacting them before AHE thinker or harness routing reads large context. Use when AGENTS.md, docs/PRODUCT.md, docs/INSTRUCTIONS.md, feature-list.json, PROGRESS.md, SESSION-HANDOFF.md, docs/todo.md, or other AHE harness artifacts have too many lines or waste context.
---

# AHE Compression

This is an internal AHE workflow skill, not a user-facing command.

Do not treat `$ahe-compression` as a user command.
Use it after `ahe-thinker` or `ahe-harness` decides that harness context is too large to read
efficiently.

## Size Detection

Run the deterministic line-count preflight before reading full harness files:

```bash
sh .codex/skills/ahe-compression/scripts/check-harness-size.sh
```

The script checks these AHE-managed files when they exist:

- `AGENTS.md`
- `docs/PRODUCT.md`
- `docs/INSTRUCTIONS.md`
- `feature-list.json`
- `PROGRESS.md`
- `SESSION-HANDOFF.md`
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
AHE_AGENT_MD_LIMIT=100 AHE_TOTAL_LINE_LIMIT=900 sh .codex/skills/ahe-compression/scripts/check-harness-size.sh
```

Exit code meanings:

- `0`: no compression needed.
- `2`: compression needed.
- Output ending in `COMPRESSION_REQUIRED`: compression needed.
- Any other nonzero code: detector failed; fall back to `wc -l` on the same
  file set and continue the decision manually.

## Compression Decision

- If the detector exits `2`, compress before normal AHE routing continues.
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
- Preserve required headers and file formats for `PROGRESS.md`,
  `SESSION-HANDOFF.md`, `feature-list.json`, and `AGENTS.md`.
- Keep `feature-list.json` valid JSON. Shorten old completed-feature evidence,
  but preserve each feature `id`, `name`, `description`, `dependencies`,
  `status`, and current unfinished details.
- Keep `docs/PRODUCT.md` and `docs/INSTRUCTIONS.md` as the current harness
  contract. Remove duplicate historical wording only when the active contract
  remains clear.
- Keep `PROGRESS.md` focused on current status, recent completed work,
  decisions that still matter, blockers, and latest verification.
- Keep `SESSION-HANDOFF.md` focused on the startup path for the next session,
  important files, open questions, and current verification status.
- Back up material before deleting substantial historical context by moving it
  under `.ahe/backups/compression-YYYYMMDD-HHMMSS/` when that context may still
  be useful.

## Completion

- Re-run the size detector after compression.
- Run JSON validation when `feature-list.json` changed.
- Run the repository's normal harness verification command when compression
  changed tracked harness files.
- Update `PROGRESS.md` and `SESSION-HANDOFF.md` with the compression evidence
  when they changed or when compression affects the active workflow.
