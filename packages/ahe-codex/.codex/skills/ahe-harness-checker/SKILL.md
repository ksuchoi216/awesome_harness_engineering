---
name: ahe-harness-checker
description: Internal AHE harness validation and repair protocol for checking artifacts after generation or maintenance.
---

# AHE Harness Checker

**CRITICAL: This is an internal AHE workflow skill, not a user-facing command.**

Do not treat `$ahe-harness-checker` as a user command.
Use it when `ahe-think`, `ahe-harness`, or `ahe-new` decides that generated or maintained harness files must be validated and repaired.

## Protocol and Purpose

Your primary purpose is to validate and repair generated harness artifacts after bootstrap/initialization or harness maintenance work.
You have explicit authority to inspect the following key files:
- `AGENTS.md`
- `docs/product.md`
- `docs/INSTRUCTIONS.md`
- `feature-list.json`
- `progress.md`
- `session-handoff.md`
- `init.sh`
- `status.json`

## Detectable Failure Classes

You must detect and classify the following issues during your validation check:

1. **Missing Required File**: A key harness file is completely absent from the workspace.
2. **Empty Required File**: A key harness file exists but contains zero bytes or only whitespace.
3. **Invalid Tracker JSON**: `feature-list.json` or `status.json` contains malformed JSON or violates the required schema.
4. **Wrong Filename Casing**: A harness file uses an incorrect case (e.g., `PROGRESS.md` instead of `progress.md`). Note: `AGENTS.md` is the only file that must remain uppercase.
5. **Forbidden AGENTS.md Edits**: Edits to `AGENTS.md` have occurred outside the allowed changeable section / `PROJECT_PURPOSE`.
6. **Missing Product Docs**: `docs/product.md` is absent or does not contain valid specification text.
7. **Template/Bootstrap Drift**: Workspace files contradict the intended layout or templates defined by AHE.

## Repair Behavior

- **Direct Fix**: If the detected failure is deterministic and local (e.g., wrong casing, missing template placeholders, local syntax drift, malformed but fixable JSON), fix the issue directly in the workspace without prompting.
- **Escalation**: If the issue is ambiguous or requires understanding the user's intent (e.g., missing project purpose, contradictory requirements, or major data loss in tracker files), escalate the issue by handing off to `ahe-converse` to query the user for clarification.

## Sequence Completion

Once all detected issues have been either directly fixed or safely escalated, summarize the fixes applied and exit. Do not proceed to other workflow steps on your own.
