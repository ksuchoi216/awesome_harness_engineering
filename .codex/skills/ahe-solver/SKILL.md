---
name: ahe-solver
description: Internal AHE feature-solving workflow for dividing, planning, and solving feature work after the active goal is clear enough.
---

# AHE Solver

This is an internal AHE workflow skill, not a user-facing command.

Do not treat `$ahe-solver` as a user command.
Use it when `ahe-thinker` decides that the next job is building or planning a
feature.

## Command Workflow: ahe-solver

- Read the active feature context from `docs/product.md`, `feature-list.json`,
  `progress.md`, and any relevant code files.
- Divide broad work into smaller problems when useful.
- Plan each smaller problem before implementation.
- Call `ahe-reviewer` when repo or code understanding is needed.
- Call `ahe-conversator` when feature requirements, scope, or success criteria
  are still unclear.
- Report the solved step, remaining work, and recommended next agent back to
  `ahe-thinker`.
