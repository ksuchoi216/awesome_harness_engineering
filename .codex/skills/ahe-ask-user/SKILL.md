---
name: ahe-ask-user
description: Internal AHE protocol. Use when an AHE workflow skill needs to ask the user for missing project, product, constraint, architecture, verification, or harness information before continuing.
---

# AHE Ask User

This is an internal AHE protocol skill, not a user-facing command.

Do not treat `$ahe-ask-user` as a user command. Do not list it in `$ahe-help`. Use it only when another AHE workflow skill is blocked by missing user input.

## When to Ask

Ask the user only when the missing answer materially changes one of these:

- Project purpose or target user.
- Product behavior, scope, success criteria, or out-of-scope boundaries.
- Implementation constraints, architecture direction, or verification commands.
- Harness file ownership, overwrite behavior, or reset behavior.
- `.ahe/process_status.json`, `PROGRESS.md`, or `SESSION-HANDOFF.md` state.

If the missing detail can be inferred safely from existing files, infer conservatively and record the assumption in the active workflow artifact.

## Question Protocol

- Inspect relevant existing files before asking.
- Ask exactly one question at a time.
- Use a Codex-supported structured response request when meaningful options exist.
- Provide 2-3 mutually exclusive options when useful, and allow custom input when predefined options are not enough.
- Keep the question short and specific to the active AHE workflow.
- Ask again when the answer is vague, off-topic, contradictory, or incomplete according to the calling skill's clarification criteria.

## State Persistence

Before pausing for user input, update `.ahe/process_status.json` when it exists or when the active workflow uses it:

- Set the active command or skill name.
- Set `workflow_complete` to `false`.
- Set `current_step` to the pending question or missing field.
- Refresh `updated_at`.
- Preserve already collected project and product data.

Update `PROGRESS.md` and `SESSION-HANDOFF.md` when the pending question changes the active workflow state, blocks completion, or affects the next session's startup path.

## Resume Protocol

When resuming after the user answers:

- Read `.ahe/process_status.json` and the relevant workflow artifacts.
- Summarize the already collected data briefly.
- Identify the missing field that is still blocking progress.
- Ask the next focused question, or continue the calling workflow when the answer satisfies its clarification criteria.
