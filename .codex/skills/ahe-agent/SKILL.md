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
  5. Ask the user the following exact prompt:
     ```text
     Is your language Python?

     1. Yes

     2. No

     3. Custom input
     ```
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

If a user answer needs clarification or a more detailed description, use this exact prompt:

Please choose one option:

1. Yes

2. No

3. Custom input

Enter 1, 2, or type your own answer:

