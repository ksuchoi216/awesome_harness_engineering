---
name: ahe
description: Agent Harness Engineering - A conversation-first workflow for creating and maintaining agent-facing project harness files.
---

# AHE

AHE is a Codex chat workflow skill for creating and maintaining project harness files.

## Command Router Rule

When the user message starts with one of the commands below, Codex must treat it as an AHE workflow command instead of a shell command.

General routing:

- `$ahe-init` -> initialize harness engineering
- `$ahe-agent` -> modify the project purpose in `AGENTS.md`
- `$ahe-product` -> modify `docs/PRODUCT.md`
- `$ahe-constraints` -> modify `docs/constraints.md`
- `$ahe-architecture` -> modify `docs/achitecture.md`
- `$ahe-update` -> update `feature-list.json`, `PROGRESS.md`, and `SESSION-HANDOFF.md`
- `$ahe-clear` -> back up and remove the current product-tracking files

## Command Intent

- `$ahe-init`: initialize or refresh the harness. If `AGENTS.md` already exists, ask the user whether it is correct first.
- `$ahe-agent`: modify only the project purpose in `AGENTS.md`.
- `$ahe-product`: modify `docs/PRODUCT.md`.
- `$ahe-constraints`: modify `docs/constraints.md`.
- `$ahe-architecture`: modify `docs/achitecture.md`.
- `$ahe-update`: update `feature-list.json`, `PROGRESS.md`, and `SESSION-HANDOFF.md`.
- `$ahe-clear`: create backups and then remove the previous `docs/PRODUCT.md`, `PROGRESS.md`, `SESSION-HANDOFF.md`, and `feature-list.json`.

## Managed Files

AHE manages these workspace files:

- `AGENTS.md`
- `docs/PRODUCT.md`
- `docs/constraints.md`
- `docs/achitecture.md`
- `PROGRESS.md`
- `SESSION-HANDOFF.md`
- `init.sh`
- `feature-list.json`
- `.ahe/process_status.json`

Templates live under `templates/`. Schemas live under `schemas/`. Workspace runtime state must stay under `.ahe/`.

## Clarification Prompt Rule

When the user's response needs clarification or a more detailed description, Codex must ask for clarification using this exact format:

```text
Please choose one option:

1. Yes

2. No

3. Custom input

Enter 1, 2, or type your own answer:
```

If the user enters `1`, treat the answer as yes. If the user enters `2`, treat the answer as no. If the user enters `3` or any custom text, treat that text as the user's clarification input and continue the active AHE workflow.

## Command Workflow: ahe-init

When executing the `$ahe-init` command, Codex must follow these instructions step-by-step:

1. **Workspace Inspection**:
   - Inspect `AGENTS.md` and `.ahe/process_status.json`.
   - If `AGENTS.md` already exists, ask the user whether the current `AGENTS.md` is right.
   - If the user says the current `AGENTS.md` is not right, ask for the purpose of this project.
   - If `AGENTS.md` does not exist, ask for the purpose of this project immediately.
   - Update `.ahe/process_status.json` for the init workflow: set `current_command` to `$ahe-init`, set `workflow_complete` to `false`, and set `current_step` to `ask_agents_confirmation` or `ask_project_purpose` as appropriate.

2. **Sequential Conversation Flow**:
   - Ask exactly ONE focused question at a time and wait for the user's response.
   - If `AGENTS.md` exists, first ask whether it is right.
   - If the user says no, ask for the purpose of this project.
   - Save progress to `.ahe/process_status.json` after every answered question.

3. **Harness Generation**:
   - Create or update `AGENTS.md` only after the project purpose is clear.
   - Replace only the `PROJECT_PURPOSE` portion of `AGENTS.md`.
   - Keep the rest of the `AGENTS.md` file format unchanged.
   - Create or update `.ahe/process_status.json` so `current_command`, `current_step`, and `workflow_complete` match whether the init workflow is complete.

## Command Workflow: ahe-agent

When executing the `$ahe-agent` command, Codex must follow these instructions step-by-step:

1. **Agent Inspection**:
   - Inspect `AGENTS.md` and `.ahe/process_status.json`.
   - Update `.ahe/process_status.json` for the agent workflow: set `current_command` to `$ahe-agent`, set `workflow_complete` to `false`, and set `current_step` to `ask_project_purpose`.

2. **Agent Conversation Flow**:
   - Ask exactly ONE focused question at a time and wait for the user's response.
   - Ask for the new or revised project purpose.
   - Save progress after every answer.

3. **Agent Completion**:
   - Modify only the `PROJECT_PURPOSE` portion of `AGENTS.md`.
   - Do not rewrite unrelated `AGENTS.md` sections.
   - Update `.ahe/process_status.json` so `current_command`, `current_step`, and `workflow_complete` match whether the agent workflow is complete.

## Command Workflow: ahe-product

When executing the `$ahe-product` command, Codex must follow these instructions step-by-step:

1. **Product Inspection**:
   - Inspect `docs/PRODUCT.md` and `.ahe/process_status.json`.
   - Update `.ahe/process_status.json` for the product workflow: set `current_command` to `$ahe-product`, set `workflow_complete` to `false`, and set `current_step` to `ask_product_specification`.

2. **Sequential Product Conversation Flow**:
   - Ask exactly ONE focused question at a time and wait for the user's response.
   - Ask for the product specification inputs needed to update `docs/PRODUCT.md`.
   - Ask recursively for more detail whenever the product specification is incomplete or unclear.
   - Save progress after every answer.

3. **Product Completion**:
   - Create or update `docs/PRODUCT.md`.
   - If the product specification is clear, finish writing `docs/PRODUCT.md`.
   - Update `.ahe/process_status.json` so `current_command`, `current_step`, and `workflow_complete` match whether the product workflow is complete.

## Command Workflow: ahe-constraints

When executing the `$ahe-constraints` command, Codex must follow these instructions step-by-step:

1. **Constraints Inspection**:
   - Inspect `docs/constraints.md` and `.ahe/process_status.json`.
   - Update `.ahe/process_status.json` for the constraints workflow: set `current_command` to `$ahe-constraints`, set `workflow_complete` to `false`, and set `current_step` to `ask_constraints`.

2. **Constraints Conversation Flow**:
   - Ask exactly ONE focused question at a time and wait for the user's response.
   - Ask for the constraints that must be written or updated in `docs/constraints.md`.
   - Ask recursively for more detail whenever the constraints are incomplete or unclear.
   - Save progress after every answer.

3. **Constraints Completion**:
   - Create or update `docs/constraints.md`.
   - If the constraints are clear, finish writing `docs/constraints.md`.
   - Update `.ahe/process_status.json` so `current_command`, `current_step`, and `workflow_complete` match whether the constraints workflow is complete.

## Command Workflow: ahe-architecture

When executing the `$ahe-architecture` command, Codex must follow these instructions step-by-step:

1. **Architecture Inspection**:
   - Inspect `docs/achitecture.md` and `.ahe/process_status.json`.
   - Update `.ahe/process_status.json` for the architecture workflow: set `current_command` to `$ahe-architecture`, set `workflow_complete` to `false`, and set `current_step` to `ask_architecture`.

2. **Architecture Conversation Flow**:
   - Ask exactly ONE focused question at a time and wait for the user's response.
   - Ask for the architecture description that must be written or updated in `docs/achitecture.md`.
   - Ask recursively for more detail whenever the architecture description is incomplete or unclear.
   - Save progress after every answer.

3. **Architecture Completion**:
   - Create or update `docs/achitecture.md`.
   - If the architecture description is clear, finish writing `docs/achitecture.md`.
   - Update `.ahe/process_status.json` so `current_command`, `current_step`, and `workflow_complete` match whether the architecture workflow is complete.

## Command Workflow: ahe-update

When executing the `$ahe-update` command, Codex must follow these instructions step-by-step:

1. **Update Inspection**:
   - Inspect `feature-list.json`, `PROGRESS.md`, `SESSION-HANDOFF.md`, and `.ahe/process_status.json`.
   - Update `.ahe/process_status.json` for the update workflow: set `current_command` to `$ahe-update`, set `workflow_complete` to `false`, and set `current_step` to `ask_update_summary`.

2. **Sequential Update Conversation Flow**:
   - Ask exactly ONE focused question at a time and wait for the user's response.
   - First ask what changed and which feature entries need updating.
   - Then ask what verification evidence, blockers, or status changes should be recorded.
   - Then ask what next recommended action should be written into `SESSION-HANDOFF.md`.
   - Save progress after every answer.

3. **Update Completion**:
   - Update `feature-list.json`.
   - Update `PROGRESS.md`.
   - Update `SESSION-HANDOFF.md`.
   - Update `.ahe/process_status.json` so `current_command`, `current_step`, and `workflow_complete` match whether the update workflow is complete.

## Command Workflow: ahe-clear

When executing the `$ahe-clear` command, Codex must follow these instructions step-by-step:

1. **Clear Preparation**:
   - Inspect `docs/PRODUCT.md`, `PROGRESS.md`, `SESSION-HANDOFF.md`, `feature-list.json`, and `.ahe/process_status.json`.
   - If `.ahe/backups/` does not exist, create it.
   - Create a timestamped backup directory under `.ahe/backups/`.
   - Copy the current `docs/PRODUCT.md` into the backup directory, preserving the `docs/PRODUCT.md` relative path.
   - Copy the current `PROGRESS.md` into the backup directory, preserving the `PROGRESS.md` relative path.
   - Copy the current `SESSION-HANDOFF.md` into the backup directory, preserving the `SESSION-HANDOFF.md` relative path.
   - Copy the current `feature-list.json` into the backup directory, preserving the `feature-list.json` relative path.

2. **Clear Removal**:
   - Remove the previous `docs/PRODUCT.md`.
   - Remove the previous `PROGRESS.md`.
   - Remove the previous `SESSION-HANDOFF.md`.
   - Remove the previous `feature-list.json`.
   - Update `.ahe/process_status.json` so `current_command` is `$ahe-clear`, `current_step` is `null`, and `workflow_complete` is `true`.

## Session Tracking and Handoff Sync

These rules apply across every AHE workflow.

1. **Tracking Update Rules**:
   - Update `.ahe/process_status.json` at workflow start.
   - Update `.ahe/process_status.json` after every answered question.
   - Refresh `updated_at` every time workflow state changes.
   - Keep `current_command`, `current_step`, and `workflow_complete` aligned with the active workflow state.
   - Keep the `files` status map aligned with the actual workspace files.

2. **Progress and Handoff Content Requirements**:
   - Update `PROGRESS.md` whenever the active feature, workflow status, blockers, or verification state changes.
   - Update `SESSION-HANDOFF.md` whenever the current objective, completed work, important files, verification evidence, or recommended next step changes.
   - PROGRESS.md must reflect the current active feature and latest completed work.
   - SESSION-HANDOFF.md must leave the next Codex session with a concrete startup path.
