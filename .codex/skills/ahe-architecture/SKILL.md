---
name: ahe-architecture
description: Update docs/achitecture.md with the current architecture direction.
---

# AHE Architecture

Use this skill when the user invokes `$ahe-architecture`.

## Command Workflow: ahe-architecture

- Read `docs/achitecture.md` if it exists.
- Engage in an interactive conversation with the user to clarify and document the architectural design:
  - Ask clarifying questions about technical stack, components, and design decisions.
  - Suggest architectural patterns or drafts in chat and ask for user feedback.
  - Recursively refine the details based on user input until they are fully satisfied.
- Once finalized, update `docs/achitecture.md`.
- Keep `PROGRESS.md` and `SESSION-HANDOFF.md` aligned when architecture decisions affect current work.

## Clarification Rule

If a user answer needs clarification or a more detailed description, use this exact prompt:

Please choose one option:

1. Yes

2. No

3. Custom input

Enter 1, 2, or type your own answer:

