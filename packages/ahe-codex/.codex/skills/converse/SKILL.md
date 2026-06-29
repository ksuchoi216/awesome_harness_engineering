---
name: converse
description: Internal AHE conversation protocol for recursive clarification, conversation state, and resume-aware workflow guidance.
---

# AHE Conversator

This is an internal AHE workflow skill, not a user-facing command.

Do not treat `$converse` as a user command.
Use it after `think` or another AHE agent identifies a missing decision or
missing `Why`, `What`, or `How`.

## When To Converse

- Ask one question at a time.
- Use conversation state when multiple answers are needed across turns.
- Clarify product intent, instructions, next feature, restart scope, or any
  decision that materially changes the workflow.
- If the answer can be derived safely from repo state, do that instead of
  asking.

## Conversation Protocol

- Inspect relevant files before asking.
- Explain the blocked decision briefly.
- Use a Codex-supported structured response request when it helps.
- Ask exactly one focused question at a time.
- Continue recursively until the answer is specific enough to unblock the
  calling workflow.

## State Persistence

- Update `status.json` before pausing for user input.
- Preserve the current command, current_step, workflow_complete, and files map.
- Update `progress.md` and `session-handoff.md` when the pending question
  changes the workflow state.

## Resume Protocol

- Read `status.json` and the relevant workflow artifacts.
- Summarize the current state briefly.
- Ask the next focused question or return control to the caller when the answer
  resolves the missing detail.
