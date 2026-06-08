---
name: ahe-init
description: Initialize AHE in the current workspace and create the base harness files.
---

# AHE Init

Use this skill when the user invokes `$ahe-init`.

## Command Workflow: ahe-init

### Workspace Inspection

- Read `AGENTS.md` if it already exists.
- Read `docs/PRODUCT.md`, `docs/constraints.md`, and `docs/achitecture.md` when they exist.
- Read `.ahe/process_status.json` when it exists.

### Sequential Conversation Flow

- If `AGENTS.md` already exists, ask the user whether the current `AGENTS.md` is right.
- If the current `AGENTS.md` is not right or does not exist, ask for the purpose of this project.
- Update only the `PROJECT_PURPOSE` portion of `AGENTS.md`.
- Execute the following six steps sequentially, calling each subprocess and updating the progress status (`current_step` in `.ahe/process_status.json`):
  1. call "ahe-agents" (status: "ahe-agents")
  2. call "ahe-product" (status: "ahe-product")
  3. call "ahe-architecture" (status: "ahe-architecture")
  4. call "ahe-constraints" (status: "ahe-constraints")
  5. call "ahe-copy" (status: "ahe-copy")
  6. call "ahe-update" (status: "ahe-update")

### Harness Generation

- Create or refresh `AGENTS.md`.
- Create `.ahe/process_status.json` and update it at each step to indicate the active status from the six steps sequence.
- Create missing harness files from `.codex/ahe-shared/templates/`.
- Keep the generated files aligned with the installed shared templates.

## Clarification Rule

If a user answer needs clarification or a more detailed description, use this exact prompt:

Please choose one option:

1. Yes

2. No

3. Custom input

Enter 1, 2, or type your own answer:
