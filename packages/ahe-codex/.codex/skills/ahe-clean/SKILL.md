---
name: ahe-clean
description: Use when valid harness tracking artifacts contain too much stale completed history and the current next step is harder to see.
---

# AHE Clean

This is an internal AHE workflow skill, not a user-facing command.

Do not treat `$ahe-clean` as a user command.
Use it when `ahe-think` decides that completed tracker history should be compacted
to restore clarity for current work.

## Purpose

- Reduce stale completed history in `feature-list.json`.
- Reduce stale completed history in `session-handoff.md`.
- Keep the active work legible without turning tracking artifacts into archives.
- Follow the tracking-policy contract owned by `ahe-harness`.

## Scope

- Read only the context needed to judge relevance:
  - `docs/product.md`
  - active `docs/product{number}.md` stage when present
  - `feature-list.json`
  - `progress.md`
  - `session-handoff.md`
- Do not become a general harness editor.
- Do not rewrite `docs/product.md` or `docs/INSTRUCTIONS.md`.
- Touch `progress.md` only when the active-feature or latest-completed-work text
  must stay consistent after cleanup.

## Cleanup Rules For `feature-list.json`

- Preserve all non-`done` features.
- Preserve the active feature from `progress.md`.
- Preserve completed dependency features needed for the active feature.
- Preserve completed features still needed to understand the active product
  stage or the current next work.
- Remove `done` features that are not relevant under those rules.
- Replace removed completed history with one stable summary feature entry.
- The summary entry must stay `status: "done"`.
- The summary entry must explain that older unrelated completed work was
  compacted.
- The summary entry must record a covered feature ID span or covered count.
- The summary entry must be updated in place on future cleanup runs instead of
  duplicating summaries.

## Cleanup Rules For `session-handoff.md`

- In `## Last Completed Work`, preserve only:
  - items directly related to the active feature;
  - items needed to explain current harness state;
  - items needed to justify the next recommended step.
- Remove unrelated older completed bullets.
- Replace removed bullets with one compact summary bullet describing that older
  unrelated completed work was condensed.
- Keep `## Current Product Context`, `## Important Files`,
  `## Next Recommended Action`, and `## Verification Status` governed by the
  normal handoff rules; do not broadly compress them here.

## Completion

- Keep `feature-list.json` valid JSON.
- Keep `session-handoff.md` focused on the next-session startup path.
- Preserve current-work clarity rather than long-form history.
