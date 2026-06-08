---
name: ahe-constraints
description: Update docs/constraints.md for project-specific implementation constraints.
---

# AHE Constraints

Use this skill when the user invokes `$ahe-constraints`.

## Command Workflow: ahe-constraints

- Read `docs/constraints.md` if it exists.
- Engage in an interactive conversation with the user to clarify and document project constraints:
  - Ask clarifying questions about technical limits, environment constraints, and rules.
  - Draft suggestions for the constraint definitions in chat and ask for user approval.
  - Recursively ask for feedback or additional constraints until the details are clear and approved.
- Once finalized, update `docs/constraints.md`.
- Keep `PROGRESS.md` and `SESSION-HANDOFF.md` aligned when constraints change active work.

## Clarification Rule

If a user answer needs clarification or a more detailed description, ask question recursively to clarify the response, and use this exact prompt:

Question: {question}
Please choose one option:

1. Yes

2. No

3. Custom input

Enter 1, 2, or type your own answer:

