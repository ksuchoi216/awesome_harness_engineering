---
name: ahe-harness-checker
description: Internal AHE harness validation and repair protocol for checking artifacts after generation or maintenance.
---

# AHE Harness Checker

This is an internal AHE workflow skill, not a user-facing command.

Do not treat `$ahe-harness-checker` as a user command.
Use it when `ahe-think`, `ahe-harness`, or `ahe-new` decides that generated or maintained harness files must be validated and repaired.

## Purpose

- Validate and repair generated harness artifacts after bootstrap/initialization or harness maintenance work.
- Inspect the following key files:
  `AGENTS.md`, `docs/product.md`, `docs/INSTRUCTIONS.md`, `feature-list.json`, `progress.md`, `session-handoff.md`, `init.sh`, and `status.json`.

## Failure Classes

The checker must detect and classify the following issues:
1. **Missing Required File**: A key harness file is completely absent from the workspace.
2. **Empty Required File**: A key harness file exists but contains zero bytes or only whitespace.
3. **Invalid Tracker JSON**: `feature-list.json` or `status.json` contains malformed JSON or violates the required schema.
4. **Wrong Filename Casing**: A harness file uses an incorrect case (e.g. `PROGRESS.md` instead of `progress.md`, except `AGENTS.md` which must remain uppercase).
5. **Forbidden AGENTS.md Edits**: Edits to `AGENTS.md` have occurred outside the allowed changeable section / `PROJECT_PURPOSE`.
6. **Missing Product Docs**: `docs/product.md` is absent or does not contain valid specification text.
7. **Template/Bootstrap Drift**: Workspace files contradict the intended layout or templates defined by AHE.

## Repair Behavior

- If the detected failure is deterministic and local (e.g., wrong casing, missing template placeholders, local syntax drift), fix the issue directly in the workspace.
- If the issue is ambiguous or requires understanding the user's intent (e.g., missing project purpose, contradictory requirements), escalate the issue by handing off to `ahe-converse` to query the user.
