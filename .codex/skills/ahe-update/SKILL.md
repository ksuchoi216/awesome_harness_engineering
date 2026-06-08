---
name: ahe-update
description: Synchronize feature-list.json, PROGRESS.md, and SESSION-HANDOFF.md with current work.
---

# AHE Update

Use this skill when the user invokes `$ahe-update`.

## Command Workflow: ahe-update

- Read `feature-list.json`.
- Read `PROGRESS.md` if it exists.
- Read `SESSION-HANDOFF.md`.
- Read `docs/todo.md` when it exists.
- Apply the queued `docs/todo.md` content to `docs/PRODUCT.md`. if `docs/PRODUCT.md` does not exist, create it.
- Remove the applied content from `docs/todo.md` because that todo content was already applied in `docs/PRODUCT.md`.
- Update `feature-list.json`.
- Update `PROGRESS.md`.
- Update `SESSION-HANDOFF.md`.

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
