---
name: ahe-harness
description: Internal AHE harness workflow for managing product docs, instructions, feature tracking, session artifacts, todo sync, and compression-aware maintenance.
---

# AHE Harness

This is an internal AHE workflow skill, not a user-facing command.

Do not treat `$harness` as a user command.
Use it when `think` or another worker decides that harness artifacts must
be created, updated, reconciled, or compressed. It remains responsible for tracker compression, while test-suite cleanup is routed by `think` through `review` first and then `solve` or `harness` as needed.

## Command Workflow: harness

### Harness Inspection

- Read all `docs/*.md` files when they exist. Treat every docs file as
  supporting project context, even when `AGENTS.md` does not name it directly.
- Especially read `docs/product.md` and
  `docs/product{number}.md` files when present because they explain what to do.
- Read `AGENTS.md`, `feature-list.json`, `progress.md`, `session-handoff.md`,
  and `docs/todo.md` when they exist.
- Read `status.json` when it exists.
- Treat `docs/product.md` as the canonical source of truth and
  `feature-list.json` as a derived tracker.
- Treat `docs/product.md` as overview context even when a numbered product stage is active.
- Recognize only `docs/product{number}.md` files as ordered product stages.
- Ignore non-numeric product files such as `docs/product-alpha.md` for stage ordering.
- Choose the lowest-numbered product stage whose derived feature work is not complete.
- Use `docs/product.md` as the normal overview-only source when no numbered product stage exists.

### Harness Decision Paths

- Clarify product goal, scope, and success criteria when `docs/product.md`
  needs to change.
- Clarify project instructions when `docs/INSTRUCTIONS.md` needs to change.
- Clarify what next feature or goal should be tracked when the next work item is
  unclear.
- `docs/product.md` is the canonical home for product specification details collected during `ahe new`.
- Write product behavior, scope, requirements, success criteria, and workflow details into `docs/product.md`.
- `docs/product.md` is the canonical source of truth. Concrete feature items for `feature-list.json` must be derived from it only after it has been populated.
- Derive concrete feature items from only the active product stage, not future stages.
- Advance from `docs/product1.md` to `docs/product2.md` only after all feature-list items derived from `docs/product1.md` are `done`.
- Apply the same done-before-advance rule for later stages such as `docs/product2.md` to `docs/product3.md`.
- Do not move product specification details into `AGENTS.md`.
- Update only the relevant docs among `docs/product.md` and
  `docs/INSTRUCTIONS.md`.
- If the user is adding new work, append it into the last `## TODO` section of
  `docs/todo.md`, create that section when needed, and update
  `feature-list.json`.
- Apply the queued `docs/todo.md` content to `docs/product.md`.
- Remove the applied content from `docs/todo.md` because that todo content is
  already reflected in `docs/product.md`.
- Update `feature-list.json` to derive the specific feature items from the updated `docs/product.md`.
- Update `progress.md`.
- Update `session-handoff.md`.
- For `ahe compress`, if the harness-size detector signals compression pressure, replace old completed feature entries with one summarized done feature.
- Keep the summarized feature valid for the existing schema by preserving its
  own `id`, `name`, `description`, `dependencies`, `status`, and short
  evidence.
- Preserve unfinished, blocked, or active feature items in full detail.
- Reconcile `feature-list.json` against `docs/product.md` after compression.
- If no new feature can be derived from `docs/product.md`, call `converse` to ask what next feature, product direction, or goal should be tracked.
- If a numbered product stage is active and no new feature can be derived from
  that active product stage, call `converse` with the same clarification
  target.
- Call `review` directly when code or progress evidence must be checked
  before updating harness files.

### Harness Completion

- Keep `feature-list.json` valid JSON.
- Do not create backup copies when compressing harness history.
- Keep `progress.md` focused on current work, decisions that still matter,
  blockers, and recent verification evidence.
- Keep `session-handoff.md` focused on the next-session startup path.
- Keep `status.json` aligned with the active workflow.

## Clarification Rule

When the next harness step is not clear, follow the `think` protocol first. If `think` finds missing information, follow the `converse` protocol. Ask again recursively using a Codex-supported structured response request, provide 2-3 meaningful mutually exclusive options
when possible, and allow custom input when predefined options are not enough.

### User Response Target

- Collect the product, instruction, tracking, or next-feature details required
  to update harness artifacts safely.

### Questions to Ask

- Ask who the product is for and what problem it solves when product intent is
  unclear.
- Ask what behavior, scope boundaries, and success criteria should be
  documented.
- Ask what rule, practice, or guideline belongs in `docs/INSTRUCTIONS.md`.
- Ask what work should be added next when `docs/product.md` does not imply a new
  feature safely.

### Clarification Criteria

- The answer must be concrete enough to update the relevant harness files
  without guessing.
- The answer must describe actionable work, the affected area, and the intended
  outcome when queuing a todo item.

### Re-ask When

- Ask again when the answer is vague, contradictory, or incomplete.
- Ask again when the response names a topic without enough detail to update the
  harness safely.

## Session Tracking and Handoff Sync

### Tracking Update Rules

- Update `status.json` at workflow start.
- Update `status.json` after every answered question.
- Refresh `updated_at` every time workflow state changes.
- Keep `current_command`, `current_step`, and `workflow_complete` aligned with the active workflow state.
- Keep the `files` status map aligned with the actual workspace files.

### Progress and Handoff Content Requirements

- Update `progress.md` whenever the active feature, workflow status, blockers, or verification state changes.
- Update `session-handoff.md` whenever the current objective, completed work, important files, verification evidence, or recommended next step changes.
- progress.md must reflect the current active feature and latest completed work.
- session-handoff.md must leave the next Codex session with a concrete startup path.
