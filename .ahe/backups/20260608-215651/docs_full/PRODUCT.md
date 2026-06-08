# AHE Project Specification

## 1. Project Name

AHE

Recommended meaning:

text Agent Harness Engineering 

## 2. Product Definition

AHE is a Codex chat workflow skill.

AHE lets the user type command-like messages inside Codex chat, such as:

text ahe ahe init ahe product ahe check ahe resume ahe clear 

Codex must interpret these messages as AHE workflow commands through the installed AHE skill.

AHE is not primarily a terminal CLI.  
AHE is a conversation-first workflow for creating and maintaining agent-facing project harness files.

The primary goal is to help Codex understand:

- what the project is
- how the project should be developed
- what constraints Codex must follow
- how to verify changes
- what product or feature is currently being built
- how to resume work across future Codex chat sessions

## 3. Primary User Experience

The main user interface is Codex chat.

Example:

text User: ahe init  Codex: AHE init workflow started. First, what is the project name? 

The user should not need to manually run terminal commands during the normal AHE workflow.

AHE should behave like a command-driven conversation system inside Codex.

## 4. Core Scenario

A typical AHE session works like this:

text 1. User opens Codex chat in a workspace. 2. User types `ahe init`. 3. Codex starts the harness engineering workflow. 4. Codex asks focused questions to create `AGENTS.md`. 5. Codex creates or updates supporting workspace files. 6. Codex stores progress in `.ahe/process_status.json`. 7. User leaves the chat before finishing. 8. User later opens Codex chat again. 9. User types `ahe` or `ahe resume`. 10. Codex reads `.ahe/process_status.json`. 11. Codex resumes the workflow from the previous step. 12. When harness engineering is complete, Codex moves to product specification discussion. 13. Codex creates or updates `docs/PRODUCT.md`. 

## 5. Architecture

AHE has three separate layers.

text 1. Installed Codex Skill 2. Workspace Runtime State 3. Generated Harness Files 

These layers must not be mixed.

## 6. Installed Codex Skill

The installed AHE skill lives under:

text .codex/skills/ahe/ 

Recommended structure:

text .codex/   skills/     ahe/       SKILL.md       templates/         AGENTS.md         PRODUCT.md         PROGRESS.md         SESSION-HANDOFF.md         init.sh         feature-list.json       schemas/         process_status.schema.json 

### Responsibility

.codex/skills/ahe/ contains reusable AHE workflow definition files.

It contains:

- SKILL.md
- templates
- schemas
- examples if needed

It must not contain workspace-specific runtime state.

Do not store the following under .codex/skills/ahe/:

text .ahe/process_status.json .ahe/backups/ workspace-specific product status workspace-specific progress state 

## 7. Workspace Runtime State

Workspace-specific AHE state lives under:

text .ahe/ 

Recommended structure:

text .ahe/   process_status.json   backups/ 

### Responsibility

.ahe/ belongs to the current workspace.

It stores the current AHE workflow state, including:

- current command
- current step
- collected answers
- completion status
- generated file status
- inferred project environment
- last updated timestamp

.ahe/process_status.json is not part of the AHE skill package.  
It is runtime state for the current workspace.

## 8. Generated Harness Files

AHE creates and maintains the following files in the workspace:

text AGENTS.md docs/PRODUCT.md PROGRESS.md SESSION-HANDOFF.md init.sh feature-list.json .ahe/process_status.json 

Recommended workspace structure after initialization:

text {workspace}/   AGENTS.md   PROGRESS.md   SESSION-HANDOFF.md   init.sh   feature-list.json   docs/     PRODUCT.md   .ahe/     process_status.json     backups/   .codex/     skills/       ahe/         SKILL.md         templates/         schemas/ 

## 9. File Responsibilities

### 9.1 AGENTS.md

AGENTS.md is the global project instruction file for Codex.

It contains stable, project-level guidance.

AHE should create AGENTS.md through conversation with the user.

Required sections:

text # AGENTS.md  ## Project Name  ## Project Objectives  ## Product Specification  ## Global Constraints  ## Working Rules  ## Default Environment  ## Primary Verification Command  ## Verification Commands  ## File Ownership  ## Handoff Rules  ## Do Not Do 

AGENTS.md should not contain detailed product requirements.  
Detailed product requirements belong in docs/PRODUCT.md.

### 9.2 docs/PRODUCT.md

docs/PRODUCT.md is the current product specification.

It replaces numbered task documents.

There should be one canonical product specification file:

text docs/PRODUCT.md 

It contains the current product goal, requirements, completion criteria, and implementation notes.

Required sections:

text # PRODUCT.md  ## Product Name  ## Product Objective  ## Background  ## Current Goal  ## Requirements  ## Completion Criteria  ## User Workflow  ## Files to Create or Modify  ## Verification Commands  ## Out of Scope  ## Open Questions  ## Notes 

docs/PRODUCT.md is the main product-level working document that Codex should read before implementation.

### 9.3 PROGRESS.md

PROGRESS.md is a human-readable progress log.

Suggested sections:

text # PROGRESS.md  ## Current Status  ## Completed  ## In Progress  ## Blocked  ## Decisions  ## Change Log 

### 9.4 SESSION-HANDOFF.md

SESSION-HANDOFF.md is a compact handoff document for future Codex sessions.

Suggested sections:

text # SESSION-HANDOFF.md  ## Current Product Context  ## Last Completed Work  ## Current Open Questions  ## Important Files  ## Next Recommended Action  ## Verification Status 

### 9.5 init.sh

init.sh is a workspace initialization helper.

For v0.1, the default environment is Python.

The default script should be conservative and non-destructive.

It should detect common Python environment files and print recommended setup commands instead of blindly changing the environment.

It may detect:

text pyproject.toml requirements.txt uv.lock poetry.lock conda.yaml environment.yml 

Default behavior:

text - detect project environment - print recommended setup commands - print default verification commands - avoid destructive changes - avoid installing dependencies without user confirmation 

### 9.6 feature-list.json

feature-list.json is a structured product feature inventory.

Initial template:

json {   "features": [] } 

AHE may update this file when the user defines product features during the ahe product workflow.

### 9.7 .ahe/process_status.json

.ahe/process_status.json stores machine-readable workflow state for the current workspace.

Example:

json {   "version": "0.1.0",   "mode": "codex-chat-workflow",   "current_command": "ahe init",   "current_step": "ask_project_objectives",   "workflow_complete": false,   "environment": {     "language": "python",     "detected_from_workspace": false   },   "project": {     "name": null,     "objectives": null   },   "product": {     "spec_path": "docs/PRODUCT.md",     "exists": false,     "complete": false   },   "files": {     "AGENTS.md": {       "exists": false,       "complete": false     },     "docs/PRODUCT.md": {       "exists": false,       "complete": false     },     "PROGRESS.md": {       "exists": false,       "complete": false     },     "SESSION-HANDOFF.md": {       "exists": false,       "complete": false     },     "init.sh": {       "exists": false,       "complete": false     },     "feature-list.json": {       "exists": false,       "complete": false     }   },   "updated_at": null } 

## 10. Command Model

AHE commands are conversation-level pseudo-commands.

They are typed inside Codex chat.

Supported v0.1 commands:

text ahe ahe init ahe product ahe check ahe resume ahe clear 

These commands should not be executed as shell commands unless the user explicitly asks to run them in the terminal.

## 11. Command Router Rule

When the user message starts with ahe, Codex must treat it as an AHE workflow command.

General routing:

text ahe          -> smart entrypoint ahe init     -> initialize global project harness ahe product  -> create or update docs/PRODUCT.md ahe check    -> validate AHE-managed files ahe resume   -> resume unfinished AHE workflow ahe clear    -> back up AGENTS.md and docs/PRODUCT.md, then ask for a new goal and product spec 

## 11.1 Clarification Prompt Rule

When the user's response needs clarification or a more detailed description, Codex should ask with this exact prompt:

text Please choose one option:  1. Yes  2. No  3. Custom input  Enter 1, 2, or type your own answer: 

If the user enters `1`, Codex should treat the answer as yes.  
If the user enters `2`, Codex should treat the answer as no.  
If the user enters `3` or custom text, Codex should treat that text as the clarification input and continue the active AHE workflow.

## 12. Smart Entrypoint: ahe

When the user types:

text ahe 

Codex should:

text 1. Inspect `.ahe/process_status.json`. 2. If an unfinished workflow exists, resume it. 3. If AHE is initialized, show current status and recommended next action. 4. If AHE is not initialized, recommend `ahe init`. 

ahe is a smart entrypoint.

It should behave like ahe resume when there is unfinished workflow state.

## 13. Command: ahe init

### Purpose

ahe init starts the global harness engineering workflow.

The main file created through conversation is:

text AGENTS.md 

Supporting files are created or updated from workspace-aware defaults.

### Behavior

When the user types:

text ahe init 

Codex should:

text 1. Inspect the current workspace. 2. Check whether `.ahe/process_status.json` exists. 3. If an unfinished workflow exists, resume it instead of restarting. 4. Infer project language and environment where possible. 5. If the environment is unclear, default to Python. 6. Start a focused conversation to complete `AGENTS.md`. 7. Ask one question at a time. 8. Save progress to `.ahe/process_status.json` after each answer. 9. Generate or update supporting files. 10. Run the AHE check workflow. 11. When global harness is complete, move to product specification discussion. 

### Required User Inputs for AGENTS.md

AHE should ask the user to complete the following:

text Project name Project objectives Global constraints Working rules Primary verification command Additional verification commands Do-not-do list 

The product specification reference should point to:

text docs/PRODUCT.md 

If docs/PRODUCT.md does not exist yet, AGENTS.md should say:

text Product specification has not been defined yet. Run `ahe product` to create `docs/PRODUCT.md`. 

### Files Generated or Updated by ahe init

text AGENTS.md PROGRESS.md SESSION-HANDOFF.md init.sh feature-list.json .ahe/process_status.json 

docs/PRODUCT.md may be created after ahe init completes, through ahe product.

## 14. Command: ahe product

### Purpose

ahe product creates or updates the canonical product specification:

text docs/PRODUCT.md 

This workflow starts after the global harness is complete.

### Behavior

When the user types:

text ahe product 

Codex should:

text 1. Inspect `docs/PRODUCT.md` if it exists. 2. Inspect `.ahe/process_status.json`. 3. Ask what product or feature the user wants to build. 4. Ask one focused question at a time. 5. Create or update `docs/PRODUCT.md`. 6. Update `AGENTS.md` so it references `docs/PRODUCT.md`. 7. Update `PROGRESS.md`. 8. Update `SESSION-HANDOFF.md`. 9. Update `.ahe/process_status.json`. 10. Run `ahe check`. 

### Required Product Fields

text Product name Product objective Background Current goal Requirements Completion criteria User workflow Files to create or modify Verification commands Out of scope Open questions Notes 

### Completion Condition

The product workflow is complete when:

text docs/PRODUCT.md exists docs/PRODUCT.md has required sections required product fields are filled AGENTS.md references docs/PRODUCT.md ahe check reports no missing product fields 

## 15. Command: ahe check

### Purpose

ahe check validates AHE-managed files and reports missing or inconsistent parts.

### Checks

Codex should check:

text Required files exist Required sections exist Required fields are filled Filename casing is correct AGENTS.md references docs/PRODUCT.md .ahe/process_status.json matches the actual workspace state init.sh exists and is executable or clearly marked as a script feature-list.json is valid JSON 

### Required Files

text AGENTS.md docs/PRODUCT.md PROGRESS.md SESSION-HANDOFF.md init.sh feature-list.json .ahe/process_status.json 

### Example Output

text AHE Check  [x] AGENTS.md     - [x] Project name     - [x] Project objectives     - [x] Product specification reference     - [x] Global constraints     - [x] Verification commands  [x] docs/PRODUCT.md     - [x] Product objective     - [x] Requirements     - [x] Completion criteria  [x] PROGRESS.md [x] SESSION-HANDOFF.md [x] init.sh [x] feature-list.json [x] .ahe/process_status.json  Result: AHE harness is complete. 

If something is missing:

text AHE Check  [x] AGENTS.md [ ] docs/PRODUCT.md  Issue: `docs/PRODUCT.md` does not exist.  Recommended next action: Run `ahe product`. 

## 16. Command: ahe resume

### Purpose

ahe resume resumes an unfinished AHE workflow.

### Behavior

When the user types:

text ahe resume 

Codex should:

text 1. Read `.ahe/process_status.json`. 2. Identify the previous `current_command`. 3. Identify the previous `current_step`. 4. Summarize already collected fields. 5. Ask the next missing question. 

If no unfinished workflow exists:

text 1. Run a lightweight AHE status check. 2. Recommend the next useful command. 

Example:

text No unfinished AHE workflow found.  Current status: [x] AGENTS.md [ ] docs/PRODUCT.md  Recommended next action: Run `ahe product`. 

## 16.1 Command: ahe clear

### Purpose

ahe clear starts a new product direction while preserving the current global instructions and product specification.

### Behavior

When the user types:

text ahe clear 

Codex should:

text 1. Create a timestamped backup directory under `.ahe/backups/`. 2. Copy `docs/PRODUCT.md` to the backup directory, preserving the relative path. 3. Copy `AGENTS.md` to the backup directory, preserving the relative path. 4. Update `.ahe/process_status.json` with `current_command` set to `ahe clear`, `workflow_complete` set to `false`, and `current_step` set to `ask_new_goal`. 5. Ask one focused question: what is the new goal? 6. After the user answers, save the new goal and ask for the new `docs/PRODUCT.md` content or product specification inputs. 7. Do not overwrite `docs/PRODUCT.md` or `AGENTS.md` until the new goal and new product specification are collected. 8. Update `PROGRESS.md` and `SESSION-HANDOFF.md` with the backup location and clear workflow state. 9. Run `ahe check` after the new product specification is written. 

### Required Backup Files

text AGENTS.md docs/PRODUCT.md 

## 17. Default Environment

The default environment is Python.

If AHE cannot confidently infer the project language, it should assume Python.

AHE may infer Python from files such as:

text pyproject.toml requirements.txt setup.py setup.cfg uv.lock poetry.lock Pipfile conda.yaml environment.yml src/ tests/ 

If another language is clearly detected, AHE may adapt commands and templates accordingly.

Examples:

text package.json       -> JavaScript or TypeScript go.mod             -> Go Cargo.toml         -> Rust pom.xml            -> Java build.gradle       -> Java or Kotlin 

## 18. Default Python Verification Commands

For Python projects, use the following default verification commands unless the workspace indicates otherwise:

markdown ## Verification Commands  - Tests: `pytest tests/ -x` - Type check: `mypy src/ --strict` - Lint: `ruff check src/` - Full verification: `make check` if a `Makefile` exists; otherwise run all commands above manually. 

If the workspace has different commands, AHE should ask the user whether to use the detected commands or the default Python commands.

## 19. Default Python init.sh

For Python projects, generate a conservative init.sh.

Default template:

bash #!/usr/bin/env bash set -euo pipefail  echo "AHE workspace initialization" echo "Detected or default environment: Python" echo  if [ -f "pyproject.toml" ]; then   echo "Detected pyproject.toml" fi  if [ -f "requirements.txt" ]; then   echo "Detected requirements.txt"   echo "Recommended install command:"   echo "  pip install -r requirements.txt" fi  if [ -f "uv.lock" ]; then   echo "Detected uv.lock"   echo "Recommended install command:"   echo "  uv sync" fi  if [ -f "poetry.lock" ]; then   echo "Detected poetry.lock"   echo "Recommended install command:"   echo "  poetry install" fi  if [ -f "environment.yml" ]; then   echo "Detected environment.yml"   echo "Recommended install command:"   echo "  conda env update -f environment.yml" fi  if [ -f "conda.yaml" ]; then   echo "Detected conda.yaml"   echo "Recommended install command:"   echo "  conda env update -f conda.yaml" fi  echo echo "Recommended verification commands:" echo "  pytest tests/ -x" echo "  mypy src/ --strict" echo "  ruff check src/"  if [ -f "Makefile" ]; then   echo "  make check" fi 

This script should not install dependencies automatically by default.  
It should print safe, inspectable setup recommendations.

## 20. Safety Rules

AHE must be conservative.

Rules:

text Do not silently overwrite existing files. Create backups under `.ahe/backups/` before rewriting existing AHE-managed files. Ask one focused question at a time. Use uppercase filenames for root harness documents. Keep skill definition and workspace runtime state separate. Do not use hooks in v0.1. Do not perform automatic background actions. Do not execute shell commands unless the user explicitly asks. Do not treat `ahe init` as a shell command by default. 

## 21. Filename Rules

Generated root harness markdown files must use uppercase names:

text AGENTS.md PROGRESS.md SESSION-HANDOFF.md 

The product specification path must be:

text docs/PRODUCT.md 

Do not generate:

text agents.md progress.md session-handoff.md docs/product.md 

## 22. No Hooks in v0.1

AHE v0.1 does not use hooks.

Excluded:

text pre-task hooks post-task hooks automatic session-end hooks automatic file modification hooks automatic product transition hooks 

Reason:

AHE v0.1 should only act when the user explicitly types an AHE command.

## 23. v0.1 Scope

### Include

text Codex chat workflow AHE SKILL.md Command router ahe ahe init ahe product ahe check ahe resume ahe clear AGENTS.md generation docs/PRODUCT.md generation PROGRESS.md generation SESSION-HANDOFF.md generation init.sh generation feature-list.json generation .ahe/process_status.json runtime state Python default environment npm installer with local development flow `npx --yes --package=file:. ahe install` and deployment target `npx ahe install` No hooks No automatic background behavior 

### Exclude

text Hooks Subagents Automatic session-end behavior Automatic commits Remote registry GUI Multiple numbered work documents 

## 23.1 Installer Distribution

AHE also ships as an npm package so a workspace can install the Codex skill files with:

text npx ahe install

The installer is intentionally small.

Before deployment, after cloning the repository, local development should use:

text npx --yes --package=file:. ahe install

If the install target is a different workspace than the cloned package directory, local development should use:

text npx --yes --package=/path/to/awesome_harness_engineering ahe install

Required behavior:

text 1. Create `.codex/skills/ahe/` if missing. 2. Copy the packaged `SKILL.md`, templates, and schemas into `.codex/skills/ahe/`. 3. Do not create workspace runtime files under `.ahe/`. 4. Do not create `AGENTS.md` or other root harness files. 5. Fail instead of silently overwriting an existing install unless the user explicitly passes an overwrite option. 

## 24. Completion Definition

AHE harness engineering is complete when:

text AGENTS.md exists and has required global sections docs/PRODUCT.md exists and has required product sections PROGRESS.md exists SESSION-HANDOFF.md exists init.sh exists feature-list.json exists and is valid JSON .ahe/process_status.json exists AGENTS.md references docs/PRODUCT.md ahe check reports no missing required fields 

## 25. Final Design Principle

AHE is not a project generator.

AHE is a Codex workflow harness generator.

It does not build the user's application directly.  
It prepares the workspace so Codex can understand the project, preserve context across sessions, and work from a clear product specification.
