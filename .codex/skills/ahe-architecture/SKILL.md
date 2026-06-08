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

If a user answer needs clarification or a more detailed description, ask again recursively using a Codex-supported structured response request. Ask a short question, provide 2-3 meaningful mutually exclusive options when possible, and allow custom input when predefined options are not enough.

### User Response Target

- Collect the architecture direction needed to update `docs/achitecture.md`.

### Questions to Ask

- Ask about the technical stack, major components, or system boundaries.
- Ask about important design decisions, interfaces, or data flow when they matter.
- Ask which architectural option is preferred when multiple directions are plausible.

### Clarification Criteria

- The answer must identify the stack, components, or decision direction clearly enough to document the architecture.
- The answer must be concrete enough that the architecture description does not rely on unstated assumptions.

### Re-ask When

- Ask again when the answer is vague, contradictory, or only names a technology without the role it plays.
- Ask again when component responsibilities or the overall direction are still unclear.
