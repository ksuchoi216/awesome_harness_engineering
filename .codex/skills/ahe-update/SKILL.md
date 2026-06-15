---
name: ahe-update
description: Internal AHE workflow for synchronizing tracked work and handoff artifacts.
---

# AHE Update

This is an internal AHE workflow skill, not a user-facing command.

Do not treat `$ahe-update` as a user command.
Use it after `ahe-thinking` decides that tracked harness work should be synchronized.

## Command Workflow: ahe-update

- Read `feature-list.json`.
- Read `PROGRESS.md` if it exists.
- Read `SESSION-HANDOFF.md`.
- Read `docs/todo.md` when it exists.
- If the user is adding new work, clarify the todo item, append it under the last `## TODO` section in `docs/todo.md`, and create that section when it does not exist.
- Apply the queued `docs/todo.md` content to `docs/PRODUCT.md`. If `docs/PRODUCT.md` does not exist, create it.
- Remove the applied content from `docs/todo.md` because that todo content was already applied in `docs/PRODUCT.md`.
- Update `feature-list.json` to derive the specific feature items from the updated `docs/PRODUCT.md`.
- Update `PROGRESS.md`.
- Update `SESSION-HANDOFF.md`.

## Clarification Rule

When the next update step is not clear, follow the `ahe-thinking` protocol first. If `ahe-thinking` finds missing information, follow the `ahe-conversation` protocol. Ask again recursively using a Codex-supported structured response request, provide 2-3 meaningful mutually exclusive options when possible, and allow custom input when predefined options are not enough.

### User Response Target

- Collect either an actionable todo entry to queue or a clear instruction to synchronize the existing queued work.

### Questions to Ask

- Ask what work needs to be done when the user is adding a new todo item.
- Ask which file, feature area, or workflow the todo affects.
- Ask what outcome or completion signal the todo should capture.
- Ask whether the user wants to queue new work, apply queued work, or do both when that is unclear.

### Clarification Criteria

- The answer must describe actionable work, the affected area, and the intended outcome when queuing a todo item.
- The answer must be clear enough to decide whether to queue work, apply queued work, or do both.

### Re-ask When

- Ask again when the answer is too broad, off-topic, or only names a topic without describing the work.
- Ask again when dependencies, affected area, intended outcome, or update action are still unclear.

## Session Tracking and Handoff Sync

### Tracking Update Rules

- Update `.ahe/process_status.json` at workflow start.
- Update `.ahe/process_status.json` after every answered question.
- Refresh `updated_at` every time workflow state changes.
- Keep `current_command`, `current_step`, and `workflow_complete` aligned with the active workflow state.
- Keep the `files` status map aligned with the actual workspace files.

### Progress and Handoff Content Requirements

- Update `PROGRESS.md` whenever the active feature, workflow status, blockers, or verification state changes.
- Update `SESSION-HANDOFF.md` whenever the current objective, completed work, important files, verification evidence, or recommended next step changes.
- PROGRESS.md must reflect the current active feature and latest completed work.
- SESSION-HANDOFF.md must leave the next Codex session with a concrete startup path.
