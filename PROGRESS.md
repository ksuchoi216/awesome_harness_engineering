# PROGRESS.md

## Current Status

**Last Updated:** 2026-06-09 02:54 +0900
**Session ID:** feat-019-clarification-prompt-question
**Active Feature:** None

## Completed

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
  - Details: `feat-017 AHE Agent Initialize Workflow on AGENTS.md Absence` is complete. `$ahe-agent` now handles workspace setup when `AGENTS.md` is missing.
  - Blockers: None.

## Blocked

- [ ] No current blocker.

## Decisions

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
