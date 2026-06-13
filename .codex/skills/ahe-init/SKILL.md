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
- Execute the following four steps sequentially, calling each subprocess and updating the progress status (`current_step` in `.ahe/process_status.json`):
  1. call "ahe-agent" (status: "ahe-agent")
  2. call "ahe-spec" (status: "ahe-spec")
  3. call "ahe-copy" (status: "ahe-copy")
  4. call "ahe-update" (status: "ahe-update")

### Harness Generation

- Create or refresh `AGENTS.md`.
- Create `.ahe/process_status.json` and update it at each step to indicate the active status from the four steps sequence.
- Create missing harness files from `.codex/ahe-shared/templates/`.
- Keep the generated files aligned with the installed shared templates.

## Clarification Rule

When required information is missing, follow the `ahe-ask-user` protocol. Ask again recursively using a Codex-supported structured response request, provide 2-3 meaningful mutually exclusive options when possible, and allow custom input when predefined options are not enough.

### User Response Target

- Collect the project purpose and any setup confirmation needed to continue the six-step initialization workflow.

### Questions to Ask

- Ask whether the existing `AGENTS.md` is correct.
- Ask what the purpose of this project is when `AGENTS.md` is missing or incorrect.
- Ask follow-up questions when the purpose or setup choice is still unclear.

### Clarification Criteria

- The answer must be specific enough to update `PROJECT_PURPOSE`.
- The answer must make it clear whether initialization should continue with the current `AGENTS.md` or with a new purpose.
- The answer must resolve any setup choice that blocks the next workflow step.

### Re-ask When

- Ask again when the answer is vague, off-topic, contradictory, or incomplete.
- Ask again when the answer does not identify the project goal, target user, or intended outcome clearly enough to continue initialization.
