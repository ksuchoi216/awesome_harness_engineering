---
name: ahe-review
description: Internal AHE review workflow for understanding repo code, harness files, and CodeGraph context before another agent acts.
---

# AHE Reviewer

This is an internal AHE workflow skill, not a user-facing command.

Do not treat `$ahe-review` as a user command.
Use it when `ahe-think` or another worker needs evidence from code or harness
state before deciding what to do next.

## Review Scope

- Inspect repo code, harness files, verification history, and feature progress.
- If `.codegraph/` exists, prefer `.codegraph` or CodeGraph-backed review
  context when available.
- Check `AGENTS.md`, all existing `docs/*.md` files, `feature-list.json`,
  `progress.md`, `session-handoff.md`, and `docs/todo.md` when the question is
  about harness state.
- Treat `docs/product.md` as overview context and `docs/product{number}.md`
  files as ordered product stages when reviewing product or feature drift.
- Ignore non-numeric product docs such as `docs/product-alpha.md` for stage
  ordering.
- Verify that `feature-list.json` reflects only the active product stage, not
  future product stages.
- Especially read `docs/product.md` and
  `docs/product{number}.md` files when present because they explain what to do.

## Handoffs

- Report findings back to `ahe-think` by default.
- Call `ahe-harness` directly when review finds harness drift, stale tracking,
  or product doc / feature-list mismatches.
- Call `ahe-converse` only when the missing information must come from the
  user.

## Output

- State what was reviewed.
- State the relevant evidence or mismatch.
- State the recommended next agent.
