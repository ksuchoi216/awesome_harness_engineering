# AHE MVP Specification

## 1. Project Name

AHE

Recommended meaning:

text Agent Harness Engineering 

## 2. Product Definition

AHE is a Codex chat workflow skill.

AHE lets the user type command-like messages inside Codex chat:

text ahe ahe init ahe agent ahe product ahe check ahe update ahe resume 

Codex must interpret these messages as AHE workflow commands through the installed AHE skill.

AHE is not primarily a terminal CLI.

AHE is a conversation-first workflow for creating and maintaining lightweight project harness files for Codex-driven development.

## 3. MVP Goal

The MVP goal is to create a single Codex skill that can:

text 1. Initialize required harness files. 2. Edit the PROJECT PURPOSE block in AGENTS.md. 3. Create and update docs/PRODUCT.md. 4. Create docs/ARCHITECTURE.md and docs/CONSTRAINTS.md as free-form context files. 5. Check harness consistency and report logical issues. 6. Update tracking artifacts. 7. Resume interrupted AHE workflows. 

## 4. Primary User Experience

All AHE workflows happen inside Codex chat.

Example:

text user> ahe init codex> What is the purpose of this project? 

The user should not need to manually run shell commands during the normal AHE workflow.

AHE commands must not be executed as shell commands unless the user explicitly asks.

## 5. Core Design Principle

AGENTS.md is the primary control surface.

The most important editable region is the PROJECT PURPOSE block near the top of AGENTS.md.

Most project direction should be expressed through this block.

When the project purpose becomes too long or too detailed, AHE uses supporting docs:

text docs/PRODUCT.md docs/ARCHITECTURE.md docs/CONSTRAINTS.md 

These docs are part of the MVP harness, but the user does not have to provide detailed content for all of them during initialization.

If the user has no product, architecture, or constraints description, AHE should still create minimal files.

## 6. Installed Skill Location

The installed AHE skill lives under:

text .codex/skills/ahe/ 

Recommended MVP structure:

text .codex/   skills/     ahe/       SKILL.md       templates/         AGENTS.md         PRODUCT.md         ARCHITECTURE.md         CONSTRAINTS.md         init.sh         feature_list.json         progress.md         session-handoff.md       schemas/         process_status.schema.json         feature_list.schema.json       examples/         init_flow.md         agent_flow.md         product_flow.md         update_flow.md 

.codex/skills/ahe/ contains reusable skill definition files.

It must not contain workspace runtime state.

## 7. Workspace Runtime State

Workspace-specific AHE state lives under:

text .ahe/ 

Recommended structure:

text .ahe/   process_status.json   backups/   products/ 

Responsibilities:

text .ahe/process_status.json = current AHE workflow state .ahe/backups/             = technical backups before rewriting files .ahe/products/            = archived previous PRODUCT.md files 

.ahe/ belongs to the current workspace.

It must not be copied into .codex/skills/ahe/.

## 8. Required Artifacts

The following files are created and maintained by AHE in MVP:

text AGENTS.md init.sh feature_list.json progress.md docs/PRODUCT.md docs/ARCHITECTURE.md docs/CONSTRAINTS.md .ahe/process_status.json 

The following file may be created or refreshed when useful:

text session-handoff.md 

## 9. Managed Docs

AHE-managed docs are:

text docs/PRODUCT.md docs/ARCHITECTURE.md docs/CONSTRAINTS.md 

### docs/PRODUCT.md

docs/PRODUCT.md is the compact product specification.

It should use this structure:

markdown # PRODUCT.md  ## Product Goal  ## Core Requirements  ## Completion Criteria 

If the user provides product content, AHE should organize it into the three sections.

If the user does not provide product content, AHE should create the empty template.

### docs/ARCHITECTURE.md

docs/ARCHITECTURE.md is a free-form architecture document.

It should use this minimal structure:

markdown # ARCHITECTURE.md 

AHE should not force predefined subsections.

If the user provides architecture content, AHE should place it under the title.

If the user does not provide architecture content, AHE should create the title-only file.

### docs/CONSTRAINTS.md

docs/CONSTRAINTS.md is a free-form constraints document.

It should use this minimal structure:

markdown # CONSTRAINTS.md 

AHE should not force predefined subsections.

If the user provides constraints, AHE should place them under the title.

If the user does not provide constraints, AHE should create the title-only file.

## 10. AGENTS.md Template

AGENTS.md is the main operating instruction file for Codex.

AHE creates it from this template:

markdown # {{AGENT_FILE_NAME}}  {{PROJECT_PURPOSE}}  ## Startup Workflow  Before writing code:  1. **Confirm working directory** with `pwd` 2. **Read this file** completely 3. **Read project docs if present** (`docs/ARCHITECTURE.md`, `docs/PRODUCT.md`, `docs/CONSTRAINTS.md`, README.md or equivalent) 4. **Run `./init.sh`** to verify environment is healthy 5. **Read `feature_list.json`** to see current feature state 6. **Review recent commits** with `git log --oneline -5`  If baseline verification is failing, repair that first before adding new scope.  ## Working Rules  - **One feature at a time**: Pick exactly one unfinished feature from `feature_list.json` - **Verification required**: Don't claim done without running verification commands - **Update artifacts**: Before ending session, update `progress.md` and `feature_list.json` - **Stay in scope**: Don't modify files unrelated to the current feature - **Leave clean state**: Next session must be able to run `./init.sh` immediately  ## Required Artifacts  - `feature_list.json` — Feature state tracker (source of truth) - `progress.md` — Session continuity log - `init.sh` — Standard startup and verification path - `session-handoff.md` — Optional, for larger sessions  ## Definition of Done  A feature is done only when ALL of the following are true:  - [ ] Target behavior is implemented - [ ] Required verification actually ran (tests / lint / type-check) - [ ] Evidence recorded in `feature_list.json` or `progress.md` - [ ] Repository remains restartable from standard startup path  ## End of Session  Before ending a session:  1. Update `progress.md` with current state 2. Update `feature_list.json` with new feature status 3. Record any unresolved risks or blockers 4. Commit with descriptive message once work is in safe state 5. Leave repo clean enough for next session to run `./init.sh` immediately  ## Verification Commands  - Tests: `pytest tests/ -x` - Type check: `mypy src/ --strict` - Lint: `ruff check src/` - Full verification: `make check` if a `Makefile` exists; otherwise run all commands above manually.  ## Escalation  If you encounter:  - **Architecture decisions**: Consult project architecture docs if present, otherwise ask user - **Unclear requirements**: Check product/requirements docs if present, otherwise ask user - **Repeated test failures**: Update progress, flag for human review - **Scope ambiguity**: Re-read `feature_list.json` for definition of done 

## 11. PROJECT PURPOSE Block

The PROJECT PURPOSE block is the free-form instruction block near the top of AGENTS.md.

Template location:

markdown # AGENTS.md  {{PROJECT_PURPOSE}}  ## Startup Workflow 

AHE must treat this block as editable.

AHE must not treat it as immutable after ahe init.

Most user direction should be captured by updating this block with:

text ahe agent 

## 12. User Input Refinement Loop

Every AHE workflow step that depends on user input must follow the same refinement loop.

AHE should not assume the first user answer is final.

### Loop

text 1. Ask one focused question. 2. Receive user input. 3. Summarize or clarify the user's input. 4. Decide whether the input is enough for the current step. 5. If enough, ask for confirmation or continue. 6. If not enough, ask a targeted follow-up question. 7. Repeat until the step is complete. 8. Save progress to `.ahe/process_status.json`. 9. Move to the next workflow step. 

### Abstract Flow

text user input -> thinking clarification -> enough?    -> yes: done and go to next step    -> no: ask again and return to user input 

### Confirmation Pattern

text I understood this as:  <summary>  Choose one: 1. accept and continue 2. revise 3. directly provide final text 

### Optional Context Pattern

text Do you have <context type>?  1. yes 2. no / create empty file 3. directly provide content 

## 13. Command Set

MVP commands:

text ahe ahe init ahe agent ahe product ahe check ahe update ahe resume 

## 14. Command: ahe

### Purpose

ahe is the smart entrypoint.

### Behavior

When the user types:

text ahe 

Codex should:

text 1. Inspect `.ahe/process_status.json`. 2. If an unfinished workflow exists, resume it. 3. If no unfinished workflow exists, inspect the current harness state. 4. Recommend the next useful action. 

Routing:

text unfinished workflow exists  -> behave like `ahe resume` AGENTS.md missing           -> recommend `ahe init` AGENTS.md exists            -> summarize current state and suggest next action 

## 15. Command: ahe init

### Purpose

ahe init is the first-run initialization workflow.

It creates required harness files.

### Required Outputs

text AGENTS.md init.sh feature_list.json progress.md docs/PRODUCT.md docs/ARCHITECTURE.md docs/CONSTRAINTS.md .ahe/process_status.json 

### Workflow

ahe init should run this sequence:

text ahe init -> ask project purpose -> run ahe agent-style purpose update -> ask about product description -> create or update docs/PRODUCT.md -> ask about architecture description -> create or update docs/ARCHITECTURE.md -> ask about constraints description -> create or update docs/CONSTRAINTS.md -> ask programming language -> copy and update init.sh -> copy and update progress.md -> copy and update feature_list.json -> create/update .ahe/process_status.json -> run ahe check -> finish 

### Project Purpose Step

Codex asks:

text What is the purpose of this project? 

After the user answers, Codex summarizes the purpose and asks:

text Your project purpose is:  <summary>  Choose one: 1. accept and continue 2. revise 3. directly provide final text 

After confirmation, Codex writes the final purpose into the PROJECT PURPOSE block in AGENTS.md.

### Product Description Step

Codex asks:

text Do you have a product description?  1. yes 2. no / create empty PRODUCT.md 3. directly provide content 

If the user provides product content, Codex creates or updates:

text docs/PRODUCT.md 

If the user chooses no, Codex creates the empty docs/PRODUCT.md template.

### Architecture Description Step

Codex asks:

text Do you have an architecture description?  1. yes 2. no / create empty ARCHITECTURE.md 3. directly provide content 

If the user provides architecture content, Codex creates or updates:

text docs/ARCHITECTURE.md 

If the user chooses no, Codex creates:

markdown # ARCHITECTURE.md 

### Constraints Description Step

Codex asks:

text Do you have separate constraints?  1. yes 2. no / create empty CONSTRAINTS.md 3. directly provide content 

If the user provides constraints, Codex creates or updates:

text docs/CONSTRAINTS.md 

If the user chooses no, Codex creates:

markdown # CONSTRAINTS.md 

### Language Step

Codex asks:

text What is your programming language or main environment?  1. Python 2. directly mention another language or environment 

If unclear, default to Python.

### Resume Support

ahe init must update .ahe/process_status.json after every completed step.

If the user disconnects, ahe or ahe resume must continue from the saved step.

## 16. Command: ahe agent

### Purpose

ahe agent modifies the PROJECT PURPOSE block in AGENTS.md.

This command is used when the user wants to change project direction, add a new feature direction, or revise Codex's top-level instruction.

### Workflow

text ahe agent -> ask for new or revised purpose -> summarize proposed purpose -> ask user to accept/revise/directly provide final text -> update only AGENTS.md PROJECT PURPOSE block -> preserve all other AGENTS.md sections -> ask whether to update product description -> if yes, update docs/PRODUCT.md -> run logical consistency check between AGENTS.md and docs/PRODUCT.md -> finalize 

### Target Block

Only replace the block between:

markdown # AGENTS.md 

and:

markdown ## Startup Workflow 

Do not rewrite the full AGENTS.md.

### Product Continuation Prompt

After updating the PROJECT PURPOSE, Codex must ask:

text The PROJECT PURPOSE has changed.  Do you want to update docs/PRODUCT.md?  1. yes, update product description 2. no, leave PRODUCT.md as-is 3. directly provide product content 

If the user chooses yes or directly provides content, Codex updates docs/PRODUCT.md.

### Product Consistency Rule

If docs/PRODUCT.md exists, Codex must check logical consistency between:

text AGENTS.md PROJECT PURPOSE docs/PRODUCT.md 

If they conflict, Codex must ask the user before finalizing.

## 17. Command: ahe product

### Purpose

ahe product creates or updates docs/PRODUCT.md.

This command is used when the user wants to explicitly edit the product description.

### Workflow

text ahe product -> ask whether to update existing product or create a new product -> if update, ask for update content -> if create, ask for new product content -> update docs/PRODUCT.md -> run logical consistency check with AGENTS.md PROJECT PURPOSE -> if inconsistent, ask whether to revise AGENTS.md PROJECT PURPOSE -> finalize product 

### Initial Question

Codex asks:

text Do you want to update the current PRODUCT.md or create a new product description?  1. update current PRODUCT.md 2. create new PRODUCT.md 3. directly provide product content 

### Product Archive Rule

When creating a new product and an existing docs/PRODUCT.md exists, archive the existing file first.

Archive path:

text .ahe/products/PRODUCT.YYYYMMDD-HHMMSS.md 

### PRODUCT.md Structure

docs/PRODUCT.md should stay compact:

markdown # PRODUCT.md  ## Product Goal  ## Core Requirements  ## Completion Criteria 

## 18. Command: ahe check

### Purpose

ahe check performs an overall harness inspection and reports logical problems to the user.

ahe check should not modify files unless the user explicitly asks.

### Input Sources

ahe check inspects:

text AGENTS.md docs/PRODUCT.md docs/ARCHITECTURE.md docs/CONSTRAINTS.md feature_list.json init.sh progress.md session-handoff.md if present .ahe/process_status.json .ahe/products/ if present src/ if useful tests/ if useful 

### Required Checks

Codex should check:

text AGENTS.md exists AGENTS.md has a non-empty PROJECT PURPOSE block init.sh exists feature_list.json exists and is valid JSON progress.md exists docs/PRODUCT.md exists docs/ARCHITECTURE.md exists docs/CONSTRAINTS.md exists .ahe/process_status.json exists 

### Logical Checks

Codex should also look for:

text AGENTS.md PROJECT PURPOSE conflicts with docs/PRODUCT.md docs/PRODUCT.md conflicts with feature_list.json feature_list.json status conflicts with progress.md init.sh does not match detected language/environment progress.md claims completed work that feature_list.json does not reflect session-handoff.md is stale if present 

### Output

ahe check should report:

text what is valid what is missing what looks logically inconsistent what seems already done what appears to be the next thing to do recommended next command or action 

## 19. Command: ahe update

### Purpose

ahe update updates current tracking artifacts.

It is used when the user wants to synchronize the current workspace state into AHE continuity files.

Unlike ahe check, which inspects and reports issues, ahe update writes updates to tracking artifacts.

### Main Outputs

ahe update updates:

text feature_list.json progress.md session-handoff.md .ahe/process_status.json 

### Input Sources

ahe update should inspect:

text AGENTS.md docs/PRODUCT.md docs/ARCHITECTURE.md docs/CONSTRAINTS.md feature_list.json progress.md session-handoff.md if present .ahe/process_status.json src/ if useful tests/ if useful git status git log --oneline -5 

### Behavior

When the user types:

text ahe update 

Codex should:

text 1. Inspect the current workspace state. 2. Read AGENTS.md PROJECT PURPOSE. 3. Read docs/PRODUCT.md. 4. Read docs/ARCHITECTURE.md. 5. Read docs/CONSTRAINTS.md. 6. Read feature_list.json. 7. Read progress.md. 8. Read session-handoff.md if present. 9. Inspect git status and recent commits. 10. Infer what changed since the last recorded progress. 11. Propose updates to feature_list.json, progress.md, session-handoff.md, and .ahe/process_status.json. 12. Ask for confirmation before writing. 13. Apply updates if confirmed. 14. Summarize what was updated. 

### Required User Confirmation

Before writing changes, AHE should summarize the planned updates and ask for confirmation.

Example:

text I will update the tracking artifacts as follows:  - feature_list.json: mark feature-002 as in_progress - progress.md: add current session summary - session-handoff.md: refresh next-step handoff - .ahe/process_status.json: mark current workflow as updated  Choose one: 1. apply updates 2. revise 3. cancel 

### Artifact Responsibilities

#### feature_list.json

Update feature status based on observed work and user confirmation.

Allowed statuses:

text todo in_progress blocked done 

AHE must not mark a feature as done unless there is enough evidence.

#### progress.md

Update the human-readable session continuity log.

It should include:

text - current state - completed work - in-progress work - blockers - decisions - last verification - next recommended action 

#### session-handoff.md

session-handoff.md may be created or refreshed by ahe update.

It should be short and useful for the next Codex session.

Suggested structure:

markdown # session-handoff.md  ## Summary  ## Current Feature  ## What Changed  ## Verification  ## Risks / Blockers  ## Next Step 

#### .ahe/process_status.json

Update workflow state, including:

text current_command current_step workflow_complete last_update_command updated_at 

## 20. Command: ahe resume

### Purpose

ahe resume resumes an unfinished workflow.

This is especially important for ahe init.

### Workflow

text ahe resume -> read .ahe/process_status.json -> identify current_command -> identify current_step -> summarize collected information -> continue from the saved step 

If there is no unfinished workflow, behave like ahe.

## 21. Default Python Behavior

Python is the default language/environment.

Default verification commands:

text pytest tests/ -x mypy src/ --strict ruff check src/ make check if a Makefile exists; otherwise run all commands above manually 

Default init.sh should be conservative and non-destructive.

It should detect common Python files:

text pyproject.toml requirements.txt uv.lock poetry.lock environment.yml conda.yaml src/ tests/ 

It should print recommended setup and verification commands.

It must not install dependencies automatically unless the user explicitly asks.

## 22. Safety Rules

AHE must be conservative.

Rules:

text Do not silently overwrite existing files. Create backups under `.ahe/backups/` before rewriting existing AHE-managed files. Archive old PRODUCT.md under `.ahe/products/` when creating a new product. Ask one focused question at a time. Use the user input refinement loop for all user-provided information. Keep skill definition and workspace runtime state separate. Do not use hooks in MVP. Do not perform automatic background actions. Do not execute shell commands unless the user explicitly asks. Do not treat `ahe init` as a shell command by default. Do not silently resolve conflicts between AGENTS.md and PRODUCT.md. Do not silently mark features as done. 

## 23. MVP Scope

Include:

text Codex chat workflow Single AHE skill AGENTS.md generation AGENTS.md PROJECT PURPOSE editing init.sh generation feature_list.json generation/update progress.md generation/update session-handoff.md generation/update through ahe update docs/PRODUCT.md generation/update docs/ARCHITECTURE.md generation/update docs/CONSTRAINTS.md generation/update .ahe/process_status.json .ahe/products/ product archive ahe resume support Python default environment user input refinement loop 

## 24. Completion Definition

AHE harness initialization is complete when:

text AGENTS.md exists AGENTS.md has a non-empty PROJECT PURPOSE block init.sh exists feature_list.json exists and is valid JSON progress.md exists docs/PRODUCT.md exists docs/ARCHITECTURE.md exists docs/CONSTRAINTS.md exists .ahe/process_status.json exists ahe check reports no missing required artifacts 

## 25. Final Design Principle

AHE is not a project generator.

AHE is a Codex workflow harness generator.

It prepares a workspace so Codex can:

text understand the project purpose resume interrupted workflows track feature state update progress inspect product/architecture/constraint context work one feature at a time leave the repository restartable 



## Installation and Distribution Model

AHE is distributed as a Node/npm package.

The primary runtime UX is Codex chat, but the initial installation should be done through an npm package.

Recommended install command:

bash npx ahe install 

If the unscoped package name is unavailable or too generic, use a scoped package:

bash npx @your-scope/ahe install 

## npm Package Responsibility

The npm package is responsible for installing the AHE Codex skill into the current workspace.

It should create or update:

text .codex/skills/ahe/   SKILL.md   templates/     AGENTS.md     PRODUCT.md     ARCHITECTURE.md     CONSTRAINTS.md     init.sh     feature_list.json     progress.md     session-handoff.md   schemas/     process_status.schema.json     feature_list.schema.json   examples/     init_flow.md     agent_flow.md     product_flow.md     update_flow.md 

The npm installer should not run the AHE chat workflow.

It only installs the skill files.

After installation, the user interacts with AHE inside Codex chat:

text ahe init ahe agent ahe product ahe check ahe update ahe resume 

## Package Structure

Recommended package source structure:

text ahe/   package.json   README.md   bin/     ahe.js   skill/     SKILL.md     templates/       AGENTS.md       PRODUCT.md       ARCHITECTURE.md       CONSTRAINTS.md       init.sh       feature_list.json       progress.md       session-handoff.md     schemas/       process_status.schema.json       feature_list.schema.json     examples/       init_flow.md       agent_flow.md       product_flow.md       update_flow.md 

## package.json

The package should expose a CLI command through the bin field.

Example:

json {   "name": "ahe",   "version": "0.1.0",   "description": "Codex chat workflow skill for Agent Harness Engineering",   "type": "module",   "bin": {     "ahe": "./bin/ahe.js"   },   "files": [     "bin/",     "skill/",     "README.md"   ],   "engines": {     "node": ">=18"   } } 

If using a scoped package:

json {   "name": "@your-scope/ahe",   "version": "0.1.0",   "description": "Codex chat workflow skill for Agent Harness Engineering",   "type": "module",   "bin": {     "ahe": "./bin/ahe.js"   } } 

## CLI Commands for Installer

The npm CLI should stay minimal.

Required command:

bash ahe install 

Optional helper commands:

bash ahe doctor ahe version 

### ahe install

Installs the AHE skill into the current workspace.

Behavior:

text 1. Confirm current working directory. 2. Create `.codex/skills/ahe/` if missing. 3. Copy `skill/SKILL.md` into `.codex/skills/ahe/SKILL.md`. 4. Copy templates into `.codex/skills/ahe/templates/`. 5. Copy schemas into `.codex/skills/ahe/schemas/`. 6. Copy examples into `.codex/skills/ahe/examples/`. 7. Do not create workspace runtime files. 8. Do not create AGENTS.md. 9. Do not create `.ahe/process_status.json`. 10. Print next step: open Codex chat and type `ahe init`. 

The installer should finish with a message like:

text AHE Codex skill installed.  Next: 1. Open Codex chat in this workspace. 2. Type `ahe init`. 

### ahe doctor

Checks whether AHE skill files are installed correctly.

It may verify:

text .codex/skills/ahe/SKILL.md exists .codex/skills/ahe/templates/ exists .codex/skills/ahe/schemas/ exists 

It should not validate workspace harness files such as AGENTS.md or feature_list.json.

Workspace harness validation belongs to the Codex chat command:

text ahe check 

## Installation Output

After running:

bash npx ahe install 

Expected workspace structure:

text {workspace}/   .codex/     skills/       ahe/         SKILL.md         templates/           AGENTS.md           PRODUCT.md           ARCHITECTURE.md           CONSTRAINTS.md           init.sh           feature_list.json           progress.md           session-handoff.md         schemas/           process_status.schema.json           feature_list.schema.json         examples/           init_flow.md           agent_flow.md           product_flow.md           update_flow.md 

The installer must not create:

text AGENTS.md init.sh feature_list.json progress.md docs/ .ahe/ 

Those files are created later through the Codex chat workflow:

text ahe init 

## Security Requirements

The AHE npm installer must be conservative.

Rules:

text Do not read OpenAI, Codex, GitHub, npm, SSH, or cloud credentials. Do not access tokens from environment variables. Do not send telemetry by default. Do not make network requests except npm package download itself. Do not run postinstall logic that modifies the workspace. Do not execute arbitrary shell commands. Do not install dependencies into the user's project. Only write files under `.codex/skills/ahe/` during `ahe install`. Ask or fail if `.codex/skills/ahe/` already exists and overwrite is not explicitly allowed. 

Recommended overwrite options:

bash ahe install --force ahe install --backup 

Default behavior:

text If `.codex/skills/ahe/` already exists, do not overwrite silently. Show a warning and ask the user to rerun with `--force` or `--backup`. 

## Separation Between Installer and Workflow

AHE has two layers:

text 1. npm installer layer 2. Codex chat workflow layer 

### npm installer layer

Runs in the terminal.

Purpose:

text Install `.codex/skills/ahe/`. 

Commands:

bash npx ahe install ahe install ahe doctor ahe version 

### Codex chat workflow layer

Runs inside Codex chat.

Purpose:

text Create and maintain workspace harness files. 

Commands:

text ahe ahe init ahe agent ahe product ahe check ahe update ahe resume 

The npm installer must not perform the chat workflow.

The Codex chat workflow must not depend on running npm commands after installation.

## User Flow

Fresh install:

bash npx ahe install 

Then inside Codex chat:

text ahe init 

Normal usage after initialization:

text ahe ahe agent ahe product ahe check ahe update ahe resume 