---
name: ahe-agent
description: Update the project purpose in AGENTS.md without changing the rest of the file.
---

# AHE Agent

Use this skill when the user invokes `$ahe-agent`.

## Command Workflow: ahe-agent

- Check if `AGENTS.md` exists in the workspace.
- If `AGENTS.md` does not exist:
  1. Copy `agents.md` from the template directory `.codex/ahe-shared/templates/` (or `templates/` in the workspace).
  2. Rename it to `AGENTS.md` (uppercase).
  3. Ask what the purpose of this project is to user.
  4. Update the project purpose portion in the new `AGENTS.md`.
  5. Ask whether the project language is Python using a Codex-supported structured response request with meaningful options and custom input.
  - If the user chooses "No" (option 2), ask again: "Which language do you use?" and capture their custom answer.
- If `AGENTS.md` exists in the workspace:
  - Read `AGENTS.md`.
  - Engage in an interactive conversation with the user to refine the project purpose:
    - Ask clarifying questions about the goal, target audience, and core features.
    - Suggest a draft of the new project purpose in the chat and ask for user feedback.
    - Recursively ask for details or adjustments until the user confirms they are satisfied.
  - Modify only the `PROJECT_PURPOSE` portion of `AGENTS.md`. This should be done once finalized.
  - Do not rewrite other sections of `AGENTS.md`.

## Clarification Rule

If a user answer needs clarification or a more detailed description, ask again recursively using a Codex-supported structured response request. Ask a short question, provide 2-3 meaningful mutually exclusive options when possible, and allow custom input when predefined options are not enough.

### User Response Target

- Collect a concrete project purpose and, when needed, the project language.

### Questions to Ask

- Ask what the purpose of this project is.
- Ask follow-up questions about the goal, target audience, or core capability when the purpose is still unclear.
- Ask whether the project language is Python and ask which language is used when the answer is no or custom.

### Clarification Criteria

- The answer must be specific enough to write the `PROJECT_PURPOSE` section in `AGENTS.md`.
- The answer must state what the project is for and what problem or outcome it targets.
- The language answer must clearly identify whether Python guidance applies.

### Re-ask When

- Ask again when the answer is vague, off-topic, or too abstract, such as `code`.
- Ask again when the answer does not identify the user, problem, or intended outcome clearly enough to update `PROJECT_PURPOSE`.
- Ask again when the language answer is ambiguous or does not clearly name the language in use.
