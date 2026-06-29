---
name: solve
description: Internal AHE feature-solving workflow for dividing, planning, and solving feature work after the active goal is clear enough.
---

# AHE Solver

This is an internal AHE workflow skill, not a user-facing command.

Do not treat `$solve` as a user command.
Use it when `think` decides that the next job is building or planning a
feature.

## Command Workflow: solve

- Read the active feature context from `docs/product.md`, `feature-list.json`,
  `progress.md`, and any relevant code files.
- Read all existing `docs/*.md` files as supporting context.
- When numbered product stages exist, solve against the active product stage:
  start with `docs/product1.md`, advance to later numeric stages only after the
  current stage's derived feature-list items are `done`, and keep future product stages as context rather than implementation scope.
- Keep `docs/product.md` as overview context while working from an active
  product stage.
- Divide broad work into smaller problems when useful.
- Plan each smaller problem before implementation.
- Call `review` when repo or code understanding is needed.
- Call `converse` when feature requirements, scope, or success criteria
  are still unclear.
- Report the solved step, remaining work, and recommended next agent back to
  `think`.
