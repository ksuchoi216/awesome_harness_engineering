# PROGRESS.md

## Current Status

**Last Updated:** 2026-06-15 16:07 +0900
**Session ID:** feat-034-product-instructions-contract
**Active Feature:** None

## Completed

- [x] Implemented `feat-035 AHE Init Alias Hook Detection` by updating the `UserPromptSubmit` hook so exact `ahe-init` and exact `$ahe-init` route to the same new-start directive as exact `ahe init`, while normal prompts that merely mention `ahe-init` still do not trigger AHE. Updated `docs/PRODUCT.md` and `tests/test_ahe_hook.py` to document and verify the alias behavior. Verified with `./init.sh`, `pytest tests/test_ahe_hook.py -x`, `pytest tests/ -k 'not helper_scripts_target_global_codex_home'`, `ruff check src/ tests/`, `node --check .codex/hooks/ahe-hook.js`, `python3 -m json.tool feature-list.json`, direct hook smoke checks for `ahe init`, `ahe-init`, `$ahe-init`, and normal mention suppression, plus Python LSP diagnostics on `tests/test_ahe_hook.py`. Full `pytest tests/ -x` remains blocked by the pre-existing `scripts/install.sh` nested `npx --package=... ahe install` smoke path hanging or being killed with signal 9; `mypy` is not installed.

- [x] Implemented `feat-034 PRODUCT+INSTRUCTIONS Required Contract` by replacing the old constraints/architecture requirements with a new `docs/INSTRUCTIONS.md` contract. Updated `ahe-init`, `ahe-spec`, `ahe-thinking`, `ahe-conversation`, and `ahe-hook.js` to enforce `INSTRUCTIONS.md` alongside `PRODUCT.md` as the required harness documents. Updated `docs/PRODUCT.md` and tests (`test_init_workflow.py`, `test_spec_workflow.py`, `test_specialized_workflows.py`, `test_clarification_prompt.py`, `test_command_set.py`, `test_ahe_hook.py`) to drop the constraints doc and validate the new instructions doc. Verified with `./init.sh`, `pytest tests/ -x`, `ruff check src/ tests/`, and `node --check .codex/hooks/ahe-hook.js`.

- [x] Implemented `feat-033 PRODUCT.md First Harness Contract` by enforcing `docs/PRODUCT.md` as the canonical source of truth for product/specification, making `feature-list.json` a derived tracker. Updated `ahe-hook.js`, `ahe-thinking`, `ahe-update`, `ahe-init`, and `ahe-spec` to prioritize `docs/PRODUCT.md` and require it to be populated before writing specific features. Updated `tests/test_ahe_hook.py`, `tests/test_spec_workflow.py`, `tests/test_specialized_workflows.py`, and `tests/test_init_workflow.py`. Verified with `./init.sh`, `pytest tests/ -x`, `ruff check src/ tests/`. `mypy` is not installed so it could not run.

- [x] Implemented `feat-032 Scoped AHE Init Restart` by changing the `ahe-init` contract so empty workspaces start normally, existing AHE-managed harness files are read and summarized before any reset, and the user must choose a free-form restart scope before backup/removal/overwrite work begins. Updated `ahe-spec` and the exact `ahe init` hook so product specification details go to `docs/PRODUCT.md`, not `AGENTS.md`. Added contract coverage in `tests/test_init_workflow.py`, `tests/test_spec_workflow.py`, and `tests/test_ahe_hook.py`, then verified with `./init.sh`, `pytest tests/ -x`, JSON validation, `ruff check src/`, `node --check .codex/hooks/ahe-hook.js`, and LSP diagnostics. `mypy` is not installed, so the documented type-check command could not run.

- [x] Implemented `feat-031 Two-Entrypoint AHE Surface` by removing `.codex/skills/ahe-help/SKILL.md`, folding the internal `ahe-clear` reset path into `.codex/skills/ahe-init/SKILL.md`, deleting `.codex/skills/ahe-clear/SKILL.md` and `tests/test_clear_workflow.py`, updating install/uninstall skill lists, shrinking the installed public surface to `ahe init` and exact `ahe`, and extending the hook contract so exact `ahe init` acts as the new-start path. Updated `docs/PRODUCT.md`, `feature-list.json`, `SESSION-HANDOFF.md`, and contract tests, then verified with `./init.sh`, `pytest tests/ -x`, and `python3 -m json.tool feature-list.json`.

- [x] Implemented `feat-030 Internal AHE Thinking Orchestrator` by adding `.codex/skills/ahe-thinking/SKILL.md` as a hidden internal protocol, updating `.codex/skills/ahe-conversation/SKILL.md` to act only after `ahe-thinking` identifies the missing detail, wiring `ahe-init`, `ahe-spec`, `ahe-update`, and `ahe-clear` to follow `ahe-thinking` before clarification, and updating the exact `ahe` hook so it classifies exactly one harness state and continues automatically with `thinking -> conversation if needed -> execution -> thinking`. Updated installer/uninstaller skill lists, `docs/PRODUCT.md`, `feature-list.json`, `SESSION-HANDOFF.md`, and contract tests, then verified with `./init.sh`, `pytest tests/ -x`, and `python3 -m json.tool feature-list.json`.

- [x] Implemented `feat-029 Simplified AHE Status Report Confirmation` by reducing the exact `ahe` first-response table to `AGENTS.md`, `PRODUCT.md`, `feature-list.json`, and `PROGRESS.md`, then requiring a direct next-step confirmation after the table using one of `harness engineering`, `start a new task`, or `resume existing harness work`. Updated `.codex/hooks/ahe-hook.js`, `docs/PRODUCT.md`, `feature-list.json`, and `tests/test_ahe_hook.py`, then verified with `pytest tests/test_ahe_hook.py -x`.

- [x] Implemented `feat-028 Adaptive CodeGraph Preflight` by updating the exact `ahe` hook directive so AHE first checks `command -v codegraph`, reports `NOT INSTALLATION of codegraph` and skips init/sync when the CLI is missing, runs `codegraph init` when `.codegraph/` is missing, and runs `codegraph sync` when `.codegraph/` exists. Updated `docs/PRODUCT.md`, `feature-list.json`, and `tests/test_ahe_hook.py`, then verified with `./init.sh`, `pytest tests/ -x`, `python3 -m json.tool feature-list.json`, and `codegraph sync`.

- [x] Implemented `feat-027 AHE First Response Status Report` by updating the exact `ahe` hook directive so automatic operation first reports harness engineering status in a consistent Markdown table before edits or workflow execution. Updated `docs/PRODUCT.md`, `feature-list.json`, and `tests/test_ahe_hook.py`, then verified with `./init.sh`, `pytest tests/ -x`, `python3 -m json.tool feature-list.json`, and `codegraph sync`.

- [x] Implemented `feat-026 Internal AHE Conversation Protocol` by replacing the previous internal clarification protocol with `ahe-conversation`, expanding the protocol language for recursive clarification, conversation state, decision points, and resume-aware workflow guidance. Updated interactive skills, installer/uninstaller lists, product docs, and tests for the new internal protocol name.

- [x] Implemented `feat-025 Reduced AHE Public Command Surface` by removing public `$ahe-agent`, `$ahe-copy`, and `$ahe-todo`, folding AGENTS/template copy behavior into `$ahe-init`, and folding queued todo capture into `$ahe-update`. Updated help, installer/uninstaller lists, hook guidance, process-status schema, product docs, tracking artifacts, and tests for the five-command public surface.

- [x] Implemented `feat-024 Consolidated AHE Spec Skill` by replacing `$ahe-product`, `$ahe-constraints`, and `$ahe-architecture` with one `$ahe-spec` workflow that updates `docs/PRODUCT.md`, `docs/constraints.md`, and `docs/achitecture.md`. Updated init sequencing, installer/uninstaller lists, help text, process-status schema, hook guidance, product docs, and tests for the reduced command surface.

- [x] Implemented `feat-023 AHE Exact Command Auto Operation` by changing `.codex/hooks/ahe-hook.js` so exact `ahe` prompts inject an automatic AHE operation directive while ordinary AHE mentions do not trigger it. Added `tests/test_ahe_hook.py`, updated `docs/PRODUCT.md`, refreshed `feature-list.json`, and verified with `./init.sh`, `pytest tests/ -x`, `python3 -m json.tool feature-list.json`, `codegraph sync`, and `codegraph status`.

- [x] Implemented `feat-022 AHE Keyword Trigger` by adding a UserPromptSubmit hook to `.codex/hooks/ahe-hook.js` that detects the "ahe" keyword in user prompts and dynamically injects an AHE routing directive. Updated the installer, uninstaller, tracking artifacts, and test suite to verify `.codex/hooks/` deployments.

- [x] Implemented `feat-021 Internal Clarification Protocol Skill` by adding an internal clarification protocol skill, wiring the interactive AHE skills to follow it, keeping `ahe-help` user-facing only, updating installer/uninstaller coverage, and refreshing the product/tracking artifacts.

- [x] Implemented `feat-020 Codex UI-Compatible Clarification Requests` by replacing the fixed plain-text clarification prompt in all 8 interactive AHE skill files with Codex-supported structured response request guidance, adding skill-specific clarification criteria, updating `docs/PRODUCT.md`, and updating the clarification tests to match the new contract.

- [x] Implemented `feat-019 Clarification Prompt Question Inclusion and Recursive Clarification` by updating the Clarification Rule block across all 8 interactive skill files, `docs/PRODUCT.md`, and `tests/test_clarification_prompt.py`.

- [x] Implemented `feat-018 Init Workflow Multi-Step Execution` by modifying `ahe-init` to sequentially execute the six steps (ahe-agents, ahe-product, ahe-architecture, ahe-constraints, ahe-copy, ahe-update) and update the process status to track these steps. Also updated process_status.schema.json description and docs/PRODUCT.md.

- [x] Implemented `feat-017 AHE Agent Initialize Workflow on AGENTS.md Absence` by extending `$ahe-agent` to copy/rename the `agents.md` template, ask the user for the project purpose, update the project purpose, and ask about their language choice.

- [x] Implemented `feat-016 Copy Skill` by adding `ahe-copy` which copies template files (excluding `AGENTS.md` and `PRODUCT.md`) from `ahe-shared/templates/` to the workspace root, converting markdown names to uppercase.
- [x] Updated the split-skill installer, uninstaller, and package file list to include `ahe-copy`.
- [x] Documented the new copy skill in `docs/PRODUCT.md` across sections defining capabilities, layout, responsibilities, and success criteria.
- [x] Expanded the test suite (routing, command set, setup, specialized workflows, and clarification prompt validation) to verify `ahe-copy`.
- [x] Implemented `feat-015 Help Skill` by adding `ahe-help` which lists all available `ahe` commands to the user.
- [x] Updated the split-skill installer, uninstaller, and package file list to include `ahe-help`.
- [x] Documented the new help skill in `docs/PRODUCT.md` across sections defining capabilities, layout, responsibilities, and success criteria.
- [x] Fixed `bin/ahe` post-install variable expansion bug by escaping dollar signs and preventing bash unbound variable crashes.
- [x] Added split-skill test coverage and specialized workflow checks for `ahe-help`.
- [x] Implemented `feat-014 Todo Queue Skill` by adding `ahe-todo` and teaching `ahe-update` to consume `docs/todo.md` into `docs/PRODUCT.md`.
- [x] Updated the split-skill installer and uninstall lists to include `ahe-todo`.
- [x] Extended the split-skill tests and product specification to cover `docs/todo.md` queue behavior.
- [x] Implemented `feat-013 Split AHE Skills` by replacing the monolithic AHE skill with seven separate skill directories and moving templates/schemas into `.codex/ahe-shared`.
- [x] Updated `bin/ahe`, `package.json`, and `scripts/uninstall.sh` so install and uninstall operate on the split-skill layout.
- [x] Rewrote the skill contract tests to validate the split AHE skills instead of `.codex/skills/ahe/SKILL.md`.
- [x] Verified the split-skill layout with `python3 tests/test_*.py`, `bash -n` checks, `bash bin/ahe version`, and `./init.sh`.
- [x] Implemented `feat-012 Reduced AHE Skill Surface` by reducing AHE to `$ahe-init`, `$ahe-agent`, `$ahe-product`, `$ahe-constraints`, `$ahe-architecture`, `$ahe-update`, and `$ahe-clear`.
- [x] Rewrote the skill and product contracts around the reduced command surface.
- [x] Replaced the old check/resume test expectations with the new reduced-command workflow tests.
- [x] Implemented `feat-011 Alias Commands and Update Workflow` by adding `$ahe-init`, `$ahe-product`, and `$ahe-update` aliases plus the `ahe update` workflow contract.
- [x] Updated `docs/PRODUCT.md` to include the alias commands and `ahe update`.
- [x] Added `tests/test_update_workflow.py` and expanded `tests/test_chat_command_routing.py`.
- [x] Implemented `feat-010 Global Codex Helper Scripts` by changing `scripts/install.sh` and `scripts/uninstall.sh` to target `${HOME}/.codex`.
- [x] Added helper-script coverage to `tests/test_project_setup.py`.
- [x] Implemented `feat-009 Clear Workflow Reset Semantics` by changing the `ahe clear` contract to back up the full harness context, reset `AGENTS.md` objective guidance, remove the old product spec after backup, and collect the new spec recursively.
- [x] Updated `docs/PRODUCT.md` and `tests/test_clear_workflow.py` to match the new `ahe clear` semantics.
- [x] Created `.ahe/backups/20260608-215651/` for the `ahe clear` workflow.
- [x] Copied `AGENTS.md`, the `docs/` folder, `PROGRESS.md`, `SESSION-HANDOFF.md`, and `init.sh` into the clear-workflow backup directory.
- [x] Backed up the current root AHE-managed files into `.ahe/backups/20260608-144947/`.
- [x] Added the packaged installer scaffold and embedded skill assets under `.codex/skills/ahe/`.
- [x] Verified the setup artifacts with shell checks, JSON validation, installer doctor/version, installer smoke install, and direct execution of the Python test assertions.
- [x] Implemented `feat-002 Chat Command Routing` by expanding `.codex/skills/ahe/SKILL.md` and adding `tests/test_chat_command_routing.py`.
- [x] Implemented `feat-003 Init Workflow` by adding step-by-step instructions to `.codex/skills/ahe/SKILL.md` and creating `tests/test_init_workflow.py`.
- [x] Implemented `feat-004 Product Workflow` by adding a dedicated `ahe product` workflow contract to `.codex/skills/ahe/SKILL.md` and creating `tests/test_product_workflow.py`.
- [x] Fixed the `npx ahe install` smoke-test path resolution in `bin/ahe` so packaged installs work when the shell entrypoint is invoked through npm's `.bin` symlink.
- [x] Implemented `feat-005 Check and Resume Workflows` by adding dedicated `ahe check` and `ahe resume` workflow contracts to `.codex/skills/ahe/SKILL.md`.
- [x] Added `tests/test_check_resume_workflows.py` to verify validation scope, report behavior, resume-state inspection, and next-question handling.
- [x] Implemented `feat-006 Session Tracking and Handoff` by adding a cross-workflow tracking sync contract to `.codex/skills/ahe/SKILL.md`.
- [x] Added `tests/test_session_tracking_handoff.py` to verify process-status synchronization and progress/handoff update rules.
- [x] Implemented `feat-007 Clear Workflow` by adding the `ahe clear` command contract to `.codex/skills/ahe/SKILL.md`.
- [x] Updated `docs/PRODUCT.md` so the product specification includes `ahe clear`.
- [x] Added `tests/test_clear_workflow.py` to verify backup and new-goal conversation requirements.
- [x] Implemented `feat-008 Clarification Prompt Format` by adding a global clarification rule to `.codex/skills/ahe/SKILL.md`.
- [x] Updated `docs/PRODUCT.md` with the exact three-option clarification prompt format.
- [x] Added `tests/test_clarification_prompt.py` to verify the exact prompt lines and option meanings.

## In Progress

- [ ] No active implementation in progress.
  - Details: `feat-035 AHE Init Alias Hook Detection` is complete. Exact `ahe init`, exact `ahe-init`, and exact `$ahe-init` now inject the same AHE new-start directive.
  - Blockers: None.

## Blocked

- [ ] No current blocker.

## Decisions

- **Existing harness files require a restart-scope question**: Exact `ahe init` now reads existing AHE-managed files, summarizes the current project purpose and product specification state, and asks what scope to restart before backing up, removing, overwriting, or refreshing anything.
  - Context: The user said missing files should initialize normally, but existing files must be inspected first and the user must decide how far to restart, such as from `purpose` or from `product`.
  - Alternatives considered: Continuing the previous broad new-start reset would be faster but risks destroying or replacing more harness context than the user intended.
- **Specification details belong in `docs/PRODUCT.md`**: `AGENTS.md` remains limited to project purpose and base agent settings; product behavior, requirements, success criteria, and workflow details flow through `ahe-spec`.
  - Context: The user clarified that free conversation during `ahe init` can produce specification details, but those details should be reflected in `product.md` rather than expanding `AGENTS.md`.
  - Alternatives considered: Keeping all init-collected detail in `AGENTS.md` would blur the project-purpose file with the product specification.
- **Exact init aliases are new-start commands**: The hook now treats exact `ahe-init` and exact `$ahe-init` as aliases for exact `ahe init`, but still ignores normal sentences that merely mention those strings.
  - Context: The user reported that `ahe init` or `ahe-init` did not seem to be detected; local reproduction confirmed `ahe-init` and `$ahe-init` emitted no hook output.
  - Alternatives considered: Supporting only `$ahe-init` through Codex skill invocation would leave the plain `ahe-init` chat command ambiguous and would not fix the observed hook detection gap.

- **AHE keyword detection acts via a hook, not a skill trigger**: Added `ahe-hook.js` and `hooks.json` to leverage Codex's `UserPromptSubmit` hook instead of just adding a `triggers` block to `ahe-help`.
  - Context: The user requested "detecting the 'ahe' in user's query like ultrawork in codex", and ultrawork works by injecting a transparent directive via hooks.
  - Alternatives considered: Using `triggers: ["ahe"]` in `SKILL.md` would immediately launch a specific skill (e.g. `ahe-help`), which is more intrusive than a background directive injection.
- **Exact `ahe` starts automatic operation, normal mentions do not**: The hook now requires the prompt to trim and case-fold to exactly `ahe`.
  - Context: The user wanted a simple command users can remember, but did not want ordinary AHE discussion to trigger automatic routing.
  - Alternatives considered: Keeping broad `\bahe\b` matching would interrupt prompts like "explain ahe" and make the hook too aggressive.
- **Exact `ahe` first reports harness status as a table**: Automatic operation must start its first response with a stable Markdown table using `Item` and `Content` columns before recommending or executing a next step.
  - Context: The user wants to see the current harness engineering state first after AHE checks files, CodeGraph, and next-step routing.
  - Alternatives considered: Jumping straight into the next workflow would hide the status information the user needs to understand why AHE chose that path.
- **The exact `ahe` report should stay minimal and ask for the next step outside the table**: The table now covers only `AGENTS.md`, `PRODUCT.md`, `feature-list.json`, and `PROGRESS.md`, and AHE must ask the user to confirm one simple next-step choice after the table.
  - Context: The user said broader rows and embedding the next step in the table made the report harder to read and made the next action easy to miss.
  - Alternatives considered: Keeping optional docs, git state, or a next-step row would preserve more detail but would work against the requested simpler first response.
- **`ahe-thinking` decides and `ahe-conversation` clarifies**: AHE now uses a separate internal decision layer to judge the current `project`, `feature`, or `sub-feature`, decide which of `Why`, `What`, and `How` are required, and hand only the missing detail to `ahe-conversation`.
  - Context: The user wanted critical thinking to run freely between actions and wanted clarification to recurse from project level down into features and sub-features only as needed.
  - Alternatives considered: Keeping `ahe-conversation` as both judge and questioner would preserve fewer moving parts, but it would blur the difference between deciding what is missing and asking for it.
- **Exact `ahe` should continue automatically after classification**: The hook now classifies exactly one state from `harness engineering not enough`, `in the middle of building features`, or `completed all`, then continues without a separate confirmation step.
  - Context: The user explicitly wanted `대화 -> 실행 -> 대화 -> 실행` continuity rather than a recommendation that stops.
  - Alternatives considered: Keeping a post-table confirmation prompt would be safer in some ambiguous cases but would not match the requested continuous flow.
- **New starts and resets belong to `ahe-init`**: AHE no longer keeps a separate internal clear workflow; exact `ahe init` and `$ahe-init` cover both first-time initialization and fresh-start reset behavior through backup plus replacement.
  - Context: The user said actual usage should be only `ahe init` for a new start and `ahe` for progress.
  - Alternatives considered: Keeping `ahe-clear` internally would preserve a narrower reset workflow, but it duplicates the new-start responsibility now owned by `ahe-init`.
- **CodeGraph preflight is adaptive**: Exact `ahe` now checks `command -v codegraph`; missing CLI reports `NOT INSTALLATION of codegraph` and skips init/sync, missing `.codegraph/` runs `codegraph init`, and existing `.codegraph/` runs `codegraph sync`.
  - Context: The user wants AHE to initialize or sync CodeGraph automatically when possible while adapting cleanly when CodeGraph is not installed.
  - Alternatives considered: Always attempting `codegraph init` or `codegraph sync` would create noisy failures on machines without the CLI.
- **Automatic operation prefers CodeGraph but remains usable without it**: The directive tells Codex to check `.codegraph/` and prefer CodeGraph exploration when available, then fall back to normal repo inspection if CodeGraph is missing.
  - Context: The user specifically requested review through CodeGraph and pointed to the local `.codegraph/` flow.
  - Alternatives considered: Installing or initializing CodeGraph from AHE would add an external dependency side effect outside this package's current installer contract.
- **Ambiguous next steps must ask the user**: When feature state, active process state, dependencies, or CodeGraph review do not identify one safe next workflow, AHE asks a short clarification question with meaningful options.
  - Context: The user explicitly asked AHE not to guess when the next step is hard to decide.
  - Alternatives considered: Choosing the first plausible action would be faster but risks working on the wrong harness task.
- **Product, constraints, and architecture share one public spec workflow**: `$ahe-spec` now owns `docs/PRODUCT.md`, `docs/constraints.md`, and `docs/achitecture.md` instead of exposing three separate public skills.
  - Context: The user said AHE had too many skills and specifically asked to put `ahe-constraints`, `ahe-product`, and `ahe-architecture` together.
  - Alternatives considered: Keeping alias skills would preserve compatibility but would not reduce the visible skill count.
- **Init owns setup plumbing and update owns queued work**: `ahe-init` now absorbs the old `ahe-agent` and `ahe-copy` responsibilities, and `ahe-update` now absorbs the old `ahe-todo` capture path.
  - Context: The user said the remaining skill list was still too complicated after the `ahe-spec` consolidation.
  - Alternatives considered: Keeping the subcommands as aliases would preserve compatibility but would not reduce the visible skill count or cognitive load.
- **ahe-conversation is the internal protocol**: The internal skill now describes recursive clarification, stateful decision points, resume context, and workflow continuation instead of a narrow question helper.
  - Context: The user said the previous internal name was too simple and clarification requires many questions and answers with thinking about what to check and how to approach the work.
  - Alternatives considered: Keeping the old internal protocol as a compatibility alias would reduce churn but preserve a misleading internal name.
- **Clarification UI guidance should target Codex structured response requests, not a hardcoded text block**: Interactive AHE skills now instruct Codex to ask short structured questions with meaningful options and custom input, then re-ask until each skill's clarification criteria are satisfied.
  - Context: The user wants the Codex response picker UI behavior rather than literal prompt text rendered in chat.
  - Alternatives considered: Keeping the exact `Question: {question}` text block would preserve the old test contract but would not match the desired Codex UI behavior.
- **ahe-copy ignores AGENTS.md and PRODUCT.md**: The `ahe-copy` skill explicitly ignores the agents and product files, copying all other templates directly to the workspace root.
  - Context: The user requested a skill to copy the other template files for initialization while leaving agents/product handling separate.
  - Alternatives considered: Copying product spec to `docs/` and agents.md to root, which was the previous plan.
- **AHE-help lists all command details inside SKILL.md**: `$ahe-help` prints the full split-skill command set and descriptions.
  - Context: The user requested a skill to show a list of commands in AHE.
  - Alternatives considered: Implementing a dynamic listing in Node/Bash versus placing the descriptions in `SKILL.md`. Documenting inside `SKILL.md` is standard for Codex split skills.
- **Escape dollar signs in heredoc success messages**: Changed `cat <<EOF` post-install outputs to escape `$` to avoid bash unbound variable crashes under `set -u`.
  - Context: Bash crashed because it attempted to expand `$ahe` as a variable during installation.
  - Alternatives considered: Removing the command list or changing heredoc quote style. Escaping preserves both variable interpolation for other parts and the exact command symbols.
- **Package.json files whitelist should target the parent dotfolder**: Changed `package.json` `files` array to target `.codex/` instead of `.codex/skills/` and `.codex/ahe-shared/`.
  - Context: npm pack ignored the subfolders starting with a dot, but targets the parent dotfolder correctly when listed directly.
  - Alternatives considered: Renaming `.codex` or omitting it from packaging. Specifying `.codex/` allows local and remote npx runs to successfully install the skill files.
- **Fast todo capture should bypass immediate `docs/PRODUCT.md` editing**: `ahe-todo` writes queued work to `docs/todo.md`, and `ahe-update` is responsible for applying it to `docs/PRODUCT.md` later.
  - Context: The user wants a lighter-weight capture path that still updates `feature-list.json`.
  - Alternatives considered: Writing directly to `docs/PRODUCT.md` from `ahe-todo` would collapse the separation between quick capture and later structured application.
- **AHE should be exposed as separate Codex skills, not one command router file**: the repository now installs seven `ahe-*` skill directories and keeps reusable templates and schemas under `.codex/ahe-shared`.
  - Context: The user wants each AHE capability visible and invokable directly in Codex.
  - Alternatives considered: Keeping one `ahe` skill with internal subcommand routing still shows only one skill in Codex and does not satisfy the requested UX.
- **Installer implementation is part of feat-001**: `npx ahe install` now has a concrete package scaffold instead of staying as a later placeholder.
  - Context: The product goal and user instructions both require installation to be included now.
  - Alternatives considered: Deferring the installer to a later feature would leave the setup feature incomplete.
- **The installer bin is a shell script**: The npm package exposes `./bin/ahe` instead of a Node entry file.
  - Context: This workspace has no `node` binary, but npm can still package a portable shell bin for `npx ahe install`.
  - Alternatives considered: A Node CLI would be harder to verify locally in the current environment.
- **Local development uses a file package spec**: cloned-repo testing should use `npx --yes --package=file:. ahe install`.
  - Context: The package is not deployed yet, but the user still wants the install UX to be exercised through `npx`.
  - Alternatives considered: Using only `bash bin/ahe install` does not match the intended installer entrypoint closely enough.
- **The installer must resolve its real package path before copying skill files**: `npx` executes `bin/ahe` through npm's `.bin` symlink, so the installer has to follow symlinks before computing `PACKAGE_ROOT`.
  - Context: The full pytest run exposed a failure where the installer looked for `.codex/skills/ahe` under `node_modules/.codex` instead of `node_modules/ahe/.codex`.
  - Alternatives considered: Weakening the smoke test would hide a real packaging defect and would not verify the published install path.
- **Workflow contracts should be explicit in the installed skill, not only in `docs/PRODUCT.md`**: `ahe check` and `ahe resume` now have dedicated sections in `.codex/skills/ahe/SKILL.md`.
  - Context: The installed skill is the artifact Codex will actually use in chat, so relying on the product spec alone leaves runtime behavior underspecified.
  - Alternatives considered: Leaving the behavior only in `docs/PRODUCT.md` would keep the implementation contract incomplete for the actual installed skill surface.
- **Tracking rules should live in one cross-workflow section instead of being inferred from scattered command steps**: `.ahe/process_status.json`, `PROGRESS.md`, and `SESSION-HANDOFF.md` now have explicit synchronization rules in the installed skill.
  - Context: The schema defined the shape of runtime state, but not when all three tracking artifacts must move together during active workflows.
  - Alternatives considered: Repeating partial tracking rules in each command section would leave the sync contract fragmented and easier to drift.

## Change Log

- `.codex/hooks/ahe-hook.js`, `docs/PRODUCT.md`, `tests/test_ahe_hook.py`, `feature-list.json`, `PROGRESS.md`, `SESSION-HANDOFF.md` - Added exact init alias hook detection for `ahe-init` and `$ahe-init`, with normal mention suppression.
- `.codex/skills/ahe-init/SKILL.md`, `.codex/skills/ahe-spec/SKILL.md`, `.codex/hooks/ahe-hook.js`, `docs/PRODUCT.md`, `feature-list.json`, `PROGRESS.md`, `SESSION-HANDOFF.md`, `tests/test_init_workflow.py`, `tests/test_spec_workflow.py`, `tests/test_ahe_hook.py` - Added scoped `ahe init` restart semantics and canonical `docs/PRODUCT.md` specification placement.
- `.codex/hooks/hooks.json`, `.codex/hooks/ahe-hook.js`, `bin/ahe`, `scripts/uninstall.sh`, `tests/test_project_setup.py`, `feature-list.json` - Added native keyword detection via a Node.js `UserPromptSubmit` hook script.
- `.codex/skills/ahe-thinking/SKILL.md`, `.codex/skills/ahe-conversation/SKILL.md`, `.codex/skills/ahe-init/SKILL.md`, `.codex/skills/ahe-spec/SKILL.md`, `.codex/skills/ahe-update/SKILL.md`, `.codex/skills/ahe-clear/SKILL.md`, `.codex/hooks/ahe-hook.js`, `bin/ahe`, `scripts/uninstall.sh`, `docs/PRODUCT.md`, `feature-list.json`, `SESSION-HANDOFF.md`, `tests/test_ahe_hook.py`, `tests/test_clarification_prompt.py`, `tests/test_command_set.py`, `tests/test_project_setup.py` - Added the internal `ahe-thinking` orchestrator, split decision-making from recursive clarification, and changed exact `ahe` routing from post-table confirmation into automatic state classification and continuation.
- `.codex/skills/ahe-init/SKILL.md`, `.codex/hooks/ahe-hook.js`, `bin/ahe`, `scripts/uninstall.sh`, `docs/PRODUCT.md`, `feature-list.json`, `SESSION-HANDOFF.md`, `tests/test_ahe_hook.py`, `tests/test_chat_command_routing.py`, `tests/test_command_set.py`, `tests/test_init_workflow.py`, `tests/test_project_setup.py`, `tests/test_specialized_workflows.py` - Reduced AHE usage to exact `ahe init` and exact `ahe`, removed `ahe-help`, and merged the old clear/reset path into `ahe-init`.
- `.codex/hooks/ahe-hook.js`, `docs/PRODUCT.md`, `tests/test_ahe_hook.py`, `feature-list.json`, `PROGRESS.md`, `SESSION-HANDOFF.md` - Added adaptive CodeGraph preflight for exact `ahe`: check command installation, run init or sync based on `.codegraph/`, and skip both commands when the CLI is unavailable.
- `.codex/hooks/ahe-hook.js`, `docs/PRODUCT.md`, `tests/test_ahe_hook.py`, `feature-list.json`, `PROGRESS.md`, `SESSION-HANDOFF.md` - Required exact `ahe` automatic operation to first report harness engineering status in a consistent Markdown table before proceeding.
- `.codex/skills/ahe-conversation/SKILL.md`, `.codex/skills/ahe-init/SKILL.md`, `.codex/skills/ahe-spec/SKILL.md`, `.codex/skills/ahe-update/SKILL.md`, `.codex/skills/ahe-clear/SKILL.md`, `bin/ahe`, `scripts/uninstall.sh`, `docs/PRODUCT.md`, `feature-list.json`, `PROGRESS.md`, `SESSION-HANDOFF.md`, `tests/test_clarification_prompt.py`, `tests/test_command_set.py`, `tests/test_project_setup.py` - Replaced the previous internal clarification protocol with `ahe-conversation`.
- `.codex/hooks/ahe-hook.js`, `docs/PRODUCT.md`, `tests/test_ahe_hook.py`, `feature-list.json`, `PROGRESS.md` - Upgraded exact `ahe` prompts into automatic AHE operation routing with harness inspection, CodeGraph review guidance, unfinished-feature continuation, ambiguity clarification, and next-task handling.
- `.codex/skills/ahe-init/SKILL.md`, `.codex/skills/ahe-update/SKILL.md`, `.codex/skills/ahe-help/SKILL.md`, `.codex/ahe-shared/schemas/process_status.schema.json`, `.codex/hooks/ahe-hook.js`, `bin/ahe`, `scripts/uninstall.sh`, `docs/PRODUCT.md`, `feature-list.json`, `PROGRESS.md`, `SESSION-HANDOFF.md`, `tests/` - Reduced the public AHE command surface to `init`, `spec`, `update`, `clear`, and `help`.
- `.codex/skills/ahe-spec/SKILL.md`, `.codex/skills/ahe-init/SKILL.md`, `.codex/skills/ahe-help/SKILL.md`, `.codex/ahe-shared/schemas/process_status.schema.json`, `.codex/hooks/ahe-hook.js`, `bin/ahe`, `scripts/uninstall.sh`, `docs/PRODUCT.md`, `feature-list.json`, `PROGRESS.md`, `tests/` - Consolidated the product, constraints, and architecture skills into `$ahe-spec` and updated the reduced public command surface.
- `.codex/skills/ahe-init/SKILL.md`, `.codex/skills/ahe-agent/SKILL.md`, `.codex/skills/ahe-product/SKILL.md`, `.codex/skills/ahe-todo/SKILL.md`, `.codex/skills/ahe-constraints/SKILL.md`, `.codex/skills/ahe-architecture/SKILL.md`, `.codex/skills/ahe-clear/SKILL.md`, `.codex/skills/ahe-copy/SKILL.md`, `bin/ahe`, `scripts/uninstall.sh`, `docs/PRODUCT.md`, `feature-list.json`, `tests/test_clarification_prompt.py`, `tests/test_command_set.py`, `tests/test_project_setup.py` - Added internal clarification protocol coverage while keeping help user-facing.
- `.codex/skills/ahe-init/SKILL.md`, `.codex/skills/ahe-agent/SKILL.md`, `.codex/skills/ahe-product/SKILL.md`, `.codex/skills/ahe-todo/SKILL.md`, `.codex/skills/ahe-constraints/SKILL.md`, `.codex/skills/ahe-architecture/SKILL.md`, `.codex/skills/ahe-clear/SKILL.md`, `.codex/skills/ahe-copy/SKILL.md`, `docs/PRODUCT.md`, `tests/test_clarification_prompt.py`, `tests/test_specialized_workflows.py`, `feature-list.json` - Replaced the fixed clarification prompt format with Codex UI-compatible structured response request guidance and added skill-specific clarification criteria.
- `.codex/skills/ahe-agent/SKILL.md`, `docs/PRODUCT.md`, `tests/test_specialized_workflows.py` - Updated `$ahe-agent` workflow (when `AGENTS.md` is missing) to ask what the purpose of the project is to the user.
- `.codex/skills/ahe-init/SKILL.md`, `.codex/ahe-shared/schemas/process_status.schema.json`, `docs/PRODUCT.md`, `tests/test_init_workflow.py` - Updated `ahe-init` to execute the six sequential steps and update progress status tracking.
- `.codex/skills/ahe-copy/SKILL.md`, `bin/ahe`, `scripts/uninstall.sh`, `docs/PRODUCT.md`, `tests/`, `feature-list.json` - Implemented the `ahe-copy` skill to copy workspace templates except AGENTS/PRODUCT, capitalizing markdown filenames, and validated it with tests.
- `.codex/skills/` (agent, constraints, architecture, todo, clear), `tests/test_clarification_prompt.py` - Added Clarification Rule section and interactive conversation flows across all interactive AHE skills to enforce multi-turn dialogs and precise clarification prompts.
- `.codex/skills/ahe-help/SKILL.md`, `bin/ahe`, `scripts/uninstall.sh`, `docs/PRODUCT.md`, `package.json`, `tests/`, `feature-list.json` - Implemented the `ahe-help` skill, corrected post-install success output escaping, resolved npm packaging dotfolder omissions, and updated the test suite.
- `.codex/skills/ahe-todo/SKILL.md`, `.codex/skills/ahe-update/SKILL.md`, `docs/PRODUCT.md`, `feature-list.json`, `tests/`, `bin/ahe`, `scripts/uninstall.sh` - Added the todo queue skill and taught update to consume queued todo content into the product spec.
- `.codex/skills/`, `.codex/ahe-shared/`, `bin/ahe`, `package.json`, `scripts/uninstall.sh`, `tests/`, `docs/PRODUCT.md` - Reorganized AHE into seven separate skills with shared assets outside the skills directory and updated installation plus verification coverage.
- `.ahe/backups/20260608-215651/`, `.ahe/process_status.json`, `PROGRESS.md`, `SESSION-HANDOFF.md` - Started `ahe clear`, backed up `AGENTS.md` and `docs/PRODUCT.md`, and advanced the workflow to the new-goal question.
- `.codex/skills/ahe/SKILL.md`, `docs/PRODUCT.md`, `feature-list.json`, `tests/test_clear_workflow.py` - Changed `ahe clear` to back up the full harness files, reset `AGENTS.md` objective guidance, remove the old product spec after backup, and rewrite `docs/PRODUCT.md` recursively.
- `scripts/install.sh`, `scripts/uninstall.sh`, `tests/test_project_setup.py`, `docs/PRODUCT.md` - Changed the helper scripts to install/uninstall under `${HOME}/.codex` and added verification coverage.
- `.codex/skills/ahe/SKILL.md`, `docs/PRODUCT.md`, `feature-list.json`, `tests/test_chat_command_routing.py`, `tests/test_update_workflow.py` - Added `$ahe-*` aliases and the `ahe update` workflow for feature-list, progress, and handoff maintenance.
- `.codex/skills/ahe/SKILL.md`, `docs/PRODUCT.md`, `feature-list.json`, `tests/` - Reduced AHE to the seven `$ahe-*` commands and removed the old check/resume-centered contract surface.
- `package.json`, `bin/ahe` - Added the minimal installer package and CLI entrypoint.
- `.codex/skills/ahe/` - Added the embedded skill, templates, and schemas copied by the installer.
- `init.sh`, `templates/` - Normalized the setup scripts and canonical template names to the conservative product spec.
- `.ahe/process_status.json`, `tests/test_project_setup.py` - Added runtime state and setup verification coverage.
- `.codex/skills/ahe/SKILL.md`, `tests/test_chat_command_routing.py` - Added Chat Command Routing definitions and verification logic.
- `scripts/install.sh`, `scripts/uninstall.sh` - Added helper scripts for local installation and uninstallation of the AHE skill.
- `.codex/skills/ahe/SKILL.md`, `tests/test_init_workflow.py` - Implemented Init Workflow instructions and test validation.
- `tests/test_project_setup.py` - Fixed case-sensitivity issue for macOS compatibility.
- `.codex/skills/ahe/SKILL.md`, `tests/test_product_workflow.py` - Added the Product Workflow contract and verification coverage.
- `bin/ahe`, `tests/test_project_setup.py` - Made the installer smoke test hermetic and fixed symlink-aware package root resolution for `npx` installs.
- `.codex/skills/ahe/SKILL.md`, `tests/test_check_resume_workflows.py` - Added explicit Check and Resume workflow contracts and verification coverage.
- `.codex/skills/ahe/SKILL.md`, `tests/test_session_tracking_handoff.py` - Added explicit cross-workflow tracking and handoff synchronization rules and verification coverage.
- `.codex/skills/ahe/SKILL.md`, `docs/PRODUCT.md`, `feature-list.json`, `tests/test_clear_workflow.py` - Added `ahe clear` workflow routing, behavior, tracking, and tests.
- `.codex/skills/ahe/SKILL.md`, `docs/PRODUCT.md`, `feature-list.json`, `tests/test_clarification_prompt.py` - Added the exact clarification prompt format for unclear or under-detailed user responses.
- [x] Implemented `feat-036 NPM Deployment Preparation` by renaming the package in `package.json` to `ahe-codex`, adding repository URL, author info, keywords, and prepublish scripts. Updated `AGENTS.md` and `docs/PRODUCT.md` so that the installation instructions now reflect the `ahe-codex` name, effectively enabling `npm install ahe-codex` or `npx --package=ahe-codex ahe install`.
- [x] Added `scripts/deploy.sh` to provide an interactive, automated flow for publishing the `ahe-codex` package to npm.
- [x] Changed package name to `@ksuchoi216/ahe` per the user's request, referencing the `@openai/codex` convention.
- [x] Added `publishConfig: {"access": "public"}` to `package.json` to allow publishing scoped packages.
- [x] Implemented `ahe uninstall` inside `bin/ahe` to provide users an easy way to clean up installed Codex skills.
