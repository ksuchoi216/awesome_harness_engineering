---
name: ahe
description: Agent Harness Engineering - A conversation-first workflow for creating and maintaining agent-facing project harness files.
---

# AHE

AHE is a Codex chat workflow skill for creating and maintaining project harness files.

## Command Router Rule

When the user message starts with `ahe`, Codex must treat it as an AHE workflow command instead of a shell command.

General routing:

- `ahe` -> smart entrypoint
- `ahe init` -> initialize global project harness
- `ahe product` -> create or update docs/PRODUCT.md
- `ahe check` -> validate AHE-managed files
- `ahe resume` -> resume unfinished AHE workflow

## Command Intent

- `ahe`: inspect `.ahe/process_status.json`, resume unfinished work when present, otherwise show current status and the next recommended action.
- `ahe init`: ask one focused question at a time, create or update `AGENTS.md`, and initialize the workspace harness files.
- `ahe product`: create or update `docs/PRODUCT.md` and sync the tracking artifacts.
- `ahe check`: validate required files, required sections, filename casing, and process status consistency.
- `ahe resume`: continue the most recent unfinished AHE workflow from `.ahe/process_status.json`.

## Managed Files

AHE manages these workspace files:

- `AGENTS.md`
- `docs/PRODUCT.md`
- `PROGRESS.md`
- `SESSION-HANDOFF.md`
- `init.sh`
- `feature-list.json`
- `.ahe/process_status.json`

Templates live under `templates/`. Schemas live under `schemas/`. Workspace runtime state must stay under `.ahe/`.

## Command Workflow: ahe init

When executing the `ahe init` command, Codex must follow these instructions step-by-step:

1. **Workspace Inspection**:
   - Inspect the current workspace to check if `.ahe/process_status.json` exists.
   - If `.ahe/process_status.json` exists and `workflow_complete` is `false`, resume the unfinished workflow instead of restarting. Follow the **Resume Workflow** instructions.
   - If not, inspect workspace files to infer the programming language (e.g., Python from `pyproject.toml`, `requirements.txt`, `setup.py`, `uv.lock`, `poetry.lock`, `conda.yaml`, `environment.yml`; JavaScript/TypeScript from `package.json`; Go from `go.mod`; Rust from `Cargo.toml`). If language is ambiguous, default to `python`.
   - Create the initial `.ahe/process_status.json` conforming to `.codex/skills/ahe/schemas/process_status.schema.json`, set `current_command` to `ahe init`, `workflow_complete` to `false`, `environment.language` to the inferred/default language, and `current_step` to `ask_project_name`.

2. **Sequential Conversation Flow**:
   Ask the user for each piece of information needed to build `AGENTS.md`. Ask exactly ONE question at a time and wait for the user's response. Save progress to `.ahe/process_status.json` after the user answers each question:
   - **Step 1: Project Name**: Ask the user for the name of the project. (Store in `project.name`)
   - **Step 2: Project Objectives**: Ask the user for the project objectives/goals. (Store list in `project.objectives`)
   - **Step 3: Global Constraints**: Ask the user for any global constraints or rules.
   - **Step 4: Working Rules**: Ask the user for any specific working rules.
   - **Step 5: Primary Verification Command**: Ask the user for the primary command to run tests/verify code.
   - **Step 6: Additional Verification Commands**: Ask the user for other verification commands (linting, type checking).
   - **Step 7: Do-not-do list**: Ask the user what actions or modifications must be avoided.

3. **Harness Generation**:
   Once all fields are collected, perform these file modifications:
   - If any AHE-managed file (`AGENTS.md`, `PROGRESS.md`, `SESSION-HANDOFF.md`, `init.sh`, `feature-list.json`) already exists in the workspace, create a backup of it under `.ahe/backups/` before rewriting it.
   - Create or update `AGENTS.md` in the root workspace using the `templates/agents.md` template.
     - Replace `{{AGENT_FILE_NAME}}` with `AGENTS.md`.
     - Replace `{{PROJECT_PURPOSE}}` with the collected project name, objectives, global constraints, working rules, verification commands, and do-not-do list.
     - Include a Product Specification reference pointing to `docs/PRODUCT.md`. Write: "Product specification has not been defined yet. Run `ahe product` to create `docs/PRODUCT.md`."
   - Create or update `init.sh` in the root workspace based on `templates/init.sh`, customized for the project's language environment. The script must be conservative and non-destructive.
   - Create `PROGRESS.md` using `templates/progress.md`.
   - Create `SESSION-HANDOFF.md` using `templates/session-handoff.md`.
   - Create `feature-list.json` using `templates/feature-list.json`.
   - Mark the file statuses inside `.ahe/process_status.json` under `files` as `exists: true` and `complete: true`.
   - Update `.ahe/process_status.json`: set `current_command` to `null`, `current_step` to `null`, `workflow_complete` to `true`, and `updated_at` to the current ISO timestamp.
   - Run the validation check (equivalent to `ahe check`) and display the results to the user. Prompt them that harness initialization is complete and they should run `ahe product` next.

