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
- Read existing workspace-root harness files that may be copied from templates, including `PROGRESS.md`, `SESSION-HANDOFF.md`, `feature-list.json`, and `init.sh`.
- Read `.ahe/process_status.json` when it exists.

### Sequential Conversation Flow

- If `AGENTS.md` already exists, ask the user whether the current `AGENTS.md` is right.
- If the current `AGENTS.md` is not right or does not exist, ask for the purpose of this project.
- If `AGENTS.md` does not exist, copy `AGENTS.md` from `.codex/ahe-shared/templates/`.
- Update only the `PROJECT_PURPOSE` portion of `AGENTS.md`.
- Ask whether the project language is Python using a Codex-supported structured response request with meaningful options and custom input.
- If the user answers that the project language is not Python, ask again: "Which language do you use?".
- Find all template files under `.codex/ahe-shared/templates/`.
- Ignore `AGENTS.md` and `PRODUCT.md` when copying template files.
- Before copying a template file into the workspace root, check whether the target file already exists and ask for explicit overwrite confirmation when needed.
- Execute the following three steps sequentially, updating the progress status (`current_step` in `.ahe/process_status.json`):
  1. complete the embedded init setup work (status: "ahe-init")
  2. call "ahe-spec" (status: "ahe-spec")
  3. call "ahe-update" (status: "ahe-update")

### Harness Generation

- Create or refresh `AGENTS.md`.
- Create or refresh missing workspace-root harness files from `.codex/ahe-shared/templates/`, converting markdown filenames to uppercase when needed.
- Create `.ahe/process_status.json` and update it at each step to indicate the active status from the three-step sequence.
- Create missing harness files from `.codex/ahe-shared/templates/`.
- Keep the generated files aligned with the installed shared templates.

## Clarification Rule

When required information is missing, follow the `ahe-conversation` protocol. Ask again recursively using a Codex-supported structured response request, provide 2-3 meaningful mutually exclusive options when possible, and allow custom input when predefined options are not enough.

### User Response Target

- Collect the project purpose, language choice, and overwrite decisions needed to continue initialization safely.

### Questions to Ask

- Ask whether the existing `AGENTS.md` is correct.
- Ask what the purpose of this project is when `AGENTS.md` is missing or incorrect.
- Ask whether the project language is Python and ask which language is used when the answer is no or custom.
- Ask whether template files should be overwritten when target files already exist.
- Ask follow-up questions when the purpose, language, or overwrite choice is still unclear.

### Clarification Criteria

- The answer must be specific enough to update `PROJECT_PURPOSE`.
- The answer must make it clear whether initialization should continue with the current `AGENTS.md` or with a new purpose.
- The answer must clearly identify whether Python guidance applies.
- The answer must make overwrite intent explicit for existing template targets.
- The answer must resolve any setup choice that blocks the next workflow step.

### Re-ask When

- Ask again when the answer is vague, off-topic, contradictory, or incomplete.
- Ask again when the answer does not identify the project goal, target user, or intended outcome clearly enough to continue initialization.
- Ask again when the language answer is ambiguous or does not clearly name the language in use.
- Ask again when the overwrite decision is not explicit.
