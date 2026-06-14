---
name: ahe-conversation
description: Internal AHE protocol for recursive clarification, conversation state, and resume-aware workflow guidance.
---

# AHE Conversation

This is an internal AHE protocol skill, not a user-facing command.

Do not treat `$ahe-conversation` as a user command.
Use it only when another AHE workflow skill needs more conversation before it can
continue safely.
Use it after `ahe-thinking` identifies a missing decision or missing `Why`,
`What`, or `How`.

## When to Converse

Start or continue an AHE conversation when the missing answer materially changes
one of these:

- Project purpose or target user.
- Product behavior, scope, success criteria, or out-of-scope boundaries.
- Implementation constraints, architecture direction, or verification commands.
- Harness file ownership, overwrite behavior, or reset behavior.
- `.ahe/process_status.json`, `PROGRESS.md`, or `SESSION-HANDOFF.md` state.
- The next workflow step when several valid paths are possible.
- The missing `Why`, `What`, or `How` for the current `project`, `feature`, or
  `sub-feature`.

If the missing detail can be inferred safely from existing files, infer
conservatively and record the assumption in the active workflow artifact.

## Conversation Protocol

- Inspect relevant existing files before asking.
- Let `ahe-thinking` judge what is missing before you ask.
- Explain the decision point briefly when context helps the user answer.
- Ask exactly one question at a time.
- Use a Codex-supported structured response request when meaningful options exist.
- Provide 2-3 mutually exclusive options when useful, and allow custom input when
  predefined options are not enough.
- Keep each question specific to the active AHE workflow.
- Think through what the answer will unlock before asking.
- Ask again when the answer is vague, off-topic, contradictory, or incomplete
  according to the calling skill's clarification criteria.
- Continue until the calling workflow has enough information to act.
- Do not expand the scope of questioning beyond the missing detail that
  `ahe-thinking` identified.

## State Persistence

Before pausing for user input, update `.ahe/process_status.json` when it exists
or when the active workflow uses it:

- Set the active command or skill name.
- Set `workflow_complete` to `false`.
- Set `current_step` to the pending question, decision point, or missing field.
- Refresh `updated_at`.
- Preserve already collected project and product data.

Update `PROGRESS.md` and `SESSION-HANDOFF.md` when the pending conversation
changes the active workflow state, blocks completion, or affects the next
session's startup path.

## Resume Protocol

When resuming after the user answers:

- Read `.ahe/process_status.json` and the relevant workflow artifacts.
- Summarize the already collected data briefly.
- Identify the missing field or decision that is still blocking progress.
- Ask the next focused question, or continue the calling workflow when the
  answer satisfies its clarification criteria.
